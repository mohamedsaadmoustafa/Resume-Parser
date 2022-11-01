import os

import PyPDF2
# from pdfminer.high_level import extract_text
import docx2txt


class ResumeText(object):
    def __init__(self, path=''):
        self.path = path
        self._text = None

    def _checker(self):
        """ Only accept .pdf and .docs files """
        file_extension = os.path.splitext(self.path)[1]
        if file_extension == '.docx':
            self._text = self._extract_text_from_docx()
        elif file_extension == '.pdf':
            self._text = self._extract_text_from_pdf()
        elif file_extension == '.txt':
            self._text = self._extract_text_from_txt()
        else:
            print('pdf or docx file')
            # return None

    @property
    def text(self):
        #self._checker()
        return self._text

    def _extract_text_from_docx(self):
        txt = docx2txt.process(self.path)
        if txt:
            return txt.replace('\t', ' ')
        return None

    # def _extract_text_from_pdf(self):
    #    return extract_text(self.path)
    def extract_text_from_pdf(self, pdf_path):
        file = open(pdf_path, 'rb')
        reader = PyPDF2.PdfFileReader(file)
        pages = reader.numPages
        text = ''
        key, uri, ank = '/Annots', '/URI', '/A'
        for page in reader.pages:
            # add page text
            text += page.extract_text() + "\n"
            # extract hidden links in pdf and add to text
            if key in page:
                for a in page[key]:
                    obj = a.getObject()
                    if uri in obj[ank]:
                        text += obj[ank][uri]
        return text

    def _extract_text_from_txt(self):
        f = open(self.path, "r")
        return f.read()
