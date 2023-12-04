// Standard libraries
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>

// User defined header files
// #include "UIS_1.h"
// #include "UIS_2.h"
// #include "UIS_3.h"
// #include "UIS_4.h"
// #include "UIS_5.h"
#include "UIS_6.h"
// #include "UIS_11.h"
// #include "UIS_12.h"
// #include "UIS_13.h"
// #include "UIS_14.h"
// #include "UIS_15.h"
// #include "UIS_16.h"
// #include "UIS_18.h"
// #include "UIS_19.h"
// #include "UIS_20.h"
// #include "UIS_21.h"
// #include "UIS_22.h"
// #include "UIS_25.h"
// #include "UIS_27.h"
// #include "UIS_28.h"
// #include "UIS_29.h"
// #include "UIS_30.h"
// #include "UIS_34.h"
// #include "UIS_35.h"
// #include "UIS_36.h"
// #include "UIS_37.h"
// #include "UIS_38.h"
// #include "UIS_39.h"
// #include "UIS_40.h"
// #include "UIS_41.h"
// #include "UIS_42.h"
// #include "UIS_43.h"
// #include "UIS_44.h"
// #include "UIS_45.h"
// #include "UIS_46.h"
// #include "UIS_47.h"
// #include "UIS_48.h"
// #include "UIS_49.h"
// #include "UIS_50.h"

#include "functions.h"
#include "constants.h"


int sm_K_vec_arr[N_KVEC_PAIRS][3];

// gcc -o exe main.c -lm
// ./exe DELTA TOL P1 P2 EPSILON_SEQ_ERROR > out_txt

int main(int argc, char *argv[])
{
  clock_t start, end;
  start = clock();

  double DELTA = atof(argv[1]);
  double TOL = atof(argv[2]) ;
  double P1 = atof(argv[3]);
  double P2 = atof(argv[4]);
  double EPSILON_SEQ_ERROR = atof(argv[5]);

  // printf("DELTA = %f \n", DELTA);
  // printf("TOL = %f \n", TOL);
  // printf("P1 = %f \n", P1);
  // printf("P2 = %f \n", P2);
  // printf("EPSILON_SEQ_ERROR = %f \n", EPSILON_SEQ_ERROR);
  // DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR

  // HILS(arr_out_UIS_1, N_i_1, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_2, N_i_2, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_3, N_i_3, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_4, N_i_4, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_5, N_i_5, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);

    HILS(arr_out_UIS_6, N_i_6, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_11, N_i_11, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_12, N_i_12, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_13, N_i_13, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_14, N_i_14, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_15, N_i_15, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_16, N_i_16, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_18, N_i_18, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_19, N_i_19, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_20, N_i_20, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_21, N_i_21, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_22, N_i_22, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_25, N_i_25, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_27, N_i_27, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_28, N_i_28, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_29, N_i_29, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_30, N_i_30, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_34, N_i_34, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_36, N_i_36, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_37, N_i_37, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_39, N_i_39, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_40, N_i_40, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_41, N_i_41, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_42, N_i_42, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_43, N_i_43, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_44, N_i_44, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_45, N_i_45, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_46, N_i_46, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_47, N_i_47, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_48, N_i_48, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_49, N_i_49, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);


  // HILS(arr_out_UIS_50, N_i_50, DELTA, TOL, P1, P2, EPSILON_SEQ_ERROR);

    
  end = clock();
  double duration = ((double)end - start)/CLOCKS_PER_SEC;
  // printf("Time taken to execute in seconds : %f\n", duration);
}