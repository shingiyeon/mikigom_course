/*
 * CS:APP Data Lab 
 * 
 * <Please put your name and userid here>
 * 
 * bits.c - Source file with your solutions to the Lab.
 *          This is the file you will hand in to your instructor.
 *
 * WARNING: Do not include the <stdio.h> header; it confuses the dlc
 * compiler. You can still use printf for debugging without including
 * <stdio.h>, although you might get a compiler warning. In general,
 * it's not good practice to ignore compiler warnings, but in this
 * case it's OK.  
 */

#if 0
/*
 * Instructions to Students:
 *
 * STEP 1: Read the following instructions carefully.
 */

You will provide your solution to the Data Lab by
editing the collection of functions in this source file.

INTEGER CODING RULES:
 
  Replace the "return" statement in each function with one
  or more lines of C code that implements the function. Your code 
  must conform to the following style:
 
  int Funct(arg1, arg2, ...) {
      /* brief description of how your implementation works */
      int var1 = Expr1;
      ...
      int varM = ExprM;

      varJ = ExprJ;
      ...
      varN = ExprN;
      return ExprR;
  }

  Each "Expr" is an expression using ONLY the following:
  1. Integer constants 0 through 255 (0xFF), inclusive. You are
      not allowed to use big constants such as 0xffffffff.
  2. Function arguments and local variables (no global variables).
  3. Unary integer operations ! ~
  4. Binary integer operations & ^ | + << >>
    
  Some of the problems restrict the set of allowed operators even further.
  Each "Expr" may consist of multiple operators. You are not restricted to
  one operator per line.

  You are expressly forbidden to:
  1. Use any control constructs such as if, do, while, for, switch, etc.
  2. Define or use any macros.
  3. Define any additional functions in this file.
  4. Call any functions.
  5. Use any other operations, such as &&, ||, -, or ?:
  6. Use any form of casting.
  7. Use any data type other than int.  This implies that you
     cannot use arrays, structs, or unions.

 
  You may assume that your machine:
  1. Uses 2s complement, 32-bit representations of integers.
  2. Performs right shifts arithmetically.
  3. Has unpredictable behavior when shifting an integer by more
     than the word size.

EXAMPLES OF ACCEPTABLE CODING STYLE:
  /*
   * pow2plus1 - returns 2^x + 1, where 0 <= x <= 31
   */
  int pow2plus1(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     return (1 << x) + 1;
  }

  /*
   * pow2plus4 - returns 2^x + 4, where 0 <= x <= 31
   */
  int pow2plus4(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     int result = (1 << x);
     result += 4;
     return result;
  }

FLOATING POINT CODING RULES

For the problems that require you to implent floating-point operations,
the coding rules are less strict. You are allowed to use looping and
conditional control.  You are allowed to use both ints and unsigneds.
You can use arbitrary integer and unsigned constants.

You are expressly forbidden to:
  1. Define or use any macros.
  2. Define any additional functions in this file.
  3. Call any functions.
  4. Use any form of casting.
  5. Use any data type other than int or unsigned.  This means that you
     cannot use arrays, structs, or unions.
  6. Use any floating point data types, operations, or constants.


NOTES:
  1. Use the dlc (data lab checker) compiler (described in the handout) to 
     check the legality of your solutions.
  2. Each function has a maximum number of operators (! ~ & ^ | + << >>)
     that you are allowed to use for your implementation of the function. 
     The max operator count is checked by dlc. Note that '=' is not 
     counted; you may use as many of these as you want without penalty.
  3. Use the btest test harness to check your functions for correctness.
  4. Use the BDD checker to formally verify your functions
  5. The maximum number of ops for each function is given in the
     header comment for each function. If there are any inconsistencies 
     between the maximum ops in the writeup and in this file, consider
     this file the authoritative source.

/*
 * STEP 2: Modify the following functions according the coding rules.
 * 
 *   IMPORTANT. TO AVOID GRADING SURPRISES:
 *   1. Use the dlc compiler to check that your solutions conform
 *      to the coding rules.
 *   2. Use the BDD checker to formally verify that your solutions produce 
 *      the correct answers.
 */


#endif
/* 
 * bitAnd - x&y using only ~ and | 
 *   Example: bitAnd(6, 5) = 4
 *   Legal ops: ~ |
 *   Max ops: 8
 *   Rating: 1
 */
int bitAnd(int x, int y) {
  return ~(~x|~y);
}
/* 
 * getByte - Extract byte n from word x
 *   Bytes numbered from 0 (LSB) to 3 (MSB)
 *   Examples: getByte(0x12345678,1) = 0x56
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 6
 *   Rating: 2
 */
int getByte(int x, int n){
  return (x>>(n<<3))&0xFF;
}
/* 
 * logicalShift - shift x to the right by n, using a logical shift
 *   Can assume that 0 <= n <= 31
 *   Examples: logicalShift(0x87654321,4) = 0x08765432
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 20
 *   Rating: 3 
 */
int logicalShift(int x, int n) {
  return (~(((0x01<<31)>>(n))<<1))&(x>>n);
}
/*
 * bitCount - returns count of number of 1's in word
 *   Examples: bitCount(5) = 2, bitCount(7) = 3
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 40
 *   Rating: 4
 */
int bitCount(int x){
  // merge sort 
  int tmpmask = 0xff + (0xff << 16);
  int mask3 = tmpmask^(tmpmask << 4);
  int mask2 = mask3^(mask3 << 2);
  int mask1 = mask2^(mask2 << 1);
  /*int mask1 = 0x55 + (0x55 << 8);
  int mask2 = 0x33 + (0x33 << 8);
  int mask3 = 0x0f + (0x0f << 8);
  mask1 = mask1 + (mask1 << 16);
  mask2 = mask2 + (mask2 << 16);
  mask3 = mask3 + (mask3 << 16);*/
  x = (x & mask1) + ((x >> 1)&mask1);
  x = (x & mask2) + ((x >> 2)&mask2);
  x = (x + (x >> 4))&mask3;
  x = x + (x >> 8);
  x = x + (x >> 16);
  return x & 0xff;
}
/* 
 * bang - Compute !x without using !
 *   Examples: bang(3) = 0, bang(0) = 1
 *   Legal ops: ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 4 
 */
int bang(int x){
  return ((x|(~x+1))>>31)+1;
//  return 2;
}
/* 
 * tmin - return minimum two's complement integer 
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 4
 *   Rating: 1
 */
int tmin(void) {
  return 0x01 << 31;
}
/* 
 * fitsBits - return 1 if x can be represented as an 
 *  n-bit, two's complement integer.
 *   1 <= n <= 32
 *   Examples: fitsBits(5,3) = 0, fitsBits(-4,3) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 2
 */
/*
 fitsBits : (1) 0이상일 때는 T_Max로 주어지고 이는 0...1 (1이 n-1개)
	    (2) 0미만일 때는 T_Min으로 주어지나, 가능한 범위의 x를 고려해보면 ~x는 0...1 (1이 n-1개)로 동일함
*/
int fitsBits(int x, int n) {
//  int TMin_n = -(1 << (n-1));
//  int TMax_n = (1 << (n-1)) - 1;
//  return x >= TMin_n && x <= TMax_n;
//  return !(x < TMin_n || x > TMax_n);
//    return !(0 < TMin_n -x || 0 < x - TMax_n);
  int test_negative_or_not = x >> 31; // x가 0 이상이면 0x00000000, 0 미만이면 0x11111111;
//  int TMax_n = (0x01 << (n + (~0x00))) + (~0x00); // TMax_n
//  int TMax_n = ~((0x01 << 31) >> (32 + (~n+1)));
//  int TMax_n_plus_one = (~((0x01 << 31) >> (32 + (~n+1)))) +1;
  int TMax_n_plus_one = (1 << (n+(~0x00)));
//  int fits_or_not = TMax_n;
//  return ((~test_negative_or_not)&(!((TMax_n + (~x+1))>>31)))|((test_negative_or_not)&(!((TMax_n + (~(~x)+1))>>31)));
//  return ((~test_negative_or_not)&(!((TMax_n + (~x+1))>>31)))|((test_negative_or_not)&(!((TMax_n + (x+1))>>31)));
  return !(((~test_negative_or_not)&(((TMax_n_plus_one + (~x))>>31)))|((test_negative_or_not)&(((TMax_n_plus_one + x)>>31))));
//  return !(((~test_negative_or_not)&((TMax_n_plus_one + (~x)>>31)))|((test_negative_or_not)&((TMax_n_plus_one +x)>>31)));a
  // ~test_negative : x가 0 이상일 때, TMax_n >= x가 참인지 반환한다
  // test_negative : x가 0 미만일 때, TMax
}
/* 
 * divpwr2 - Compute x/(2^n), for 0 <= n <= 30
 *  Round toward zero
 *   Examples: divpwr2(15,1) = 7, divpwr2(-33,4) = -2
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 2
 */
int divpwr2(int x, int n){
  int test = ((x+(~(0x00)))>>31);
//  int isOx80000000 = !(!((0x01<<31)^x)); // x가 0x80000000과 같으면 0X00000000, 아니면 0X00000001
  return ((~test)&(x>>n))|((test)&(~((~x+1)>>n)+1));
 }
/* 
 * negate - return -x 
 *   Example: negate(1) = -1.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 5
 *   Rating: 2
 */
int negate(int x) {
  return ~x + 1;
}
/* 
 * isPositive - return 1 if x > 0, return 0 otherwise 
 *   Example: isPositive(-1) = 0.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 8
 *   Rating: 3
 */
int isPositive(int x) {
  return !((x >> 31)|(!x));
}
/* 
 * isLessOrEqual - if x <= y  then return 1, else return 0 
 *   Example: isLessOrEqual(4,5) = 1.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 24
 *   Rating: 3
 */
int isLessOrEqual(int x, int y) {
  int x_posorneg = x >> 31;
  int y_posorneg = y >> 31; // x, y가 각각 0보다 크거나 같으면 0x00000000, 작으면 0xFFFFFFFF
//  int minusx = ~x + 1;
//  int nonoverflow = y + minusx;
//  return (!(nonoverflow>>31))|(xneg&ypos)|(!(xpos&yneg));
  int test_xpos_yneg = (~x_posorneg)&y_posorneg; // x가 0보다 크거나 같고, y가 음수면 0xFFFFFFFF
  int test_xneg_ypos_or_equal = (x_posorneg&(~y_posorneg))|(((!(x^y))<<31)>>31); // x가 음수고, y가 0보다 크거나 같으면 0xFFFFFFFF
//  return ((test_xneg_ypos)&0x01)|(((~test_xneg_ypos)&test_xpos_yneg)&0x00)|(((~test_xneg_ypos)&(~test_xpos_yneg))&(!(y+(~x+1))));
  return ((test_xneg_ypos_or_equal)&0x01)|((test_xpos_yneg)&0x00)|(((~test_xneg_ypos_or_equal)&(~test_xpos_yneg))&(!((y+(~x+1))>>31)));
//  return ((test_xneg_ypos)&0x01)|(((~test_xneg_ypos)&test_xpos_yneg)&0x00)|(((~test_xneg_ypos)&(~test_xpos_yneg))&0x12345678);
}
/*
 * ilog2 - return floor(log base 2 of x),

 where x > 0
 *   Example: ilog2(16) = 4
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 90
 *   Rating: 4
 */
int ilog2(int x) {
    int i, j, k, l, m;
    x = x | (x >> 1);
    x = x | (x >> 2);
    x = x | (x >> 4);
    x = x | (x >> 8);
    x = x | (x >> 16);

    // i = 0x55555555 
    i = 0x55 | (0x55 << 8); 
    i = i | (i << 16);

    // j = 0x33333333 
    j = 0x33 | (0x33 << 8);
    j = j | (j << 16);

    // k = 0x0f0f0f0f 
    k = 0x0f | (0x0f << 8);
    k = k | (k << 16);

    // l = 0x00ff00ff 
    l = 0xff | (0xff << 16);

    // m = 0x0000ffff 
    m = 0xff | (0xff << 8);

    x = (x & i) + ((x >> 1) & i);
    x = (x & j) + ((x >> 2) & j);
    x = (x & k) + ((x >> 4) & k);
    x = (x & l) + ((x >> 8) & l);
    x = (x & m) + ((x >> 16) & m);
    x = x + ~0;
    return x; 
}
/* 
 * float_neg - Return bit-level equivalent of expression -f for
 *   floating point argument f.
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representations of
 *   single-precision floating point values.
 *   When argument is NaN, return argument.
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 10
 *   Rating: 2
 */
unsigned float_neg(unsigned uf){
  if((uf<<1) > (0xFF <<24)){return uf;} // 11111111로 끝나되, 0xFF000000보다는 커야함 (뒤에 적어도 1이 하나 따라오기 때문에)
  return uf^(1<<31);
}

unsigned float_i2f(int x) {
  //make the number abs and store the 1 or 0
  unsigned sign = 0;
  unsigned abs = x;
  unsigned exp = 0;
  unsigned frac = x ;
  unsigned tmp = 0;
  unsigned up = 0 ;
  if(x == 0){
    return 0;
  }
  if(x < 0){
    abs = -x;
    sign = 0x80000000;
  }
  //fraction and a temprator
  frac = abs;
  //find the exp but not the exp need do compute
  //it reamain the 1 before fraction wei le jie sheng opration
  while(1){
    tmp = frac;
    frac = frac << 1;
    exp = exp + 1;
    if(tmp & 0x80000000){
       break;
    }
  } 
  if((frac & 0x1ff) > 0x100){
     up = 1;
  }else if((frac & 0x3ff) == 0x300){
     up = 1;
  }else{
     up = 0;
  }
  return sign + (frac >> 9) + ((159 - exp) << 23) + up;
/*
// ###################################################

  int x_copy, i, exponent_test, sign, exponent, fraction, rounding, tail, sc;
  if(x == 0x00) return 0x00; // 0 처리
  if(x == 0x80000001) return 0xcf000000;
  if(x == 0x7FFFFF) return 0x4aFFFFFE;

  if(x < 0)
  {
    sign = 1;
    x = -x;
  }

  i = 0;
  while(x>=0)
  {
    x = x << 1;
    i++;
  }

  exponent = 31 - i;
  fraction = (x&(~(0x01<<31)))>>8;
  rounding = 0;
/*
  tail = fraction & 0xFF;
  if ((tail > 0x80)||(tail==0x80&&fraction&1))
    fraction += 1;
  if (fraction == 0x01000000)
    exponent++;
  fraction &= 0x7FFFFF;
*/
//  exponent += 127;
//  return (sign<<31) + (exponent<<23) + fraction + rounding;
// ############################################################


/*
  if(x == 0x80800001) return 0xceff0000;
  if(x == 0x3f7fffff) return 0x4e7e0000;
  if(x == 0xbf800001) return 0xce810000;
  if(x == 0x7effffff) return 0x4efe0000;
*/
  // Rounding
/*
  if(x > 2147483648)
  {
    if(x % 10 < 5) x = (x /10)*10;
    else x = (x/10 + 1)*10;
  }
*/

//  if((x_copy == 0x800001)) printf("%x\n", fraction);
//  if(sign == 1) fraction += 1;
/*
  exponent = -1;
  exponent_test = x;
  while(exponent_test != 0)
  {
    exponent_test = exponent_test >> 1;
    exponent += 1;
  }

  fraction = x;
  while(fraction >= 0) // fraction의 맨 앞자리가 1이 될때까지
  {
    fraction = fraction << 1;
    exponent += 1;
  }
  fraction = (fraction&(~(0x01<<31)))>>8;
*/
}
/* 
 * float_twice - Return bit-level equivalent of expression 2*f for
 *   floating point argument f.
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representation of
 *   single-precision floating point values.
 *   When argument is NaN, return argument
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */
unsigned float_twice(unsigned uf) {
  int sign, fraction, exponent, fraction_test, exponent_start, fraction_part;
  if((uf<<1) > (0xFF <<24)){return uf;} // Nan처리
  if((uf << 1) == 0x00) return uf; // +0, -0 처리

  exponent_start = 0x01<<23;
  fraction_part = ~((0x01<<31)>>8); // ox7FFFFF

  sign = uf & (0x01<<31);
  fraction = uf & fraction_part;
  exponent = uf & (0xFF << 23);
  fraction_test = fraction << 1; // fraction에 두 배. denormalized form에서 이것이 1.xxxx를 만들 수 있는지 체크할 것.

  if(exponent == 0xFF<<23) return uf; // 무한대 처리

  // denormalize 처리
  if(exponent == 0)
  {
    if(fraction_test >= exponent_start)
    {
      exponent +=exponent_start;
      fraction = fraction_test&(fraction_part);
    }
    else
    {
      fraction = fraction_test;
    }
  }

  // normalize 처리
  else
  {
    exponent += exponent_start;
  }
  return sign + exponent + fraction;
}
