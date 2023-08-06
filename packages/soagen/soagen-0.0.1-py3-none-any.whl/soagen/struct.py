#!/usr/bin/env python3
# This file is a part of marzer/soagen and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/soagen/blob/master/LICENSE for the full license text.
# SPDX-License-Identifier: MIT

import math
from io import StringIO

from . import utils
from .column import *
from .configurable import *
from .errors import SchemaError
from .includes import *
from .metavars import *
from .schemas import (And, Optional, Or, Schema, SchemaContext, Stripped, Use,
                      ValueOrArray)
from .type_list import *
from .variable import *
from .writer import *

NEWLINE = '\n'
TAB = '\t'



class Struct(Configurable):

	# yapf: disable
	__schema = Schema({
		Optional(r'prologue', default='')    : Stripped(str),
		Optional(r'header', default='')    : Stripped(str),
		Optional(r'footer', default='')    : Stripped(str),
		Optional(r'epilogue', default='')    : Stripped(str),
		Optional(r'brief', default='')    : Stripped(str),
		Optional(r'allocator', default='')    : Stripped(str),
		Optional(r'static_variables', default=list) : [ object ],
		Optional(r'variables', default=list)  : [ object ],
		Optional(r'movable', default=True)    : bool,
		Optional(r'copyable', default=True)    : bool,
		Optional(r'default_constructible', default=True)    : bool,
		Optional(r'swappable', default=True)    : bool,

		Optional(r'column_providers', default=True) : bool,
		Optional(r'stripes', default=list)   : [ object ],
		Optional(r'rows', default=True)    : bool,
		Optional(r'spans', default=True)   : bool,
		Optional(r'strong_indices', default=False) : bool,
		Optional(r'growth_factor', default=1.5)  : And(Or(int, float), Use(float), lambda x: x >= 1.0 and math.isfinite(x)),

		# additional #includes to add to any header files this struct appears in
		Optional(r'internal_includes', default=list) : And(ValueOrArray(str, name=r'internal_includes'), Use(lambda x: remove_implicit_includes(sorted(set([s.strip() for s in x if s]))))),
		Optional(r'external_includes', default=list) : And(ValueOrArray(str, name=r'external_includes'), Use(lambda x: remove_implicit_includes(sorted(set([s.strip() for s in x if s]))))),

		# span headers
		Optional(r'span_header', default='')  : Stripped(str),
		Optional(r'mutable_span_header', default=''): Stripped(str),
		Optional(r'const_span_header', default='')  : Stripped(str),
		Optional(r'struct_and_span_header', default='')  : Stripped(str),
		Optional(r'struct_and_mutable_span_header', default='')  : Stripped(str),

		# span footers
		Optional(r'span_footer', default='')  : Stripped(str),
		Optional(r'mutable_span_footer', default=''): Stripped(str),
		Optional(r'const_span_footer', default='')  : Stripped(str),
		Optional(r'struct_and_span_footer', default='')  : Stripped(str),
		Optional(r'struct_and_mutable_span_footer', default='')  : Stripped(str),

		# row headers
		Optional(r'row_header', default='')     : Stripped(str),
		Optional(r'lvalue_row_header', default='')   : Stripped(str),
		Optional(r'mutable_lvalue_row_header', default='') : Stripped(str),
		Optional(r'const_lvalue_row_header', default='') : Stripped(str),
		Optional(r'rvalue_row_header', default='')   : Stripped(str),
		Optional(r'mutable_row_header', default='')   : Stripped(str),
		Optional(r'const_row_header', default='')   : Stripped(str),

		# row footers
		Optional(r'row_footer', default='')     : Stripped(str),
		Optional(r'lvalue_row_footer', default='')   : Stripped(str),
		Optional(r'mutable_lvalue_row_footer', default='') : Stripped(str),
		Optional(r'const_lvalue_row_footer', default='') : Stripped(str),
		Optional(r'rvalue_row_footer', default='')   : Stripped(str),
		Optional(r'mutable_row_footer', default='')   : Stripped(str),
		Optional(r'const_row_footer', default='')   : Stripped(str)
	})
	# yapf: enable

	def __init__(self, cfg, name, vals):
		super().__init__(cfg)

		vals = Struct.__schema.validate(vals)
		self.__dict__.update(vals)

		self.name = name
		self.type = name
		if self.name in RESERVED_WORDS:
			raise SchemaError(rf"name: '{self.name}' is reserved", None)

		self.qualified_type = rf'{self.config.namespace}::{self.type}' if self.config.namespace else self.type
		self.qualified_name = self.qualified_type
		self.index = -1  # set by the config
		self.meta = MetaVars()
		self.meta.push('name', self.name)
		self.meta.push('type', self.type)
		self.meta.push('struct::name', self.name)
		self.meta.push('struct::type', self.type)
		self.meta.push('struct::scope', '')

		if not self.allocator:
			self.allocator = self.config.allocator

		for i in range(len(self.variables)):
			with SchemaContext(
				rf"variable '{self.variables[i]['name']}'" if r'name' in self.variables[i] else rf"variable [{i}]"
			):
				self.variables[i] = Variable(self, self.variables[i])
				if self.variables[i].name == self.name:
					raise SchemaError(rf"name: may not be the same as the struct", None)
		for v in self.variables:
			self.meta.push(rf'{v.name}::type', v.type)
			self.meta.push(rf'{v.name}::default', v.default if v.default else '{}')

		self.columns = []
		self.double_buffered = []
		index = 0
		for v in self.variables:
			v.index = index
			index += 1
			if v.double_buffered:
				self.double_buffered.append(v)
			self.columns += v.columns

		index = 0
		for c in self.columns:
			c.index = index
			index += 1
		self.column_types = TypeList([c.type for c in self.columns])
		self.const_column_types = TypeList(["const " + c.type for c in self.columns])
		self.index_types = TypeList(['size_t', 'index_type']) if self.strong_indices else TypeList('index_type')

		self.prologue = rf'''
		{self.config.all_structs_and_spans.prologue}

		{self.config.all_structs_and_mutable_spans.prologue}

		{self.config.all_structs_and_const_spans.prologue}

		{self.config.all_structs.prologue}

		{self.prologue}
		'''.strip()

		self.header = rf'''
		{self.config.all_structs_and_spans.header}

		{self.config.all_structs_and_mutable_spans.header}

		{self.config.all_structs_and_const_spans.header}

		{self.config.all_structs.header}

		{self.header}

		{self.struct_and_span_header}

		{self.struct_and_mutable_span_header}
		'''.strip()

		self.footer = rf'''
		{self.config.all_structs_and_spans.footer}

		{self.config.all_structs_and_mutable_spans.footer}

		{self.config.all_structs_and_const_spans.footer}

		{self.config.all_structs.footer}

		{self.footer}

		{self.struct_and_span_footer}

		{self.struct_and_mutable_span_footer}
		'''.strip()

		self.epilogue = rf'''
		{self.config.all_structs_and_spans.epilogue}

		{self.config.all_structs_and_mutable_spans.epilogue}

		{self.config.all_structs_and_const_spans.epilogue}

		{self.config.all_structs.epilogue}

		{self.epilogue}
		'''.strip()

		if not self.brief:
			self.brief = name

		static_vars = [v for v in self.config.all_structs_and_spans.static_variables]
		static_vars += [v for v in self.config.all_structs_and_mutable_spans.static_variables]
		static_vars += [v for v in self.config.all_structs_and_const_spans.static_variables]
		static_vars += [v for v in self.config.all_structs.static_variables]
		for i in range(len(self.static_variables)):
			with SchemaContext(
				rf"static variable '{self.static_variables[i]['name']}'" if r'name' in
				self.static_variables[i] else rf"static variable [{i}]"
			):
				static_vars.append(StaticVariable(self.config, self.static_variables[i]))
		static_vars = [(v, v.access) for v in static_vars]
		self.static_variables = {'public': [], 'protected': [], 'private': []}
		for v, access in static_vars:
			self.static_variables[access].append(v)
		assert len(self.static_variables) == 3

	def set_index(self, index):
		assert self.index == -1
		assert isinstance(index, int)
		assert index >= 0
		self.index = index
		self.meta.push('index', index)
		self.meta.push('struct::index', index)

	def write_class_forward_declaration(self, o: Writer):
		with MetaScope(self.config.meta_stack, self.meta):
			o(rf'class {self.type};')

	def write_class_definition(self, o: Writer):
		with MetaScope(self.config.meta_stack, self.meta) as meta:

			if self.prologue:
				o(f'''
				{self.prologue}
				''')

			def doxygen(s: str) -> str:
				nonlocal o
				if not o.doxygen:
					return ''
				s = [x.lstrip() for x in s.split('\n')]
				popped_start = 0
				while len(s) and not s[0]:
					s.pop(0)
					popped_start += 1
				s = f'{popped_start*NEWLINE}/// {rf"{NEWLINE}/// ".join(s)}'
				return s

			o(
				doxygen(
				rf'''@brief {self.brief}

			@note The code for this class was generated by soagen - https://github.com/marzer/soagen'''
				)
			)
			with ClassDefinition(o, f'class {self.name}'):

				with Private(o):
					o(
						rf'''
					template <typename ValueType,
							typename ParamType = soagen::param_type<ValueType>,
							size_t Align		 = alignof(ValueType)>
					using make_col = soagen::column_traits<ValueType, ParamType, soagen::max(Align, alignof(ValueType))>;'''
					)

				with Public(o):
					o(
						rf'''
					using size_type = std::size_t;
					using difference_type = std::ptrdiff_t;

					{doxygen("@brief The allocator type used by this class.")}
					using allocator_type = {self.allocator};'''
					)

					max_length = 0
					for col in self.columns:
						max_length = max(len(col.name), max_length)
					with StringIO() as buf:
						buf.write('soagen::table_traits<\n')
						for i in range(len(self.columns)):
							if i:
								buf.write(f',\n')
							col = self.columns[i]
							buf.write(f'\t/* {col.name:>{max_length}} */ make_col<{col.type}')
							if col.param_type:
								buf.write(rf', {col.param_type}')
							if col.alignment > 0:
								if not col.param_type:
									buf.write(rf', soagen::param_type<{col.type}>')
								buf.write(rf', {col.alignment}')
							buf.write(rf'>')
						buf.write(rf'>')
						o(
							rf'''
						{doxygen("@brief The traits for the entire table.")}
						using table_traits = {buf.getvalue()};
						'''
						)

					o(
						rf'''
					{doxygen("@brief Gets the traits for a specific column of the table.")}
					template <size_type I>
					using column_traits = typename table_traits::template column<I>;

					{doxygen("@brief Gets the type of a specific column in the table.")}
					template <size_type I>
					using column_type = typename column_traits<I>::value_type;

					{doxygen("""
					@brief The amount of rows to advance to maintain the requested alignment

					@details The multiple of rows you need to advance through the table such that
					all elements across all columns have the same memory alignment as the beginning of their column
					(i.e. they are 'perfectly aligned' with the chosen value for `alignment` in the soagen config).

					@note Typically you can ignore this; column elements are always aligned correctly according to their type.
					This is for over-alignment scenarios where you need to do things in batches (e.g. SIMD).""")}
					static constexpr size_type aligned_stride = table_traits::aligned_stride;
					'''
					)

					with ClassDefinition(o, r'struct column_indices'):
						for col in self.columns:
							o(rf'static constexpr size_type {col.name} = {col.index};')

				with Private(o):
					o(rf'// clang-format off')
					o(rf'template <size_type> struct column_name_{{}};')
					for col in self.columns:
						o(
							rf'template <> struct column_name_<{col.index}>{{  static constexpr auto value = "{col.name}"; }};'
						)
					o(rf'// clang-format on')

				with Public(o):
					o(
						rf'''
					{doxygen("@brief Gets the name of the specified column as a string.")}
					template <size_type I> static constexpr auto& column_name = column_name_<I>::value;'''
					)
					o()

					o(rf'''
					{self.header}
					''')

				for access in (r'public', r'protected', r'private'):
					if self.static_variables[access]:
						o()
						o.cpp_access_level = access
						for var in self.static_variables[access]:
							var.write(o)

				with Private(o):
					o(
						rf'''
					using table_type = soagen::table<table_traits, allocator_type>;
					table_type table_;
					'''
					)

				with Public(o):
					ctor_attrs = 'SOAGEN_NODISCARD_CTOR'
					o(
						rf'''

					{doxygen("@brief Default constructor.")}
					{ctor_attrs if self.default_constructible else ""} {self.name}() = {"default" if self.default_constructible else "delete"};

					{doxygen("@brief Move constructor.")}
					{ctor_attrs if self.movable else ""} {self.name}({self.name}&&) = {"default" if self.movable else "delete"};

					{doxygen("@brief Move-assignment operator.")}
					{self.name}& operator=({self.name}&&) = {"default" if self.movable else "delete"};

					{doxygen("@brief Copy constructor.")}
					{ctor_attrs if self.copyable else ""} {self.name}(const {self.name}&) = {"default" if self.copyable else "delete"};

					{doxygen("@brief Copy-assignment operator.")}
					{self.name}& operator=(const {self.name}&) = {"default" if self.copyable else "delete"};

					{doxygen("@brief Destructor.")}
					~{self.name}() = default;

					{doxygen("@brief Constructs with the given allocator.")}
					{ctor_attrs}
					constexpr explicit {self.name}(const allocator_type& alloc) noexcept //
						: table_{{ alloc }}
					{{}}

					{doxygen("@brief Constructs with the given allocator.")}
					{ctor_attrs}
					constexpr explicit {self.name}(allocator_type&& alloc) noexcept //
						: table_{{ static_cast<allocator_type&&>(alloc) }}
					{{}}
					'''
					)

					# note: the doxygen member groups here are based on those from the cppreference.com page for
					# std::vector: https://en.cppreference.com/w/cpp/container/vector

					with DoxygenMemberGroup(o, 'Capacity'):
						o(
							rf'''
						{doxygen("@brief Returns true if the number of rows is zero.")}
						SOAGEN_PURE_INLINE_GETTER
						constexpr bool empty() const noexcept
						{{
							return table_.empty();
						}}

						{doxygen("@brief Returns the current number of rows.")}
						SOAGEN_PURE_INLINE_GETTER
						constexpr size_type size() const noexcept
						{{
							return table_.size();
						}}

						{doxygen("@brief Returns the maximum possible number of rows.")}
						SOAGEN_PURE_INLINE_GETTER
						constexpr size_type max_size() const noexcept
						{{
							return table_.max_size();
						}}

						{doxygen("@brief Reserves storage for (at least) the given number of rows.")}
						SOAGEN_ALWAYS_INLINE
						SOAGEN_CPP20_CONSTEXPR
						{self.name}& reserve(size_type new_cap) noexcept(noexcept(std::declval<table_type&>().reserve(size_type{{}})))
						{{
							table_.reserve(new_cap);
							return *this;
						}}

						{doxygen("@brief Returns the number of rows that can be held in currently allocated storage.")}
						SOAGEN_PURE_INLINE_GETTER
						constexpr size_type capacity() const noexcept
						{{
							return table_.capacity();
						}}

						{doxygen("@brief Frees unused capacity.")}
						SOAGEN_ALWAYS_INLINE
						SOAGEN_CPP20_CONSTEXPR
						{self.name}& shrink_to_fit() noexcept(noexcept(std::declval<table_type&>().shrink_to_fit()))
						{{
							table_.shrink_to_fit();
							return *this;
						}}
						'''
						)

					with DoxygenMemberGroup(o, 'Modifiers'):
						o(
							rf'''
						{doxygen("@brief Removes all rows from table.")}
						SOAGEN_ALWAYS_INLINE
						SOAGEN_CPP20_CONSTEXPR
						{self.name}& clear() noexcept
						{{
							table_.clear();
							return *this;
						}}

						{doxygen("@brief Erases the row at the given index.")}
						SOAGEN_HIDDEN_CONSTRAINT(sfinae, bool sfinae = soagen::has_erase_member<table_type, size_type>)
						SOAGEN_ALWAYS_INLINE
						SOAGEN_CPP20_CONSTEXPR
						void erase(size_type pos) noexcept(soagen::has_nothrow_erase_member<table_type, size_type>)
						{{
							table_.erase(pos);
						}}

						{doxygen("""
						@brief	Erases the row at the given index without preserving order.

						@details	This is much faster than #erase() because it uses the swap-and-pop idiom:
									Instead of shifting all the higher rows downward, the last row is moved into the
									position of the erased one and the size of the table is reduced by 1.

						@note		If you are tracking row indices in some other place and need to maintain that invariant,
									you can use the return value to update your data accordingly.

						@returns	The index of the row that was moved into the erased row's position, if any.""")}
						SOAGEN_HIDDEN_CONSTRAINT(sfinae, bool sfinae = soagen::has_unordered_erase_member<table_type, size_type>)
						SOAGEN_ALWAYS_INLINE
						SOAGEN_CPP20_CONSTEXPR
						soagen::optional<size_type> unordered_erase(size_type pos) //
							noexcept(soagen::has_nothrow_unordered_erase_member<table_type, size_type>)
						{{
							return table_.unordered_erase(pos);
						}}
						'''
						)

						push_back_params = []
						push_back_forwarding_declvals = []
						push_back_forwarding_args = []
						for col in self.columns:
							param = rf'column_traits<{col.index}>::param_type {col.name}'
							if col.default is not None:
								param += rf'= {col.default}'
							push_back_params.append(param)
							push_back_forwarding_declvals.append(
								rf'std::declval<column_traits<{col.index}>::param_type&&>()'
							)
							push_back_forwarding_args.append(
								rf'static_cast<column_traits<{col.index}>::param_type&&>({col.name})'
							)

						o(
							rf'''
						{doxygen("@brief Pushes a new row onto the end of the table.")}
						SOAGEN_ALWAYS_INLINE
						SOAGEN_CPP20_CONSTEXPR
						{self.name}& push_back({rf",{NEWLINE+TAB*10} ".join(push_back_params)}) //
							noexcept(noexcept(std::declval<table_type&>().emplace_back({NEWLINE+TAB*12}{rf",{NEWLINE+TAB*12}".join(push_back_forwarding_declvals)})))
						{{
							table_.emplace_back({rf",{NEWLINE+TAB*12}".join(push_back_forwarding_args)});
							return *this;
						}}
						'''
						)

						emplace_back_template_params = []
						emplace_back_params = []
						emplace_back_forwarding_args = []
						for col in self.columns:
							pascal_name = utils.to_pascal_case(col.name)
							emplacer = rf'soagen::emplacer<{pascal_name}...>&&'
							emplace_back_template_params.append(rf'typename... {pascal_name}')
							emplace_back_params.append(rf'{emplacer} {col.name}')
							emplace_back_forwarding_args.append(rf'static_cast<{emplacer}>({col.name})')

						o(
							rf'''
						{doxygen("@brief Constructs a new row directly in-place at the end of the table.")}
						template <{rf",{NEWLINE+TAB*8}  ".join(emplace_back_template_params)}>
						SOAGEN_ALWAYS_INLINE
						SOAGEN_CPP20_CONSTEXPR
						{self.name}& emplace_back({rf",{NEWLINE+TAB*11}".join(emplace_back_params)}) //
						{{
							table_.emplace_back({rf",{NEWLINE+TAB*12}".join(emplace_back_forwarding_args)});
							return *this;
						}}

						{doxygen("@brief Removes the last row(s) from the table.")}
						SOAGEN_ALWAYS_INLINE
						SOAGEN_CPP20_CONSTEXPR
						{self.name}& pop_back(size_type num = 1) noexcept(noexcept(std::declval<table_type&>().pop_back(size_type{{}})))
						{{
							table_.pop_back(num);
							return *this;
						}}

						{doxygen("""@brief Resizes the table to the given number of rows.

						@availability This method is only available when all the column types are default-constructible.""")}
						SOAGEN_HIDDEN_CONSTRAINT(sfinae, bool sfinae = soagen::has_resize_member<table_type, size_type>)
						SOAGEN_ALWAYS_INLINE
						SOAGEN_CPP20_CONSTEXPR
						{self.name}& resize(size_type new_size) noexcept(soagen::has_nothrow_resize_member<table_type, size_type>)
						{{
							table_.resize(new_size);
							return *this;
						}}
						'''
						)

						if self.swappable:
							o(
								rf'''
							{doxygen("""@brief Swaps the contents of the table with another.

							@availability This method is only available when #allocator_type is swappable (or non-propagating).""")}
							SOAGEN_HIDDEN_CONSTRAINT(sfinae, bool sfinae = soagen::has_swap_member<table_type>)
							SOAGEN_ALWAYS_INLINE
							constexpr void swap({self.name}& other) noexcept(soagen::has_nothrow_swap_member<table_type>)
							{{
								table_.swap(other.table_);
							}}
							'''
							)

					with DoxygenMemberGroup(o, 'Element access'):
						o(
							rf'''
						{doxygen("""@brief Returns a pointer to the raw byte backing array.

						@availability This method is only available when all the column types are trivially-copyable.""")}
						SOAGEN_HIDDEN_CONSTRAINT(sfinae, bool sfinae = table_traits::all_trivially_copyable)
						SOAGEN_ALIGNED_COLUMN(0)
						constexpr std::byte* data() noexcept
						{{
							return soagen::assume_aligned<soagen::detail::actual_column_alignment<table_traits, allocator_type, 0>>(table_.data());
						}}

						{doxygen("""@brief Returns a pointer to the raw byte backing array.

						@availability This method is only available when all the column types are trivially-copyable.""")}
						SOAGEN_HIDDEN_CONSTRAINT(sfinae, bool sfinae = table_traits::all_trivially_copyable)
						SOAGEN_ALIGNED_COLUMN(0)
						constexpr const std::byte* data() const noexcept
						{{
							return soagen::assume_aligned<soagen::detail::actual_column_alignment<table_traits, allocator_type, 0>>(table_.data());
						}}

						{doxygen("@brief Returns a pointer to the elements of a specific column.")}
						template <size_t I>
						SOAGEN_ALIGNED_COLUMN(I)
						column_type<I>* column() noexcept
						{{
							static_assert(I < table_traits::column_count, "column index out of range");

							return soagen::assume_aligned<soagen::detail::actual_column_alignment<table_traits, allocator_type, I>>(table_.template column<I>());
						}}

						{doxygen("@brief Returns a pointer to the elements of a specific column.")}
						template <size_t I>
						SOAGEN_ALIGNED_COLUMN(I)
						std::add_const_t<column_type<I>>* column() const noexcept
						{{
							static_assert(I < table_traits::column_count, "column index out of range");

							return soagen::assume_aligned<soagen::detail::actual_column_alignment<table_traits, allocator_type, I>>(table_.template column<I>());
						}}
						'''
						)
						for i in range(len(self.columns)):
							o(
								rf'''
	 						{doxygen(f"@brief Returns a pointer to the elements in column [{i}]: {self.columns[i].name}.")}
							SOAGEN_ALIGNED_COLUMN({i})
							{self.columns[i].pointer_type} {self.columns[i].name}() noexcept
							{{
								return column<{i}>();
							}}

							{doxygen(f"@brief Returns a pointer to the elements in column [{i}]: {self.columns[i].name}.")}
							SOAGEN_ALIGNED_COLUMN({i})
							{self.columns[i].const_pointer_type} {self.columns[i].name}() const noexcept
							{{
								return column<{i}>();
							}}
							'''
							)

					o(
						rf'''
					{doxygen("@brief Returns the allocator being used by the table.")}
					SOAGEN_INLINE_GETTER
					constexpr allocator_type get_allocator() const noexcept
					{{
						return table_.get_allocator();
					}}
					'''
					)

					o(rf'''
					{self.footer}
					''')

			if self.swappable:
				o(
					rf'''
				{doxygen(f"""@brief Swaps the contents of two instances of #{self.qualified_name}.

				@availability	This overload is only available when #{self.qualified_name}::allocator_type
								is swappable (or non-propagating).""")}
				SOAGEN_HIDDEN_CONSTRAINT(sfinae, bool sfinae = soagen::has_swap_member<{self.name}>)
				SOAGEN_ALWAYS_INLINE
				constexpr void swap({self.name}& lhs, {self.name}& rhs) //
					noexcept(soagen::has_nothrow_swap_member<{self.name}>)
				{{
					lhs.swap(rhs);
				}}
				'''
				)

			if self.epilogue:
				o(f'''
				{self.epilogue}
				''')

	def write_outline_member_implementations(self, o: Writer):
		pass

	def write_soagen_specializations(self, o: Writer):
		o(rf'''
		template <>
		inline constexpr bool is_soa<{self.qualified_name}> = true;
		''')



__all__ = [r'Struct']
