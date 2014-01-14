import sys



def main():
	#correctness test of hash function
	test()



	#successful exit
	return 0

#returns 256bit hash of the number input
def sha256(inp):
	return 0

#Basic operators for hash function

def test():
	a_str = "just a test string"
	assert 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' == sha256()
	assert 'd7b553c6f09ac85d142415f857c5310f3bbbe7cdd787cce4b985acedd585266f' == sha256(a_str)
	assert '8113ebf33c97daa9998762aacafe750c7cefc2b2f173c90c59663a57fe626f21' == sha256(a_str*7)
    



if __name__ == '__main__':
	exit = main()
	sys.exit(exit)
