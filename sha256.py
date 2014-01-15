import sys
import binascii
from utils import bit_len
 

def main():
	#correctness test of hash function
	test()
	
	#successful exit
	return 0

#returns 256bit hash of the number input
def sha256(inp='0'):
	inp_data = []
	for c in inp:
		inp_data.append(int(binascii.hexlify(c.encode('ascii', 'strict')), 16))
	l = len(inp_data) * 8
	
	#Padding
	k = ((448 - 8 - l) % 512) // 8
	inp_data.append(1 << 7)
	for i in range(0, k):
		inp_data.append(0)
	for i in range(0, 8):
		i = 7 - i
		inp_data.append((l >> (i*8)) & 0xff)
	
	#Block decomposition
	l = len(inp_data) * 8
	N = l // 512
	M = []
	for i in range(0, N):
		mi = []
		for j in range(0, 64):
			mi.append(inp_data[i * 64 + j])
		M.append(mi)

	#Hash computation
	h1, h2, h3, h4 = 0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a
	h5, h6, h7, h8 = 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
	
	for t in range(0, N): 
		a, b, c, d = h1, h2, h3, h4
		e, f, g, h = h5, h6, h7, h8

		W = block_decom(M[t])
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
		
			#print('t = ' + str(i) + \
			#'\t  ' + str(hex(a)).upper()[2:] + \
			#'\t  ' + str(hex(b)).upper()[2:] + \
			#'\t  ' + str(hex(c)).upper()[2:] + \
			#'\t  ' + str(hex(d)).upper()[2:] + \
			#'\t  ' + str(hex(e)).upper()[2:] + \
			#'\t  ' + str(hex(f)).upper()[2:] + \
			#'\t  ' + str(hex(g)).upper()[2:] + \
			#'\t  ' + str(hex(h)).upper()[2:])

		h1 = (h1 + a) & 0xffffffff
		h2 = (h2 + b) & 0xffffffff
		h3 = (h3 + c) & 0xffffffff
		h4 = (h4 + d) & 0xffffffff
		h5 = (h5 + e) & 0xffffffff
		h6 = (h6 + f) & 0xffffffff
		h7 = (h7 + g) & 0xffffffff
		h8 = (h8 + h) & 0xffffffff

	return hex((h1 << 224) | (h2 << 192) | (h3 << 160) | (h4 << 128) | (h5 << 96) | (h6 << 64) | (h7 << 32 ) | h8)

#Basic operators for hash function
RoR = lambda A, n: ((A & 0xffffffff) >> (n & 31) | (((A & 0xffffffff) << (32 - (n & 31))) & 0xffffffff))
Rs = lambda A, n: (A & 0xffffffff) >> (n & 31)
Con = lambda A, B: (A << bit_len(B)) | B
Ch = lambda x, y, z: ((x & y) ^ (~x & z)) & 0xffffffff
Maj = lambda x, y, z: ((x & y) ^ (x & z) ^ (y & z)) & 0xffffffff
Sig0 = lambda x: RoR(x, 2) ^ RoR(x, 13) ^ RoR(x, 22)
Sig1 = lambda x: RoR(x, 6) ^ RoR(x, 11) ^ RoR(x, 25)
Del0 = lambda x: RoR(x, 7) ^ RoR(x, 18) ^ Rs(x, 3)
Del1 = lambda x: RoR(x, 17) ^ RoR(x, 19) ^ Rs(x, 10)
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
		word = (block512[i*4] << 24) + (block512[i*4 + 1] << 16) +\
		 (block512[i*4 + 2] << 8) + block512[i*4 + 3] 
		W.append(word)
	for i in range(16, 64):
		W.append((Del1(W[i-2]) + W[i-7] + Del0(W[i-15]) + W[i-16]) & 0xffffffff)
	return W



def test():
	print(sha256('abc'))
	assert (0xba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad == sha256('abc'))
	assert 0xd7b553c6f09ac85d142415f857c5310f3bbbe7cdd787cce4b985acedd585266f == sha256('just a test string')
    



if __name__ == '__main__':
	exit = main()
	sys.exit(exit)
