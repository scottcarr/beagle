#include <time.h>
#include "mpu6050-utils.h"

#define N_SAMPLES           (1000)
#define SAMPLE_SIZE         (28) // 14 channels * 2 bytes per channel
#define BITS_PER_G          (16384.0)
#define BITS_PER_DEG_PER_S  (131.0)

void print_samples(char *samples_buff, struct timespec ts[])
{
    int i,j,k;

    for (i = 0; i < N_SAMPLES; i++)
    {
        printf("%i.%09i", ts[i].tv_sec, ts[i].tv_nsec); 
        j = i*SAMPLE_SIZE;
        for (k = 0; k < SAMPLE_SIZE / 2; k += 2){ 
            short smp = (samples_buff[j+k] << 8) | samples_buff[j+k+1];
            float fsmp = (float)smp;
            if (k < 7) {
                fsmp /= BITS_PER_G;
            } else {
                fsmp /= BITS_PER_DEG_PER_S;
            }
            printf(",%f", fsmp);
        }
        printf("\n");
    }
}

int main()
{
    char samples_buff[N_SAMPLES * SAMPLE_SIZE];
    char *smp_buff_ptr = samples_buff;
    struct timespec ts[N_SAMPLES];
    int i;
    open_mpu6050();
    wake_up();
    set_sample_div();
    for (i = 0; i < N_SAMPLES; i++) {
        clock_gettime(CLOCK_REALTIME, ts+i);
        read_sample(smp_buff_ptr);
        smp_buff_ptr += SAMPLE_SIZE;
    }
    print_samples(samples_buff, ts);
    return 0;
}
