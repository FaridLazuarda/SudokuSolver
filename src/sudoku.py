from IOProcess import *

# tesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

# ukuran puzzle
SIZE = 9

def print_board(bo):
    """
    fungsi untuk print board
    """
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

def zero_loc(board, row, col):
    """
    fungsi untuk mengecek apakah sel sudah terisi
    jika belum akan diisi sebuah angka
    """
    zeros = 0
    for i in range(SIZE):
        for j in range (SIZE):
            # sel belum terisi
            if board[i][j] == 0:
                row = i
                col = j
                zeros = 1
                a = [row, col, zeros]
                return row,col,zeros
    row,col = -1,-1
    return row,col,zeros

def placeable(board, n, r, c):
    """
    fungsi apakah dapat meletakkan suatu angka pada sel
    """
    # cek baris
    for i in range(SIZE):
        if board[r][i] == n:
            return False
    # cek kolom
    for i in range(SIZE):
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

def solve(board):
    """
    fungsi backtrack untuk menyelesaikan puzzle
    """
    row, col = 0,0
    # jika semua sel terisi maka sudah selesai
    row,col,zero = zero_loc(board, row, col)
    if zero == 0:
        return True
    
    # angka 1-9
    for i in range(1,SIZE+1):
        if placeable(board, i, row, col):
            board[row][col] = i
            # backtrack
            if solve(board):
                return True
            board[row][col]=0
    return False

def fives(board):
    """
    mencetak koordinat angka 5 pada matriks sudoku
    """
    print("\nLokasi para 5 : ",end='')
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 5:
                print("(" + str(i) + "," + str(j) + ")",end=" ")

if __name__ == "__main__":
    """
    main function
    """
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

    solve(mat)
    if solve(mat):
        print("\nPuzzle akhir :")
        print_board(mat)
        fives(mat)
    else:
        print("Unsolvable")

    write_result(mat, input_file, is_pic)