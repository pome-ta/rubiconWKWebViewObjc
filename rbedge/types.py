import ctypes

from pyrubicon.objc.types import CGFloat, with_preferred_encoding, __LP64__

if __LP64__:
  _NSDirectionalEdgeInsets = b'{NSDirectionalEdgeInsets=dddd}'
else:
  _NSDirectionalEdgeInsets = b'{NSDirectionalEdgeInsets=ffff}'


@with_preferred_encoding(_NSDirectionalEdgeInsets)
class NSDirectionalEdgeInsets(ctypes.Structure):
  _fields_ = [
    ('top', CGFloat),
    ('leading', CGFloat),
    ('bottom', CGFloat),
    ('trailing', CGFloat),
  ]

  def __repr__(self):
    return f'<NSDirectionalEdgeInsets({self.top}, {self.leading}, {self.bottom}, {self.trailing})>'

  def __str__(self):
    return f'top={self.top}, leading={self.leading}, bottom={self.bottom}, trailing={self.trailing}'


def NSDirectionalEdgeInsetsMake(top, leading, bottom, trailing):
  return NSDirectionalEdgeInsets(top, leading, bottom, trailing)

