import PyPDF2 
import re
import pandas as pd

def get_file(filename):
    'Reads in files from Data folder'
    #Change this to get requests
    pdf_file = 'Data/' + filename
    pdffile = open(pdf_file, 'rb')
    pdfreader = PyPDF2.PdfFileReader(pdffile)
    num_pages = pdfreader.getNumPages()
    #Get it in text format and split by \n
    pages = [pdfreader.getPage(i).extractText().split('\n') for i in range(num_pages)]
    return pages

def preprocess(pages):
    'Preprocesses the text. Removes ! and puts it into a dataframe'
    #Remove !!'s around the titles'
    #Make into a dataframe for easier manipulation
    pattern = '(![ ]*)|[   ][A-Z]'
    r = re.compile(pattern)
    titles = []
    for page_num, page in enumerate(pages):
        for line_num, line in enumerate(page):
            if r.match(line):
                if len(line.split()) < 8:
                    line = re.sub(r'!|#|"|$|&|%', '', line)
                    line = line.strip()
                    titles.append((page_num, line_num,line))
    titles = pd.DataFrame(titles, columns=['page_number', 'line_number', 'title'])
    return titles

def make_dict(titles, filename):
    'Makes a dictionary out of the dataframe. Titles are keys and the text are values'
    segments = {}
    pages = get_file(filename)
    for i in range(1,len(titles)):
        if titles['page_number'][i-1] == titles['page_number'][i]:
            segments[titles['title'][i-1]] = pages[titles['page_number'][i-1]][titles['line_number'][i-1]+1:titles['line_number'][i]]
            continue
        segments[titles['title'][i-1]] = pages[titles['page_number'][i-1]][titles['line_number'][i-1]+1:]
    return segments

def pipeline(filename):
    pages = get_file(filename)
    titles = preprocess(pages)
    segments = make_dict(titles, filename)
    return segments

if __name__ == '__main__':
    filename = 'coke_1.pdf'
    print(pipeline(filename='coke_1.pdf'))
