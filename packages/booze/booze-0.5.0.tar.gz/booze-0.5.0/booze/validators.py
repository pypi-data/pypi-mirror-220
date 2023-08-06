import re
from abc import ABC, abstractmethod
from booze.errors import *
from contextlib import suppress
with suppress(ImportError):
    from booze.coercer import Coerce
    

class Validator(ABC):
    @abstractmethod
    def __init__(self, coercer: 'Coerce'):
        raise NotImplementedError
    
    @abstractmethod
    def __call__(self, value):
        raise NotImplementedError


class Integer(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    
    def __call__(self, value):
        try:
            self.coercer.value = int(value)
            return True
        except (TypeError, ValueError):
            return False


class Float(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
        
    def __call__(self, value):
        try:
            self.coercer.value = float(value)
            return True
        except (TypeError, ValueError):
            return False


class Boolean(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer

    def __call__(self, value):
        if self.coercer.value is None:
            return False
        if isinstance(value, bool):
            return True
        elif value == 1:
            self.coercer.value = True
            return True
        elif value == 0:
            self.coercer.value = False
            return True
        return False


class String(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
        
    def __call__(self, value):
        self.coercer.value = str(value)
        return isinstance(value, str)


class List(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    def __call__(self, value):
        return isinstance(value, list)


class Dictionary(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    def __call__(self, value):
        return isinstance(value, dict)


class Min(Validator):
    def __init__(self, coercer: 'Coerce', value):
        self.coercer = coercer
        self.min = value
        
    def __call__(self, value):
        try:
            if self.min is None:
                return False
            
            if not isinstance(value, int) and not isinstance(value, float):
                return False
            
            if self.min < value:
                return True
            
            else:
                return False
            
        except (TypeError, ValueError) as e:
            return False


class Max(Validator):
    def __init__(self, coercer: 'Coerce', value):
        self.coercer = coercer
        self.max = value
        
    def __call__(self, value):
        try:
            if not isinstance(value, int) and not isinstance(value, float):
                return False
            if value > self.max:
                return False
            else:
                return True
        except (TypeError, ValueError):
            return False


class Length(Validator):
    def __init__(self, coercer: 'Coerce', length_min, length_max):
        self.coercer = coercer
        self.length_min = length_min
        self.length_max = length_max
        
    def __call__(self, value):
        test = self.length_min <= len(value) <= self.length_max
        return test


class MinLength(Validator):
    def __init__(self, coercer: 'Coerce', length_min):
        self.coercer = coercer
        self.length_min = length_min
        
    def __call__(self, value):
        test = self.length_min <= len(value)
        return test


class MaxLength(Validator):
    def __init__(self, coercer: 'Coerce', length_max):
        self.coercer = coercer
        self.length_max = length_max
        
    def __call__(self, value):
        test = len(value) <= self.length_max
        return test


class Contains(Validator):
    def __init__(self, coercer: 'Coerce', value):
        self.coercer = coercer
        self.value = value
    def __call__(self, value):
        return self.value in value


class Email(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    def __call__(self, value):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, value) is not None


class Numeric(Validator):
    def __init__(self, coercer: 'Coerce'):
        self.coercer = coercer
    def __call__(self, value):
        return isinstance(value, (int, float))
