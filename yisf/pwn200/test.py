from z3 import *

a1 = Bitvec('a1',8)
s = Solver()
s.add(LShR(RShR(a1,16),16)|a1|LShR(RShR(a1,24),24) = 99)

print s.check()
