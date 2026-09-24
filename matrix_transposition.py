# This program demonstrates **matrix transposition** — converting rows into columns.

def print_pretty_list(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

def matrix_transpose(matrix):
    return [[el[i] for el in matrix] for i in range(4)]

def main():
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    print_pretty_list(matrix)
    transposed = matrix_transpose(matrix)
    print_pretty_list(transposed)

if __name__ == "__main__":
    main()
