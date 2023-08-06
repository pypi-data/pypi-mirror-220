#!/usr/bin/env python3
# This file is a part of marzer/soagen and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/soagen/blob/master/LICENSE for the full license text.
# SPDX-License-Identifier: MIT



class ConfigBase(object):
	pass



class Configurable(object):

	def __init__(self, cfg):
		assert cfg is not None

		if isinstance(cfg, ConfigBase):
			self.__cfg = cfg
			return

		try:
			c = cfg.config()
			if isinstance(c, ConfigBase):
				self.__cfg = c
				return
		except:
			pass

		try:
			c = cfg.config
			if isinstance(c, ConfigBase):
				self.__cfg = c
				return
		except:
			pass

		self.__cfg = None

	@property
	def config(self) -> ConfigBase:
		return self.__cfg



RESERVED_WORDS = (
	# c++ keywords
	r'alignas',
	r'alignof',
	r'and',
	r'and_eq',
	r'asm',
	r'atomic_cancel',
	r'atomic_commit',
	r'atomic_noexcept',
	r'auto',
	r'bitand',
	r'bitor',
	r'bool',
	r'break',
	r'case',
	r'catch',
	r'char',
	r'char8_t',
	r'char16_t',
	r'char32_t',
	r'class',
	r'compl',
	r'concept',
	r'const',
	r'consteval',
	r'constexpr',
	r'constinit',
	r'const_cast',
	r'continue',
	r'co_await',
	r'co_return',
	r'co_yield',
	r'decltype',
	r'default',
	r'delete',
	r'do',
	r'double',
	r'dynamic_cast',
	r'else',
	r'enum',
	r'explicit',
	r'export',
	r'extern',
	r'false',
	r'float',
	r'for',
	r'friend',
	r'goto',
	r'if',
	r'inline',
	r'int',
	r'long',
	r'mutable',
	r'namespace',
	r'new',
	r'noexcept',
	r'not',
	r'not_eq',
	r'nullptr',
	r'operator',
	r'or',
	r'or_eq',
	r'private',
	r'protected',
	r'public',
	r'reflexpr',
	r'register',
	r'reinterpret_cast',
	r'requires',
	r'return',
	r'short',
	r'signed',
	r'sizeof',
	r'static',
	r'static_assert',
	r'static_cast',
	r'struct',
	r'switch',
	r'template',
	r'this',
	r'thread_local',
	r'throw',
	r'true',
	r'try',
	r'typedef',
	r'typeid',
	r'typename',
	r'union',
	r'unsigned',
	r'using',
	r'virtual',
	r'void',
	r'volatile',
	r'wchar_t',
	r'while',
	r'xor',
	r'xor_eq',
	# std::vector-like interface:
	r'erase',
	r'unordered_erase',
	r'push_back',
	r'emplace_back',
	r'assign',
	r'clear',
	r'empty',
	r'size',
	r'max_size',
	r'capacity',
	r'begin',
	r'cbegin',
	r'end',
	r'cend',
	r'reserve',
	r'resize',
	r'swap',
	r'data',
	r'shrink_to_fit',
	r'get_allocator',
	r'size_type',
	r'difference_type',
	r'allocator_type',
	# soagen-specific:
	r'table_',
	r'table_type',
	r'table_traits',
	r'make_col',
	r'aligned_stride',
	r'column',
	r'column_name',
	r'column_indices',
	r'column_type',
	r'column_traits',
	r'emplacer',
	# future-proofing:
	r'move',
	r'copy',
	r'update',
	r'reset',
	r'span',
	r'const_span',
	r'row',
	r'row_view',
	r'index_type',
	r'size_bytes',
	r'zerofill',
	r'zerofill_column',
	r'swap_columns',
)
