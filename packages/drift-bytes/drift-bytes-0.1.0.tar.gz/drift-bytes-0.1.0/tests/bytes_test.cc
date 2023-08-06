// Copyright 2023 PANDA GmbH

#include <drift_bytes/bytes.h>

#include <limits>

#include <catch2/catch_test_macros.hpp>

#include "catch2/generators/catch_generators.hpp"

using drift_bytes::Bytes;

TEST_CASE("Scalars") {
  auto val = GENERATE(
      true, std::numeric_limits<uint8_t>::max(),
      std::numeric_limits<uint16_t>::max(),
      std::numeric_limits<uint32_t>::max(),
      std::numeric_limits<uint64_t>::max(), std::numeric_limits<int8_t>::max(),
      std::numeric_limits<int16_t>::max(), std::numeric_limits<int32_t>::max(),
      std::numeric_limits<int64_t>::max(), std::numeric_limits<float>::max(),
      std::numeric_limits<double>::max());

  CAPTURE(val);

  auto bytes = drift_bytes::Bytes();
  bytes.scalar(val);

  decltype(val) new_val;
  new_val = bytes.scalar<decltype(val)>();

  REQUIRE(new_val == val);
}

TEST_CASE("Strings") {
  std::string val =
      GENERATE("Hello", "World", "Hello World", "Hello World!", "äöü");

  CAPTURE(val);

  auto bytes = drift_bytes::Bytes();
  bytes.scalar(val);

  auto new_val = bytes.scalar<decltype(val)>();

  REQUIRE(new_val == val);
}

TEST_CASE("Vectors") {
  std::vector<int> val = GENERATE(std::vector<int>{1, 2, 3, 4, 5},
                                  std::vector<int>{1, 2, 3, 4, 5, 6, 7, 8, 9});

  CAPTURE(val);

  auto bytes = drift_bytes::Bytes();
  bytes.vec(val);

  auto new_val = bytes.vec<int>();

  REQUIRE(new_val == val);
}

TEST_CASE("Matrices") {
  std::vector<std::vector<int>> val = GENERATE(
      std::vector<std::vector<int>>{{1, 2}, {3, 4}, {5, 6}, {7, 8}, {9, 10}},
      std::vector<std::vector<int>>{{1, 2, 3, 4, 5}, {6, 7, 8, 9, 10}});

  CAPTURE(val);

  auto bytes = drift_bytes::Bytes();
  bytes.vec(val);

  auto new_val = bytes.mat<int>();

  REQUIRE(new_val == val);
}

TEST_CASE("Mixed data") {
  int a;
  std::vector<float> fvec = {1.0, 2.0, 3.0};
  std::string s = "Hello World!";
  std::vector<std::vector<int>> mat = {{1, 2, 3}, {4, 5, 6}};

  auto bytes = drift_bytes::Bytes();
  bytes.scalar(a);
  bytes.vec(fvec);
  bytes.scalar(s);
  bytes.mat(mat);

  auto new_a = bytes.scalar<decltype(a)>();
  auto new_fvec = bytes.vec<float>();
  auto new_s = bytes.scalar<decltype(s)>();
  auto new_mat = bytes.mat<int>();

  REQUIRE(new_a == a);
  REQUIRE(new_fvec == fvec);
  REQUIRE(new_s == s);
  REQUIRE(new_mat == mat);
}

TEST_CASE("Serialization") {
  std::vector<std::vector<int>> mat = {{1, 2, 3}, {4, 5, 6}};

  auto bytes = drift_bytes::Bytes();
  bytes.mat(mat);

  bytes = drift_bytes::Bytes(bytes.str());

  auto new_mat = bytes.mat<int>();
  REQUIRE(new_mat == mat);
}
