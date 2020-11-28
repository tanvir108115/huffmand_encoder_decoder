<h1 align="center"> Huffmand encoding and decoding</h1>
<h2 align="center"><a  href="https://google.com">Live Demo</a></h2>

## Description
This is a Huffman encoder and decoder project, which can perform 3 functions. The first function will encode the input file and save it in "FILENAME.bin" format. The second function can decode the BIN file created by the first function. Finally the third function with perform both function 1 and 2 sequencially. Python Langugage has been used to write the code.

## Instruction to run the program:
1. Download the files named app.py and run.py and save them in the same folder.
2. Copy the file location. Example is shown below:  
![Instruction 1](https://github.com/tanvir108115/huffmand_encoder_decoder/blob/main/raw/1.gif "Logo Title Text 1")
3. Double click on run.py. 
4. If it opens up the command window and runs the program, go to step 7.
5. Incase command window does not open up the command window, open up the command windows where downloaded file from step 1 has been saved.
6. Copy and paste the following code in the command window and press enter <code>python run.py</code>
7. Select the operation you want by entering 1, 2 or 3.
8. For 1 and 3 operation you will only be asked to enter the path to the main file.
9. For operation 2 you will be asked the compressed file location and the output file format. (IMPORTANT: Without the right format, windows will not be able to open the file)
10. If only operation 2 is being selected, make sure you have not deleted the "library.txt" file that was created in the same folder as run.py during operation 1.
11. After the operation is done it will show the completion message followed by the output path.

## About this project:
1. This project should me able to do Halfman encode and decode for any file format. So far I have tested ".txt" ".jpg" ".mkv" and ".rar" format.
2. Multithreading has been used for the encoding part.
3. It can compress file of any size as long as the disk has enough space. (Usually it will require 2 times space than the size of file)
3. Decompressing for too large file will give Memory error as I was not able to succesfully implement multithreading and data dumping for large files yet. ( Loss of data was proportional to file size while tried to use multithread for this part.)

## Future scopes:
1. Add multithreadig for decompression also.
2. Save file format information in bin file so that decompress function can recognise automatically.
