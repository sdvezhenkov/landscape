import pytest
from pydantic import BaseModel, Field, ValidationError

from app.tools.essential.model.cast.cast_model import cast_model


class ExampleType1(BaseModel):
    a: int = 1
    b: dict = Field(default_factory=dict)


class ExampleType2(BaseModel):
    a: int
    b: dict


class ExampleType3(BaseModel):
    a: int = 1


class ExampleType4(BaseModel):
    a: int


def test_cast_model_mapping():
    passed_type = ExampleType1
    expected_type = ExampleType2
    passed_model = passed_type()
    expected_model = cast_model(passed_model, expected_type)
    assert type(expected_model) is expected_type
    assert expected_model.a == passed_model.a
    assert expected_model.b == passed_model.b

def test_cast_model_downcast():
    passed_type = ExampleType1
    expected_type = ExampleType4
    passed_model = passed_type()
    expected_model = cast_model(passed_model, expected_type)
    assert type(expected_model) is expected_type
    assert expected_model.a == passed_model.a

def test_cast_model_upcast():
    passed_type = ExampleType3
    expected_type = ExampleType2
    passed_model = passed_type()
    with pytest.raises(ValidationError):
        cast_model(passed_model, expected_type)
