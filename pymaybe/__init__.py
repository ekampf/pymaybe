# -*- coding: utf-8 -*-

__author__ = 'Eran Kampf'
__email__ = 'eran@ekampf.com'
__version__ = '0.1.6'

from sys import getsizeof


class Maybe(object):
    pass


class Nothing(Maybe):
    def is_some(self):
        return False

    def is_none(self):
        return True

    def get(self):
        raise Exception('No such element')

    def or_else(self, els=None):
        if callable(els):
            return els()

        return els

    def __call__(self, *args, **kwargs):
        return Nothing()

    # region Comparison

    def __cmp__(self, other):
        if other.__class__ == Nothing:
            return 0

        return -1

    def __eq__(self, other):
        if other.__class__ == Nothing:
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if other.__class__ == Nothing:
            return False

        if other.__class__ == Something:
            return True

        return True if other else False

    def __gt__(self, other):
        return False

    def __le__(self, other):
        return True

    def __ge__(self, other):
        if other.__class__ == Nothing:
            return True

        if other is None:
            return True

        return False

    # endregion

    def __getattr__(self, name):
        return Nothing()

    # region Dict
    def __len__(self):
        return 0

    def __getitem__(self, key):
        return Nothing()

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    # endregion

    # region Custom representation
    def __repr__(self):
        return repr(None)

    def __str__(self):
        return str(None)

    def __unicode__(self):
        return unicode(None)

    def __nonzero__(self):
        return False

    # endregion


class Something(Maybe):
    def __init__(self, value):
        self.__value = value

    def __call__(self, *args, **kwargs):
        return maybe(self.__value(*args, **kwargs))

    # region Comparison
    def __cmp__(self, other):
        if other.__class__ == Nothing:
            return 1

        if other.__class__ == Something:
            return cmp(self.get(), other.get())
        else:
            return cmp(self.get(), other)

    def __eq__(self, other):
        if other.__class__ == Nothing:
            return False

        if other.__class__ == Something:
            return self.get() == other.get()

        return self.get() == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if other.__class__ == Nothing:
            return False

        if other.__class__ == Something:
            return self.get() < other.get()

        return self.get() < other

    def __gt__(self, other):
        if other.__class__ == Nothing:
            return True

        if other.__class__ == Something:
            return self.get() > other.get()

        return self.get() > other

    def __le__(self, other):
        if other.__class__ == Nothing:
            return False

        if other.__class__ == Something:
            return self.get() <= other.get()

        return self.get() <= other

    def __ge__(self, other):
        if other.__class__ == Nothing:
            return True

        if other.__class__ == Something:
            return self.get() >= other.get()

        return self.get() >= other
    # endregion

    def is_some(self):
        return True

    def is_none(self):
        return False

    def get(self):
        return self.__value

    # pylint: disable=W0613
    def or_else(self, els=None):
        return self.__value

    def __getattr__(self, name):
        try:
            return maybe(getattr(self.__value, name))
        except Exception:
            return Nothing()

    def __setattr__(self, name, v):
        if name == "_Something__value":
            return super(Something, self).__setattr__(name, v)

        return setattr(self.__value, name, v)

    # region Containers Methods

    def __len__(self):
        return len(self.__value)

    def __getitem__(self, key):
        try:
            return maybe(self.__value[key])
        except (KeyError, TypeError, IndexError):
            return Nothing()

    def __setitem__(self, key, value):
        self.__value[key] = value

    def __delitem__(self, key):
        del self.__value[key]

    def __iter__(self):
        try:
            iterator = iter(self.__value)
        except TypeError:
            iterator = iter([self.__value])

        return iterator

    def __reversed__(self):
        return maybe(reversed(self.__value))

    def __missing__(self, key):
        klass = self.__value.__class__
        if hasattr(klass, '__missing__') and \
                callable(getattr(klass, '__missing__')):
            return maybe(self.__value.__missing__(key))

        return Nothing()

    # endregion

    # region Custom representation

    def __repr__(self):
        return repr(self.__value)

    def __str__(self):
        return str(self.__value)

    def __int__(self):
        return int(self.__value)

    def __long__(self):
        return long(self.__value)

    def __float__(self):
        return float(self.__value)

    def __complex__(self):
        return complex(self.__value)

    def __oct__(self):
        return oct(self.__value)

    def __hex__(self):
        return hex(self.__value)

    def __index__(self):
        return self.__value.__index__()

    def __trunc__(self):
        return self.__value.__trunc__()

    def __coerce__(self, other):
        return coerce(self.__value, other)

    def __unicode__(self):
        return unicode(self.__value)

    def __nonzero__(self):
        return True

    def __dir__(self):
        return dir(self.__value)

    def __sizeof__(self):
        return getsizeof(self.__value)

    # endregion

    # region Arithmetics

    def __add__(self, other):
        return maybe(self.__value + other)

    def __sub__(self, other):
        return maybe(self.__value - other)

    def __mul__(self, other):
        return maybe(self.__value * other)

    def __floordiv__(self, other):
        return maybe(self.__value // other)

    def __div__(self, other):
        return maybe(self.__value / other)

    def __mod__(self, other):
        return maybe(self.__value % other)

    def __divmod__(self, other):
        """Implements behavior for long division using the divmod() built in function."""
        return maybe(divmod(self.__value, other))

    def __pow__(self, other):
        """Implements behavior for exponents using the ** operator."""
        return maybe(self.__value ** other)

    def __lshift__(self, other):
        """Implements left bitwise shift using the << operator."""
        return maybe(self.__value << other)

    def __rshift__(self, other):
        """Implements right bitwise shift using the >> operator."""
        return maybe(self.__value >> other)

    def __and__(self, other):
        """Implements bitwise and using the & operator."""
        return maybe(self.__value & other)

    def __or__(self, other):
        """Implements bitwise or using the | operator."""
        return maybe(self.__value | other)

    def __xor__(self, other):
        """Implements bitwise xor using the ^ operator."""
        return maybe(self.__value ^ other)

    def __radd__(self, other):
        """Implements reflected addition."""
        return maybe(other + self.__value)

    def __rsub__(self, other):
        """Implements reflected subtraction."""
        return maybe(other - self.__value)

    def __rmul__(self, other):
        """Implements reflected multiplication."""
        return maybe(other * self.__value)

    def __rfloordiv__(self, other):
        """Implements reflected integer division using the // operator."""
        return maybe(other // self.__value)

    def __rdiv__(self, other):
        """Implements reflected division using the / operator."""
        return maybe(other / self.__value)

    def __rmod__(self, other):
        """Implements reflected modulo using the % operator."""
        return maybe(other % self.__value)

    def __rdivmod__(self, other):
        """Implements behavior for long division using the divmod() built in function, when divmod(other, self) is called."""
        return maybe(divmod(other, self.__value))

    def __rpow__(self, other):
        """Implements behavior for reflected exponents using the ** operator."""
        return maybe(other ** self.__value)

    def __rlshift__(self, other):
        """Implements reflected left bitwise shift using the << operator."""
        return maybe(other << self.__value)

    def __rrshift__(self, other):
        """Implements reflected right bitwise shift using the >> operator."""
        return maybe(other >> self.__value)

    def __rand__(self, other):
        """Implements reflected bitwise and using the & operator."""
        return maybe(other & self.__value)

    def __ror__(self, other):
        """Implements reflected bitwise or using the | operator."""
        return maybe(other | self.__value)

    def __rxor__(self, other):
        """Implements reflected bitwise xor using the ^ operator."""
        return maybe(other ^ self.__value)

    # endregion

    # region Augmented assignment

    def __iadd__(self, other):
        """Implements addition with assignment."""
        self.__value += other
        return self

    def __isub__(self, other):
        """Implements subtraction with assignment."""
        self.__value -= other
        return self

    def __imul__(self, other):
        """Implements multiplication with assignment."""
        self.__value *= other
        return self

    def __ifloordiv__(self, other):
        """Implements integer division with assignment using the //= operator."""
        self.__value //= other
        return self

    def __idiv__(self, other):
        """Implements division with assignment using the /= operator."""
        self.__value /= other
        return self

    def __imod__(self, other):
        """Implements modulo with assignment using the %= operator."""
        self.__value %= other
        return self

    def __ipow__(self, other):
        """Implements behavior for exponents with assignment using the **= operator."""
        self.__value **= other
        return self

    def __ilshift__(self, other):
        """Implements left bitwise shift with assignment using the <<= operator."""
        self.__value <<= other
        return self

    def __irshift__(self, other):
        """Implements right bitwise shift with assignment using the >>= operator."""
        self.__value >>= other
        return self

    def __iand__(self, other):
        """Implements bitwise and with assignment using the &= operator."""
        self.__value &= other
        return self

    def __ior__(self, other):
        """Implements bitwise or with assignment using the |= operator."""
        self.__value |= other
        return self

    def __ixor__(self, other):
        """Implements bitwise xor with assignment using the ^= operator."""
        self.__value ^= other
        return self

    # endregion


def maybe(value):
    """Wraps an object with a Maybe instance.

      >>> maybe("I'm a value")
      "I'm a value"

      >>> maybe(None);
      None

      Testing for value:

        >>> maybe("I'm a value").is_some()
        True
        >>> maybe("I'm a value").is_none()
        False
        >>> maybe(None).is_some()
        False
        >>> maybe(None).is_none()
        True

      Simplifying IF statements:

        >>> maybe("I'm a value").get()
        "I'm a value"

        >>> maybe("I'm a value").or_else(lambda: "No value")
        "I'm a value"

        >>> maybe(None).get()
        Traceback (most recent call last):
        ...
        Exception: No such element

        >>> maybe(None).or_else(lambda: "value")
        'value'

        >>> maybe(None).or_else("value")
        'value'

      Wrap around values from object's attributes:

        class Person(object):
            def __init__(name):
                self.eran = name

        eran = maybe(Person('eran'))

        >>> eran.name
        'eran'
        >>> eran.phone_number
        None
        >>> eran.phone_number.or_else('no phone number')
        'no phone number'

        >>> maybe(4) + 8
        12
        >>> maybe(4) - 2
        2
        >>> maybe(4) * 2
        8

      And methods:

        >>> maybe('VALUE').lower()
        'value'
        >>> maybe(None).invalid().method().or_else('unknwon')
        'unknwon'

      Enabled easily using NestedDictionaries without having to worry
      if a value is missing.
      For example lets assume we want to load some value from the
      following dictionary:
        nested_dict = maybe({
            'store': {
                'name': 'MyStore',
                    'departments': {
                    'sales': { 'head_count': '10' }
                }
            }
        })

        >>> nested_dict['store']['name']
        'MyStore'
        >>> nested_dict['store']['address']
        None
        >>> nested_dict['store']['address']['street'].or_else('No Address Specified')
        'No Address Specified'
        >>> nested_dict['store']['departments']['sales']['head_count'].or_else('0')
        '10'
        >>> nested_dict['store']['departments']['marketing']['head_count'].or_else('0')
        '0'

    """
    if isinstance(value, Maybe):
        return value

    if value is not None:
        return Something(value)

    return Nothing()


def get_doctest_globs():
    class Person(object):
        def __init__(self, name):
            self.name = name

    eran = Person('eran')

    globals_dict = {
        'nested_dict': maybe({
            'store': {
                'name': 'MyStore',
                'departments': {
                    'sales': {'head_count': '10'}
                }
            }
        }),
        'eran': maybe(eran),
        'maybe': maybe,
    }

    return globals_dict


if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=get_doctest_globs())
