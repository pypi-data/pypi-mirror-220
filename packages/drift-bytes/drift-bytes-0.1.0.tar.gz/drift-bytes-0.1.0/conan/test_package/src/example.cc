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
