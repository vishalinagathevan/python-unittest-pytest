import Mathlip
def test_calc_addition():
    output = Mathlip.calc_addition(10, 20)
    assert output == 30
    
def test_calc_multiple():  
    output = Mathlip.calc_multiple(10,2)
    assert output == 20  