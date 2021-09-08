#!/usr/bin/env python
import argparse
import sys
import textwrap


# For reading Command Line Arguments (CLA) used argprase module from standard library

def read_Args():
    parser = argparse.ArgumentParser(description="./wrapper_Sequences",
                                     usage="./wrapper_Sequences.py  input_file --output output_file --join true --wrap wrap_size or"
                                           "./wrapper_Sequences.py  input_file --output output_file  --wrap wrap_size")
    parser.add_argument('file', type=argparse.FileType('r'),
                        nargs='+')  # '+' requires one or more input_file
    parser.add_argument('--output', type=argparse.FileType('w'),
                        help='arg:name of output file')  # in case of not providing output_file it returns None
    parser.add_argument('--wrap', help='arg:the size of wrapping text ')
    parser.add_argument('--join', help='joins Sequences with different IDs, arg: True', choices="true, True")

    # vars turns the parsed CLA into a dictionary, where key:name of the CLA, value: value of CLA
    args_vars = vars(parser.parse_args())
    files_list = [f.name for f in args_vars['file']]  # all files for reading will be saved in a list
    output_file = args_vars['output']
    wrap_size = args_vars['wrap']
    return files_list, output_file, wrap_size


# Two functions do line wrapping the Sequences and writes to file without header data:
# 1. Line wrapping the Sequences with different IDs separately
def TBFSBS_writer_WrapSequences():
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
                            out_file.write('\n' + wrapped_string + '\n')
                        sequence = str()
                    else:
                        sequence += line
                wrapped_string = '\n'.join(textwrap.wrap(sequence, width=int(wrap_size)))
                out_file.write("\n" + wrapped_string)


# 2. Line wrapping the joined group of Sequences (with different IDs)
def TBFSBS_writer_WrapJoinSequences():
    sequences = ""
    input_files, output_file, wrap_size = read_Args()
    for file in input_files:
        with open(file, "r") as in_file:
            with open(output_file.name, "w") as out_file:
                while line := in_file.readline():
                    if line.startswith('%'):
                        continue
                    else:
                        sequences += line
                wrapped_string = '\n'.join(textwrap.wrap(sequences, width=int(wrap_size)))
                out_file.write("\n" + wrapped_string)


def main():
    if len(sys.argv) < 2:
        print("Usage: ./wrapper_Sequences.py  input_file --output output_file --join true --wrap wrap_size ")
        sys.exit(1)
    elif len(sys.argv) > 3 and sys.argv[5] == 'true' or sys.argv[5] == 'True':
        TBFSBS_writer_WrapJoinSequences()
        sys.exit(0)
    else:
        TBFSBS_writer_WrapSequences()
        sys.exit(0)


if __name__ == '__main__':
    main()
