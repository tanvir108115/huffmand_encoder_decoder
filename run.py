import os
from app import huffmancoding


def clear(): os.system('cls')

clear()
print("Select the number of task you want to do")
print(" 1. Encode \n 2. Decode \n 3. Both encode and decode")
x = input("Answer: ")
library_path = r"library.txt"  # set path of library. By default it is in the same folder as data/compressed file

if x == '1' or x == '3':
    path = input("Enter the original file path: ")
    clear()
    if x == '1':
        y = huffmancoding(path, library_path,"")
        y.compress()
    else:
        y = huffmancoding(path, library_path,"")
        y.compress_decompress()
elif x == '2':
    path = input("Enter path for binary file:")
    extension = input("Enter file format:")
    if extension[0]!=".":
        extension="."+extension
    y = huffmancoding(path, library_path,extension)
    clear()
    y.decompress()
else:
    print("Invalid selection")
input("Press any key to exit")
