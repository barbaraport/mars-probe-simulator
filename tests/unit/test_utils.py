from uuid import uuid4

from tests.utils import is_valid_uuid


def test_when_is_valid_uuid_then_should_return_true():
    assert is_valid_uuid(str(uuid4()))


def test_when_is_invalid_uuid_then_should_return_false():
    assert not is_valid_uuid("invalid")
