import mock
import pytest
from copy import deepcopy
from collections.abc import MutableMapping
from typing import Any, Iterator, Mapping
from ..persistent import WithPersistentParameters


@pytest.fixture
def mock_persistent():
    remote_dict = MockHashObjSetting()

    def init(self):
        self._parameters = remote_dict

    with mock.patch.object(WithPersistentParameters, "__init__", init):
        yield remote_dict


class MockHashObjSetting(MutableMapping):
    def __init__(self) -> None:
        self._adict = dict()
        super().__init__()

    def __repr__(self) -> str:
        return repr(self._adict)

    def get_all(self) -> dict:
        return deepcopy(self._adict)

    def __getitem__(self, key: str) -> Any:
        return self._adict[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, Mapping):
            value = deepcopy(value)
        self._adict[key] = value

    def __delitem__(self, key: str) -> None:
        del self._adict[key]

    def __iter__(self) -> Iterator[Any]:
        yield from self._adict

    def __len__(self) -> int:
        return len(self._adict)
