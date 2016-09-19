x = function(x, z)
  local mod = function(f, n, m, z) f(f, n, m, z) end 
  mod(function(f, n, m, z) if m <= z then io.write(n .. "x" .. m .. "=" .. n * m .. "\t") f(f, n, m + 1, z) else print() end end, x, 1, z)
 end
f = function(n) return function(f, x, y, z) f(f, n, x, y, z) end end
test2 = f(x)
test2(function(f, n, x, y, z) if x <= y then n(x, z) f(f, n, x + 1, y, z) end end, 2, 10, 16)
