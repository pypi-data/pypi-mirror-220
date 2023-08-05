from ..persistent import WithPersistentParameters


def test_persistent_parameters(mock_persistent):
    class MyParameters(WithPersistentParameters, parameters=["a", "b"]):
        def __init__(self) -> None:
            super().__init__()
            self._set_parameter_default("a", 1)

    parameters = MyParameters()

    expected = {"a": 1}
    assert mock_persistent == expected
    assert parameters.a == 1
    assert parameters.b is None

    parameters.a = 2
    expected["a"] = 2
    assert mock_persistent == expected
    assert parameters.a == 2

    parameters = MyParameters()
    assert parameters.a == 2

    parameters.a = None
    expected["a"] = None
    assert mock_persistent == {"a": None}
    assert parameters.a is None
    assert parameters.b is None


def test_persistent_parameters_dict(mock_persistent):
    class MyParameters(WithPersistentParameters, parameters=["adict"]):
        def __init__(self) -> None:
            super().__init__()
            self._set_parameter_default("adict", dict())

    parameters = MyParameters()
    expected = {}

    assert mock_persistent == {"adict": expected}
    assert parameters.adict == expected

    parameters.adict["a"] = 2
    parameters.adict["fix"] = -1
    expected["adict"] = {"a": 2, "fix": -1}
    assert mock_persistent == expected
    assert parameters.adict == expected["adict"]

    parameters.adict["a"] = {"x": 1, "fix": -2}
    expected["adict"]["a"] = {"x": 1, "fix": -2}
    assert mock_persistent == expected
    assert parameters.adict["a"]["x"] == 1

    parameters.adict["a"]["x"] = {"y": 2, "fix": -3}
    expected["adict"]["a"]["x"] = {"y": 2, "fix": -3}
    assert mock_persistent == expected
    assert parameters.adict["a"]["x"]["y"] == 2

    parameters.adict["a"]["x"]["y"] = 3
    expected["adict"]["a"]["x"]["y"] = 3
    assert mock_persistent == expected
    assert parameters.adict["a"]["x"]["y"] == 3
