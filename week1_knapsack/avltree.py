# copyright (c) 2005 Antoon Pardon
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

left, right = 0, 1
root, dummy = left, right
opposite = (1,0)

left_scale, in_balance, right_scale = 0, 1, 2

down = (left_scale, right_scale)
more = (-1, 1)

class NoKey(Exception):
  pass

class TreeError(Exception):
  pass

class Cell:
  def __init__(self):
    self.child = [None, None]
    self.scale = in_balance
    self.key = None
    self.value = None
  #end __init__
#end Cell

class NotImplemented(Exception):
  pass

class Thread:
  def __init__(self, reference):
    self.ref = reference
  #end __init__
#end Thread

def thread_on(c):
  if isinstance(c, Thread):
    return c
  else:
    return Thread(c)
  #end if
#end thread_on

def thread_off(c):
  if isinstance(c, Thread):
    return c.ref
  else:
    return c
  #end if
#end thread_off

def is_thread(c):
  return isinstance(c, Thread)
#end is_thread

class Tree(object):

  cmp = cmp

  def __init__(*args, **kwds):
    self = args[0]
    self.child = [None, None]
    self.child[root] = thread_on(self)
    self.child[dummy] = None 
    self.nr_of_items = 0
    self.stamp = 0
    Tree.update(*args, **kwds)
  #end __init__

  def __setitem__(self, key, value):
    error = None
    this = self.child[root]
    old = self
    old.child[left] = None
    old.scale = in_balance
    insert_side = left
    dirs = 0
    thread = [None, None]
    while 1:
      if is_thread(this):
        thread[insert_side] = this
        thread[opposite[insert_side]] = thread_on(old)
        this = Cell()
        this.child[left] = thread[left]
        this.child[right] = thread[right]
        this.scale = in_balance
        this.key = key
        this.value = value
        self.nr_of_items += 1
        self.stamp += 1
        grown = True
        found = False
        break
      #end if
      try:
        diff = self.cmp(key, this.key)
      except:
        diff = 0
        value = this.value
        error = KeyError
      #end try
      if diff < 0:
        this, old = turn(this, old, left)
        insert_side = left
	dirs = 2 * dirs + insert_side
      elif diff > 0:
        this, old = turn(this, old, right)
        insert_side = right
	dirs = 2 * dirs + insert_side
      else:
        this.value = value
        grown = False
        found = True
	break
      #end if
    #end while
    while old is not None:
      insert_side = dirs % 2
      dirs = dirs / 2
      old, this = turn(old, this, insert_side)
      if grown:
        if this.scale == down[insert_side]:
          this = balance(this)
          grown = False
        else:
          this.scale += more[insert_side]
          grown = this.scale != in_balance
	#end if
      #end if
    #end while
    assert this is self
    if error is not None:
      raise KeyError, key
    #end if
  #end __setitem__

  def __len__(self):
    return self.nr_of_items

  def __contains__(self, key):
    try:
      self.get(key, NoKey)
      return True
    except KeyError:
      return False
    #end try
  #end __contains__

  has_key = __contains__

  def __getitem__(self, key):
    if isinstance(key, slice):
      return Tree_Iterator(self, key.start, key.stop, key.step, 0)
    #end if
    return self.get(key, NoKey)
  #end __getitem__

  def get(self, key, default = None):
    this = self.child[root]
    while 1:
      if is_thread(this):
        if default is NoKey:
          raise KeyError, key
        else:
          return default
	#end if
      #end if
      try:
        diff = self.cmp(key, this.key)
      except:
        raise KeyError, key
      #end try
      if diff < 0:
        this = this.child[left]
      elif diff > 0:
        this = this.child[right]
      else:
        return this.value
      #end if
    #end while
  #end get

  def pop(self, key, default = NoKey):
    this = self.child[root]
    old = self
    old.child[left] = None
    old.scale = in_balance
    result = default
    delete_side = left
    dirs = 0
    while 1:
      if is_thread(this):
        shrunk = False
        break
      #end if
      try:
        diff = self.cmp(key, this.key)
      except:
        shrunk = False
        result = NoKey
        break
      #end try
      if diff < 0:
        this, old = turn(this, old, left)
	delete_side = left
	dirs = 2 * dirs + delete_side
      elif diff > 0:
        this, old = turn(this, old, right)
	delete_side = right
	dirs = 2 * dirs + delete_side
      else:
        result = this.value
        self.nr_of_items -= 1
        self.stamp += 1
        if this.scale == left_scale:
          delete_side = left
        elif this.scale == right_scale:
          delete_side = right
        #end if
        other_side = opposite[delete_side]
        while not is_thread(this.child[delete_side]):
          this, old = turn(this, old, delete_side)
	  dirs = 2 * dirs + delete_side
          while not is_thread(this.child[other_side]):
            this, old = turn(this, old, other_side)
	    dirs = 2 * dirs + other_side
          #end while
          target = thread_off(this.child[other_side])
          target.key, target.value = this.key, this.value
        #end while
        delete_side = dirs % 2
        this = this.child[delete_side]
        shrunk = True
	break
      #end if
    #end while
    while old is not None:
      delete_side = dirs % 2
      dirs = dirs / 2
      old, this = turn(old, this, delete_side)
      if shrunk:
        if this.scale == down[opposite[delete_side]]:
          this = balance(this)
          shrunk = this.scale == in_balance
        else:
          this.scale -= more[delete_side]
          shrunk = this.scale == in_balance
        #end if
      #end if
    #end while
    assert this is self
    if result is NoKey:
      raise KeyError, key
    else:
      return result
    #end if
  #end pop

  def __delitem__(self, key):
    self.pop(key, None)
  #end __delitem__

  def __cmp__(self, tree):
    diff = self.cmp(len(self), len(tree))
    if diff != 0:
      return diff
    #end if
    if not isinstance(tree, Tree):
      tree = Tree(tree)
    #end if
    one = Cell()
    one.child = 2 * [self.child[root]]
    two = Cell()
    two.child = 2 * [tree.child[root]]
    while 1:
      one = neighbour(one, right)
      two = neighbour(two, right)
      if one is self and two is tree:
        return 0
      else:
        assert one is not self
        assert two is not tree
        diff = self.cmp((one.key, one.value),(two.key, two.value))
        if diff != 0:
          return diff
	#end if
      #end if
    #end while
  #end __cmp__


  def popitem(self):

    if self.nr_of_items == 0:
      raise KeyError
    #end if
    this = Cell() 
    this.child = 2 * [self.child[root]]
    this = neighbour(this, right)
    key = this.key
    value = self.pop(key)
    return key, value
  #end popitem

  def setdefault(self, key, default = None):
    try:
      return self[key]
    except KeyError:
      self[key] = default
      return default
    #end try
  #end setdefault

  def clear(self):
    self.nr_of_items = 0
    self.stamp += 1
    self.child[root] = thread_on(self)
  #end clear

  def update(*args, **kwargs):
    self = args[0]
    for seq in args[1:]:
      try:
        for k, v in seq.iteritems():
          self[k] = v
        #end for
        return
      except AttributeError:
        pass
      #end try
      try:
        for k in seq.iterkeys():
          self[k] = seq[k]
        #end for
        return
      except AttributeError:
        pass
      #end try
      try:
        for k in seq.keys():
          self[k] = seq[k]
        #end for
        return
      except AttributeError:
        pass
      #end try
      for k, v in seq:
        self[k] = v
      #end for
    #end for
    for k, v in kwargs.iteritems():
      self[k] = v
    #end for
  #end update

  def copy(self):
    cp = Tree(self)
    return cp
  #end copy

  def iterkeys(self, start = None, stop = None, step = None):
    return Tree_Iterator(self, start, stop, step, 0)
  #end iterkeys

  __iter__ = iterkeys

  def keys(self, start = None, stop = None, step = None):
    return list(self.iterkeys(start, stop, step))
  #end keys

  def itervalues(self, start = None, stop = None, step = None):
    return Tree_Iterator(self, start, stop, step, 1)
  #end itervalues

  def values(self, start = None, stop = None, step = None):
    return list(self.itervalues(start, stop, step))
  #end values

  def iteritems(self, start = None, stop = None, step = None):
    return Tree_Iterator(self, start, stop, step, slice(None,None,None))
  #end iteritems

  def items(self, start = None, stop = None, step = None):
    return list(self.iteritems(start, stop, step))
  #end items

  #@classmethod
  def fromkeys(cls, seq, value = None):
    tree = cls()
    for k in seq:
      tree[k] = value
    return tree
  #end fromkeys
  fromkeys = classmethod(fromkeys)
#end Tree

def turn(one, two, side):
  tmp = one
  one = one.child[side]
  tmp.child[side] = two
  two = tmp
  return one, two
#end turn

def rotate(cell, heavy_side):
  tmp = cell.child[heavy_side]
  cell.child[heavy_side] = tmp.child[opposite[heavy_side]]
  if is_thread(cell.child[heavy_side]):
    cell.child[heavy_side] = thread_on(tmp)
  #end if
  tmp.child[opposite[heavy_side]] = cell
  return tmp
#end rotate

def balance(cell):
  c_bal = cell.scale
  if c_bal != in_balance:
    heavy_side = c_bal / 2
    help = cell.child[heavy_side]
    h_bal = help.scale
    if h_bal == c_bal:
      cell.scale = in_balance
      help.scale = in_balance
      return rotate(cell, heavy_side)
    elif (h_bal == in_balance):
      help.scale = 2 - c_bal
      return rotate(cell, heavy_side)
    else:
      cell.child[heavy_side] = rotate(help, 1 - heavy_side)
      cell = rotate(cell, heavy_side)
      c_bal = cell.scale
      cell.child[left].scale = (3 - c_bal) / 2
      cell.child[right].scale = (4 - c_bal) / 2
      cell.scale = in_balance
      return cell
    #end if
  #end if
#end balance

class Tree_Iterator:
  def __init__(self, tree, start = None, stop = None, step = None, kind=0):
    if step is None:
      step = 1
    #end if
    self.sentinel = stop
    if not isinstance(step, int):
      raise TypeError, "step must be int: %s" % step
    #end if
    self.this = Cell() 
    self.tree = tree
    self.stamp = tree.stamp
    if step > 0:
      self.step = step
      self.direction = right
    else:
      self.step = - step
      self.direction = left
    #end if
    self.stride = 1
    self.kind = kind
    if start == None:
      self.this.child = 2 * [tree.child[root]]
    else:
      old = tree
      new = tree.child[root]
      diff = -1
      while 1:
        if is_thread(new):
	  if diff < 0:
	    self.this.child = [new, thread_on(old)]
	  else:
	    self.this.child = [thread_on(old), new]
	  #end if
	  return
	#end if
	try:
	  diff = tree.cmp(start, new.key)
	except:
	  raise KeyError, start
	#end try
	old = new
	if diff < 0:
	  new = new.child[left]
	elif diff > 0:
	  new = new.child[right]
	else:
	  self.this.child = 2 * [thread_on(new)]
	  return
	#end if
      #end while
    #end if
  #end init

  def __iter__(self):
    return self
  #end __iter__

  def next(self):
    if self.stamp != self.tree.stamp:
      raise RuntimeError
    #end if
    step = self.stride
    self.stride = self.step
    while 1:
      step -= 1
      self.this = neighbour(self.this, self.direction)
      if self.this is self.tree:
        raise StopIteration
      #end if
      if self.sentinel is not None:
        if self.tree.cmp(self.this.key, self.sentinel) * more[self.direction] >= 0:
          raise StopIteration
	#end if
      #end if
      if step == 0:
        return (self.this.key, self.this.value)[self.kind]
      #end if
    #end while
  #end next
#end Tree_Iterator

def neighbour(here, direction):

  here = here.child[direction]
  if is_thread(here):
    return thread_off(here)
  else:
    other = opposite[direction]
    while not is_thread(here.child[other]):
      here = here.child[other]
    #end while
    return here
  #end if
#end neighbour