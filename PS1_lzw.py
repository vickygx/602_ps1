import argparse

def lzw_compress(filename, max_size=2**16):
    pass

def lzw_decompress(filename, max_size=2**16):
    pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, help='filename to compress or decompress', default='test')
    parser.add_argument('-d', '--decompress', help='decompress file', action='store_true')

    args = parser.parse_args()

    if not args.decompress:
        lzw_compress(args.filename)
    else:
        lzw_decompress(args.filename)


