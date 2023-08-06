// Copyright 2023 PANDA GmbH

#ifndef DRIFT_BYTES_BYTES_H_
#define DRIFT_BYTES_BYTES_H_

#include <array>
#include <cassert>
#include <functional>
#include <iostream>
#include <numeric>
#include <ostream>
#include <sstream>
#include <string>
#include <vector>

#include <cereal/archives/portable_binary.hpp>
#include <cereal/types/string.hpp>
#include <cereal/types/vector.hpp>

namespace drift_bytes {

/**
 * Serializes and deserializes variables.
 */
class Bytes {
 public:
  using Shape = std::vector<size_t>;

  Bytes() = default;
  explicit Bytes(std::string &&bytes) { buffer_ << bytes; }

  std::string str() const { return buffer_.str(); }

  template <typename T>
  T scalar() {
    cereal::PortableBinaryInputArchive archive(buffer_);
    T t;
    archive(t);
    return t;
  }

  template <typename T>
  std::vector<T> vec() {
    cereal::PortableBinaryInputArchive archive(buffer_);
    std::vector<T> t;
    archive(t);
    return t;
  }

  template <typename T>
  std::vector<std::vector<T>> mat() {
    cereal::PortableBinaryInputArchive archive(buffer_);
    std::vector<std::vector<T>> t;
    archive(t);
    return t;
  }

  template <typename T>
  void scalar(const T &t) {
    cereal::PortableBinaryOutputArchive archive(buffer_);
    archive(t);
  }

  template <typename T>
  void vec(const std::vector<T> &t) {
    cereal::PortableBinaryOutputArchive archive(buffer_);
    archive(t);
  }

  template <typename T>
  void mat(const std::vector<std::vector<T>> &t) {
    cereal::PortableBinaryOutputArchive archive(buffer_);
    archive(t);
  }

 private:
  std::stringstream buffer_;
};

}  // namespace drift_bytes
#endif  // DRIFT_BYTES_BYTES_H_
