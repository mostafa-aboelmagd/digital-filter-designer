/* Filter Realisation: Direct Form II */
#include <stdio.h>

#define NUM_B 7
#define NUM_A 7
static const double b[NUM_B] = { 1.00000000, -0.00000000, -3.00000000, 0.00000000, 3.00000000, -0.00000000, -1.00000000 };
static const double a[NUM_A] = { 1.00000000, -5.62356098, 13.18538363, -16.50032958, 11.62429681, -4.37133452, 0.68554463 };

/* Delay elements: NUM_A-1 */
#define N_DELAY (NUM_A - 1)
static double w[N_DELAY] = {0};

double filter_sample(double x) {
    double y = b[0] * x + (N_DELAY > 0 ? w[0] : 0.0);
    for (int i = 0; i < N_DELAY - 1; i++) {
        w[i] = b[i+1] * x - a[i+1] * y + w[i+1];
    }
    if (N_DELAY > 0)
        w[N_DELAY-1] = b[NUM_B-1] * x - a[NUM_A-1] * y;
    return y;
}

void reset_filter() {
    for (int i = 0; i < N_DELAY; i++) {
        w[i] = 0.0;
    }
}

int main() {
    double input = 1.0;
    double output = filter_sample(input);
    printf("Output: %f\n", output);
    return 0;
}
