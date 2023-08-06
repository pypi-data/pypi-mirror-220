// Copyright 2023PANDA GmbH
#include <drift_bytes/bytes.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using drift_bytes::Bytes;

PYBIND11_MODULE(_drift_bytes, m) {
  auto klass = py::class_<drift_bytes::Bytes>(m, "Bytes");
  klass.def(py::init<>())
      .def_static(
          "from_bytes",
          [](py::bytes bytes) { return drift_bytes::Bytes(std::move(bytes)); })
      .def("to_bytes",
           [](drift_bytes::Bytes &bytes) { return py::bytes(bytes.str()); })
      // Scalar types
      .def("get_bool",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<bool>(); })
      .def("set_bool",
           [](drift_bytes::Bytes &bytes, bool val) { bytes.scalar(val); })
      .def("get_int8",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<int8_t>(); })
      .def("set_int8",
           [](drift_bytes::Bytes &bytes, int8_t val) { bytes.scalar(val); })
      .def("get_int16",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<int16_t>(); })
      .def("set_int16",
           [](drift_bytes::Bytes &bytes, int16_t val) { bytes.scalar(val); })
      .def("get_int32",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<int32_t>(); })
      .def("set_int32",
           [](drift_bytes::Bytes &bytes, int32_t val) { bytes.scalar(val); })
      .def("get_int64",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<int64_t>(); })
      .def("set_int64",
           [](drift_bytes::Bytes &bytes, int64_t val) { bytes.scalar(val); })
      .def("get_uint8",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<uint8_t>(); })
      .def("set_uint8",
           [](drift_bytes::Bytes &bytes, uint8_t val) { bytes.scalar(val); })
      .def("get_uint16",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<uint16_t>(); })
      .def("set_uint16",
           [](drift_bytes::Bytes &bytes, uint16_t val) { bytes.scalar(val); })
      .def("get_uint32",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<uint32_t>(); })
      .def("set_uint32",
           [](drift_bytes::Bytes &bytes, uint32_t val) { bytes.scalar(val); })
      .def("get_uint64",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<uint64_t>(); })
      .def("set_uint64",
           [](drift_bytes::Bytes &bytes, uint64_t val) { bytes.scalar(val); })
      .def("get_float32",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<float>(); })
      .def("set_float32",
           [](drift_bytes::Bytes &bytes, float val) { bytes.scalar(val); })
      .def("get_float64",
           [](drift_bytes::Bytes &bytes) { return bytes.scalar<double>(); })
      .def("set_float64",
           [](drift_bytes::Bytes &bytes, double val) { bytes.scalar(val); })
      .def(
          "get_string",
          [](drift_bytes::Bytes &bytes) { return bytes.scalar<std::string>(); })
      .def("set_string", [](drift_bytes::Bytes &bytes,
                            const std::string &val) { bytes.scalar(val); })
      // Vector types
      .def("get_bool_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<bool>(); })
      .def("set_bool_vec", [](drift_bytes::Bytes &bytes,
                              const std::vector<bool> &val) { bytes.vec(val); })
      .def("get_int8_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<int8_t>(); })
      .def("set_int8_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<int8_t> &val) {
             bytes.vec(val);
           })
      .def("get_int16_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<int16_t>(); })
      .def("set_int16_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<int16_t> &val) {
             bytes.vec(val);
           })
      .def("get_int32_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<int32_t>(); })
      .def("set_int32_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<int32_t> &val) {
             bytes.vec(val);
           })
      .def("get_int64_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<int64_t>(); })
      .def("set_int64_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<int64_t> &val) {
             bytes.vec(val);
           })
      .def("get_uint8_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<uint8_t>(); })
      .def("set_uint8_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<uint8_t> &val) {
             bytes.vec(val);
           })
      .def("get_uint16_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<uint16_t>(); })
      .def("set_uint16_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<uint16_t> &val) {
             bytes.vec(val);
           })
      .def("get_uint32_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<uint32_t>(); })
      .def("set_uint32_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<uint32_t> &val) {
             bytes.vec(val);
           })
      .def("get_uint64_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<uint64_t>(); })
      .def("set_uint64_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<uint64_t> &val) {
             bytes.vec(val);
           })
      .def("get_float32_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<float>(); })
      .def("set_float32_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<float> &val) {
             bytes.vec(val);
           })
      .def("get_float64_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<double>(); })
      .def("set_float64_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<double> &val) {
             bytes.vec(val);
           })
      .def("get_string_vec",
           [](drift_bytes::Bytes &bytes) { return bytes.vec<std::string>(); })
      .def("set_string_vec",
           [](drift_bytes::Bytes &bytes, const std::vector<std::string> &val) {
             bytes.vec(val);
           });
}
