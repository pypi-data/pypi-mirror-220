# Python DriftBytes

Python bindings for [DriftBytes](https://github.com/panda-official/DriftBytes).

## Requirements

* Python >= 3.8
* CMake >= 3.16 (for building)
* C++17 compiler (for building)
* conan >= 1.56, < 2.0 (for building)

## Installation

```bash
pip install drift-bytes
```

## Usage Example

```python
from drift_bytes import Bytes

byte_buffer = Bytes()
byte_buffer.set_int8(42)
val = byte_buffer.get_int8()

print(val)
```
