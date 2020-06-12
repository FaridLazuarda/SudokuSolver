from IOProcess import *

# ukuran puzzle
SIZE = 9

# fungsi untuk print board
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0:
            if i == 0:
                print(" ┎─────────┰─────────┰─────────┒")
            else:
                print(" ┠─────────╂─────────╂─────────┨")

        for j in range(len(bo[0])):
            if j % 3 == 0:
                print(" ┃ ", end=" ")

            if j == 8:
                print(bo[i][j], " ┃")
            else:
                print(bo[i][j], end=" ")

    print(" ┖─────────┸─────────┸─────────┚")

# fungsi untuk mengecek apakah sel sudah terisi
# jika belum akan diisi sebuah angka
def number_unassigned(board, row, col):
    num_unassign = 0
    for i in range(0,SIZE):
        for j in range (0,SIZE):
            # sel belum terisi
            if board[i][j] == 0:
                row = i
                col = j
                num_unassign = 1
                a = [row, col, num_unassign]
                return a
    a = [-1, -1, num_unassign]
    return a

# fungsi apakah dapat meletakkan suatu angka pada sel
def is_safe(board, n, r, c):
    # cek baris
    for i in range(0,SIZE):
        if board[r][i] == n:
            return False
    # cek kolom
    for i in range(0,SIZE):
        if board[i][c] == n:
            return False
    row_start = (r//3)*3
    col_start = (c//3)*3
    # cek submatriks
    for i in range(row_start,row_start+3):
        for j in range(col_start,col_start+3):
            if board[i][j]==n:
                return False
    return True

# fungsi backtrack untuk menyelesaikan puzzle
def solve_sudoku(board):
    row = 0
    col = 0
    # jika semua sel terisi maka sudah selesai
    a = number_unassigned(board, row, col)
    if a[2] == 0:
        return True
    row = a[0]
    col = a[1]
    # angka 1-9
    for i in range(1,10):
        if is_safe(board, i, row, col):
            board[row][col] = i
            # backtrack
            if solve_sudoku(board):
                return True
            board[row][col]=0
    return False

# mencetak koordinat angka 5 pada matriks sudoku
def fives(board):
    print("\nLokasi para 5 : ",end='')
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 5:
                print("(" + str(i) + "," + str(j) + ")",end=" ")

# main function
if __name__ == "__main__":
    choice = input("Apakah menggunakan input gambar? [y/n] ")
    is_pic = False
    if choice == "y":
        is_pic = True

    input_file = input("Masukkan pilihan test case 1-4 : ")
    print("Puzzle awal :")
    if is_pic:
        mat = open_image(input_file)
        print_board(mat)
    else:
        mat = open_txt(input_file)
        print_board(mat)

    solve_sudoku(mat)
    if solve_sudoku(mat):
        print("\nPuzzle akhir :")
        print_board(mat)
        fives(mat)
    else:
        print("Unsolvable")

    write_result(mat, input_file, is_pic)