#include <stdio.h>
#include <fftw3.h>
#include <time.h>

typedef struct sample {
    double time;
    double accelx;
    double accely;
    double accelz;
    double temp;
    double gyrox;
    double gyroy;
    double gyroz;
}sample;

void printSample(sample* s)
{
    printf("time: %f\n", s->time);
    printf("accelx: %f\n", s->accelx);
    printf("accely: %f\n", s->accely);
    printf("accelz: %f\n", s->accelz);
    printf("temp: %f\n", s->temp);
    printf("gyrox: %f\n", s->gyrox);
    printf("gyroy: %f\n", s->gyroy);
    printf("gyroz: %f\n", s->gyroz);
}

int readSample(FILE* f, sample* smp)
{
    if (fscanf(f,
               "%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf\n",
               &smp->time,
               &smp->accelx,
               &smp->accely,
               &smp->accelz,
               &smp->temp,
               &smp->gyrox,
               &smp->gyroy,
               &smp->gyroz) == 8) {
        return 0;
    } else {
        return -1;
    }
}

void compact_on_accelx(sample* s, fftwf_complex* buff, size_t n)
{
    int i;
    for (i = 0; i < n; i++) {
        buff[i][0] = s[i].accelx;
        buff[i][1] = 0;
    }
}

void test_1_sec() {
    int n = 1000;
    int i = 0;
    sample s[n];
    fftwf_complex *in, *out;
    fftwf_plan p;
    struct timespec t0, t1;

    in = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex)*n);
    out = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex)*n);
    FILE* f = fopen("beagle_data_ubuntu.csv", "r");
    if (f == NULL) {
        printf("file open failed\n");
    }
    while (0 == readSample(f, s + i++)) 
        ;
    compact_on_accelx(s, in, n);
    p = fftwf_plan_dft_1d(n, in, out, FFTW_FORWARD, FFTW_ESTIMATE);
    clock_gettime(CLOCK_REALTIME, &t0);
    fftwf_execute(p);
    clock_gettime(CLOCK_REALTIME, &t1);
    printf("time 1,000 samples (ns): %ld\n", t1.tv_nsec - t0.tv_nsec);
    fftwf_destroy_plan(p);
    fftwf_free(in);
    fftwf_free(out);
    close(f);
}

void test_10_sec()
{
    int n = 10000;
    int i = 0;
    sample s[n];
    fftwf_complex *in, *out;
    fftwf_plan p;
    struct timespec t0, t1;

    in = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex)*n);
    out = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex)*n);
    FILE* f = fopen("beagle_data_ubuntu.csv", "r");
    if (f == NULL) {
        printf("file open failed\n");
    }
    while (0 == readSample(f, s + i++)) 
        ;
    for (i = 0; i < 10; i++) {
        compact_on_accelx(s, in+1000*i, 1000);
    }
    p = fftwf_plan_dft_1d(n, in, out, FFTW_FORWARD, FFTW_ESTIMATE);
    clock_gettime(CLOCK_REALTIME, &t0);
    fftwf_execute(p);
    clock_gettime(CLOCK_REALTIME, &t1);
    printf("time 10,000 samples (ns): %ld\n", t1.tv_nsec - t0.tv_nsec);
    fftwf_destroy_plan(p);
    fftwf_free(in);
    fftwf_free(out);
    close(f);
}

void test_100_sec()
{
    int n = 100000;
    int i = 0;
    sample s[n];
    fftwf_complex *in, *out;
    fftwf_plan p;
    struct timespec t0, t1;

    in = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex)*n);
    out = (fftwf_complex*) fftwf_malloc(sizeof(fftwf_complex)*n);
    FILE* f = fopen("beagle_data_ubuntu.csv", "r");
    if (f == NULL) {
        printf("file open failed\n");
    }
    while (0 == readSample(f, s + i++)) 
        ;
    for (i = 0; i < 100; i++) {
        compact_on_accelx(s, in+1000*i, 1000);
    }
    p = fftwf_plan_dft_1d(n, in, out, FFTW_FORWARD, FFTW_ESTIMATE);
    clock_gettime(CLOCK_REALTIME, &t0);
    fftwf_execute(p);
    clock_gettime(CLOCK_REALTIME, &t1);
    printf("time 100,000 samples (ns): %ld\n", t1.tv_nsec - t0.tv_nsec);
    fftwf_destroy_plan(p);
    fftwf_free(in);
    fftwf_free(out);
    close(f);
}

int main(int argc, char* argv[]) 
{
    test_1_sec();
    test_10_sec();
    test_100_sec();
}
