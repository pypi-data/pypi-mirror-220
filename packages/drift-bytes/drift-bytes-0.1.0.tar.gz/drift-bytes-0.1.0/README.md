# DriftBytes

A serializer for typed data in the Drift infrastructure.

## Description

This is an alternative to [WaveletBuffer](https://github.com/panda-official/WaveletBuffer) that uses a different serialization format
which is suitable for non-floating point data.

## Features

* Supports all integer types
* Supports all floating point types
* Supports UTF-8 strings
* Supports vectors and matrices of all supported types

## Requirements

* CMake >= 3.16
* C++17 compiler
* conan >= 1.56, < 2.0


## Usage Example

```c++
#include <drift_bytes/bytes.h>

#include <iostream>

using drift_bytes::Bytes;

int main() {
    uint8_t val{42};
    auto bytes = Bytes();
    bytes.scalar(val);
    auto new_val = bytes.scalar<uint8_t>();

    std::cout << new_val << std::endl;
}
```

## Bulding

```bash
mkdir build && cd build
conan install ../conan --build=missing -of .
cmake .. -DCMAKE_TOOLCHAIN_FILE=./build/Release/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build .
```
