
import argparse
import gc
import os

from app.src import app

parser = argparse.ArgumentParser()

parser.add_argument('-if', "--input_folder", help="where the documents are located", )
parser.add_argument('-o', "--output", help="where the clustering result will be outputted", )

args = parser.parse_args()


if __name__ == '__main__':
    input = args.input_folder
    output = args.output

    app.main(input, output)


