import functools
import random

def identity(x):
    return x

class Treap(object):
    def __init__(self, key=None, cmp=None, parent=None):
        self.elem = None
        self.parent = parent
        self.right = None
        self.left = None
        self.key = key
        if self.key is None:
            self.key = identity

        if cmp is not None:
            self.key = functools.cmp_to_key(cmp)

    def insert(self, elem):
        self._insert(elem, priority=random.random())

    def _insert(self, elem, priority):
        if self.elem is None:
            self.elem = elem
            self.priority = priority
        elif self.key(elem) <= self.key(self.elem):
            if self.left is None:
                self.left = Treap(key=self.key, parent=self)

            self.left._insert(elem,priority)
            #possibly readjust tree to maintain heap order
            if self.left.priority > self.priority:
                self.right_rotate()
        else: #self.key(elem) > self.key(self.elem)
            if self.right is None:
                self.right = Treap(key=self.key, parent=self)

            self.right._insert(elem,priority)
            #possibly readjust tree to maintain heap order
            if self.right.priority > self.priority:
                self.left_rotate()

    def left_rotate(self):
        '''Perform a left rotation, promoting self.right and demoting self
        a                   c
       / \       =>        / \
      b   c               a   e
         / \             / \
        d   e           b   d
        This operation preserves binary search tree order'''
        new_boss = self.right #in the diagram, this is c
        self.right = new_boss.left #set d as a's right child
        if self.right is not None:
            self.right.parent = self

        new_boss.left = self
        new_boss.parent = self.parent
        if self._isRightChild():
            new_boss.parent.right = new_boss
        elif self._isLeftChild():
            new_boss.parent.left = new_boss
        self.parent = new_boss
        self=new_boss

    def right_rotate(self):
        '''Perform a right rotation, promoting self.left and demoting self
          c             a     
         / \           / \    
        a   e    =>   b   c   
       / \               / \  
      b   d             d   e 
        This operation preserves binary search tree order'''
        new_boss = self.left #in the diagram, this is a
        self.left = new_boss.right #set d as c's left child
        if self.left is not None:
            self.left.parent = self

        new_boss.right = self
        new_boss.parent = self.parent
        if self._isRightChild():
            new_boss.parent.right = new_boss
        elif self._isLeftChild():
            new_boss.parent.left = new_boss
        self.parent = new_boss
        self=new_boss

    def _find(self,elem):
        '''given an element, return the sub-Treap that has it at its root, or None'''
        if self.elem is None:
            return None

        if self.key(elem) == self.key(self.elem):
            return self
        elif self.key(elem) < self.key(self.elem):
            return self.left._find(elem)
        elif self.key(elem) > self.key(self.elem):
            return self.right._find(elem)



