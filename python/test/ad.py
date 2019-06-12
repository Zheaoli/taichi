import taichi_lang as ti
from pytest import approx
import math
import autograd.numpy as np
from autograd import grad

def test_size1():
  ti.reset()
  x = ti.var(ti.i32)

  @ti.layout
  def place():
    ti.root.dense(ti.i, 1).place(x)

  x[0] = 1
  assert x[0] == 1

# test_size1()

def grad_test(tifunc, npfunc=None):
  if npfunc is None:
    npfunc = tifunc
  ti.reset()

  x = ti.var(ti.f32)
  y = ti.var(ti.f32)

  @ti.layout
  def place():
    ti.root.dense(ti.i, 1).place(x, x.grad, y, y.grad)

  @ti.kernel
  def func():
    for i in x:
      y[i] = tifunc(x[i])

  v = 0.2

  y.grad[0] = 1
  x[0] = v
  func()
  func.grad()

  assert y[0] == approx(npfunc(v))
  assert x.grad[0] == approx(grad(npfunc)(v))

def test_poly():
  grad_test(lambda x: x)
  grad_test(lambda x: x * x)
  grad_test(lambda x: ti.sqr(x))
  grad_test(lambda x: x * x * x)
  grad_test(lambda x: x * x * x * x)
  grad_test(lambda x: 0.4 * x * x - 3)
  grad_test(lambda x: (x - 3) * (x - 1))
  grad_test(lambda x: (x - 3) * (x - 1) + x * x)

def test_trigonometric():
  grad_test(lambda x: ti.sin(x), lambda x: np.sin(x))
  grad_test(lambda x: ti.cos(x), lambda x: np.cos(x))
