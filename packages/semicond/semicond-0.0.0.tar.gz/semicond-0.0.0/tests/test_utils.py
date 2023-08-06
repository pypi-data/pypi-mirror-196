import semicond as sc

class MyObj:
    pass

def test_ensure_list():
    assert sc.ensure_list(1) == [1]
    assert sc.ensure_list("123") == ["123"]
    assert sc.ensure_list((1, 2, 3)) == [1, 2, 3]
    obj = MyObj()
    assert sc.ensure_list(obj) == [obj]
