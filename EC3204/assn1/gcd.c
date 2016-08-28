/* Compute the greast common divisor of 815 and 625*/
void main() {
    int a = 815, b = 625;
    printf("a = %4d b = %4d\n", a, b);
    while (a != b) {
        if (a > b) a = a - b;
        else b = b - a;
        printf("a = %4d b = %4d\n", a, b);
    }
}
