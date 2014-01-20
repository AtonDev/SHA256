#include <stdio.h>
#include <sys/timeb.h>
//data syze in bytes
#define DATA_SIZE 1000000

#define  SHR(x,n) ((x & 0xFFFFFFFF) >> n)
#define ROTR(x,n) (SHR(x,n) | (x << (32 - n)))

#define D0(x) (ROTR(x, 7) ^ ROTR(x,18) ^  SHR(x, 3))
#define D1(x) (ROTR(x,17) ^ ROTR(x,19) ^  SHR(x,10))

#define S0(x) (ROTR(x, 2) ^ ROTR(x,13) ^ ROTR(x,22))
#define S1(x) (ROTR(x, 6) ^ ROTR(x,11) ^ ROTR(x,25))

#define MJ(x,y,z) ((x & y) | (z & (x | y)))
#define CH(x,y,z) (z ^ (x & (y ^ z)))

typedef unsigned int uint;
typedef unsigned long long uint64_t;

typedef struct bigint
{
	uint val[8];
} int256_t;

typedef struct block
{
	unsigned char val[64];
} m_block;

uint K[64] = {	0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 
				0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
				0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 
				0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
				0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 
				0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
				0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 
				0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
				0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 
				0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
				0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 
				0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
				0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 
				0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
				0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 
				0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};

//implicit declarations
int256_t sha256(unsigned char input[], uint64_t size);
void print_H(int256_t hash);

int main(int argc, char const *argv[])
{
	//data formation
	uint data_size = DATA_SIZE + (-DATA_SIZE % 64);
	unsigned char data[data_size];

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
	bandwidth = (double) DATA_SIZE / (diff * 1000);
    printf("\nSHA took %u milliseconds ", diff);
    printf("for data of size %d MByte\n", DATA_SIZE / 1000000);
    printf("At %.2f Mbyte/s\n", bandwidth);
	return 0;
}

int256_t sha256(unsigned char data[], uint64_t size)
{	
	//printf("%02x", data[0]);
	//printf("%02x", data[1]);
	//printf("%02x\n", data[2]);
	int256_t H;
	/* Padding:
	 * append a 1, k*8 + 7 0s, and size in bits of  data on the right. */
	uint l = (size << 3) % 512;
	uint k = ((448 - 8 - l) % 512) / 8;
	data[size] = 0x80;
	for (int i = size + 1; i <= size + k; ++i)
	{
		data[i] = (0 & 0xff);
	}
	for (int i = 0; i < 8; ++i)
	{
		data[size + k + 1 + i] = ((size << 3) >> ((7 - i) * 8)) & 0xff;
	}

	//Block decomposition
	uint data_size = (size + (-size % 64));
	uint N = (data_size >> 6);

	//print
	//printf("k: %d\n", k);
	//printf("l: %08x\n", l);
	//for (int i = 0; i < data_size; ++i)
	//{
	//	  printf("data[%d]", i);
	//    printf("\t%02x\n", data[i]);
	//}

	//Hash computation
	H.val[0] = 0x6a09e667;
	H.val[1] = 0xbb67ae85;
	H.val[2] = 0x3c6ef372;
	H.val[3] = 0xa54ff53a;
	H.val[4] = 0x510e527f;
	H.val[5] = 0x9b05688c;
	H.val[6] = 0x1f83d9ab;
	H.val[7] = 0x5be0cd19;


	for (int t = 0; t < N; ++t)
	{
		uint a = H.val[0];
		uint b = H.val[1];
		uint c = H.val[2];
		uint d = H.val[3];
		uint e = H.val[4];
		uint f = H.val[5];
		uint g = H.val[6];
		uint h = H.val[7];
		int temp0, temp1;

	    // block decomposition
	    uint W[64];
	    for (int i = 0; i < 16; ++i)
	    {
	    	uint index = t * 64 + i * 4;
	    	W[i] = ((uint)data[index] << 24) | ((uint)data[index + 1] << 16) \
	    	| ((uint)data[index + 2] << 8) | (uint)data[index + 3];
	    	//printf("W[%d]", i);
	    	//printf("\t%08x\n", W[i]);
	    }
	    for (int i = 16; i < 64; ++i)
	    {
	    	W[i] =  D1(W[i-2]) + W[i-7] + D0(W[i-15]) + W[i-16];
	    }

	    //hash computation
	    for (int i = 0; i < 64; ++i)
	    {
	    	temp1 = (h + S1(e) + CH(e, f, g) + K[i] + W[i]) & 0xffffffff;
			temp0 = (S0(a) + MJ(a, b, c)) & 0xffffffff;
			//printf("temp1: %08x\n", temp1);
			//printf("h: %08x\n", h);
			//printf("s1: %08x\n", S1(e));
			//printf("Ch: %08x\n", CH(e, f, g));
			//printf("K[i]: %08x\n", K[i]);
			//printf("W[i]: %08x\n", W[i]);
			h = g;
			g = f;
			f = e;
			e = (d + temp1) & 0xffffffff;
			d = c;
			c = b;
			b = a;
			a = (temp0 + temp1) & 0xffffffff;
			//printf("t = %d", i);
			//printf("\t  %08x", a);
			//printf("  %08x", b);
			//printf("  %08x", c);
			//printf("  %08x", d);
			//printf("  %08x", e);
			//printf("  %08x", f);
			//printf("  %08x", g);
			//printf("  %08x\n", h);
	    }
		


	    H.val[0] = (H.val[0] + a) & 0xffffffff;
		H.val[1] = (H.val[1] + b) & 0xffffffff;
		H.val[2] = (H.val[2] + c) & 0xffffffff;
		H.val[3] = (H.val[3] + d) & 0xffffffff;
		H.val[4] = (H.val[4] + e) & 0xffffffff;
		H.val[5] = (H.val[5] + f) & 0xffffffff;
		H.val[6] = (H.val[6] + g) & 0xffffffff;
		H.val[7] = (H.val[7] + h) & 0xffffffff;
		
	}


	return H;
}

void print_H(int256_t hash) 
{
	printf("Hash:\n");
	for (int i = 0; i < 8; ++i)
	{
		printf("%08x ", (int) hash.val[i]);
	}
	printf("\n");
}






















