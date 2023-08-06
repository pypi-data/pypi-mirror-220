"""Test vectors in Bytes class"""
from drift_bytes import Bytes


def test__bool_vec():
    """Test bool vectors"""
    b = Bytes()
    b.set_bool_vec([True, False, True])
    assert b.get_bool_vec() == [True, False, True]
    b.set_bool_vec([False, True, False])
    assert b.get_bool_vec() == [False, True, False]


def test__int8_vec():
    """Test int8 vectors"""
    b = Bytes()
    b.set_int8_vec([0, 127, -128])
    assert b.get_int8_vec() == [0, 127, -128]
    b.set_int8_vec([127, -128, 0])
    assert b.get_int8_vec() == [127, -128, 0]


def test__int16_vec():
    """Test int16 vectors"""
    b = Bytes()
    b.set_int16_vec([0, 32767, -32768])
    assert b.get_int16_vec() == [0, 32767, -32768]
    b.set_int16_vec([32767, -32768, 0])
    assert b.get_int16_vec() == [32767, -32768, 0]


def test__int32_vec():
    """Test int32 vectors"""
    b = Bytes()
    b.set_int32_vec([0, 2147483647, -2147483648])
    assert b.get_int32_vec() == [0, 2147483647, -2147483648]
    b.set_int32_vec([2147483647, -2147483648, 0])
    assert b.get_int32_vec() == [2147483647, -2147483648, 0]


def test__int64_vec():
    """Test int64 vectors"""
    b = Bytes()
    b.set_int64_vec([0, 9223372036854775807, -9223372036854775808])
    assert b.get_int64_vec() == [0, 9223372036854775807, -9223372036854775808]
    b.set_int64_vec([9223372036854775807, -9223372036854775808, 0])
    assert b.get_int64_vec() == [9223372036854775807, -9223372036854775808, 0]


def test__uint8_vec():
    """Test uint8 vectors"""
    b = Bytes()
    b.set_uint8_vec([0, 255])
    assert b.get_uint8_vec() == [0, 255]
    b.set_uint8_vec([255, 0])
    assert b.get_uint8_vec() == [255, 0]


def test__uint16_vec():
    """Test uint16 vectors"""
    b = Bytes()
    b.set_uint16_vec([0, 65535])
    assert b.get_uint16_vec() == [0, 65535]
    b.set_uint16_vec([65535, 0])
    assert b.get_uint16_vec() == [65535, 0]


def test__uint32_vec():
    """Test uint32 vectors"""
    b = Bytes()
    b.set_uint32_vec([0, 4294967295])
    assert b.get_uint32_vec() == [0, 4294967295]
    b.set_uint32_vec([4294967295, 0])
    assert b.get_uint32_vec() == [4294967295, 0]


def test__uint64_vec():
    """Test uint64 vectors"""
    b = Bytes()
    b.set_uint64_vec([0, 18446744073709551615])
    assert b.get_uint64_vec() == [0, 18446744073709551615]
    b.set_uint64_vec([18446744073709551615, 0])
    assert b.get_uint64_vec() == [18446744073709551615, 0]


def test__float32_vec():
    """Test float32 vectors"""
    b = Bytes()
    b.set_float32_vec([0.0, 1.0, -1.0])
    assert b.get_float32_vec() == [0.0, 1.0, -1.0]
    b.set_float32_vec([1.0, -1.0, 0.0])
    assert b.get_float32_vec() == [1.0, -1.0, 0.0]


def test__float64_vec():
    """Test float64 vectors"""
    b = Bytes()
    b.set_float64_vec([0.0, 1.0, -1.0])
    assert b.get_float64_vec() == [0.0, 1.0, -1.0]
    b.set_float64_vec([1.0, -1.0, 0.0])
    assert b.get_float64_vec() == [1.0, -1.0, 0.0]


def test__string_vec():
    """Test string vectors"""
    b = Bytes()
    b.set_string_vec(["", "a", "abc"])
    assert b.get_string_vec() == ["", "a", "abc"]
    b.set_string_vec(["abc", "a", ""])
    assert b.get_string_vec() == ["abc", "a", ""]
