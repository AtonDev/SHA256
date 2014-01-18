#include <stdio.h>
#include <sys/timeb.h>
//data syze in bytes
#define DATA_SIZE 1000000

typedef unsigned short byte;

typedef struct bigint
{
	unsigned int val[4];
} int256_t;

//implicit declarations
int256_t sha256(byte input[], int size);


int main(int argc, char const *argv[])
{
	//data formation
	byte data[DATA_SIZE];


	//time elapsed
	struct timeb start, end;
    int diff;
    double bandwidth;
    int i = 0;
    ftime(&start);

    sha256(data, DATA_SIZE);

    ftime(&end);
    diff = (int) (1000.0 * (end.time - start.time)
        + (end.millitm - start.millitm));
	bandwidth = (double) DATA_SIZE / diff * 1000
    printf("\nSHA took %u milliseconds ", diff);
    printf("for data of size %d MByte\n", DATA_SIZE / 1000000);
    printf("At %.2f Mbyte/s\n", bandwidth);
	return 0;
}

int256_t sha256(byte input[], int size)
{
	struct bigint result;
	
	return result;
}