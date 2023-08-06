"""Test for Bytes"""
import pytest

from drift_bytes import Bytes


def test__bad_encoding():
    """Test bad encoding"""
    b = Bytes()
    b.set_bool(True)

    with pytest.raises(RuntimeError):
        b.get_float32()


def test_serialization():
    """Test serialization"""
    b = Bytes()
    b.set_int8(42)

    b = Bytes.from_bytes(b.to_bytes())
    assert b.get_int8() == 42
