import argparse
import re
from PIL import Image
from os import listdir
from fpdf import FPDF


def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Method to setup the parser and add the expected arguments
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    # adding arguments to the parser
    parser.add_argument('-i', '--input-directory',
                        dest='input', default='.', required=True)
    parser.add_argument('-t', '--target', dest='target',
                        default='merged.pdf', help='name or directory of the output')
    parser.add_argument('-d', '--delete', action='store_true', dest='delete',
                        help='if this argument is set all source files will be deleted')
    return parser


def create_pdf(files: list, target: str):
    """
This methods merges all files from given list into a single PDF
    :param target: Location where the result should be stored
    :param files: List of files which need to be merged into a PDF
    """
    files.sort()    # sort the files by name
    pdf = FPDF()
    for file in files:
        image_file = Image.open(file)

        size_tuple = image_file.size
        orientation = "P"
        if size_tuple[0] < size_tuple[1]:
            orientation = "L"
            size_tuple = (size_tuple[1], size_tuple[0])
        pixel_size = .5 # Converting sizes between the image and pdf
        pdf.add_page(orientation, (size_tuple[0]*pixel_size,size_tuple[1]*pixel_size))
        pdf.image(file, type="JPG")
        print("File: {} successfully added".format(file))
    pdf.output(target, 'F')


def parse_arguments(parser: argparse.ArgumentParser):
    """
    Method which parses all arguments and executes the corresponding command
    :param parser: Parser which handles the arguments
    """
    arguments = parser.parse_args()
    # look for JPGs inside the input directory
    directory = arguments.input
    files = []
    pattern = re.compile('.+\.jpg')
    print("Following files were found:")
    for file in listdir(directory):
        match = pattern.match(file)
        if match:
            filename = directory + '\\' + file
            print('\t' + filename)
            files.append(filename)
    # check if target argument is set
    if arguments.target:
        target = arguments.target
    else:
        target = 'merged.pdf'
    create_pdf(files, target)
    # delete all source files if the argument is given
    if arguments.delete:
        pass


def main():
    parser = setup_argument_parser()
    parse_arguments(parser)


if __name__ == '__main__':
    main()
