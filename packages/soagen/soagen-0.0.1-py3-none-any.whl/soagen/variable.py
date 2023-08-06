#!/usr/bin/env python3
# This file is a part of marzer/soagen and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/soagen/blob/master/LICENSE for the full license text.
# SPDX-License-Identifier: MIT

import re

from . import log, utils
from .column import Column
from .configurable import *
from .errors import SchemaError
from .schemas import And, Optional, Or, Schema, Stripped, Use
from .writer import *



def guess_var_type(value) -> str:
	assert value is not None
	if isinstance(value, bool):
		return r'bool'
	elif isinstance(value, str):
		return rf'const char*'
	elif isinstance(value, float):
		return r'float'
	elif isinstance(value, int):
		return r'int'
	elif isinstance(value, (tuple, list)) and value:
		types = [guess_var_type(v) for v in value]
		if types.count(types[0]) == len(types):
			return rf'{types[0]}[{len(types)}]'
		else:
			return rf'std::{"pair" if len(types) == 2 else "tuple"}<{", ".join(types)}>'
	else:
		return None



def emit_var_value(value) -> str:
	assert value is not None
	if isinstance(value, bool):
		return r'true' if value else r'false'
	elif isinstance(value, str):
		return rf'"{value}"'
	elif isinstance(value, float):
		return rf'{value}f'
	elif isinstance(value, int):
		return str(value)
	else:
		assert isinstance(value, (tuple, list))
		types = [guess_var_type(v) for v in value]
		values = [emit_var_value(v) for v in value]
		return rf'{{ {", ".join(values)} }}'



class Variable(Configurable):

	# yapf: disable
	__schema = Schema({
		r'name': And(Stripped(str, allow_empty=False, name=r'variable name'), Use(utils.to_snake_case)),
		Optional(r'type', default=None): Stripped(str, allow_empty=False, name='variable type'),
		Optional(r'double_buffered', default=False): bool,
		Optional(r'param_type', default=''): Stripped(str),
		Optional(r'brief', default=''): Stripped(str),
		Optional(r'default', default=None): Or(str, int, float, bool, tuple, list),
		Optional(r'literal_default', default=None): Stripped(str),
		Optional(r'alignment', default=0)  : And(Or(int, str), Use(int), lambda x: x <= 0 or utils.is_pow2(x), error=r'alignment must be a power-of-two integer'),
	})
	# yapf: enable

	def __init__(self, struct, vals):
		super().__init__(struct)
		self.struct = struct
		self.index = -1  # set by the struct

		vals = Variable.__schema.validate(vals)
		self.__dict__.update(vals)

		if self.name in RESERVED_WORDS:
			raise SchemaError(rf"name: '{self.name}' is reserved", None)

		if self.type is None and self.default is None:
			raise SchemaError("type or non-literal default value must be specified", None)
		elif self.type is None:
			self.type = guess_var_type(self.default)
			if self.type is None:
				raise SchemaError("could not determine type from default value", None)

		if self.default is not None:
			self.default = emit_var_value(self.default)
		elif self.literal_default is not None and self.literal_default:
			self.default = self.literal_default

		self.pointer_type = rf'{self.type}*'
		if re.fullmatch(r'[a-zA-Z_][a-zA-Z_0-9:]*', self.type):
			self.const_pointer_type = rf'const {self.pointer_type}'
		else:
			self.const_pointer_type = rf'std::add_const_t<{self.type}>*'

		self.columns = [Column(self)]
		if self.double_buffered:
			self.columns.append(Column(self, True))



class StaticVariable(Configurable):

	__schema = Schema({
		'name': And(Stripped(str, allow_empty=False, name='static variable name'), Use(utils.to_snake_case)),
		Optional(r'type', default=None): Stripped(str, allow_empty=False, name='static variable type'),
		Optional(r'value', default=None): Or(str, int, float, bool, tuple, list),
		Optional(r'literal_value', default=None): Stripped(str),
		Optional(r'const', default=None): Or('', 'const', 'constexpr', bool),
		Optional(r'access', default='public'): Or('public', 'protected', 'private'),
		Optional(r'brief', default=''): Stripped(str),
	})

	def __init__(self, cfg, vals):
		super().__init__(cfg)
		self.__dict__.update(StaticVariable.__schema.validate(vals))

		if self.name in RESERVED_WORDS:
			raise SchemaError(rf"name: '{self.name}' is reserved", None)

		if self.type is None and self.value is None:
			raise SchemaError("type or value must be specified", None)
		elif self.type is None:
			self.type = guess_var_type(self.value)
			if self.type is None:
				raise SchemaError("could not determine type from value", None)

		if self.value is not None:
			self.value = emit_var_value(self.value)
		elif self.literal_value is not None and self.literal_value:
			self.value = self.literal_value

		if self.const is None:
			self.const = 'constexpr'
		elif isinstance(self.const, bool):
			self.const = 'const' if self.const else ''

	def write(self, o: Writer):
		if self.brief:
			o(f'/// @brief {self.brief}')
		s = 'static '
		if self.const != 'constexpr' and self.value is not None:
			s += 'inline '
		if self.const != 'const':
			s += f'{self.const} '
		s += f'{self.type} '
		if self.const == 'const':
			s += f'{self.const} '
		s += self.name
		if self.value is not None:
			s += rf' = {self.value}'

		s += ';'
		o(s)



__all__ = [r'Variable', r'StaticVariable']
