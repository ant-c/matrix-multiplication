# matrix-multiplication

This program takes in two input files (A matrix/B matrix), an output file name, and the number of threads from the user. Upon valid input, matrix computation sections are split and the threads are fired off to execute their portion of the result. After all threads have completed their work, the result is displayed in an output file. The execution time dramatically improved compared to the multi-threaded approach!
