#include <stdio.h>

int mbedtls_safer_memcmp( int A[], int B[], int n )
{
    int i;
    unsigned char diff = 0;

    for( i = 0; i < n; i++ )
        diff |= A[i] ^ B[i];

    return( diff );
}

int main() {
    int A[5] = {1, 2, 3, 4, 5};
    int B[5] = {1, 2, 3, 4, 5};
    int ret;
    if (mbedtls_safer_memcmp(A, B, 5) == 0) {
        ret = 0;
    }
    else{
        ret = 1;
    }
    printf("%d\n", ret);
    // printf("%d\n", x);
    // return x;
}