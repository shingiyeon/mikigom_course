abstract class IntSet{
  def incl(x: Int): IntSet
  def contains(x: Int): Boolean
  def union(other: IntSet): IntSet
}

class Empty extends IntSet {
  def contains(x: Int): Boolean = false
  def incl(x: Int): IntSet = new NonEmpty(x, new Empty, new Empty)
  override def toString = "."
  def union(other: IntSet): IntSet = other
}

class NonEmpty(elem: Int, left:IntSet, right: IntSet) extends IntSet {
  def contains(x: Int): Boolean =
    if (x < elem) left contains x
    else if (x > elem) right contains x
    else true
  def incl(x: Int): IntSet =
    if (x < elem) new NonEmpty(elem, left incl x, right)
    else if (x > elem) new NonEmpty(elem, left, right incl x)
    else this
  override def toString = "{" + left + elem + right + "}"
  def union(other: IntSet): IntSet =
    ((left union right) union other) incl elem
}

val t1 = new NonEmpty(3, new Empty, new Empty)
val t2 = t1 incl 4

new Empty incl 2
(new NonEmpty(7, new Empty, new Empty)) contains 3

(new NonEmpty(7, new Empty, new Empty)) union (new NonEmpty(5, new Empty, new Empty))

////////////////////////////

abstract class Base {
  def foo = 1
  def bar: Int
}

class Sub extends Base {
  override def foo = 2
  def bar = 3
}

////////////////////////

trait List[T] {
  def isEmpty: Boolean
  def head: T
  def tail: List[T]
}

class Cons[T](val head: T, val tail: List[T]) extends List[T] {
  def isEmpty = false
}

class Nil[T] extends List[T] {
  def isEmpty = true
  def head: Nothing = throw new NoSuchElementException("Nil.head")
  def tail: Nothing = throw new NoSuchElementException("Nil.tail")
}

def singleton[T](elem: T) = new Cons[T](elem, new Nil[T])

singleton[Int](1)
singleton(1)

object nth {
  def nth[T](n: Int, xs: List[T]): T =
    if (n == 0) xs.head
    else nth(n - 1, xs.tail)

  val list = new Cons(1, new Cons(2, new Cons(3, new Nil)))

  nth(2, list)
  nth(3, list)
}