// Name : Junghoon Seo
// ID : s20145071

/* 
 * trans.c - Matrix transpose B = A^T
 *
 * Each transpose function must have a prototype of the form:
 * void trans(int M, int N, int A[N][M], int B[M][N]);
 *
 * A transpose function is evaluated by counting the number of misses
 * on a 1KB direct mapped cache with a block size of 32 bytes.
 */ 
#include <stdio.h>
#include "cachelab.h"

int is_transpose(int M, int N, int A[N][M], int B[M][N]);

/* 
 * transpose_submit - This is the solution transpose function that you
 *     will be graded on for Part B of the assignment. Do not change
 *     the description string "Transpose submission", as the driver
 *     searches for that string to identify the transpose function to
 *     be graded. 
 */
char transpose_submit_desc[] = "Transpose submission";
void transpose_submit(int M, int N, int A[N][M], int B[M][N])
{

    int i, j, n, m, temp, diag;
    int r0, r1, r2, r3, r4, r5, r6, r7;

    if(M==32)
	{
        for (i = 0; i < N-8; i += 8)
            for (j = i + 8; j < M; j += 8)
       		    for (n = 0; n < 8; ++n)
            	    for (m = 0; m < 8; ++m)
              		 	B[j+m][i+n] = A[i+n][j+m];

       for (i = 8; i < N; i += 8)
            for (j = 0; j < i; j += 8)
                for (n = 0; n < 8; ++n)
                    for (m = 0; m < 8; ++m)
                        B[j+m][i+n] = A[i+n][j+m];

       for (i = 0; i < N; i += 8)
        {
           for (n = 0; n < 8; ++n) 
            {
                r0 = A[i + n][i + 0];
                r1 = A[i + n][i + 1];
                r2 = A[i + n][i + 2];
                r3 = A[i + n][i + 3];
                r4 = A[i + n][i + 4];
                r5 = A[i + n][i + 5];
                r6 = A[i + n][i + 6];
                r7 = A[i + n][i + 7];

                B[i + n][i + 0] = r0;
                B[i + n][i + 1] = r1;
                B[i + n][i + 2] = r2;
                B[i + n][i + 3] = r3;
                B[i + n][i + 4] = r4;
                B[i + n][i + 5] = r5;
                B[i + n][i + 6] = r6;
                B[i + n][i + 7] = r7;
            }

            for (n = 0; n < 4; ++n) 
            {
                for (m = n; m < 4; ++m) 
                {
                    r1 = B[i + n][i + m];
                    B[i + n][i + m] = B[i + m][i + n];
                    B[i + m][i + n] = r1;

                    r1 = B[i + n + 4][i + m + 4];
                    B[i + n + 4][i + m + 4] = B[i + m + 4][i + n + 4];
                    B[i + m + 4][i + n + 4] = r1;

                    r1 = B[i + n][i + m + 4];
                    B[i + n][i + m + 4] = B[i + m][i + n + 4];
                    B[i + m][i + n + 4] = r1;

                    r1 = B[i + n + 4][i + m];
                    B[i + n + 4][i + m] = B[i + m + 4][i + n];
                    B[i + m + 4][i + n] = r1;
                }
            }

            for (n = 0; n < 4; ++n) 
            {
                for (m = 0; m < 4; ++m) 
                {
                    r1 = B[i + n][i + m + 4];
                    B[i + n][i + m + 4] = B[i + n + 4][i + m];
                    B[i + n + 4][i + m] = r1;
                }
            }
        }
    }


    if(M==64)
    {
        for (i = 0; i < 56; i += 8) 
        {
            for (n = 0; n < 4; ++n) 
            {
                r0 = A[i + n][i + 0];
                r1 = A[i + n][i + 1];
                r2 = A[i + n][i + 2];
                r3 = A[i + n][i + 3];
                r4 = A[i + n][i + 4];
                r5 = A[i + n][i + 5];
                r6 = A[i + n][i + 6];
                r7 = A[i + n][i + 7];

                B[i + n][i + 0] = r0;
                B[i + n][i + 1] = r1;
                B[i + n][i + 2] = r2;
                B[i + n][i + 3] = r3;
                B[i + n][i + 4] = r4;
                B[i + n][i + 5] = r5;
                B[i + n][i + 6] = r6;
                B[i + n][i + 7] = r7;

                B[n][56] = r4;
                B[n][57] = r5;
                B[n][58] = r6;
                B[n][59] = r7;
            }

        for (n = 0; n < 4; ++n) 
        {
            for (m = n; m < 4; ++m) 
            {
                r1 = B[i + n][i + m];
                B[i + n][i + m] = B[i + m][i + n];
                B[i + m][i + n] = r1;
            }
        }

        for (n = 4; n < 8; ++n) 
        {

            r0 = A[i + n][i + 0];
            r1 = A[i + n][i + 1];
            r2 = A[i + n][i + 2];
            r3 = A[i + n][i + 3];
            r4 = A[i + n][i + 4];
            r5 = A[i + n][i + 5];
            r6 = A[i + n][i + 6];
            r7 = A[i + n][i + 7];

            B[i + n][i + 0] = r0;
            B[i + n][i + 1] = r1;
            B[i + n][i + 2] = r2;
            B[i + n][i + 3] = r3;
            B[i + n][i + 4] = r4;
            B[i + n][i + 5] = r5;
            B[i + n][i + 6] = r6;
            B[i + n][i + 7] = r7;

            B[n - 4][60] = r0;
            B[n - 4][61] = r1;
            B[n - 4][62] = r2;
            B[n - 4][63] = r3;
        }

        for (n = 4; n < 8; ++n) 
        {
            for (m = n; m < 8; ++m) 
            {
                r1 = B[i + n][i + m];
                B[i + n][i + m] = B[i + m][i + n];
                B[i + m][i + n] = r1;
            }
        }

        for (n = 0; n < 4; ++n) 
        {
            for (m = n; m < 4; ++m) 
            {
                r1 = B[n][m + 56];
                B[n][m + 56] = B[m][n + 56];
                B[m][n + 56] = r1;

                r1 = B[n][m + 60];
                B[n][m + 60] = B[m][n + 60];
                B[m][n + 60] = r1;
            }
        }

        for (n = 0; n < 4; ++n) 
            for (m = 0; m < 4; ++m) 
                B[i + n + 4][i + m] = B[n][56 + m];

        for (n = 0; n < 4; ++n)
            for (m = 0; m < 4; ++m)
                B[i + n][i + m + 4] = B[n][60 + m];
    }

    for (n = 0; n < 4; ++n) 
    {
         r0 = A[56 + n][56 + 0];
         r1 = A[56 + n][56 + 1];
         r2 = A[56 + n][56 + 2];
         r3 = A[56 + n][56 + 3];
         r4 = A[56 + n][56 + 4];
         r5 = A[56 + n][56 + 5];
         r6 = A[56 + n][56 + 6];
         r7 = A[56 + n][56 + 7];

         B[56 + n][56 + 0] = r0;   
         B[56 + n][56 + 1] = r1;   
         B[56 + n][56 + 2] = r2;
         B[56 + n][56 + 3] = r3;
         B[56 + n][56 + 4] = r4;
         B[56 + n][56 + 5] = r5;
         B[56 + n][56 + 6] = r6;
         B[56 + n][56 + 7] = r7;
    }

    for (n = 0; n < 4; ++n) 
    {
        for (m = n; m < 4; ++m)     
        {
            r1 = B[n + 56][m + 56];
            B[n + 56][m + 56] = B[m + 56][n + 56];
            B[m + 56][n + 56] = r1;

            r1 = B[n + 56][m + 60];
            B[n + 56][m + 60] = B[m + 56][n + 60];
            B[m + 56][n + 60] = r1;
        }
    }

    for (n = 4; n < 8; ++n) 
    {
        r0 = A[56 + n][56 + 0];
        r1 = A[56 + n][56 + 1];
        r2 = A[56 + n][56 + 2];
        r3 = A[56 + n][56 + 3];
        r4 = A[56 + n][56 + 4];
        r5 = A[56 + n][56 + 5];
        r6 = A[56 + n][56 + 6];
        r7 = A[56 + n][56 + 7];

        B[56 + n][56 + 0] = r0;
        B[56 + n][56 + 1] = r1;
        B[56 + n][56 + 2] = r2;
        B[56 + n][56 + 3] = r3;
        B[56 + n][56 + 4] = r4;
        B[56 + n][56 + 5] = r5;
        B[56 + n][56 + 6] = r6;
        B[56 + n][56 + 7] = r7;
    }

    for (n = 0; n < 4; ++n) 
    {
        for (m = n; m < 4; ++m) 
        {
            r1 = B[n + 60][m + 60];
            B[n + 60][m + 60] = B[m + 60][n + 60];
            B[m + 60][n + 60] = r1;

            r1 = B[n + 60][m + 56];
            B[n + 60][m + 56] = B[m + 60][n + 56];
            B[m + 60][n + 56] = r1;
        }
    }

    for (n = 0; n < 4; ++n) 
    {
        r0 = B[56 + n][60 + 0];
        r1 = B[56 + n][60 + 1];
        r2 = B[56 + n][60 + 2];
        r3 = B[56 + n][60 + 3];

        r4 = B[60 + n][56 + 0];
        r5 = B[60 + n][56 + 1];
        r6 = B[60 + n][56 + 2];
        r7 = B[60 + n][56 + 3];

        B[60 + n][56 + 0] = r0;
        B[60 + n][56 + 1] = r1;
        B[60 + n][56 + 2] = r2;
        B[60 + n][56 + 3] = r3;

        B[56 + n][60 + 0] = r4;
        B[56 + n][60 + 1] = r5;
        B[56 + n][60 + 2] = r6;
        B[56 + n][60 + 3] = r7;
    }


    for (i = 0; i < 64 - 8; i += 8) 
    {
        for (j = i + 8; j < 64; j += 8) 
        {
           for (n = 0; n < 8; ++n) 
            {
                for (m = 0; m < 4; ++m) 
                {
                    B[j+m][i+n] = A[i+n][j+m];
                }
            }
           for (n = 7; n >= 0; --n) 
            {
                for (m = 4; m < 8; ++m) 
                {
                    B[j+m][i+n] = A[i+n][j+m];
                }
            }
        }
    }

    for (i = 8; i < 64; i += 8) 
    {
        for (j = 0; j < i; j += 8) 
        {

            for (n = 0; n < 8; ++n) 
            {
                for (m = 0; m < 4; ++m) 
                {
                    B[j+m][i+n] = A[i+n][j+m];
                }
            }

            for (n = 7; n >= 0; --n) 
            {
                for (m = 4; m < 8; ++m) 
                {
                    B[j+m][i+n] = A[i+n][j+m];
                }
            }
        }
     }
  }

  else if((M == 61) && (N == 67))
  {
    for(j=0; j<M; j+=8)
    {
      for(i=0; i<N; i+=8)
      {
        for(n=i; (n<i+8)&&(n<67); n++)
        {
          for(m=j; (m<j+8)&&(m<61); m++)
          {
            if(n != m)
              B[m][n] = A[n][m];
            else
            {
              temp = A[n][m];
              diag = n;
            }
            if(i==j)
              B[diag][diag] = temp;
          } 
        }
      }
    }
  }
}
/* 
 * You can define additional transpose functions below. We've defined
 * a simple one below to help you get started. 
 */ 

/* 
 * trans - A simple baseline transpose function, not optimized for the cache.
 */
char trans_desc[] = "Simple row-wise scan transpose";
void trans(int M, int N, int A[N][M], int B[M][N])
{
    int i, j, tmp;

    for (i = 0; i < N; i++) {
        for (j = 0; j < M; j++) {
            tmp = A[i][j];
            B[j][i] = tmp;
        }
    }    

}

/*
 * registerFunctions - This function registers your transpose
 *     functions with the driver.  At runtime, the driver will
 *     evaluate each of the registered functions and summarize their
 *     performance. This is a handy way to experiment with different
 *     transpose strategies.
 */
void registerFunctions()
{
    /* Register your solution function */
    registerTransFunction(transpose_submit, transpose_submit_desc); 

    /* Register any additional transpose functions */
    registerTransFunction(trans, trans_desc); 

}

/* 
 * is_transpose - This helper function checks if B is the transpose of
 *     A. You can check the correctness of your transpose by calling
 *     it before returning from the transpose function.
 */
int is_transpose(int M, int N, int A[N][M], int B[M][N])
{
    int i, j;

    for (i = 0; i < N; i++) {
        for (j = 0; j < M; ++j) {
            if (A[i][j] != B[j][i]) {
                return 0;
            }
        }
    }
    return 1;
}

