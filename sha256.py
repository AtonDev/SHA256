import sys
import binascii
from utils import bit_len
 

def main():
	#correctness test of hash function
	print('4: ', bit_len(4))
	test()
	
	#successful exit
	return 0

#returns 256bit hash of the number input
def sha256(inp='0'):
	inp = int(binascii.hexlify(inp.encode('ascii', 'strict')), 16)
	l = bit_len(inp)

	
	

	print('l: ', l)
	if l >= (1 << 64):
		return 1
	
	#Padding
	k = (448 - 1 - l) % 512
	inp = (inp << 1) | 1
	inp = inp << k
	inp = (inp << 64) | (l & 0xffffffffffffffff)
	
	#Block decomposition
	l = bit_len(inp)
	print('L: ', l)
	N = l // 512
	block_mask = pow(2, 512) - 1
	M = []
	while (inp > 0):
		block = inp & block_mask
		M.append(block)
		inp = inp >> 512


	#Hash computation
	h1, h2, h3, h4 = 0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a
	h5, h6, h7, h8 = 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
	
	print('N: ', N)
	for t in range(0, N): 
		print('----------------------------------')
		a, b, c, d = h1, h2, h3, h4
		e, f, g, h = h5, h6, h7, h8
		W = block_decom(M[t])
		print(W)
		for i in range(0,64):
			temp1 = (h + Sig1(e) + Ch(e, f, g) + K[i] + W[i]) & 0xffffffff
			temp0 = (Sig0(a) + Maj(a, b, c)) & 0xffffffff
			h = g
			g = f
			f = e
			e = (d + temp1) & 0xffffffff
			d = c
			c = b
			b = a
			a = (temp0 + temp1) & 0xffffffff
		
		h1 += a & 0xffffffff
		h2 += b & 0xffffffff
		h3 += c & 0xffffffff
		h4 += d & 0xffffffff
		h5 += e & 0xffffffff
		h6 += f & 0xffffffff
		h7 += g & 0xffffffff
		h8 += h & 0xffffffff

	return hex(Con(Con(Con(h1, h2) ,Con(h3, h4)) ,Con(Con(h5, h6) ,Con(h7, h8))))

#Basic operators for hash function
RoR = lambda A, n: ((A & 0xffffffff) >> (n & 31) | (((A & 0xffffffff) << (32 - (n & 31))) & 0xffffffff))
Rs = lambda A, n: (A & 0xffffffff) >> (n & 31)
Con = lambda A, B: (A << bit_len(B)) | B
Ch = lambda x, y, z: ((x & y) ^ (~x & z)) & 0xffffffff
Maj = lambda x, y, z: ((x & y) ^ (x & z) ^ (y & z)) & 0xffffffff
Sig0 = lambda x: RoR(x, 2) ^ RoR(x, 13) ^ RoR(x, 22)
Sig1 = lambda x: RoR(x, 6) ^ RoR(x, 11) ^ RoR(x, 25)
Del0 = lambda x: RoR(x, 7) ^ RoR(x, 18) ^ RoR(x, 3)
Del1 = lambda x: RoR(x, 17) ^ RoR(x, 19) ^ RoR(x, 10)
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]



def block_decom(block512):
	W = []
	for i in range(0,16):
		W.insert(0, block512 & 0xffffffff)
		block512 = block512 >> 32
	for i in range(16, 64):
		W.append((Del1(W[i-2]) + W[i-7] + Del0(W[i-15]) + W[i-16]) & 0xffffffff)
	return W



def test():
	print(sha256('abc'))
	assert 0xba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad == sha256('abc')
	assert 0xd7b553c6f09ac85d142415f857c5310f3bbbe7cdd787cce4b985acedd585266f == sha256('just a test string')
    



if __name__ == '__main__':
	exit = main()
	sys.exit(exit)
