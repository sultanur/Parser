#!/usr/bin/env python
import argparse
import sys
import textwrap


# For reading Command Line Arguments (CLA) used argprase module from standard library
def read_Args():
    parser = argparse.ArgumentParser(description="./parse.py",
                                     usage="./parse.py  input_file1 [input_file2  input_file3 ...]  or "
                                           "./parse.py  input_file --output output_file --wrap wrap_size")
    parser.add_argument('file', type=argparse.FileType('r'),
                        nargs='+')  # '+' requires one input_file or more on command line
    parser.add_argument('--output', type=argparse.FileType('w'),
                        help='arg:name of output file')  # in case of not providing output_file it returns None
    parser.add_argument('--wrap', help='arg:the size of wrapping text ', type=int)

    # vars turns the parsed CLA into a dictionary, where key:name of the CLA, value: value of CLA
    args_vars = vars(parser.parse_args())
    files_list = [f.name for f in args_vars['file']]  # all files for reading will be saved in a list
    output_file = args_vars['output']
    wrap_size = args_vars['wrap']
    if args_vars['output'] is not None:
        return files_list, output_file, wrap_size
    else:
        return files_list


# Implemented parsing of TBFSBS header format separately for reuse of it in printing to console and in writing in file.
def TBFSBS_Header(line):
    id_seq = 'ID: {}'.format(line.split()[1])
    value_start = 'Value: {0:.1f}  (print only one digit after decimal point) '.format(float(line.split()[2]))
    value = 'Value: {0:.1f} '.format(float(line.split()[2]))
    description = 'Description: {}'.format(' '.join(line.split()[3:]))
    return id_seq, value_start, value, description


# Function prints in console parsed TBFSBS_header and the length of Sequence.
def printParse_SequenceLength():
    files = read_Args()
    for file in files:
        print("filename: {}\n".format(file))
        count_chars = 0
        start_flag = True
        with open(file, "r") as read_file:
            while line := read_file.readline():
                if line.startswith('%'):
                    if count_chars != 0:
                        print('Sequence length: {}\n'.format(count_chars))
                    count_chars = 0
                    id_sequence, value_start, value, description = TBFSBS_Header(line)
                    print(id_sequence)
                    if start_flag:
                        print(value_start)
                    else:
                        print(value)
                    print(description)
                else:
                    start_flag = False
                    count_chars += len(line.rstrip())
            print('Sequence length: {}\n'.format(count_chars))


# Function writes to output file parsed TBFSBS_header and the result of wrapping the Sequence from input file.
# For wrapping used textwrap module from Standard library
def TBFSBS_writerWrapper():
    start_flag = True
    sequence = ""
    input_files, output_file, wrap_size = read_Args()
    for file in input_files:
        with open(file, "r") as in_file:
            with open(output_file.name, "w") as out_file:
                while line := in_file.readline():
                    if line.startswith('%'):
                        if (len(sequence)) != 0:
                            wrapped_string = '\n'.join(
                                textwrap.wrap(sequence, width=int(wrap_size)))
                            out_file.write('Sequence: \n')
                            out_file.write(wrapped_string + "\n\n")
                        sequence = str()
                        id_seq, value_start, value, description = TBFSBS_Header(line)
                        out_file.write(id_seq + '\n')
                        if start_flag:
                            out_file.write(value_start + '\n')
                        else:
                            out_file.write(value + '\n')
                        out_file.write(description + '\n')
                        start_flag = False
                    else:
                        sequence += line
                wrapped_string = '\n'.join(textwrap.wrap(sequence, width=int(wrap_size)))
                out_file.write('Sequence: \n')
                out_file.write(wrapped_string)


def main():
    if len(sys.argv) < 2:
        print("Usage: ./parse.py input_file1 [input_file2  input_file3 ...] "
              "\n or ./parse.py  input_file --output output_file --wrap wrap_size")
        sys.exit(1)
    elif len(sys.argv) > 3 and sys.argv[2] == '--output':
        TBFSBS_writerWrapper()
        sys.exit(0)
    else:
        printParse_SequenceLength()
        sys.exit(0)


if __name__ == '__main__':
    main()
