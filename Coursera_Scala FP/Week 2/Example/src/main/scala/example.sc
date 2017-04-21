//def sumInts(a: Int, b: Int): Int =
//  if (a > b) 0 else a + sumInts(a + 1, b)

def cube(x: Int): Int = x * x * x

//def sumCubes(a: Int, b: Int): Int =
//  if (a > b) 0 else cube(a) + sumCubes(a + 1, b)

// def sum(f: Int => Int, a: Int, b: Int) = {
//  def loop(a: Int, acc: Int): Int =
//    if (a > b) acc
//    else loop(a + 1, f(a) + acc)
//  loop(a, 0)
//}

//sum(x=> x * x, 3, 5)

def sum(f: Int => Int): (Int, Int) => Int = {
  def sumF(a: Int, b: Int): Int =
    if (a > b) 0
    else f(a) + sumF(a + 1, b)
  sumF
}

def sumInts = sum(x => x)
def sumCubes = sum(x => x * x * x)

sum(cube)(1, 10)

def product(f: Int => Int)(a: Int, b: Int): Int =
  if (a > b) 1
  else f(a) * product(f)(a +1, b)
product(x => x*x)(3, 4)

def fact(n: Int) = product(x => x)(1, n)
fact(5)

def mapReduce(f: Int => Int, combine: (Int, Int) => Int, zero: Int)(a: Int, b: Int): Int =
  if(a > b) zero
  else combine(f(a), mapReduce(f, combine, zero)(a+1, b))

def product2(f: Int => Int)(a: Int, b: Int): Int =
  mapReduce(f, (x, y) => x* y, 1)(a, b)

product2(x => x* x)(3, 4)