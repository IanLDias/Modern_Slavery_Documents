import PyPDF2 
import re
import pandas as pd
import textract

def get_file(file_path, parser):
    'Reads in files from Data folder'
    #Change this to get requests
    if parser == 'pypdf':
        pdffile = open(file_path, 'rb')
        pdfreader = PyPDF2.PdfFileReader(pdffile)
        num_pages = pdfreader.getNumPages()
        #Get it in text format and split by \n
        pages = [pdfreader.getPage(i).extractText().split('\n') for i in range(num_pages)]
        return pages
    elif parser == 'textract':
        text = textract.process(file_path, encoding='ascii')
        text = str(text)
        text = text.replace('\\n', ' ')
        return text
    else:
        raise Exception('Could not find file parser')

def preprocess(pages, parser):
    'Preprocesses the text. Removes ! and puts it into a dataframe'
    #Remove !!'s around the titles'
    #Make into a dataframe for easier manipulation
    pattern = '(![ ]*)|[   ][A-Z]'
    r = re.compile(pattern)
    titles = []
    if parser == 'pypdf':
        for page_num, page in enumerate(pages):
            for line_num, line in enumerate(page):
                if r.match(line):
                    if len(line.split()) < 8:
                        line = re.sub(r'!|#|"|$|&|%', '', line)
                        line = line.strip()
                        titles.append((page_num, line_num,line))
        titles = pd.DataFrame(titles, columns=['page_number', 'line_number', 'title'])
        return titles
    elif parser == 'textract':
        lines = pages.split('.')
        no_punc_lines = []
        for line in lines:
            line = re.sub(r'!|#|"|$|&|%', '', line)
            line = line.strip()
            no_punc_lines.append(line)
        return no_punc_lines

def make_dict(titles, filename, parser):
    'Makes a dictionary out of the dataframe. Titles are keys and the text are values'
    if parser == 'pypdf':
        segments = {}
        pages = get_file(filename, parser)
        for i in range(1,len(titles)):
            if titles['page_number'][i-1] == titles['page_number'][i]:
                segments[titles['title'][i-1]] = pages[titles['page_number'][i-1]][titles['line_number'][i-1]+1:titles['line_number'][i]]
                continue
            segments[titles['title'][i-1]] = pages[titles['page_number'][i-1]][titles['line_number'][i-1]+1:]
        return segments
    elif parser == 'textract':
        raise Exception("Can only make a dictionary using pypdf parser")
         
def pipeline(filepath, parser):
    pages = get_file(filepath, parser)
    if parser == 'pypdf':
        titles = preprocess(pages, parser)
        segments = make_dict(titles, filepath, parser)
        return segments
    elif parser == 'textract':
        text = preprocess(pages, parser)
        return text
    else:
        raise Exception('Only accepts pypdf and textract')

if __name__ == '__main__':
    filepath = 'Data/coke_1.pdf'
    try:
        pipeline(filepath=filepath, parser='textract')
        pipeline(filepath=filepath, parser='pypdf')
    except:
        print('error')
