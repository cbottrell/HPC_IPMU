EXECS=test
MPICC=mpicc

all: ${EXECS}

test: test.c
	${MPICC} -o test test.c

clean:
	rm -f ${EXECS}
