package recfun

object Main {
  def main(args: Array[String]) {
    println("Pascal's Triangle")
    for (row <- 0 to 10) {
      for (col <- 0 to row)
        print(pascal(col, row) + " ")
      println()
    }

    println("Parentheses Balancing")
    println(balance("(if (zero? x) max (/ 1 x))".toList))

    println("Counting Change")
    println(countChange(4,List(1,2)))
  }

  /**
   * Exercise 1
   */
    def pascal(c: Int, r: Int): Int = (
      if(c == 0 || r == c) 1 else pascal(c, r - 1) + pascal(c - 1, r - 1)
    )
  
  /**
   * Exercise 2
   */
    def balance(chars: List[Char]): Boolean = {
      def queuing(C: List[Char], Q: List[Char]): (List[Char], List[Char]) = {
        if(C.isEmpty)
          return (C, Q)

        var new_Q = Q :+ C.head
        val new_C = C.tail

        val last_two = new_Q.takeRight(2)
        val first = last_two.head
        val second = last_two.last
        if(first == '(' && second == ')') new_Q = new_Q.dropRight(2)

        return queuing(new_C, new_Q)
      }

      val char = chars.filter((i: Char) => i == '(' || i == ')')
      var queue = List[Char]()

      queue = queuing(char, queue)._2
      return queue.isEmpty
    }
  
  /**
   * Exercise 3
   */
    def countChange(money: Int, coins: List[Int]): Int = {
      val sorted_coins = coins.sorted

      def recursive(O: Int, T: Int): Int = {
        if (T < 0)
          return 0
        if (T == 0)
          return 1

        var sum = 0
        for(n <- 0 to O)
          sum += recursive(n, T - sorted_coins(n))

        return sum
      }

      return recursive(coins.length - 1, money)
    }
  }
