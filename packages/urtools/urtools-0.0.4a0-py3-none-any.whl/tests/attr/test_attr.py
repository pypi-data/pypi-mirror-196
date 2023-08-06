#pylint:disable=invalid-name,missing-class-docstring,missing-function-docstring
from urtools.attr import getattrs, getdunder, getpriv

class Test_getattrs:
    def test_str_0(self):
        attrs = getattrs("", mode=0)
        assert all(not a.startswith("_") for a in attrs)
    def test_str_1(self):
        attrs = getattrs("", mode=1)
        assert all(not a.startswith("__") for a in attrs)
        
    def test_str_2(self):
        attrs = getattrs("", mode=2)
        assert any(a.startswith("__") for a in attrs)
    def test_str_many(self):
        attrs0 = set(getattrs("", mode=0))
        attrs1 = set(getattrs("", mode=1))
        attrs2 = set(getattrs("", mode=2))
        assert attrs0 <= attrs1 <= attrs2

def test_getdunder():
    assert all(x.startswith("__") and x.endswith("__") for x in getdunder(""))
    
def test_getpriv():
    assert all(x.startswith("_") and not x.startswith("__") for x in getpriv(""))
    