from coercer.errors import ParsingError
from coercer.base import Base
from coercer.coercer import Coerce



def test_parsing_error_json():
    class MyClass(Base):
        name = Coerce('name').string().length(3, 10)

    try:
        obj = MyClass(name="John Doe")
        assert obj.name == "John Doe" 
    except ParsingError as error:
        error_json = error.json()
        assert error_json == {
            'Error': 'Input value for "name" must have a length between 3 and 10 characters.',
            'ValidationFunction': '_validate_length',
            'Coercer': 'Coerce'
        }


def test_parsing_error_str():
    class MyClass(Base):
        age = Coerce('age').integer().min(18).max(100)

    try:
        obj = MyClass(age="invalid")
        assert obj.age == "invalid"
    except ParsingError as error:
        error_str = str(error)
        assert error_str == 'ParsingError: Erro na validação dos dados do valor invalid, ValidationFunction: validator: Integer, Coercer: Coercer Coerce(age=invalid)'


def test_parsing_error_coercer_name():
    class MyClass(Base):
        weight = Coerce('weight').float().min(50.0).max(100.0)
        
    try:
        obj = MyClass(weight=120.0)
        assert obj.weight == 120.0
    except ParsingError as error:
        error_json = error.json()
        assert error_json == {
            'Error': 'Erro na validação dos dados do valor 120.0',
            'ValidationFunction': 'validator: Max',
            'Coercer': 'Coercer Coerce(weight=120.0)'
        }


def test_parsing_error_different_validations():
    class MyClass(Base):
        num = Coerce('num').integer().min(10).max(50)
        fav_colors = Coerce('fav_colors').list().contains("blue")

    try:
        obj = MyClass(num="30", fav_colors=["red", "green"])
        assert obj.num == 30
        assert obj.fav_colors == ["red", "green"]
    except ParsingError as error:
        error_json = error.json()
        assert error_json == {
            'Error': 'Erro na validação dos dados do valor 30',
            'ValidationFunction': 'validator: Min',
            'Coercer': 'Coercer Coerce(num=30)'
        }
