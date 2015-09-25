from PS1_lzw import lzw_compress, lzw_decompress
import array

def test_lzw_internal(compress, filename, expected_filename, maxsize=2**16):
    if compress:
        function_type = "compress"
    else:
        function_type = "decompress"

    print "\n\nRunning %s test with\n \tfilename=%s \n\tmaxsize=%d" % (function_type, filename, maxsize)

    if compress:
        lzw_compress(filename, maxsize)
    else:
        lzw_decompress(filename, maxsize)
   
    # Compare output of compress with expected_filename output
    if compress:
        output_filename = filename + ".zl"
        read_type = "H"
    else:
        output_filename = filename + ".u"
        read_type = "B"

    output_f = open(output_filename, 'rb')
    print "Comparing output (%s) with expected (%s)" % (output_filename, expected_filename)

    output_compressed = array.array(read_type, output_f.read())
    output_f.close()

    expected_f = open(expected_filename, 'rb')
    expected_compressed = array.array(read_type, expected_f.read())
    expected_f.close()

    success = output_compressed == expected_compressed
    if success:
        result = "success"
    else:
        result = "failure"

    print "Diffs:"
    for i in xrange(len(output_compressed)):
        if output_compressed[i] != expected_compressed[i]:
            print "index: ", i
            print "output: ", output_compressed[i]
            print "expected: ", expected_compressed[i]

    print "Test results: %s" % result


if __name__ == "__main__":
    # List of tuple where each tuple consists of filename and expected_filename
    compression_tests = [("lzw_compress_tests/1.dat", "lzw_tests/1.dat.zl", 2**16),
        ("lzw_compress_tests/2.dat", "lzw_tests/2.dat.zl", 2**16),
        ("lzw_compress_tests/3.dat", "lzw_tests/3.dat.zl", 2**16),
        ("lzw_compress_tests/4.dat", "lzw_tests/4.dat.zl", 2**16),
        ("lzw_compress_tests/5.dat", "lzw_tests/5.dat.zl", 2**16),
        ("lzw_compress_tests/6.dat", "lzw_tests/6.dat.zl", 2**16),
        ("lzw_compress_tests/5.dat", "lzw_tests/5.dat.512.zl", 512),
        ("lzw_compress_tests/6.dat", "lzw_tests/6.dat.512.zl", 512),
        ]

    for (filename, expected_filename, maxsize) in compression_tests:
        test_lzw_internal(True, filename, expected_filename, maxsize)


    decompression_tests = [("lzw_decompress_tests/1.dat.zl", "lzw_tests/1.dat"),
        ("lzw_decompress_tests/2.dat.zl", "lzw_tests/2.dat"),
        ("lzw_decompress_tests/3.dat.zl", "lzw_tests/3.dat"),
        ("lzw_decompress_tests/4.dat.zl", "lzw_tests/4.dat"),
        ("lzw_decompress_tests/5.dat.zl", "lzw_tests/5.dat")]

    for (filename, expected_filename) in decompression_tests:
        test_lzw_internal(False, filename, expected_filename)

