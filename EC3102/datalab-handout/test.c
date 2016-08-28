#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int logicalShift(int x, int n) {
  int a = n + (~0x01+1);
  printf("%x\n", a);
  printf("%x\n", 0x01<<31);
  a = ~(((0x01<<31))>>a);
  printf("%x\n", a);
  a = a & (x>>n);
  printf("%x\n", a);
 
  return (~((0x01<<31)>>(n+(~0x01+1))))&(x>>n);
}

unsigned float_neg(unsigned uf){
  return uf^(1<<31);
}

int isLessOrEqual(int x, int y) {
  
  int xneg = !(!(x >> 31));
  int ypos = !(y >> 31);
  int xpos = !(x >> 31);
  int yneg = !(!(x >> 31));
  int minusx = ~x + 1;
  int nonoverflow = y + minusx;
  return (!(nonoverflow>>31))|(xneg&ypos)|(!(xpos&yneg));
}

int main() {
//	printf("%x\n", ~0x01+1);
//	printf("%x\n", logicalShift(INT_MIN,0));
//	printf("%f\n", (float) 0x12345678);
//	printf("%x\n", (float) float_neg(0x12345678));
	printf("0 %d\n", isLessOrEqual(5, -4));
	printf("1 %d\n", isLessOrEqual(3, 10));	
	printf("0 %d\n", isLessOrEqual(-7, -3));
	printf("1 %d\n", isLessOrEqual(-4, 13));
	return 0;
}
