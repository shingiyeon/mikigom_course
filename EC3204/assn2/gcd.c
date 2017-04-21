/* Compute the greast common divisor of 815 and 625*/
int main() {
    int g1;
    int g2;

    g1 = gcd(81, 625);
    g2 = rgcd(815, 625);
    
    return g1 == g2;
}

int gcd(int a, int b) {
    while (a != b) {
        if (a > b) 
            a = a - b;
        else
            b = b - a;
    }
    return a;
}

int rgcd(int a, int b) {
    if ( a == b ) {
        return a;
    } else if ( a > b ) {
        return rgcd(a - b, b);
    } else {
        return rgcd(a, b - a);
    }
}
