import os
import PyPDF2
# from pdfminer.high_level import extract_text
import docx2txt
import logging

# logging configuration
logging.basicConfig(level=logging.INFO)

class ResumeText(object):
    def __init__(self, datafile, datafile_type):
        self.datafile = datafile
        self.datafile_type = datafile_type
        self._text = None

    def _checker(self):
        """ Only accept .pdf and .docs files """
        if self.datafile_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            logging.info('Start extracting text from DOCS')
            self._extract_text_from_docx()
            logging.info('Done! DOCS text is ready!\n')

        elif self.datafile_type == 'application/pdf':
            logging.info('Start extracting text from PDF')
            self._extract_text_from_pdf()
            logging.info('Done! PDF text is ready!\n')

        elif self.datafile_type == 'text/plain':
            logging.info('Start extracting text from TXT')
            self._extract_text_from_txt()
            logging.info('Done! TXT text is ready!\n')

        else:
            logging.info('Upload a pdf , txt or docx file\n')
            #return ' '


    @property
    def text(self):
        self._checker()
        return self._text

    def _extract_text_from_docx(self):
        txt = docx2txt.process(self.datafile)
        if txt:
            self._text = txt.replace('\t', ' ')

    # def _extract_text_from_pdf(self):
    #    return extract_text(self.datafile)
    def _extract_text_from_pdf(self):
        reader = PyPDF2.PdfFileReader(self.datafile)
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
        self._text = str(text)

    def _extract_text_from_txt(self):
        self._text = str(self.datafile.read())

