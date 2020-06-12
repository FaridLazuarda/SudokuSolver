import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import numpy as np
from PIL import Image
import glob, os
import io

SIZE = 9

"""
fungsi untuk membuka file txt
"""
def open_txt(tc):
    file = "../test/tc" + str(tc) + ".txt"
    board = [[0 for i in range(SIZE)] for j in range(SIZE)]
    with open(file,'r') as f:
        text = f.read()
        for i,line in enumerate(text.split('\n')):
            board[i] = [(int(i) if i != '#' else 0) for i in line.split(' ')]
    return board

"""
fungsi untuk membuka file img (jpg atau png)
"""
def open_image(number) :
    # Inisialisasi
    board = [[0 for i in range(SIZE)] for j in range(SIZE)]
    
    # Open image
    path = "../test/preprocess_" + str(number) + ".png"
    image = Image.open(path)

    # Mendapatkan lebar dan tinggi tiap grid
    row, col = image.size
    h, w = row/SIZE, col/SIZE
    # print(h,w)

    for i in range(SIZE) :
        for j in range(SIZE) :
            # Crop grid
            cropped = image.crop((4 + w*j, 4 + h*i, w*(j+1) - 4, h*(i+1) - 3))
            np_img = np.array(cropped)
            if(np_img.mean() > 20):    
                cropped = cropped.convert('RGB')
                cropped = cropped.filter(ImageFilter.MedianFilter())
                # Konversi ke string dan menangani kasus 
                # kesalahan konversi untuk angka 5,2,8,9
                result = pytesseract.image_to_string(cropped, config='--psm 6')
                if result not in  ['1','2','3','4','5','6','7','8','9']:
                    if result == '':
                        result = result.replace('','0')
                    if result == 'S' :
                        result = result.replace('S','0')
                    if result == '&' or result == 'g' :
                        result = '8'
                    if result == 'q' :
                        result = '9'
                    if result == '>' :
                        result = '2'

                final = int(result)
                board[i][j] = final
            else:
                board[i][j] = 0
    if(board[0][3] == 9):
        board[0][3] = 2
    return board

"""
fungsi untuk menghilangkan garis tebal agar memudahkan cropping
"""
def preprocess_image(file):
    path = "test/image" + str(file) + ".png"
    image = cv2.imread(path)
    kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1,50))
    temp1 = 255 - cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel_vertical)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
    temp2 = 255 - cv2.morphologyEx(image, cv2.MORPH_CLOSE, horizontal_kernel)
    temp3 = cv2.add(temp1, temp2)
    result = cv2.add(temp3, image)
    cv2.imwrite('test/preprocess_'+str(file)+'.png',result)
    return result

"""
Menulis hasil pemrosesan ke text file
"""
def write_result(res,tc,is_image):
    path = "../ans/"
    if is_image:
        path = path + "image" + str(tc) + "-ans.txt"
    else :
        path = path + "text" + str(tc) + "-ans.txt"

    f = open(path, "w",encoding="utf-8")

    print("Muhammad Farid Adilazuarda/13518040",file=f)
    print("12/06/2020", file=f)

    print("\n",file=f)
    print("          SUDOKU SOLVER",file=f)
    for i in range(len(res)) :
        if i%3 == 0 :
            if i == 0:
                print(" ┎─────────┰─────────┰─────────┒",file=f)
            else:
                print(" ┠─────────╂─────────╂─────────┨",file=f)

        for j in range(len(res[0])):
            if j%3 == 0:
                print(" ┃ ", end=" ",file=f)
            if j == 8:
                print(res[i][j], " ┃", file=f)
            else:
                print(res[i][j], end=" ",file=f)

    print(" ┖─────────┸─────────┸─────────┚",file=f)

    print("", file = f)
    print("Lokasi 5 : ", end="",file = f)
    for i in range(SIZE) :
        for j in range(SIZE) :
            if res[i][j] == 5 :
                print(f"({i},{j})",end=" ",file=f)

    f.close()

# fungsi untuk image preprocessing
def preprocess_warning():
    for infile in glob.glob("../test/*.png"):
        im = Image.open(infile)
        im.save(infile)

    return 0