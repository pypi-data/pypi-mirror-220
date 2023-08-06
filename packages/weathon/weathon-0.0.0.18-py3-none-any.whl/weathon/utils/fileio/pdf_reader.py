import pdfplumber
from typing import List
from tqdm import tqdm
from pdf2docx import Converter


class PDFReader:

    def __init__(self, file_path:str):
        self.file_path = file_path


    def extract_text(self,pdf_pwd:str):
        page_texts = []
        with pdfplumber.open(self.file_path, password=pdf_pwd) as pdf_reader:
            for page_id, page in enumerate(tqdm(pdf_reader.pages)):
                page_text = page.extract_text()
                page_texts.append((page_id, page_text))
        return page_texts


    def extract_tables(self,pdf_pwd:str):
        page_tables = []
        with pdfplumber.open(self.file_path, password=pdf_pwd) as pdf_reader:
            for page_id, page in enumerate(tqdm(pdf_reader.pages)):
                page_tables.append((page_id, page.extract_tables()))
        return page_tables


    def pdf2docx(self,
                 docx_file: str,
                 pdf_pwd: str = None,
                 start: int = 0,
                 end: int = None,
                 pages: List = None
                 ):

        converter = Converter(self.file_path, pdf_pwd)
        converter.convert(docx_file, start, end, pages)

