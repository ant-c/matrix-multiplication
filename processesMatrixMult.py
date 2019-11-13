"""
@author  Anthony Cruz
@file    processesMatrixMult.py
@date    2018-12-01
@brief   This program performs multiprocessing matrix multiplication. There should be a change from a single
process solution to a multi-process solution.
"""

import sys
from multiprocessing import Process, Array

class Matrix:
    def __init__(self):
        """
        Constructor for matrix. Initializes fields.

        """
        self.__rows = 0
        self.__columns = 0
        self.__matrix = []
        self.__size = 0

    def set_rows(self, row):
        """
        Sets the rows of the matrix.

        Parameter
        ----------
        row : int
            row size

        """
        self.__rows = row

    def set_columns(self, column):
        """
        Sets the columns of the matrix.

        Parameter
        ----------
        column : int
            column size

        """
        self.__columns = column

    def set_matrix(self, array):
        """
        Sets the matrix array.

        Parameter
        ----------
        array : list
            matrix array

        """
        self.__matrix = array

    def set_size(self, size):
        """
        Sets the size of the matrix.

        Parameter
        ----------
        size : int
            matrix size

        """
        self.__size = size

    def update_matrix(self, value, row, col):
        """
        Updates the matrix index specified by row and col with the value.

        Parameters
        ----------
        value : int
            value to update the matrix specified index with
        row : int
            row number
        col : int
            column number

        """
        self.__matrix[row][col] = value

    def get_rows(self):
        """
        Returns the number of rows for a matrix.

        Parameters
        ----------
        (none)

        Returns
        -------
        int
            the number of rows

        """
        return self.__rows

    def get_columns(self):
        """
        Returns the number of columns for a matrix.

        Parameters
        ----------
        (none)

        Returns
        -------
        int
            the number of columns

        """
        return self.__columns

    def get_matrix(self):
        """
        Returns the matrix array.

        Parameters
        ----------
        (none)

        Returns
        -------
        list
            the matrix array

        """
        return self.__matrix

    def get_size(self):
        """
        Returns the size of the matrix.

        Parameters
        ----------
        (none)

        Returns
        -------
        int
            the size of the matrix

        """
        return self.__size

    def get_value(self, row, col):
        """
        Returns a value from matrix[row][col].

        Parameters
        ----------
        row : int
            the row index
        col : int
            the column index

        Returns
        -------
        int
            the value from matrix[row][col]

        """
        return self.__matrix[row][col]
# --------------------------------------------------------------------------------------------------


class Threads:
    def __init__(self):
        """
        Constructor for threads. Initializes fields.

        """
        self.__thread_number = 0
        self.__thread_count = 0
        self.__start = 0
        self.__end = 0
        self.__remainder = 0

    def set_id(self, id_num):
        """
        Sets the thread id.

        Parameter
        ----------
        id_num : int
            thread number
        """
        self.__thread_number = id_num

    def set_count(self, count):
        """
        Sets the total thread count.

        Parameter
        ----------
        count : int
            the total thread count
        """
        self.__thread_count = count

    def set_start(self, start):
        """
        Sets the start point a thread will start executing from.

        Parameter
        ----------
        start : int
            where a thread will begin calculations from
        """
        self.__start = start

    def set_end(self, end):
        """
        Sets the end point a thread will finish executing from.

        Parameter
        ----------
        end : int
            where a thread will end calculations
        """
        self.__end = end

    def set_remainder(self, remainder):
        """
        Sets the remainder (number of calculations % number of threads) for threads.

        Parameter
        ----------
        remainder : int
            number of calculations % number of threads
        """
        self.__remainder = remainder

    def get_id(self):
        """
        Returns the thread id.

        Parameters
        ----------
        (none)

        Returns
        -------
        int
            the thread id number

        """
        return self.__thread_number

    def get_count(self):
        """
        Returns the total thread count.

        Parameters
        ----------
        (none)

        Returns
        -------
        int
            the total thread count

        """
        return self.__thread_count

    def get_start(self):
        """
        Returns the start point a thread will start execution from.

        Parameters
        ----------
        (none)

        Returns
        -------
        int
            the start point a thread will start executing from.

        """
        return self.__start

    def get_end(self):
        """
        Returns the end point for where a thread will stop execution.

        Parameters
        ----------
        (none)

        Returns
        -------
        int
            the end point for a thread execution.

        """
        return self.__end

    def get_remainder(self):
        """
        Returns the remainder (number of calculations % number of threads).

        Parameters
        ----------
        (none)

        Returns
        -------
        int
            number of calculations % number of threads

        """
        return self.__remainder
# --------------------------------------------------------------------------------------------------


def get_arg_count():
    """
    Compares the number of arguments to the expected number of arguments (5).
    Returns 0 for success, else 1 for error.

    Parameters
    ----------
    (none)

    Returns
    -------
    int
        0 for success; 1 for error

    """
    return_status = 0

    if len(sys.argv) != 5:
        print("Missing arguments: \n./threaded <input file> <input file> <output file> <number of threads>")
        return_status = 1

    return return_status
# --------------------------------------------------------------------------------------------------


def get_matrix_data(argument, matrix):
    """
    Opens an input file and fills the 2d matrix with the data from the file.
    Checks for a valid input file.

    Parameters
    ----------
    argument : int
        which argument to read from argv[argument]
    matrix : Matrix()
        object from matrix class

    Returns
    -------
    int
        0 for success, else 1 for error

    """
    return_status = 0

    try:
        with open(sys.argv[argument], 'r') as f:
            # get rows
            value = f.readline()
            r = int(value)
            matrix.set_rows(r)

            # get columns
            value = f.readline()
            r = int(value)
            matrix.set_columns(r)

            # get matrix
            data_list = [[int(n) for n in line.split()] for line in f]
            matrix.set_matrix(data_list)
    except IOError:
        print("Error: Invalid input file.\n")
        return_status = 1

    return return_status
# ---------------------------------------------------------------------------------------------------


def thread_sections(id, result, size):
    """
    Determines the calculations per each thread to apply parallelism when multiplying two matrices.
    When workload is determined the multiply function will be called.

    Parameters
    ----------
    id : int
        Thread id number
    result: list
        Shared memory array for result
    size : int
        size of result matrix (a.rows * b.columns)

    Returns
    -------
    (none)

    """
    # set thread id
    thread_class[id].set_id(id)
    # leftover count after dividing the per thread calculations
    thread_class[id].set_remainder(int(size % thread_class[id].get_count()))

    # one thread must do the remainder
    if id == 0:
        thread_class[id].set_start(int(0))
        thread_class[id].set_end((int(size / thread_class[id].get_count()))
                                 + thread_class[id].get_remainder())
    else:
        # divide the work based on thread number and total thread count
        thread_class[id].set_start((int((size / thread_class[id].get_count())) * id)
                                   + thread_class[id].get_remainder())
        thread_class[id].set_end((int((size / thread_class[id].get_count())) * (id + 1))
                                 + thread_class[id].get_remainder())

    # call function to multiply the two matrices
    multiply(a_matrix, b_matrix, id, result)
# ---------------------------------------------------------------------------------------------------


def multiply(a, b, thread, result):
    """
    Multiplies two matrices concurrently as each thread calculates different sections.
    Thread class contains start and end points per thread.

    Parameters
    ----------
    a : Matrix object
        1st matrix
    b : Matrix object
        2nd matrix
    thread : int
        thread id number
    result: list
        shared memory array

    Returns
    -------
    (none)

    """

    for start in range(thread_class[thread].get_start(), thread_class[thread].get_end()):
        # convert to 2d indexes
        row = start % a.get_rows()
        col = int(start / b.get_columns())
        value = 0

        for i in range(a.get_columns()):
            value += a.get_value(row, i) * b.get_value(i, col)

        # update results array
        result[row * a_matrix.get_rows() + col] = value
# ---------------------------------------------------------------------------------------------------


def out_file():
    """
    Creates an output file which contains the result from the matrix multiplication.

    Parameters
    ----------
    (none)

    Returns
    -------
    (none)

    """
    # name file according to command line argument[3]
    f = open(sys.argv[3], 'w')
    # write rows on one line
    f.write(str(a_matrix.get_rows()) + "\n")
    # write columns on one line
    f.write(str(b_matrix.get_columns()) + "\n")
    # write the shared array results
    rows = a_matrix.get_rows()  # save value to eliminate many function calls
    cols = b_matrix.get_columns()
    for i in range(rows):
        for j in range(cols):
            f.write(str(result[i * rows + j]) + " ")
        f.write("\n")

    # done; close the file
    f.close()
    print("'", sys.argv[3], "' created.\n")
# ---------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Main entry-point for this application.
#
# @return Exit-code for the process - 0 for success, else an error code.
# ---------------------------------------------------------------------------
status = 0
thread_count = 0

# check argument count
if get_arg_count():
    status = 1
elif not(get_arg_count()):
    # if args are good then create Matrix objects and read input files
    a_matrix = Matrix()
    b_matrix = Matrix()

    if not get_matrix_data(1, a_matrix) and not get_matrix_data(2, b_matrix):
        # if input files are good then make sure a cols = b rows
        if a_matrix.get_columns() != b_matrix.get_rows():
            print("Error. A-matrix column must equal B-matrix row.\n")
            status = 1
        else:
            # get thread count from command line
            thread_count = int(sys.argv[4])

            # check if thread count is valid
            if thread_count > 16 or thread_count < 1:
                print("Error. Thread count must be 1-16 (inclusive).\n")
                status = 1

        if not status:
            # if no errors then create a thread class array
            thread_class = [Threads() for i in range(thread_count)]

            # set the thread count
            for i in range(thread_count):
                thread_class[i].set_count(thread_count)

            # thread array for ids
            threads = [0 for i in range(thread_count)]

            # create a shared array for processes
            result = Array('i', a_matrix.get_rows() * b_matrix.get_columns())

            # fire off threads
            if __name__ == '__main__':
                for i in range(len(threads)):
                    threads[i] = Process(target=thread_sections, args=(i, result, a_matrix.get_rows()
                                                                       * b_matrix.get_columns()))
                    threads[i].start()

                # wait for threads to complete
                for i in range(len(threads)):
                    threads[i].join()

                # write results info to output file
                out_file()

    else:
        status = 1

sys.exit(status)