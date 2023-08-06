#!/usr/bin/env python3
# This file is a part of marzer/soagen and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/soagen/blob/master/LICENSE for the full license text.
# SPDX-License-Identifier: MIT

import argparse
import logging
import os
import re
import subprocess
import sys
import zipfile
from io import StringIO
from pathlib import Path

from . import log, paths, utils
from .config import Config
from .errors import Error, SchemaError
from .includes import *
from .preprocessor import Preprocessor
from .schemas import current_context as current_schema_context
from .version import *
from .writer import Writer


def bug_report():
	bug_report_args = [arg for arg in sys.argv[1:] if arg not in (r'--bug-report', r'--bug-report-internal')]
	bug_report_zip = (Path.cwd() / r'soagen_bug_report.zip').resolve()

	log.i(rf'{log.STYLE_CYAN}Preparing a bug report!{log.STYLE_RESET}')
	log.i(r'Preparing output paths')
	utils.delete_directory(paths.BUG_REPORT_DIR, logger=log.d)
	utils.delete_file(bug_report_zip, logger=log.d)
	os.makedirs(str(paths.BUG_REPORT_DIR), exist_ok=True)

	log.i(r'Invoking soagen')
	result = subprocess.run(
		args=[r'soagen', *bug_report_args, r'--bug-report-internal'],
		cwd=str(Path.cwd()),
		check=False,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		encoding=r'utf-8'
	)

	if result.stdout is not None:
		log.i(r'Writing stdout')
		with open(paths.BUG_REPORT_DIR / r'stdout.txt', r'w', newline='\n', encoding=r'utf-8') as f:
			f.write(result.stdout)

	if result.stderr is not None:
		log.i(r'Writing stderr')
		with open(paths.BUG_REPORT_DIR / r'stderr.txt', r'w', newline='\n', encoding=r'utf-8') as f:
			f.write(result.stderr)

	log.i(r'Writing metadata')
	with open(paths.BUG_REPORT_DIR / r'metadata.txt', r'w', newline='\n', encoding=r'utf-8') as f:
		f.write(f'version: {VERSION_STRING}\n')
		f.write(f'args: {bug_report_args}\n')
		f.write(f'returncode: {result.returncode}\n')

	# zip file
	log.i(r'Zipping files')
	with zipfile.ZipFile(str(bug_report_zip), 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip:
		file_prefix_len = len(str(paths.BUG_REPORT_DIR))
		for file in utils.get_all_files(paths.BUG_REPORT_DIR, recursive=True):
			if file.suffix is not None and file.suffix.lower() in (r'.pyc', ):
				continue
			relative_file = str(file)[file_prefix_len:].replace('\\', '/').strip('/')
			zip.write(file, arcname=rf'soagen_bug_report/{relative_file}')

	log.i(r'Cleaning up')
	utils.delete_directory(paths.BUG_REPORT_DIR)

	log.i(
		f'{log.STYLE_CYAN}Zip generated: {bug_report_zip}\n'
		f'Please attach this file when you make a report at github.com/marzer/soagen/issues, thanks!{log.STYLE_RESET}'
	)



def update_hpp(preprocess=True):
	# regenerate version.hpp
	version_hpp = paths.HPP / r'version.hpp'
	log.i(rf'Writing {version_hpp}')
	with open(version_hpp, 'w', encoding='utf-8', newline='\n') as f:
		f.write(
			rf'''
//# This file is a part of marzer/soagen and is subject to the the terms of the MIT license.
//# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
//# See https://github.com/marzer/soagen/blob/master/LICENSE for the full license text.
//# SPDX-License-Identifier: MIT
#pragma once

#define SOAGEN_VERSION_MAJOR {VERSION[0]}
#define SOAGEN_VERSION_MINOR {VERSION[1]}
#define SOAGEN_VERSION_PATCH {VERSION[2]}
#define SOAGEN_VERSION_STRING "{VERSION_STRING}"
'''
		)
	# regenerate the other source headers from the templates
	if paths.MAKE_SINGLE.exists():
		for template in utils.enumerate_files(paths.HPP_TEMPLATES, all='*.hpp.in', recursive=True):
			output = Path(paths.HPP, template.stem)
			utils.run_python_script(
				paths.MAKE_SINGLE, str(template), r'--output', output, r'--namespaces', r'soagen', r'detail',
				r'--macros', r'SOAGEN'
			)
			text = utils.read_all_text_from_file(output, logger=log.i)
			try:
				text = utils.clang_format(text, cwd=output.parent)
			except:
				pass
			log.i(rf'Writing {output}')
			with open(output, 'w', encoding='utf-8', newline='\n') as f:
				f.write(text)
	else:
		log.w(rf'could not regenerate headers using muu: {paths.MAKE_SINGLE.name} did not exist or was not a file')
	# read soagen.hpp + preprocess into single header
	if preprocess:
		soagen_hpp = Path(paths.HPP, 'soagen.hpp')
		text = str(Preprocessor(soagen_hpp))
		# clang-format
		try:
			text = utils.clang_format(text, cwd=soagen_hpp.parent)
		except:
			pass
		log.i(rf'Writing {soagen_hpp}')
		with open(soagen_hpp, 'w', encoding='utf-8', newline='\n') as f:
			f.write(text)



class NonExitingArgParser(argparse.ArgumentParser):

	def error(self, message):
		self.print_usage(sys.stderr)
		raise Error(message)



def main_impl():
	# yapf: disable
	args = NonExitingArgParser(
		description=
		rf'{log.STYLE_CYAN}'
		r'''  ___  ___   __ _  __ _  ___ _ __  ''' '\n'
		r''' / __|/ _ \ / _` |/ _` |/ _ \ '_ \ ''' '\n'
		r''' \__ \ (_) | (_| | (_| |  __/ | | |''' '\n'
		r''' |___/\___/ \__,_|\__, |\___|_| |_|''' '\n'
		r'''                   __/ |           ''' '\n'
		r'''                  |___/  '''  rf'{log.STYLE_RESET}'
		rf' v{VERSION_STRING} - github.com/marzer/soagen'
		'\n\n'
		r'Struct-of-Arrays generator for C++ projects.',
		formatter_class=argparse.RawTextHelpFormatter,
		exit_on_error=False
	)
	# yapf: enable

	#--------------------------------------------------------------
	# public (user-facing, documented) arguments
	#--------------------------------------------------------------

	args.add_argument(
		r'configs',  #
		type=str,
		nargs=r'*',
		help="zero or more .toml files describing your structures-of-arrays\n"
		"(wildcards are accepted, e.g. soa\*.toml)",
	)
	args.add_argument(
		r'-v',  #
		r'--verbose',
		action=r'store_true',
		help=r"enable very noisy diagnostic output"
	)
	args.add_argument(
		r'--version',  #
		action=r'store_true',
		help=r"print the version and exit",
		dest=r'print_version'
	)
	args.add_argument(
		r'--werror',  #
		action=argparse.BooleanOptionalAction,
		default=False,
		help=rf'treat {log.STYLE_YELLOW}warnings{log.STYLE_RESET} as {log.STYLE_RED}errors{log.STYLE_RESET}'
	)
	args.add_argument(
		r'--color',  #
		action=argparse.BooleanOptionalAction,
		default=None,
		help=
		f'use {log.STYLE_RED}c{log.STYLE_YELLOW}o{log.STYLE_GREEN}l{log.STYLE_BLUE}o{log.STYLE_MAGENTA}r{log.STYLE_CYAN}s{log.STYLE_RESET} in terminal output\n'
		r'(the British spelling "colour" is also accepted)'
	)
	args.add_argument(
		r'--clang-format',  #
		action=argparse.BooleanOptionalAction,
		default=None,
		help=rf'run {log.STYLE_CYAN}clang-format{log.STYLE_RESET} on generated code (if it is available)'
	)
	args.add_argument(
		r'--doxygen',  #
		action=argparse.BooleanOptionalAction,
		default=None,
		help=rf'include {log.STYLE_CYAN}doxygen{log.STYLE_RESET} markup in the generated code'
	)
	args.add_argument(
		r'--install',  #
		type=Path,
		default=None,
		metavar=r'<dir>',
		help=rf"install {log.STYLE_CYAN}soagen.hpp{log.STYLE_RESET} into a directory"
	)
	args.add_argument(
		r'--bug-report',  #
		action=r'store_true',
		help=r"capture all inputs and outputs in a bug-report zip file"
	)

	#--------------------------------------------------------------
	# hidden/developer-only/deprecated/diagnostic arguments
	#--------------------------------------------------------------

	args.add_argument(
		r'--update',  #
		action=r'store_true',
		help=argparse.SUPPRESS
	)
	args.add_argument(
		r'--dev',  #
		action=r'store_true',
		help=argparse.SUPPRESS
	)
	args.add_argument(
		r'--bug-report-internal',  #
		action=r'store_true',
		help=argparse.SUPPRESS
	)
	args.add_argument(
		r'--colour',  #
		action=argparse.BooleanOptionalAction,
		default=None,
		dest='color',
		help=argparse.SUPPRESS
	)

	usage_str = args.format_usage()
	args = args.parse_args()
	if args.dev:
		args.update = True
		args.verbose = True

	log.reinit(
		min_level=logging.DEBUG if args.verbose else logging.INFO,
		treat_warnings_as_errors=args.werror,
		on_warning=(lambda: sys.exit(1)) if args.werror else None,
		on_error=lambda: sys.exit(1)
	)

	#--------------------------------------------------------------
	# --version
	#--------------------------------------------------------------

	if args.print_version:
		print(VERSION_STRING)
		return

	log.i(rf'{log.STYLE_CYAN}soagen{log.STYLE_RESET} v{VERSION_STRING}')

	#--------------------------------------------------------------
	# bug report invocation
	#--------------------------------------------------------------

	if args.bug_report:
		bug_report()
		return

	#--------------------------------------------------------------
	# regular invocation
	#--------------------------------------------------------------

	done_work = False

	if args.update:
		done_work = True
		update_hpp(preprocess=not args.dev)
		utils.copy_file(Path(paths.REPOSITORY, r'.clang-format'), Path(paths.HPP, r'.clang-format'), logger=log.i)

	if args.install is not None:
		done_work = True
		args.install: Path
		if not args.install.exists() or not args.install.is_dir():
			log.e(rf"--install: path '{args.install}' did not exist or was not a directory")
		utils.copy_file(paths.HPP / r'soagen.hpp', args.install, logger=log.i)

	configs = []
	for p in args.configs:
		if p.find('*') != -1:
			configs = configs + [f for f in Path('.').glob(p) if f.is_file()]
		else:
			p = Path(p)
			if not p.exists() or not p.is_file():
				log.e(rf"configs: '{p}' did not exist or was not a file")
			configs.append(p)
	configs.sort()
	if args.bug_report_internal:
		os.makedirs(str(paths.BUG_REPORT_INPUTS), exist_ok=True)
		for f in configs:
			utils.copy_file(f, paths.BUG_REPORT_INPUTS, log.i)
	configs = [Config(f) for f in configs]
	done_work = done_work or bool(configs)

	if not configs:
		if not done_work:
			log.i('No work to do.')
			if len(sys.argv) == 1:
				log.i(usage_str)
		return 0

	def get_cascading_bool_property(src, name: str, default: bool) -> bool:
		nonlocal args
		default = bool(default)
		for obj in (args, src.config, src):
			attr = getattr(obj, name)
			if attr is not None:
				attr = bool(attr)
				if attr != default:
					return bool(attr)
		return default

	def should_clang_format(src):
		if not get_cascading_bool_property(src, 'clang_format', True):
			return False
		if getattr(should_clang_format, 'ok', None) is None:
			setattr(should_clang_format, 'ok', utils.is_tool(r'clang-format'))
			if not should_clang_format.ok:
				log.w(r'clang-format not found on system PATH')
		if not should_clang_format.ok:
			return False
		return True

	def should_doxygen(src):
		return get_cascading_bool_property(src, 'doxygen', True)

	if args.bug_report_internal:
		os.makedirs(str(paths.BUG_REPORT_OUTPUTS), exist_ok=True)

	for config in configs:

		for src in (config.hpp, ):

			def write_external_includes(s: str) -> str:
				nonlocal src
				includes = sorted(set(src.external_includes + detect_includes(s)))
				PATTERN = r'\n[ \t]*//[ \t]*####[ \t]+SOAGEN_EXTERNAL_HEADERS[ \t]+####[ \t]*\n'
				if includes:
					rep = '\nSOAGEN_DISABLE_WARNINGS;'
					for inc in includes:
						rep += f'\n#include <{inc}>'
					rep += '\nSOAGEN_ENABLE_WARNINGS;\n'
					s = re.sub(PATTERN, rep, s)
				else:
					s = re.sub(PATTERN, '\n', s)
				return s

			with Writer(
				src.path,
				meta=config.meta_stack,
				clang_format=should_clang_format(src),
				doxygen=should_doxygen(src),
				on_flush=write_external_includes
			) as o:
				src.write(o)

			if args.bug_report_internal:
				utils.copy_file(src.path, paths.BUG_REPORT_OUTPUTS, logger=log.i)

		for src in (config.natvis, ):
			with Writer(src.path, meta=config.meta_stack, clang_format=False, doxygen=False) as o:
				src.write(o)

			if args.bug_report_internal:
				utils.copy_file(src.path, paths.BUG_REPORT_OUTPUTS, logger=log.i)

	# bug reports should always copy the submitter's version of soagen.hpp incase the report is related to soagen.hpp
	if args.bug_report_internal:
		utils.copy_file(paths.HPP / r'soagen.hpp', paths.BUG_REPORT_DIR, logger=log.i)

	log.i(r'All done!')



def main():
	allow_styles = True
	for arg in (r'--bug-report-internal', r'--no-color', r'--no-colour'):
		if arg in sys.argv[1:]:
			allow_styles = False
			break
	log.init(allow_styles=allow_styles)
	try:
		try:
			main_impl()
		except BaseException as err:
			log.clear_hooks()
			raise err from None
	except SystemExit as exit:
		raise exit from None
	except (SchemaError) as err:
		log.e(rf'{current_schema_context()}{err}')
		sys.exit(1)
	except (Error, SchemaError, argparse.ArgumentError) as err:
		log.e(err)
		sys.exit(1)
	except BaseException as err:
		with StringIO() as buf:
			buf.write(
				f'\n{log.STYLE_RED_DIM}*************{log.STYLE_RESET}\n\n'
				'You appear to have triggered an internal bug!'
				f'\n{log.STYLE_CYAN}Please re-run soagen with --bug-report and file an issue at github.com/marzer/soagen/issues{log.STYLE_RESET}'
				'\nMany thanks!'
				f'\n\n{log.STYLE_RED_DIM}*************{log.STYLE_RESET}\n\n'
			)
			utils.print_exception(err, include_type=True, include_traceback=True, skip_frames=1, logger=buf)
			buf.write(f'{log.STYLE_RED_DIM}*************{log.STYLE_RESET}\n')
			print(buf.getvalue(), file=sys.stderr)
		sys.exit(1)
	sys.exit(0)



if __name__ == '__main__':
	main()
