CC = gcc
FLAGS = -std=c99 

default:
	$(CC) $(FLAGS) *.c -o sha256

clean:
	rm -f sha256