from PyPDF4 import PdfFileReader, PdfFileWriter
import sys
import os

def pdfrewrite(path_in, path_out):
    reader = PdfFileReader(open(path_in, 'rb'))
    writer = PdfFileWriter()
    pages = len(reader.pages)

    for i in range(pages):
        page = reader.pages[i]
        # if "/XObject" in page["/Resources"].keys() or "/Font" in page["/Resources"].keys():
        #     writer.addPage(page)
        # /XObject图像，/Font文字
        if "/XObject" in page["/Resources"].keys():
            writer.addPage(page)

    writer.write(open(path_out, 'wb'))

def main():
      path_in = os.getcwd() + '/' + sys.argv[1]
      path_out = os.getcwd() + '/' + sys.argv[2]
      pdfrewrite(path_in, path_out)


if __name__ == '__main__':
    # path_in = input(r"input:")
    # path_out = input(r"output:")
    # pdfrewrite(path_in, path_out)
    main()