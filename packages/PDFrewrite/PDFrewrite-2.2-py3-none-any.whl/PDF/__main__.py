from PyPDF4 import PdfFileReader, PdfFileWriter
import sys
import os


def pdfrewrite(path_in, path_out, command):
    reader = PdfFileReader(open(path_in, 'rb'))
    writer = PdfFileWriter()
    pages = len(reader.pages)

    if command == 'both':
        for i in range(pages):
            page = reader.pages[i]
            if "/XObject" in page["/Resources"].keys() \
                    or "/Font" in page["/Resources"].keys():
                writer.addPage(page)
    else:
        if command == 'image':
            temp = '/XObject'
        elif command == 'text':
            temp = '/Font'
        else:
            print("ERROR!\n请进入目标文件目录并输入：\n"
                  "目标文件名, 输出文件名, 保留选项(image/text/both)\n"
                  "文件名无需后缀")
            sys.exit()
        for i in range(pages):
            page = reader.pages[i]
            if temp in page["/Resources"].keys():
                writer.addPage(page)

    writer.write(open(path_out, 'wb'))


def main():
    path_in = os.getcwd() + '/' + sys.argv[1] + '.pdf'
    path_out = os.getcwd() + '/' + sys.argv[2] + '.pdf'
    command = sys.argv[3]
    pdfrewrite(path_in, path_out, command)


if __name__ == '__main__':
    main()
