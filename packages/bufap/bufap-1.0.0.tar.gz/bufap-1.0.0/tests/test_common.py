import pytest
from bufap import common


@pytest.mark.parametrize(
    ("size", "expected"),
    [("100MB", 100000000), ("100GB", 100000000000), ("10.28KB", 10280)],
)
def test_convert_to_byte(size: str, expected: int):
    assert common.convert_to_byte(size) == expected
