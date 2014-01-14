def bit_len(num):
	bitlen = 0
	while (num != 0):
		num >>= 1
		bitlen += 1
	return bitlen
