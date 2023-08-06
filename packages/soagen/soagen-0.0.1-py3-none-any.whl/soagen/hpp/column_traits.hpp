//# This file is a part of marzer/soagen and is subject to the the terms of the MIT license.
//# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
//# See https://github.com/marzer/soagen/blob/master/LICENSE for the full license text.
//# SPDX-License-Identifier: MIT
#pragma once

#include "functions.hpp"
#include "header_start.hpp"
#if SOAGEN_CLANG >= 16
	#pragma clang diagnostic ignored "-Wunsafe-buffer-usage"
#endif

/// @cond
namespace soagen::detail
{
	// a base class for the column traits that handles all the non-alignment-dependent stuff
	// (to minimize template instantiation explosion)
	template <typename StorageType>
	struct column_traits_base
	{
		using storage_type = StorageType;
		static_assert(!is_cvref<storage_type>, "column storage_type may not be cvref-qualified");
		static_assert(!std::is_void_v<storage_type>, "column storage_type may not be void");
		static_assert(std::is_destructible_v<storage_type>, "column storage_type must be destructible");

		//--- dereferencing --------------------------------------------------------------------------------------------

		SOAGEN_PURE_GETTER
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& get(std::byte* ptr) noexcept
		{
			SOAGEN_ASSUME(ptr != nullptr);

			return *SOAGEN_LAUNDER(reinterpret_cast<storage_type*>(soagen::assume_aligned<alignof(storage_type)>(ptr)));
		}

		SOAGEN_PURE_GETTER
		SOAGEN_ATTR(nonnull)
		static constexpr const storage_type& get(const std::byte* ptr) noexcept
		{
			SOAGEN_ASSUME(ptr != nullptr);

			return *SOAGEN_LAUNDER(
				reinterpret_cast<const storage_type*>(soagen::assume_aligned<alignof(storage_type)>(ptr)));
		}

		//--- default construction -------------------------------------------------------------------------------------

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = std::is_default_constructible_v<storage_type>)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& default_construct(std::byte* destination) //
			noexcept(std::is_nothrow_default_constructible_v<storage_type>)
		{
			SOAGEN_ASSUME(destination != nullptr);

#if defined(__cpp_lib_start_lifetime_as) && __cpp_lib_start_lifetime_as >= 202207
			if constexpr (is_implicit_lifetime_type<storage_type>)
			{
				return *(
					std::start_lifetime_as<storage_type>(soagen::assume_aligned<alignof(storage_type)>(destination)));
			}
			else
			{
#endif
				return *(::new (static_cast<void*>(soagen::assume_aligned<alignof(storage_type)>(destination)))
							 storage_type);

#if defined(__cpp_lib_start_lifetime_as) && __cpp_lib_start_lifetime_as >= 202207
			}
#endif
		}

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = std::is_default_constructible_v<storage_type>)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& default_construct_at(std::byte* buffer, size_t element_index) //
			noexcept(std::is_nothrow_default_constructible_v<storage_type>)
		{
			SOAGEN_ASSUME(buffer != nullptr);

			return default_construct(buffer + element_index * sizeof(storage_type));
		}

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = std::is_default_constructible_v<storage_type>)
		SOAGEN_ATTR(nonnull)
		SOAGEN_CPP20_CONSTEXPR
		static void default_construct_at(std::byte* buffer, size_t start_index, size_t count) //
			noexcept(std::is_nothrow_default_constructible_v<storage_type>)
		{
			SOAGEN_ASSUME(buffer != nullptr);
			SOAGEN_ASSUME(count);

#if defined(__cpp_lib_start_lifetime_as) && __cpp_lib_start_lifetime_as >= 2022071
			if constexpr (is_implicit_lifetime_type<storage_type>)
			{
				std::start_lifetime_as_array<storage_type>(soagen::assume_aligned<alignof(storage_type)>(destination),
														   count);
			}
			else
#endif
				if constexpr (std::is_nothrow_default_constructible_v<storage_type>
							  || std::is_trivially_destructible_v<storage_type>)
			{
				for (const size_t e = start_index + count; start_index < e; start_index++)
					default_construct_at(buffer, start_index);
			}
			else
			{
				// machinery to provide strong-exception guarantee

				size_t i = start_index;

				try
				{
					for (const size_t e = start_index + count; i < e; i++)
						default_construct_at(buffer, i);
				}
				catch (...)
				{
					for (; i-- > start_index;)
						destruct_at(buffer, i);
					throw;
				}
			}
		}

		//--- construction ---------------------------------------------------------------------------------------------

		template <typename... Args>
		static constexpr bool is_constructible = std::is_constructible_v<storage_type, Args&&...>;
		template <typename T>
		static constexpr bool is_constructible<T*&> = std::is_same_v<storage_type, void*>;
		template <typename T>
		static constexpr bool is_constructible<T*&&> = std::is_same_v<storage_type, void*>;
		template <typename... Args>
		static constexpr bool is_constructible<emplacer<Args...>&&> = is_constructible<Args...>;

		template <typename... Args>
		static constexpr bool is_nothrow_constructible = std::is_nothrow_constructible_v<storage_type, Args&&...>;
		template <typename T>
		static constexpr bool is_nothrow_constructible<T*&> = std::is_same_v<storage_type, void*>;
		template <typename T>
		static constexpr bool is_nothrow_constructible<T*&&> = std::is_same_v<storage_type, void*>;
		template <typename... Args>
		static constexpr bool is_nothrow_constructible<emplacer<Args...>&&> = is_constructible<Args...>;

	  private:
		template <typename... Args, size_t... Indices>
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& construct_from_emplacer(std::byte* destination,
															   emplacer<Args...>&& args,
															   std::index_sequence<Indices...>) //
			noexcept(is_nothrow_constructible<Args...>)
		{
			static_assert(sizeof...(Args) == sizeof...(Indices));
			static_assert((std::is_reference_v<Args> && ...));

			if constexpr (std::is_aggregate_v<storage_type>)
			{
				return *(
					::new (static_cast<void*>(soagen::assume_aligned<alignof(storage_type)>(destination)))
						storage_type{ static_cast<Args>(
							*static_cast<std::add_pointer_t<std::remove_reference_t<Args>>>(args.ptrs[Indices]))... });
			}
			else
			{
				return *(
					::new (static_cast<void*>(soagen::assume_aligned<alignof(storage_type)>(destination)))
						storage_type(static_cast<Args>(
							*static_cast<std::add_pointer_t<std::remove_reference_t<Args>>>(args.ptrs[Indices]))...));
			}
		}

	  public:
		template <typename... Args>
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& construct_from_emplacer(std::byte* destination,
															   emplacer<Args...>&& args) //
			noexcept(is_nothrow_constructible<Args...>)
		{
			static_assert((std::is_reference_v<Args> && ...));

			return construct_from_emplacer(destination,
										   static_cast<emplacer<Args...>&&>(args),
										   std::make_index_sequence<sizeof...(Args)>{});
		}

		SOAGEN_CONSTRAINED_TEMPLATE(is_constructible<Args&&...>, typename... Args)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& construct(std::byte* destination, Args&&... args) //
			noexcept(is_nothrow_constructible<Args&&...>)
		{
			SOAGEN_ASSUME(destination != nullptr);

			if constexpr (sizeof...(Args) == 0)
			{
				return default_construct(destination);
			}
			else
			{
				if constexpr (sizeof...(Args) == 1										   //
							  && (std::is_pointer_v<std::remove_reference_t<Args>> && ...) //
							  && std::is_same_v<storage_type, void*>)
				{
					return *(
						::new (static_cast<void*>(soagen::assume_aligned<alignof(storage_type)>(destination)))
							storage_type{ const_cast<storage_type>(reinterpret_cast<const volatile void*>(args))... });
				}
				else if constexpr (sizeof...(Args) == 1 && (is_emplacer<std::remove_reference_t<Args>> && ...))
				{
					return construct_from_emplacer(destination, static_cast<Args&&>(args)...);
				}
				else if constexpr (std::is_aggregate_v<storage_type>)
				{
					return *(::new (static_cast<void*>(soagen::assume_aligned<alignof(storage_type)>(destination)))
								 storage_type{ static_cast<Args&&>(args)... });
				}
				else
				{
					return *(::new (static_cast<void*>(soagen::assume_aligned<alignof(storage_type)>(destination)))
								 storage_type(static_cast<Args&&>(args)...));
				}
			}
		}

		SOAGEN_CONSTRAINED_TEMPLATE(is_constructible<Args&&...>, typename... Args)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& construct_at(std::byte* buffer, size_t element_index, Args&&... args) //
			noexcept(is_nothrow_constructible<Args&&...>)
		{
			SOAGEN_ASSUME(buffer != nullptr);

			if constexpr (sizeof...(Args) == 0)
			{
				return default_construct(buffer + element_index * sizeof(storage_type));
			}
			else
			{
				return construct(buffer + element_index * sizeof(storage_type), static_cast<Args&&>(args)...);
			}
		}

		//--- move-construction ----------------------------------------------------------------------------------------

		static constexpr bool is_move_constructible =
			std::is_move_constructible_v<storage_type>
			|| (std::is_default_constructible_v<storage_type> && std::is_move_assignable_v<storage_type>);

		static constexpr bool is_nothrow_move_constructible = std::is_move_constructible_v<storage_type>
																? std::is_nothrow_move_constructible_v<storage_type>
																: (std::is_nothrow_default_constructible_v<storage_type>
																   && std::is_nothrow_move_assignable_v<storage_type>);

		static constexpr bool is_trivially_move_constructible =
			std::is_move_constructible_v<storage_type> ? std::is_trivially_move_constructible_v<storage_type>
													   : (std::is_trivially_default_constructible_v<storage_type>
														  && std::is_trivially_move_assignable_v<storage_type>);

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = is_move_constructible)
		SOAGEN_ATTR(nonnull)
		SOAGEN_CPP20_CONSTEXPR
		static storage_type& move_construct(std::byte* destination, std::byte* source) //
			noexcept(is_nothrow_move_constructible)
		{
			SOAGEN_ASSUME(destination != nullptr);
			SOAGEN_ASSUME(source != nullptr);
			SOAGEN_ASSUME(destination != source);

			if constexpr (std::is_move_constructible_v<storage_type>)
			{
				return construct(destination, static_cast<storage_type&&>(get(source)));
			}
			else
			{
				static_assert(std::is_default_constructible_v<storage_type>);
				static_assert(std::is_move_assignable_v<storage_type>);

				default_construct(destination);

				if constexpr (std::is_nothrow_move_assignable_v<storage_type>)
				{
					return move_assign(destination, source);
				}
				else
				{
					try
					{
						return move_assign(destination, source);
					}
					catch (...)
					{
						destruct(destination);
						throw;
					}
				}
			}
		}

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = std::is_move_constructible_v<storage_type>)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& move_construct_at(std::byte* dest_buffer,
														 size_t dest_element_index,
														 std::byte* source_buffer,
														 size_t source_element_index) //
			noexcept(std::is_nothrow_move_constructible_v<storage_type>)
		{
			SOAGEN_ASSUME(dest_buffer != nullptr);
			SOAGEN_ASSUME(source_buffer != nullptr);

			return move_construct(dest_buffer + dest_element_index * sizeof(storage_type),
								  source_buffer + source_element_index * sizeof(storage_type));
		}

		//--- copy-construction ----------------------------------------------------------------------------------------

		static constexpr bool is_copy_constructible =
			std::is_copy_constructible_v<storage_type>
			|| (std::is_default_constructible_v<storage_type> && std::is_copy_assignable_v<storage_type>);

		static constexpr bool is_nothrow_copy_constructible = std::is_copy_constructible_v<storage_type>
																? std::is_nothrow_copy_constructible_v<storage_type>
																: (std::is_nothrow_default_constructible_v<storage_type>
																   && std::is_nothrow_copy_assignable_v<storage_type>);

		static constexpr bool is_trivially_copy_constructible =
			std::is_copy_constructible_v<storage_type> ? std::is_trivially_copy_constructible_v<storage_type>
													   : (std::is_trivially_default_constructible_v<storage_type>
														  && std::is_trivially_copy_assignable_v<storage_type>);

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = is_copy_constructible)
		SOAGEN_ATTR(nonnull)
		SOAGEN_CPP20_CONSTEXPR
		static storage_type& copy_construct(std::byte* destination, const std::byte* source) //
			noexcept(is_nothrow_copy_constructible)
		{
			SOAGEN_ASSUME(destination != nullptr);
			SOAGEN_ASSUME(source != nullptr);
			SOAGEN_ASSUME(destination != source);

			if constexpr (std::is_copy_constructible_v<storage_type>)
			{
				return construct(destination, static_cast<const storage_type&>(get(source)));
			}
			else
			{
				static_assert(std::is_default_constructible_v<storage_type>);
				static_assert(std::is_copy_assignable_v<storage_type>);

				default_construct(destination);

				if constexpr (std::is_nothrow_copy_assignable_v<storage_type>)
				{
					return copy_assign(destination, source);
				}
				else
				{
					try
					{
						return copy_assign(destination, source);
					}
					catch (...)
					{
						destruct(destination);
						throw;
					}
				}
			}
		}

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = is_copy_constructible)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& copy_construct_at(std::byte* dest_buffer,
														 size_t dest_element_index,
														 const std::byte* source_buffer,
														 size_t source_element_index) //
			noexcept(is_nothrow_copy_constructible)
		{
			SOAGEN_ASSUME(dest_buffer != nullptr);
			SOAGEN_ASSUME(source_buffer != nullptr);

			return copy_construct(dest_buffer + dest_element_index * sizeof(storage_type),
								  source_buffer + source_element_index * sizeof(storage_type));
		}

		//--- destruction ----------------------------------------------------------------------------------------------

		SOAGEN_ATTR(nonnull)
		static constexpr void destruct([[maybe_unused]] std::byte* target) //
			noexcept(std::is_nothrow_destructible_v<storage_type>)
		{
			SOAGEN_ASSUME(target != nullptr);

			if constexpr (!std::is_trivially_destructible_v<storage_type>)
			{
				get(target).~storage_type();
			}
		}

		SOAGEN_ATTR(nonnull)
		static constexpr void destruct_at([[maybe_unused]] std::byte* buffer,	 //
										  [[maybe_unused]] size_t element_index) //
			noexcept(std::is_nothrow_destructible_v<storage_type>)
		{
			SOAGEN_ASSUME(buffer != nullptr);

			if constexpr (!std::is_trivially_destructible_v<storage_type>)
			{
				destruct(buffer + element_index * sizeof(storage_type));
			}
		}

		//--- move-assignment ------------------------------------------------------------------------------------------

		static constexpr bool is_move_assignable =
			std::is_move_assignable_v<storage_type>
			|| (std::is_nothrow_destructible_v<storage_type> && std::is_nothrow_move_constructible_v<storage_type>);

		static constexpr bool is_nothrow_move_assignable =
			std::is_move_assignable_v<storage_type>
				? std::is_nothrow_move_assignable_v<storage_type>
				: (std::is_nothrow_destructible_v<storage_type> && std::is_nothrow_move_constructible_v<storage_type>);

		static constexpr bool is_trivially_move_assignable =
			std::is_move_assignable_v<storage_type> ? std::is_trivially_move_assignable_v<storage_type>
													: (std::is_trivially_destructible_v<storage_type>
													   && std::is_trivially_move_constructible_v<storage_type>);

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = is_move_assignable)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& move_assign(std::byte* destination, void* source) //
			noexcept(is_nothrow_move_assignable)
		{
			SOAGEN_ASSUME(destination != nullptr);
			SOAGEN_ASSUME(source != nullptr);
			SOAGEN_ASSUME(destination != source);

			if constexpr (std::is_move_assignable_v<storage_type>)
			{
				return get(destination) = static_cast<storage_type&&>(get(static_cast<std::byte*>(source)));
			}
			else
			{
				// note we only fallback to this if they're nothrow because we don't want to leave the destination
				// in a half-constructed state (it existed before the assignment, it should still exist after)
				static_assert(std::is_nothrow_destructible_v<storage_type>);
				static_assert(std::is_nothrow_move_constructible_v<storage_type>);

				destruct(destination);
				return move_construct(destination, static_cast<std::byte*>(source));
			}
		}

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = is_move_assignable)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& move_assign_at(std::byte* dest_buffer,
													  size_t dest_element_index,
													  std::byte* source_buffer,
													  size_t source_element_index) //
			noexcept(is_nothrow_move_assignable)
		{
			SOAGEN_ASSUME(dest_buffer != nullptr);
			SOAGEN_ASSUME(source_buffer != nullptr);

			return move_assign(dest_buffer + dest_element_index * sizeof(storage_type),
							   source_buffer + source_element_index * sizeof(storage_type));
		}

		//--- copy-assignment ------------------------------------------------------------------------------------------

		static constexpr bool is_copy_assignable =
			std::is_copy_assignable_v<storage_type>
			|| (std::is_nothrow_destructible_v<storage_type> && std::is_nothrow_copy_constructible_v<storage_type>);

		static constexpr bool is_nothrow_copy_assignable =
			std::is_copy_assignable_v<storage_type>
				? std::is_nothrow_copy_assignable_v<storage_type>
				: (std::is_nothrow_destructible_v<storage_type> && std::is_nothrow_copy_constructible_v<storage_type>);

		static constexpr bool is_trivially_copy_assignable =
			std::is_copy_assignable_v<storage_type> ? std::is_trivially_copy_assignable_v<storage_type>
													: (std::is_trivially_destructible_v<storage_type>
													   && std::is_trivially_copy_constructible_v<storage_type>);

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = is_copy_assignable)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& copy_assign(std::byte* destination, const std::byte* source) //
			noexcept(is_nothrow_copy_assignable)
		{
			SOAGEN_ASSUME(destination != nullptr);
			SOAGEN_ASSUME(source != nullptr);
			SOAGEN_ASSUME(destination != source);

			if constexpr (std::is_copy_assignable_v<storage_type>)
			{
				return get(destination) = static_cast<const storage_type&>(get(source));
			}
			else
			{
				// note we only fallback to this if they're nothrow because we don't want to leave the destination
				// in a half-constructed state (it existed before the assignment, it should still exist after)
				static_assert(std::is_nothrow_destructible_v<storage_type>);
				static_assert(std::is_nothrow_move_constructible_v<storage_type>);

				destruct(destination);
				return copy_construct(destination, source);
			}
		}

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = is_copy_assignable)
		SOAGEN_ATTR(nonnull)
		static constexpr storage_type& copy_assign_at(std::byte* dest_buffer,
													  size_t dest_element_index,
													  const std::byte* source_buffer,
													  size_t source_element_index) //
			noexcept(is_nothrow_copy_assignable)
		{
			SOAGEN_ASSUME(dest_buffer != nullptr);
			SOAGEN_ASSUME(source_buffer != nullptr);

			return copy_assign(dest_buffer + dest_element_index * sizeof(storage_type),
							   source_buffer + source_element_index * sizeof(storage_type));
		}

		//--- swap -----------------------------------------------------------------------------------------------------

		static constexpr bool is_swappable =
			std::is_swappable_v<storage_type> || (is_move_constructible && is_move_assignable);

		static constexpr bool is_nothrow_swappable = std::is_swappable_v<storage_type>
													   ? std::is_nothrow_swappable_v<storage_type>
													   : (is_nothrow_move_constructible && is_nothrow_move_assignable);

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = is_swappable)
		SOAGEN_ATTR(nonnull)
		static constexpr void swap(std::byte* lhs, std::byte* rhs) //
			noexcept(is_nothrow_swappable)
		{
			SOAGEN_ASSUME(lhs != nullptr);
			SOAGEN_ASSUME(rhs != nullptr);
			SOAGEN_ASSUME(lhs != rhs);

			if constexpr (std::is_swappable_v<storage_type>)
			{
				using std::swap;
				swap(get(lhs), get(rhs));
			}
			else if constexpr (is_move_constructible && is_move_assignable)
			{
				storage_type temp(static_cast<storage_type&&>(get(lhs)));
				move_assign(lhs, rhs);
				move_assign(rhs, &temp);
			}
		}

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = is_swappable)
		SOAGEN_ATTR(nonnull)
		static constexpr void swap_at(std::byte* lhs_buffer,
									  size_t lhs_element_index,
									  std::byte* rhs_buffer,
									  size_t rhs_element_index) //
			noexcept(is_nothrow_swappable)
		{
			SOAGEN_ASSUME(lhs_buffer != nullptr);
			SOAGEN_ASSUME(rhs_buffer != nullptr);

			return swap(lhs_buffer + lhs_element_index * sizeof(storage_type),
						rhs_buffer + rhs_element_index * sizeof(storage_type));
		}

		//--- trivially-copy (memmove) ---------------------------------------------------------------------------------

		SOAGEN_HIDDEN_CONSTRAINT(sfinae, auto sfinae = std::is_trivially_copyable_v<storage_type>)
		static constexpr void trivially_copy(std::byte* dest_buffer,
											 size_t dest_element_index,
											 const std::byte* source_buffer,
											 size_t source_element_index,
											 size_t count) noexcept
		{
			SOAGEN_ASSUME(dest_buffer != nullptr);
			SOAGEN_ASSUME(source_buffer != nullptr);

			std::memmove(dest_buffer + dest_element_index * sizeof(storage_type),
						 source_buffer + source_element_index * sizeof(storage_type),
						 count * sizeof(storage_type));
		}
	};

}
/// @endcond

namespace soagen
{
	template <typename ValueType,
			  typename ParamType = param_type<ValueType>,
			  size_t Align		 = alignof(ValueType),
			  typename Base		 = detail::column_traits_base<storage_type<ValueType>>>
	struct column_traits : public Base
	{
		using value_type = ValueType;
		static_assert(!std::is_reference_v<value_type>, "column value_type may not be a reference");
		static_assert(!std::is_void_v<value_type>, "column value_type may not be void");
		static_assert(alignof(value_type) == alignof(typename Base::storage_type));
		static_assert(sizeof(value_type) == sizeof(typename Base::storage_type));

		using param_type = ParamType;
		static_assert(!std::is_void_v<param_type>, "column param_type may not be void");
		static_assert(std::is_convertible_v<param_type, value_type> || std::is_constructible_v<value_type, param_type>
						  || (std::is_pointer_v<param_type> && std::is_same_v<typename Base::storage_type, void*>),
					  "column value_type must be constructible or convertible from param_type");

		static constexpr size_t alignment = max(Align, alignof(value_type));
		static_assert(has_single_bit(alignment), "column alignment must be a power of two");

		static constexpr size_t max_capacity = static_cast<size_t>(-1) / sizeof(value_type);

		static constexpr size_t aligned_stride = lcm(alignment, sizeof(value_type)) / sizeof(value_type);
	};

	template <typename>
	inline constexpr bool is_column_traits = false;

	template <typename StorageType>
	inline constexpr bool is_column_traits<detail::column_traits_base<StorageType>> = true;

	template <typename ValueType, typename ParamType, size_t Align, typename Base>
	inline constexpr bool is_column_traits<column_traits<ValueType, ParamType, Align, Base>> = is_column_traits<Base>;

}

/// @cond
namespace soagen::detail
{
	template <typename T>
	struct to_base_traits_;

	template <typename ValueType, typename ParamType, size_t Align>
	struct to_base_traits_<column_traits<ValueType, ParamType, Align>>
	{
		using type = column_traits_base<storage_type<ValueType>>;

		static_assert(std::is_base_of_v<type, column_traits<ValueType, ParamType, Align>>);
	};

	template <typename T>
	using to_base_traits = typename to_base_traits_<T>::type;
}
/// @endcond

#include "header_end.hpp"
