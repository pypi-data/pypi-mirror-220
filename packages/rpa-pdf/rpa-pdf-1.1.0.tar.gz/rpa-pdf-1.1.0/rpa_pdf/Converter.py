
import os
import subprocess
import warnings
from PIL import Image
from fpdf import FPDF
import pdfkit
from .common import parse_output_file_path

class Converter:
    def __init__(self):
        self.__root_dir__: str = os.path.dirname(os.path.abspath(__file__))
        self.__fonts_dir__: str = os.path.join(self.__root_dir__, 'fonts')
        self.__exec_dir__: str = os.path.join(self.__root_dir__, 'exec')

    def convert(self, input_file_path: str, output_file_path: str | None = None, index: int | None = None):
        """ Converts files to the pdf format

        Args:
            input_file_path (str): full path of the input file
            output_file_path (str | None, optional): full path of the output file. Defaults to None.
            index (int | None, optional): index which will be added at the beginning of the file name. Defaults to None.
        """

        if os.path.exists(input_file_path) is False:
            raise FileNotFoundError(f'{input_file_path} does not exist')

        directory, filename = os.path.split(parse_output_file_path(input_file_path, output_file_path))
        filename_parts = os.path.splitext(filename)

        new_filename = f"{index}_{filename_parts[0]}{filename_parts[1]}"
        output_file_path = os.path.join(directory, new_filename)

        if os.path.exists(output_file_path) is True:
            os.remove(output_file_path)


        match os.path.splitext(input_file_path)[1]:
            case '.doc' | '.docx' | '.rtf' | '.txt' | '.csv':
                self.word_to_pdf(input_file_path, output_file_path)
            case '.xls' | '.xlsx' | '.xlsm':
                self.excel_to_pdf(input_file_path, output_file_path)
            case '.ppt' | '.pptx' | '.pptm' | '.ppsx':
                self.powerpoint_to_pdf(input_file_path, output_file_path)
            case '.png' | '.jpg' | '.jpeg' | '.gif' | '.tiff' | '.bmp' | '.tif':
                self.image_to_pdf(input_file_path, output_file_path)
            case '.msg' | '.eml':
                self.email_to_pdf(input_file_path, output_file_path)
            case '.html' | '.htm':
                self.html_to_pdf(input_file_path, output_file_path)
            case _:
                warnings.warn(f'[Not Implemented] {input_file_path} - cannot convert {os.path.splitext(input_file_path)[1]} file;')
                return False

    def image_to_pdf(self, input_file_path: str, output_file_path: str | None = None):
        """
        Converts image to pdf.

        Args:
            input_file_path (str): full path of image file
            output_file_path (str): output pdf file path
        """
        try:
            image = Image.open(input_file_path)
            image = image.convert('RGB')
            image.save(output_file_path)
        except (ValueError, OSError, Exception) as ex:
            raise ex

    def word_to_pdf(self, input_file_path: str, output_file_path: str | None = None):
        """
        Converts MS Word documents to pdf.

        Args:
            input_file_path (str): full path of MS Word file
            output_file_path (str): output pdf file path
        """
        converter_path = os.path.join(self.__exec_dir__, 'docto.exe')
        parameters = f'-f "{input_file_path}" -O "{output_file_path}" -T wdFormatPDF'

        try:
            subprocess.run(f'{converter_path} {parameters}', check=True)
        except subprocess.CalledProcessError as ex:
            raise ex

    def excel_to_pdf(self, input_file_path: str, output_file_path: str | None = None):
        """
        Converts MS Excel documents to pdf.

        Args:
            input_file_path (str): full path of MS Excel file
            output_file_path (str): output pdf file path

        """
        converter_path = os.path.join(self.__exec_dir__, 'docto.exe')
        parameters = f'-XL -f "{input_file_path}" -O "{output_file_path}" -T xlpdf'

        try:
            subprocess.run(f'{converter_path} {parameters}', check=True)
        except subprocess.CalledProcessError as ex:
            raise ex

    def powerpoint_to_pdf(self, input_file_path: str, output_file_path: str | None = None):
        """
        Converts MS PowerPoint documents to pdf.

        Args:
            input_file_path (str): full path of MS PowerPoint file
            output_file_path (str): output pdf file path

        """
        converter_path = os.path.join(self.__exec_dir__, 'docto.exe')
        parameters = f'-PP -f "{input_file_path}" -O "{output_file_path}" -T ppSaveAsPDF'

        try:
            subprocess.run(f'{converter_path} {parameters}', check=True)
        except subprocess.CalledProcessError as ex:
            raise ex

    def html_to_pdf(self, input_file_path: str, output_file_path: str | None = None):
        """ Converts HTML files to PDF

        Args:
            input_file_path (str): full path of the HTML/HTM file
            output_file_path (str | None, optional): full path of the output file. Defaults to None.
        """
        config = pdfkit.configuration(wkhtmltopdf=os.path.join(self.__exec_dir__, 'wkhtmltox/bin/wkhtmltopdf.exe'))

        try:
            pdfkit.from_file(input_file_path, output_file_path, configuration=config)
        except Exception as ex:
            raise ex

    def txt_to_pdf(self, input_file_path: str, output_file_path: str | None = None):
        """ Converts plain text files to PDF

        Args:
            input_file_path (str): full path of the input file
            output_file_path (str | None, optional): full path of the output file. Defaults to None.
        """
        try:
            with open(input_file_path, 'r', encoding='utf-8') as txt_file:
                text_content = txt_file.read()

            pdf = FPDF()

            pdf.add_page()

            pdf.add_font('Dejavu Sans', '', f'{self.__fonts_dir__}\\DejaVuSans.ttf', True)
            pdf.set_font(family='Dejavu Sans', style='', size=12)

            pdf.multi_cell(0,10, txt=text_content)

            pdf.output(output_file_path)

        except Exception as ex:
            raise ex

    def email_to_pdf(self, input_file_path: str, output_file_path: str | None = None):
        """ Converts email files to PDF

        Args:
            input_file_path (str): full path of the input file
            output_file_path (str | None, optional): full path of the output file. Defaults to None.
        """
        converter_path = os.path.join(self.__exec_dir__, 'EmailConverterConsole.exe')
        parameters = f'"{input_file_path}" -o "{output_file_path}"'

        try:
            subprocess.run(f'{converter_path} {parameters}', check=True)
        except subprocess.CalledProcessError as ex:
            raise ex
