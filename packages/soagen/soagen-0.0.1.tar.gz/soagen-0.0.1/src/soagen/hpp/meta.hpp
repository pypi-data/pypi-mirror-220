//# This file is a part of marzer/soagen and is subject to the the terms of the MIT license.
//# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
//# See https://github.com/marzer/soagen/blob/master/LICENSE for the full license text.
//# SPDX-License-Identifier: MIT
#pragma once

#include "core.hpp"
SOAGEN_DISABLE_WARNINGS;
#ifndef SOAGEN_COLUMN_SPAN_TYPE
	#if SOAGEN_CPP >= 20
		#include <span>
		#define SOAGEN_COLUMN_SPAN_TYPE std::span
	#elif SOAGEN_HAS_INCLUDE(<muu/span.h>)
		#include <muu/span.h>
		#define SOAGEN_COLUMN_SPAN_TYPE muu::span
	#elif SOAGEN_HAS_INCLUDE(<tcb/span.hpp>)
		#include <tcb/span.hpp>
		#define SOAGEN_COLUMN_SPAN_TYPE TCB_SPAN_NAMESPACE_NAME::span
	#endif
#endif
#ifndef SOAGEN_OPTIONAL_TYPE
	#include <optional>
	#define SOAGEN_OPTIONAL_TYPE std::optional
#endif
SOAGEN_ENABLE_WARNINGS;
#include "header_start.hpp"

namespace soagen
{
	template <typename T>
	using remove_cvref = std::remove_cv_t<std::remove_reference_t<T>>;

	template <typename T>
	inline constexpr bool is_cv = !std::is_same_v<std::remove_cv_t<T>, T>;

	template <typename T>
	inline constexpr bool is_cvref = !std::is_same_v<remove_cvref<T>, T>;

	template <typename T>
	inline constexpr bool is_integer = std::is_integral_v<T> && !std::is_same_v<T, bool>;

	template <typename... T>
	inline constexpr bool all_integer = (!!sizeof...(T) && ... && is_integer<T>);

	template <typename T>
	inline constexpr bool is_unsigned = is_integer<T> && std::is_unsigned_v<T>;

	template <typename T, typename... U>
	inline constexpr bool any_same = (false || ... || std::is_same_v<T, U>);

	template <typename T>
	inline constexpr bool is_soa = false; // specialized in generated code

	template <typename T>
	inline constexpr bool is_implicit_lifetime_type =
		std::is_scalar_v<T> || std::is_array_v<T>
		|| (std::is_aggregate_v<T> && std::is_trivially_constructible_v<T> && std::is_trivially_destructible_v<T>);

	template <auto Value>
	using index_tag = std::integral_constant<size_t, static_cast<size_t>(Value)>;

#ifdef SOAGEN_COLUMN_SPAN_TYPE

	template <typename T, size_t N = static_cast<size_t>(-1)>
	using column_span = SOAGEN_COLUMN_SPAN_TYPE<T, N>;

	template <typename T, size_t N = static_cast<size_t>(-1)>
	using const_column_span = column_span<std::add_const_t<T>, N>;

#endif

	using SOAGEN_OPTIONAL_TYPE;

	namespace detail
	{
		template <typename T>
		using has_swap_member_ = decltype(std::declval<T&>().swap(std::declval<T&>()));

		template <typename T, typename Arg>
		using has_resize_member_ = decltype(std::declval<T&>().resize(std::declval<const Arg&>()));

		template <typename T, typename Arg>
		using has_erase_member_ = decltype(std::declval<T&>().erase(std::declval<const Arg&>()));

		template <typename T, typename Arg>
		using has_unordered_erase_member_ = decltype(std::declval<T&>().unordered_erase(std::declval<const Arg&>()));
	}

	template <typename T>
	inline constexpr bool has_swap_member = is_detected<detail::has_swap_member_, T>;

	template <typename T, typename Arg = size_t>
	inline constexpr bool has_resize_member = is_detected<detail::has_resize_member_, T, Arg>;

	template <typename T, typename Arg = size_t>
	inline constexpr bool has_erase_member = is_detected<detail::has_erase_member_, T, Arg>;

	template <typename T, typename Arg = size_t>
	inline constexpr bool has_unordered_erase_member = is_detected<detail::has_unordered_erase_member_, T, Arg>;

	namespace detail
	{
		template <typename T, bool = has_swap_member<T>>
		struct has_nothrow_swap_member_ : std::bool_constant<noexcept(std::declval<T&>().swap(std::declval<T&>()))>
		{};
		template <typename T>
		struct has_nothrow_swap_member_<T, false> : std::false_type
		{};

		template <typename T, typename Arg, bool = has_resize_member<T, Arg>>
		struct has_nothrow_resize_member_
			: std::bool_constant<noexcept(std::declval<T&>().resize(std::declval<const Arg&>()))>
		{};
		template <typename T, typename Arg>
		struct has_nothrow_resize_member_<T, Arg, false> : std::false_type
		{};

		template <typename T, typename Arg, bool = has_erase_member<T, Arg>>
		struct has_nothrow_erase_member_
			: std::bool_constant<noexcept(std::declval<T&>().erase(std::declval<const Arg&>()))>
		{};
		template <typename T, typename Arg>
		struct has_nothrow_erase_member_<T, Arg, false> : std::false_type
		{};

		template <typename T, typename Arg, bool = has_unordered_erase_member<T, Arg>>
		struct has_nothrow_unordered_erase_member_
			: std::bool_constant<noexcept(std::declval<T&>().unordered_erase(std::declval<const Arg&>()))>
		{};
		template <typename T, typename Arg>
		struct has_nothrow_unordered_erase_member_<T, Arg, false> : std::false_type
		{};
	}

	template <typename T>
	inline constexpr bool has_nothrow_swap_member = detail::has_nothrow_swap_member_<T>::value;

	template <typename T, typename Arg = size_t>
	inline constexpr bool has_nothrow_resize_member = detail::has_nothrow_resize_member_<T, Arg>::value;

	template <typename T, typename Arg = size_t>
	inline constexpr bool has_nothrow_erase_member = detail::has_nothrow_erase_member_<T, Arg>::value;

	template <typename T, typename Arg = size_t>
	inline constexpr bool has_nothrow_unordered_erase_member =
		detail::has_nothrow_unordered_erase_member_<T, Arg>::value;

	// trait for determining the actual storage type for a column.
	// we can strip off const/volatile and coerce all pointers to be void* to reduce template instantiation burden
	namespace detail
	{
		template <typename ValueType>
		struct storage_type_
		{
			using type = ValueType;
		};
		template <typename T>
		struct storage_type_<T*>
		{
			using type = void*;
		};
		template <typename T>
		struct storage_type_<const T*> : public storage_type_<T*>
		{};
		template <typename T>
		struct storage_type_<volatile T*> : public storage_type_<T*>
		{};
		template <typename T>
		struct storage_type_<const volatile T*> : public storage_type_<T*>
		{};
		template <typename T>
		struct storage_type_<const T> : public storage_type_<T>
		{};
		template <typename T>
		struct storage_type_<volatile T> : public storage_type_<T>
		{};
		template <typename T>
		struct storage_type_<const volatile T> : public storage_type_<T>
		{};
	}
	template <typename ValueType>
	using storage_type = typename detail::storage_type_<ValueType>::type;

	// trait for determining the default parameter type for a column.
	// ideally we want to pass small+fast things by value, move-only things by rvalue,
	// and everything else as const lvalue.
	namespace detail
	{
		template <typename ValueType,
				  bool Value = std::is_scalar_v<ValueType>		//
							|| std::is_fundamental_v<ValueType> //
							|| (std::is_trivially_copyable_v<ValueType> && sizeof(ValueType) <= sizeof(void*) * 2),
				  bool Move = !std::is_copy_constructible_v<ValueType> && std::is_move_constructible_v<ValueType>>
		struct param_type_
		{
			using type = ValueType;
		};
		template <typename ValueType>
		struct param_type_<ValueType, false, true>
		{
			using type = std::add_rvalue_reference_t<ValueType>;
		};
		template <typename ValueType>
		struct param_type_<ValueType, false, false>
		{
			using type = std::add_lvalue_reference_t<std::add_const_t<ValueType>>;
		};
	}
	template <typename ValueType>
	using param_type = typename detail::param_type_<ValueType>::type;

	// utility class for passing multiple variadic packs through to emplace
	template <typename... Args>
	struct emplacer
	{
		static_assert(sizeof...(Args));
		static_assert((std::is_reference_v<Args> && ...));

		void* ptrs[sizeof...(Args)];

		SOAGEN_DEFAULT_RULE_OF_FIVE(emplacer);

		SOAGEN_NODISCARD_CTOR
		constexpr emplacer(Args&&... args) noexcept //
			: ptrs{ const_cast<void*>(static_cast<const volatile void*>(&args))... }
		{}
	};
	template <>
	struct emplacer<>
	{};
	template <typename... Args>
	emplacer(Args&&...) -> emplacer<Args&&...>;
	template <typename T>
	inline constexpr bool is_emplacer = false;
	template <typename... T>
	inline constexpr bool is_emplacer<emplacer<T...>> = true;
}

#include "header_end.hpp"
