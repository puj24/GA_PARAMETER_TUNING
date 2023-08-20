//Standard libraries
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<string.h>

#include "image_1.h"

int main()
{
    double p_mean = 0;
    double p_sd = 0;
    double TH = 0;

    for(int i = 0; i < BREADTH; i++)
    {
        for(int j = 0; j < LENGTH; j++)
        {
            p_mean += arr_out_img_1[i][j];
            p_sd += arr_out_img_1[i][j]*arr_out_img_1[i][j];
        }
    }
    printf("Mean value is %f\n", p_mean);

    p_mean = p_mean/(LENGTH*BREADTH);
    p_sd = sqrt(p_sd/(LENGTH*BREADTH) - p_mean*p_mean);

    TH = p_mean + 5*p_sd;

    printf("Mean value is %f\n", p_mean);
    printf("Standard Deviation is %f\n", p_sd);
    printf("Threshold value is %f\n", TH);
}