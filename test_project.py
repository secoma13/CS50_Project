from project import get_mass_length, get_init_cond, ode_fun, radians, coordinate_transf
import pytest 
import math


def test_radians():
  assert radians(0) == 0
  assert radians(45) == math.pi/4
  assert radians(-90) == -math.pi/2

def test_coordinate_tranf():
  pass

def test_ode_fun():
  pass
