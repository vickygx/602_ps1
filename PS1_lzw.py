import argparse
import array
import struct

'''
Creates a dictionary of codewords to index
'''
def initialize_lzw_compress_table():
    table = dict()
    # Initialize first 256 characters
    for i in xrange(0, 256):
        table[chr(i)] = i
    return table

def initialize_lzw_decompress_table():
    table = dict()
    for i in xrange(0, 256):
        table[i] = chr(i)
    return table

'''
Takes a filename as input and creates an LZW-compressed file named filename.zl.
The filename should contain text.

The output file is written as a binary file of codewords.
'''
def lzw_compress(filename, max_size=2**16):
    # Our table holds max_size entries. Once the dictionary if full (e.g. == max_size)  
    # we first decode the current codeword, re-initiliaze the dictionary, and finally,
    # add the new unknown codeword as an entry into the dictionary.
    # Since we are packing 16-bit codewords, we consider each codeword as an 
    # unsigned short integer ('H') 

    # Open input file
    f = open(filename, 'rb')
    compressed = array.array("B", f.read())
    f.close()

    # Open new output file as a binary file for writing.
    outname = filename + '.zl'  
    outfile = open(outname, 'wb')

    # Initialize table
    table = initialize_lzw_compress_table();

    seq = chr(compressed.pop(0))
    for symbol in compressed:
        concat = seq + chr(symbol)
        # If current sequence is in table, keep concating
        if concat in table:
            seq = concat
        else:
            # Transmit the index/code of sequence seq in the form of a 2 byte-long codeword
            outfile.write(struct.pack('H', table[seq]))
            # If table is full, reinitialize
            if len(table) == max_size:
                # Reinitializing
                table = initialize_lzw_compress_table()
            else: 
                table[concat] = len(table)
            seq = chr(symbol) 

    # Transmitting what's leftover
    outfile.write(struct.pack('H', table[seq]))

    # Closing all files
    outfile.close()

'''
Takes a filename as input and creates an uncompressed file named filename.u 
Example, filename = "test.zl", output file="test.zl.u".

The input is read as a binary file of codewords.

If the file contains an invalid codeword, the program terminates.
'''
def lzw_decompress(filename, max_size=2**16):
    # Open input file as binary readable file
    f = open(filename, 'rb')
    # Reading two byte at a time. We need 2 bytes for every codeword.
    compressed = array.array("H", f.read())
    f.close()

    # Open output file
    outname = filename + '.u'  
    outfile = open(outname, 'wb')

    table = initialize_lzw_decompress_table()
    code = compressed.pop(0)
    string = table[code]
    outfile.write(string)

    for code in compressed:
        if code >= max_size:
            return;
        # If code is not inside table, we may not have entry
        if code not in table:
            entry = string + string[0]
        # Otherwise return it
        else:
            entry = table[code]
        outfile.write(entry)

        # reinitialize table
        if len(table) == max_size:
            table = initialize_lzw_decompress_table()

        table[len(table)] = string + entry[0]
        string = entry
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, help='filename to compress or decompress', default='test')
    parser.add_argument('-d', '--decompress', help='decompress file', action='store_true')

    args = parser.parse_args()

    if not args.decompress:
        lzw_compress(args.filename)
    else:
        lzw_decompress(args.filename)


