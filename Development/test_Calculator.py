import Calculator
 
def test_Addition():
    assert Calculator.add(2,2) == 4
    assert Calculator.add(2) == 4
    assert Calculator.add(2) == 55
