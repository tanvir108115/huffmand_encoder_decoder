import heapq
import os
import json
import concurrent.futures


class huffmancoding:
    def __init__(self, path, library_path, extension):
        self.path = path
        self.extension= extension
        self.output_path = ""
        self.library_path = library_path
        self.frequency = {}
        self.heap = []
        self.code = {}
        self.encoded_text = ""
        self.dif = 1000000
        self.reverse_mapping = {}

    class heapnode:  # Custom heapnode. This custom heapnode class has been written by Bhrigu Srivastava, which I came upon while troubleshooting the heapnode class for my project
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq

        def __lt__(self, other):  # Overriding bultin less than cheacker
            return self.freq < other.freq

        def __eq__(self, other):  # Overriding bultin equal to cheacker
            if (other == None):
                return False
            if (not isinstance(other, heapnode)):
                return False
            return self.freq == other.freq

    def file_cheacker(self, file, name):  # Checks existence of file and gives appropriate error if not found
        dictionary = {
            0: "Input file",
            1: "Compressed file",
            2: "Library"
        }
        if not os.path.exists(file):
            print(f"ERROR!! {dictionary[name]} not found")
            return False
        return True

    def progress_compression(self, completed):  # Prints completed step of compression
        print(f"Compression process ({completed}/9)")

    def progress_decompression(self, completed):  # Prints completed step of decompression
        print(f"Decompressing ({completed}/3)")

    def percentage(self, length, location):
        perc = (location / length) * 100
        print(f"Progress {perc:.2f} %", end="\r")
    def multi_threading_fre(self, function):  # Multithreading function for creating frequency table
        with open(self.path, 'rb') as ifile:
            length = 0
            location = 0
            l_data = ifile.read(self.dif)
            if len(l_data)== self.dif:
                print("Multiple threads are being used")
            while len(l_data) > 0:
                length += len(l_data)
                l_data = ifile.read(self.dif)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                ifile.seek(0)
                data = ifile.read(self.dif)
                location += len(data)
                self.percentage(length, location)
                while len(data) > 0:
                    executor.submit(function, data)
                    data = ifile.read(self.dif)
                    location += len(data)
                    self.percentage(length, location)

    def multi_threading_2_encoder(self, function, mode):  # Multithreading function for encoding input data
        with open(self.path, 'rb') as ifile:
            length = 0
            location = 0
            l_data = ifile.read(self.dif)
            while len(l_data) > 0:
                length += len(l_data)
                l_data = ifile.read(self.dif)
            ifile.seek(0)
            data = ifile.read(self.dif)
            location += len(data)
            self.percentage(length, location)
            with concurrent.futures.ThreadPoolExecutor() as executor, open("encoded_file.txt", 'w') as encoded_file:
                while len(data) > 0:
                    x = executor.submit(function, data)
                    encoded_file.write(x.result())
                    data = ifile.read(self.dif)
                    location += len(data)
                    self.percentage(length, location)

    def multi_threading_3_bit(self, function, mode):  # Multithreading function for saving encoded data in bin file
        self.progress_compression(8)
        with open("padded_file.txt", 'r') as ifile:
            length = 0
            location = 0
            l_data = ifile.read(self.dif)
            while len(l_data) > 0:
                length += len(l_data)
                l_data = ifile.read(self.dif)
            ifile.seek(0)
            data = ifile.read(self.dif)
            location += len(data)
            self.percentage(length, location)
            with concurrent.futures.ThreadPoolExecutor() as executor, open(self.output_path, 'wb') as o_file:
                while len(data) > 0:
                    x = executor.submit(function, data)
                    o_file.write(x.result())
                    data = ifile.read(self.dif)
                    location += len(data)
                    self.percentage(length, location)
        if os.path.exists("padded_file.txt"):
            os.remove("padded_file.txt")


    ## Code for compressing data

    def freq_table(self, data):  # Calculates frequency of characters in input
        # frequency = {}
        for character in data:
            if not character in self.frequency:
                self.frequency[character] = 0
            self.frequency[character] += 1

        # return frequency

    def heap_maker(self, freq):  # Makes heap tree according to frequency
        self.progress_compression(3)
        for key in freq:
            node = self.heapnode(key, freq[key])
            heapq.heappush(self.heap, node)


    def merge_nodes(self):  # Merging nodes until only one node remaining
        self.progress_compression(4)
        while (len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merge = self.heapnode(None, node1.freq + node2.freq)
            heapq.heappush(self.heap, merge)
            merge.left = node1
            merge.right = node2

    def code_generator(self, root, code):
        if (root == None):
            return
        if (root.char != None):
            self.code[root.char] = code
            self.reverse_mapping[code] = root.char
            return
        self.code_generator(root.left, code + "0")
        self.code_generator(root.right, code + "1")

    def code_converter(self):
        self.progress_compression(5)
        root = heapq.heappop(self.heap)
        code = ""
        self.code_generator(root, code)

    def encoding(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.code[character]

        return encoded_text

    def padding(self):  # adds extra padding if necessary
        self.progress_compression(7)
        padding = ""
        with open("encoded_file.txt", 'r') as ifile, open("padded_file.txt", 'w') as ofile:
            length = 0
            l_data=ifile.read(self.dif)
            while len(l_data)>0:
                length+=len(l_data)
                l_data = ifile.read(self.dif)
            extra = 8 - length % 8
            for i in range(extra):
                padding += "0"
            pad_info = "{0:08b}".format(extra)
            ofile.write(pad_info)
            ifile.seek(0)
            x = ifile.read(self.dif)
            location=0
            location+=len(x)
            self.percentage(length,location)
            while len(x) > 0:
                ofile.write(x)
                x = ifile.read(self.dif)
                location += len(x)
                self.percentage(length, location)
            ofile.write(padding)
        if os.path.exists("encoded_file.txt"):
            os.remove("encoded_file.txt")

    def byte_array(self, p_data):
        b = bytearray()
        for i in range(0, len(p_data), 8):
            byte = p_data[i:i + 8]
            b.append(int(byte, 2))

        return b

    def compress(self):  # Main compression function
        file_path, self.extension = os.path.splitext(self.path)
        self.output_path = file_path + ".bin"

        if not self.file_cheacker(self.path, 0):
            return

        with open(self.library_path, 'w') as library:
            self.progress_compression(1)
            self.multi_threading_fre(self.freq_table)
            self.progress_compression(2)
            self.heap_maker(self.frequency)
            self.merge_nodes()
            self.code_converter()
            self.progress_compression(6)
            self.multi_threading_2_encoder(self.encoding, 1)
            self.padding()
            self.multi_threading_3_bit(self.byte_array, 1)
            library.write(json.dumps(self.reverse_mapping))
            self.progress_compression(9)
            print("Compression completed\n")
            print(f"Output path= {self.output_path}\n")

    # code for decompressing data

    def multi_threading_decoder(self, function, output_path):
        with open(self.library_path, 'r') as library:
            reverse_mapping = json.loads(library.read())
            with concurrent.futures.ThreadPoolExecutor() as executor, open("encoded.txt", 'r') as encoded_file, open(
                    output_path, 'wb') as ofile:
                data = encoded_file.read()
                x = []
                while len(data) > 0:
                    x.append(executor.submit(function, data, reverse_mapping))
                    data = encoded_file.read()
                executor.shutdown(wait=True)
                for i in concurrent.futures.as_completed(x):
                    ofile.write(i.result())
            if os.path.exists("encoded.txt"):
                os.remove("encoded.txt")

    def remove_padding(self):
        with open("byte_info.txt", 'r') as byte_file, open("encoded.txt", 'w') as encoded_file:
            padded_info = byte_file.read(8)
            extra_padding = int(padded_info, 2)
            encoded_text = byte_file.read(self.dif)
            while len(encoded_text) > 0:
                encoded_text_f = byte_file.read(self.dif)
                if len(encoded_text_f) > 0:
                    encoded_file.write(encoded_text)
                else:
                    encoded_file.write(encoded_text[:-1 * extra_padding])
                encoded_text = encoded_text_f
        if os.path.exists("byte_info.txt"):
            os.remove("byte_info.txt")
        self.progress_decompression(2)
        # return encoded_text

    def data_decoder(self, encoded_text, reverse_mapping):
        current_code = ""
        decoded_text = bytearray()
        for bit in encoded_text:
            current_code += bit
            if (current_code in reverse_mapping):
                character = reverse_mapping[current_code]
                decoded_text.append(character)
                current_code = ""
        return decoded_text

    def decompress(self):
        file_path, extension = os.path.splitext(self.path)
        output_path = file_path + "decompressed" + self.extension
        self.path = file_path + ".bin"
        if not self.file_cheacker(self.path, 1) or not self.file_cheacker(self.library_path, 2):
            return
        with open(self.path, 'rb') as ifile:
            data = ifile.read(1)

            with open("byte_info.txt", 'w') as byte_file:
                while (len(data) > 0):
                    data = bin(ord(data))[2:].rjust(8, '0')
                    byte_file.write(data)
                    data = ifile.read(1)
            self.progress_decompression(1)
            self.remove_padding()
            decoded_text = bytearray()
            self.multi_threading_decoder(self.data_decoder, output_path)

            self.progress_decompression(3)
            print("Decompression completed\n")
            print(f"Output path= {output_path}")

    def compress_decompress(self):
        self.compress()
        self.decompress()
