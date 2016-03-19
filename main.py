#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

from random import random
import cairo


PI = 3.14159265359
TWOPI = 2.0*PI
BACK = [1,1,1,1]
FRONT = [0,0,0,1.0]
SIZE = 1000
ONE = 1./SIZE
LINEWIDTH = ONE

NEW_COUNT = 100

RES = 'out.png'


def is_ok(x1, y1, r1, x2, y2, r2):
  return ((x1-x2)**2 + (y1-y2)**2) > (r1 + r2 + 2*ONE)**2

def add_new_circles(n, circles):

  for i in xrange(n):
    xn = random()
    yn = random()
    rn = ONE

    ok = True
    for c in circles:

      if not is_ok(xn, yn, rn, c['x'], c['y'], c['r']):
        ok = False
        break

    if ok:
      circles.append({
        'x': xn, 
        'y': yn, 
        'r': rn, 
        'active': True
      })

def increase_radius(circles):

  for c in circles:
    if c['active']:
      c['r'] += ONE

def test(circles):

  ok_count = 0

  for a, ca in enumerate(circles):

    for b, cb in enumerate(circles):

      if a == b:
        continue

      if not cb['active']:
        continue

      if not is_ok(ca['x'], ca['y'], ca['r'], cb['x'], cb['y'], cb['r']):
        cb['active'] = False

      else:
        ok_count += 1

  return ok_count


def show(ctx, circles):

  ctx.set_source_rgba(*FRONT)

  for c in circles:
    ctx.arc(c['x'], c['y'], c['r'], 0, TWOPI)
    ctx.stroke()


def main():

  sur = cairo.ImageSurface(cairo.FORMAT_ARGB32, SIZE, SIZE)
  ctx = cairo.Context(sur)
  ctx.scale(SIZE, SIZE)

  ctx.set_source_rgba(*BACK)
  ctx.set_line_width(LINEWIDTH)
  ctx.rectangle(0.0, 0.0, 1.0, 1.0)
  ctx.fill()


  circles = []
  add_new_circles(NEW_COUNT, circles)

  for i in xrange(1000):

    increase_radius(circles)

    ok_count = test(circles)

    if ok_count < 1:

      add_new_circles(NEW_COUNT, circles)

      print(i, 'adding new circles, total count: ' + str(len(circles)))

  show(ctx, circles)

  sur.write_to_png(RES)


if __name__ == '__main__':
  main()

