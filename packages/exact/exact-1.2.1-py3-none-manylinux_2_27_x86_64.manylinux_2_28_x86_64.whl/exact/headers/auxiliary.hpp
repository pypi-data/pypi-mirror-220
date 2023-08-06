/**********************************************************************
This file is part of Exact.

Copyright (c) 2022 Jo Devriendt

Exact is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation.

Exact is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
License version 3 for more details.

You should have received a copy of the GNU Affero General Public
License version 3 along with Exact. See the file used_licenses/COPYING
or run with the flag --license=AGPLv3. If not, see
<https://www.gnu.org/licenses/>.
**********************************************************************/

/**********************************************************************
This file is part of the Exact program

Copyright (c) 2021 Jo Devriendt, KU Leuven

Exact is distributed under the terms of the MIT License.
You should have received a copy of the MIT License along with Exact.
See the file LICENSE or run with the flag --license=MIT.
**********************************************************************/

/**********************************************************************
Copyright (c) 2014-2020, Jan Elffers
Copyright (c) 2019-2021, Jo Devriendt
Copyright (c) 2020-2021, Stephan Gocht
Copyright (c) 2014-2021, Jakob Nordström

Parts of the code were copied or adapted from MiniSat.

MiniSat -- Copyright (c) 2003-2006, Niklas Een, Niklas Sorensson
           Copyright (c) 2007-2010  Niklas Sorensson

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
**********************************************************************/

#pragma once

#define EXPANDED(x) STR(x)
#define STR(x) #x

#include <algorithm>
#include <boost/multiprecision/cpp_int.hpp>
#include <cassert>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <list>
#include <numeric>
#include <optional>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include "external/ankerl/unordered_dense.h"

#if UNIXLIKE
namespace xct {
inline std::ostream& operator<<(std::ostream& o, const __int128& x) {
  if (x == std::numeric_limits<__int128>::min()) return o << "-170141183460469231731687303715884105728";
  if (x < 0) return o << "-" << -x;
  if (x < 10) return o << (char)(x + '0');
  return o << x / 10 << (char)(x % 10 + '0');
}
}  // namespace xct
using int128 = __int128;
#else
using int128 = boost::multiprecision::int128_t;
#endif
using int256 = boost::multiprecision::int256_t;
using bigint = boost::multiprecision::cpp_int;
using ratio = boost::multiprecision::cpp_rational;

template <typename K, typename V, typename H = std::hash<K>>
using unordered_map = ankerl::unordered_dense::map<K, V, H>;
// using unordered_map = std::unordered_map<K, V, H>;

template <typename K, typename H = std::hash<K>>
using unordered_set = ankerl::unordered_dense::set<K, H>;
// using unordered_set = std::unordered_set<K, H>;

enum class State { SUCCESS, FAIL };
enum class SolveState { UNSAT, SAT, INCONSISTENT, TIMEOUT, INPROCESSED };
std::ostream& operator<<(std::ostream& o, enum SolveState state);

namespace xct {

template <typename T, typename U>
std::ostream& operator<<(std::ostream& o, const std::pair<T, U>& p) {
  o << p.first << "," << p.second;
  return o;
}
template <typename T, typename U, typename HASH>
std::ostream& operator<<(std::ostream& o, const unordered_map<T, U, HASH>& m) {
  for (const auto& e : m) o << e << ";";
  return o;
}
template <typename T, typename HASH>
std::ostream& operator<<(std::ostream& o, const unordered_set<T, HASH>& m) {
  for (const auto& e : m) o << e << " ";
  return o;
}
template <typename T>
std::ostream& operator<<(std::ostream& o, const std::vector<T>& m) {
  for (const auto& e : m) o << e << " ";
  return o;
}
template <typename T>
std::ostream& operator<<(std::ostream& o, const std::list<T>& m) {
  for (const auto& e : m) o << e << " ";
  return o;
}

namespace aux {

template <typename T>
T sto(const std::string& s) {
  return std::stold(s);
}
template <>
inline double sto(const std::string& s) {
  return std::stod(s);
}
template <>
inline std::string sto(const std::string& s) {
  return s;
}

template <typename T>
void swapErase(T& indexable, size_t index) {
  indexable[index] = std::move(indexable.back());
  indexable.pop_back();
}

template <typename T>
bool contains(const std::vector<T>& v, const T& x) {
  return std::find(v.cbegin(), v.cend(), x) != v.cend();
}

template <typename T>
T ceildiv(const T& p, const T& q) {
  assert(q > 0);
  assert(p >= 0);
  return p / q + (p % q != 0);
}
template <typename T>
T floordiv(const T& p, const T& q) {
  assert(q > 0);
  assert(p >= 0);
  return p / q;
}
template <typename T>
T ceildiv_safe(const T& p, const T& q) {
  assert(q > 0);
  return p / q + (p % q != 0 && p > 0);
}
template <typename T>
T floordiv_safe(const T& p, const T& q) {
  assert(q > 0);
  return p / q - (p % q != 0 && p < 0);
}
template <typename T, typename S>
S mod_safe(const T& p, const S& q) {
  assert(q > 0);
  if (p < 0) {
    return static_cast<S>(q - (-p % q));
  } else {
    return static_cast<S>(p % q);
  }
}

template <typename T>
T median(std::vector<T>& v) {
  assert(v.size() > 0);
  size_t n = v.size() / 2;
  std::nth_element(v.cbegin(), v.cbegin() + n, v.cend());
  return v[n];
}

template <typename T>
double average(const std::vector<T>& v) {
  assert(v.size() > 0);
  return std::accumulate(v.cbegin(), v.cend(), 0.0) / (double)v.size();
}

template <typename CONTAINER>
auto min(CONTAINER&& v) {
  return *std::min_element(v.cbegin(), v.cend());
}

template <typename CONTAINER>
auto max(CONTAINER&& v) {
  return *std::max_element(v.cbegin(), v.cend());
}

template <typename A, typename B>
void appendTo(A& x, const B& y) {
  x.insert(x.end(), y.cbegin(), y.cend());
}

template <typename T>
int sgn(const T& x) {
  return (0 < x) - (x < 0);
}

template <typename T>
T abs(const T& x) {
  return std::abs(x);
}
template <>
inline int128 abs(const int128& x) {
#if UNIXLIKE
  return x < 0 ? -x : x;
#else
  return boost::multiprecision::abs(x);
#endif
}
template <>
inline int256 abs(const int256& x) {
  return boost::multiprecision::abs(x);
}
template <>
inline bigint abs(const bigint& x) {
  return boost::multiprecision::abs(x);
}
template <typename S, typename R, typename U>
inline bigint abs(const boost::multiprecision::detail::expression<S, R, U>& x) {  // boost expression template fix
  return boost::multiprecision::abs(bigint(x));
}

template <typename T>
T min(const T& x, const T& y) {
  return std::min(x, y);
}
template <>
inline int128 min(const int128& x, const int128& y) {
  return x <= y ? x : y;
}
template <>
inline int256 min(const int256& x, const int256& y) {
  return x <= y ? x : y;
}
template <>
inline bigint min(const bigint& x, const bigint& y) {
  return boost::multiprecision::min(x, y);
}

template <typename T>
T max(const T& x, const T& y) {
  return std::max(x, y);
}
template <>
inline int128 max(const int128& x, const int128& y) {
  return x >= y ? x : y;
}
template <>
inline int256 max(const int256& x, const int256& y) {
  return x >= y ? x : y;
}
template <>
inline bigint max(const bigint& x, const bigint& y) {
  return boost::multiprecision::max(x, y);
}

template <typename T>
T gcd(const T& x, const T& y) {
  return std::gcd(x, y);
}
template <>
inline int128 gcd(const int128& x, const int128& y) {
  return static_cast<int128>(
      boost::multiprecision::gcd(boost::multiprecision::int128_t(x), boost::multiprecision::int128_t(y)));
}
template <>
inline int256 gcd(const int256& x, const int256& y) {
  return boost::multiprecision::gcd(x, y);
}
template <>
inline bigint gcd(const bigint& x, const bigint& y) {
  return boost::multiprecision::gcd(x, y);
}

template <typename T>
double toDouble(const T& x) {
  double res = static_cast<double>(x);
  assert(std::isfinite(res));
  return res;
}

template <>
inline double toDouble(const bigint& x) {
  double res = static_cast<double>(x);
  if (!std::isfinite(res)) {
    res = x < 0 ? std::numeric_limits<double>::lowest() : std::numeric_limits<double>::max();
  }
  assert(std::isfinite(res));
  return res;
}

template <typename T>
double divToDouble(const T& num, const T& denom) {
  double res = static_cast<double>(num) / static_cast<double>(denom);
  assert(std::isfinite(res));
  return res;
}

template <>
inline double divToDouble(const bigint& num, const bigint& denom) {
  double res = static_cast<double>(static_cast<ratio>(num) / static_cast<ratio>(denom));
  assert(std::isfinite(res));
  return res;
}

template <typename T>
unsigned msb(const T& x) {
  assert(x > 0);
  // return std::bit_floor(x); // C++20
  return boost::multiprecision::msb(boost::multiprecision::int128_t(x));
}
template <>
inline unsigned msb(const int256& x) {
  assert(x > 0);
  return boost::multiprecision::msb(x);
}
template <>
inline unsigned msb(const bigint& x) {
  assert(x > 0);
  return boost::multiprecision::msb(x);
}

template <typename T>
T powtwo(unsigned y) {
  return uint32_t(1) << y;
}
template <>
inline long long powtwo(unsigned y) {
  return uint64_t(1) << y;
}
template <>
inline int128 powtwo(unsigned y) {
  return static_cast<int128>(boost::multiprecision::pow(boost::multiprecision::int128_t(2), y));
}
template <>
inline int256 powtwo(unsigned y) {
  return boost::multiprecision::pow(int256(2), y);
}
template <>
inline bigint powtwo(unsigned y) {
  return boost::multiprecision::pow(bigint(2), y);
}

inline double log(double base, double arg) { return std::log(arg) / std::log(base); }

bigint commonDenominator(const std::vector<ratio>& ratios);

template <typename T, typename U>
T timeCall(const std::function<T(void)>& f, U& to) {
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  T result = f();
  to += std::chrono::duration_cast<std::chrono::duration<double>>(std::chrono::steady_clock::now() - start).count();
  return result;
}
template <typename U>
void timeCallVoid(const std::function<void(void)>& f, U& to) {
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  f();
  to += std::chrono::duration_cast<std::chrono::duration<double>>(std::chrono::steady_clock::now() - start).count();
}

inline std::ostream& prettyPrint(std::ostream& o, const long double& z) {
  long long iz = static_cast<long long>(z);
  if (iz == z) {
    return o << iz;
  } else {
    return o << z;
  }
}

template <typename SMALL, typename LARGE>
SMALL cast(const LARGE& x) {
  if (std::numeric_limits<SMALL>::is_specialized) {
    assert(std::numeric_limits<SMALL>::max() == 0 || static_cast<LARGE>(std::numeric_limits<SMALL>::max()) >= x);
    assert(std::numeric_limits<SMALL>::lowest() == 0 || static_cast<LARGE>(std::numeric_limits<SMALL>::lowest()) <= x);
  }
  return static_cast<SMALL>(x);
}

template <typename T>
std::optional<T> option(bool make, const T& val) {
  if (make) return std::make_optional<T>(val);
  return std::nullopt;
}

namespace rng {

extern uint32_t seed; /* The seed must be initialized to non-zero */
uint32_t xorshift32();
}  // namespace rng

int32_t getRand(int32_t min, int32_t max);
uint64_t hash(uint64_t x);

template <typename Element, typename Iterable>
uint64_t hashForSet(const Iterable& els) {
  uint64_t result = els.size();
  for (const Element& el : els) {
    result ^= hash(std::hash<Element>()(el));
  }
  return result;
}

template <typename Element, typename Iterable>
uint64_t hashForList(const Iterable& els) {
  uint64_t result = els.size();
  for (const Element& el : els) {
    result ^= hash(std::hash<Element>()(el)) + 0x9e3779b9 + (result << 6) + (result >> 2);
  }
  return result;
}

template <typename T>
const std::string str(const T& t) {
  std::stringstream ss;
  ss << t;
  return ss.str();
}

template <typename... Args>
using predicate = std::function<bool(Args...)>;

template <typename CONTAINER, typename LAM_MAP>
auto comprehension(CONTAINER&& container, LAM_MAP&& map) {
  std::vector<decltype(map(*container.begin()))> w;
  w.reserve(container.size());
  std::transform(container.begin(), container.end(), std::back_inserter(w), map);
  return w;
}

template <typename CONTAINER, typename LAM_MAP, typename LAM_FILTER>
auto comprehension(CONTAINER&& container, LAM_MAP&& map, LAM_FILTER&& filter) {
  std::vector<decltype(map(*container.begin()))> w;
  w.reserve(container.size());
  for (const auto& el : container) {
    if (filter(el)) w.push_back(map(el));
  }
  return w;
}

}  // namespace aux

}  // namespace xct
