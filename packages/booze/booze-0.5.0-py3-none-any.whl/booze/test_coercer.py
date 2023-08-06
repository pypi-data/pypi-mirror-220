from booze import Coerce, ParsingError
import pytest


def test_integer_validation():
    coerce = Coerce('integer').integer()
    assert coerce.parse(42) == 42
    assert coerce.parse("42") == 42

    with pytest.raises(ParsingError):
        coerce.parse("not_an_integer")


def test_float_validation():
    coerce = Coerce('float').float()

    assert coerce.parse(3.14) == 3.14
    assert coerce.parse("3.14") == 3.14

    with pytest.raises(ParsingError):
        coerce.parse("not_a_float")


def test_boolean_validation():
    coerce = Coerce('boolean').boolean()

    assert coerce.parse(True) is True
    assert coerce.parse(1) is True
    assert coerce.parse(False) is False
    assert coerce.parse(0) is False

    with pytest.raises(ParsingError):
        coerce.parse("not_a_boolean")

def test_string_validation():
    coerce = Coerce().string()
    
    assert coerce.parse("Hello, World!") == "Hello, World!"
    with pytest.raises(ParsingError):
        coerce.parse(42)

def test_list_validation():
    coerce = Coerce().list()

    assert coerce.parse([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ParsingError):
        coerce.parse("not_a_list")

def test_dictionary_validation():
    coerce = Coerce().dictionary()
    
    assert coerce.parse({"key": "value", "number": 42}) == {"key": "value", "number": 42}

    with pytest.raises(ParsingError):
        coerce.parse("not_a_dict")

def test_min_validation():
    coerce = Coerce().integer().min(5)
    
    assert coerce.parse(10) == 10

    with pytest.raises(ParsingError):
        coerce.parse(3)

def test_max_validation():
    coerce = Coerce().float().max(10.0)
    
    assert coerce.parse(5.5) == 5.5

    with pytest.raises(ParsingError):
        coerce.parse(15.0)

def test_length_validation():
    coerce = Coerce().string().length(5)
    
    assert coerce.parse("hello") == "hello"

    with pytest.raises(ParsingError):
        coerce.parse("hello world")

def test_contains_validation():
    coerce = Coerce().list().contains(42)
    
    assert coerce.parse([1, 2, 42, 3]) == [1, 2, 42, 3]

    with pytest.raises(ParsingError):
        coerce.parse([1, 2, 3])

def test_email_validation():
    coerce = Coerce()
    coerce.email()
    assert coerce.parse("test@example.com") == "test@example.com"

    with pytest.raises(ParsingError):
        coerce.parse("invalid_email")

def test_numeric_validation():
    coerce = Coerce().numeric().float()
    
    assert coerce.parse(3.14) == 3.14

    with pytest.raises(ParsingError):
        coerce.parse("not_a_numeric_value")

# Add more test functions for other validation rules as needed...

# Example of a test case for an unknown validation rule
def test_unknown_validation_rule():
    coerce = Coerce()
    with pytest.raises(AttributeError):
        coerce.unknown_rule()

