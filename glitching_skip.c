#include <stdio.h>

int mbedtls_mpi_cmp_mpi( int X, int Y )
{
    if(X == Y) {
        return 0;
    }
    else{
        return 1;
    }
}

int main() {
    int X = 12;
    int Y = 15;
    int ret;
    if( mbedtls_mpi_cmp_mpi( X, Y ) != 0 )
    {
        ret = 1;
    }
    else {
        ret = 0;
    }
    printf("%d\n", ret);
}

