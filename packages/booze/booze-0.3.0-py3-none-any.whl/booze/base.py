import inspect


class Base:
    """
    The Base class is a metaprogramming-based class that allows automatic parsing and validation of keyword arguments
    passed during object creation. It provides a convenient way to create objects with pre-defined validation rules
    for attributes.
    """
    def __new__(cls, **kwargs):
        parsers = {}
        for key, item in cls.__dict__.items():
            if not str(key).startswith('_') :
                parsers[key] = item
        
        def repr(self):
            string = '<'
            string += type(self).__name__
            string += '(' + ', '.join([
                f"{key}='{item}'" if isinstance(item, str) else f"{key}={item}"
                for key, item in self.__dict__.items()
            ])
            string += ')>'
            return string
        
        def to_dict(self):
            return {
                key: getattr(self, key) for key in parsers
                if not inspect.ismethod(getattr(self, key))
            }

        cls.__repr__ = repr
        cls.__str__ = repr
        cls.to_dict = to_dict
        
        obj = object.__new__(cls)
        for key, value in kwargs.items():
            
            parser = parsers[key]
            parsed = parser.parse(value)
            
            obj.__setattr__(key, parsed)
            
        return obj
