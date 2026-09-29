from project import radians, coordinate_transf, kin_en, pot_en
import pytest 
import math


def test_radians():
  assert radians(0) == 0
  assert radians(45) == math.pi/4
  assert radians(-90) == -math.pi/2


def test_kin_en():
  assert kin_en(1, 1, 0, 0, 1, 1, 1, 1) == 0
  assert kin_en(0.1, 0.1, 0, 1, 1, 1, 1, 1) == 0.5
  assert kin_en(1, 1, 1, 0, 1, 1, 1, 1) == 1
 
def test_pot_en():
  assert math.floor(pot_en(10, 10)) == 980 # Otherwise the idenitity does not hold due to numerical errors
  assert pot_en(0, 10) == 0
  assert pot_en(10, 0) == 0

def test_coordinate_transf():
  assert coordinate_transf(1, 1, 0, 0) == (0, -1, 0, -2)


