#include <stdio.h>
#include <sys/timeb.h>
//data syze in bytes
#define DATA_SIZE 1000000

typedef unsigned short byte;
typedef unsigned int uint;
typedef unsigned long long uint64_t;

typedef struct bigint
{
	uint val[4];
} int256_t;

//implicit declarations
int256_t sha256(byte input[], uint64_t size);


int main(int argc, char const *argv[])
{
	//data formation
	uint data_size = DATA_SIZE + (-DATA_SIZE % 64);
	byte data[data_size];

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
	bandwidth = (double) DATA_SIZE / diff * 1000;
    printf("\nSHA took %u milliseconds ", diff);
    printf("for data of size %d MByte\n", DATA_SIZE / 1000000);
    printf("At %.2f Mbyte/s\n", bandwidth);
	return 0;
}

int256_t sha256(byte data[], uint64_t size)
{
	int256_t result;
	
	/* Padding:
	 * append a 1, k*8 + 7 0s, and size in bits of  data on the right. */
	uint l = (size << 3) % 512;
	uint k = ((448 - 8 - l) % 512) >> 8;
	data[size] = (1 << 7);
	for (int i = size + 1; i <= size + k; ++i)
	{
		data[i] = 0;
	}
	for (int i = 0; i < 8; ++i)
	{
		data[size + k + 1 + i] = (size << 3) >> (i * 8);
	}

	//Block decomposition

	//Hash computation

	return result;
}


























