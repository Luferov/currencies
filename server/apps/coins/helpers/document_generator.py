"""Модуль генератора документа."""
import subprocess
import zipfile
from datetime import datetime
from os import makedirs, remove
from os.path import exists, join, relpath
from pathlib import PosixPath
from typing import NamedTuple, Optional

from django.conf import settings
from django.template import Context, Template


def get_tmp_document_name() -> str:
    """Получение названия документа, указывающего на временный документ.

    :return: название документа
    """
    return f'document_{datetime.strftime(datetime.now(), "%H-%M-%d-%m-%Y")}_tmp'


class DocumentGeneratorException(Exception): # noqa N818
    """Исключение генератора документа."""

    pass


class DocumentData(NamedTuple):
    """Данные документа."""

    name: str       # Название
    path: str       # Путь к файлу относительно storage
    full_path: str  # Полный путь к файлу


class DocumentGenerator:
    """Генератор документа."""

    def __init__(self, context: Context, template_xml: PosixPath | str, template_docx: PosixPath | str) -> None:
        """Конструктор генератора документа.

        :param context: контекст
        :param template_xml: файл шаблона xml
        :param template_docx: файл шаблона docx
        """
        self.context = context
        self.template_xml = template_xml
        self.template_docx = template_docx
        self.docx_document: Optional[DocumentData] = None

    @staticmethod
    def get_document_name() -> str:
        """Получение названия документа.

        :return: название документа
        """
        return get_tmp_document_name()

    def generate_docx(self, documents_dir: str = settings.DOCUMENTS_DIR) -> DocumentData:
        """Генерация документа docx.

        :param documents_dir: абсолютный путь к директории, в которой необходимо создавать документ.
        :return: данные сгенерированного документа
        """
        with open(self.template_xml) as file:
            template = Template(file.read())
        renderer_template = template.render(self.context)
        document_name = self.get_document_name()
        document_full_path = join(documents_dir, f'{document_name}.docx')
        if not exists(documents_dir):
            makedirs(documents_dir)
        with zipfile.ZipFile(self.template_docx, 'r') as source_zip_file, \
             zipfile.ZipFile(document_full_path, 'w') as target_zip_file:
            for zip_info in source_zip_file.infolist():
                if zip_info.filename == 'word/document.xml':
                    target_zip_file.writestr(zip_info, renderer_template)
                else:
                    target_zip_file.writestr(zip_info, source_zip_file.read(zip_info.filename))
        self.docx_document = DocumentData(
            name=document_name,
            path=join(relpath(documents_dir, settings.BASE_DIR), f'{document_name}.docx'),
            full_path=document_full_path,
        )
        return self.docx_document

    def generate_pdf(
            self,
            remove_docx: bool = False,
            pdf_documents_dir: str = settings.DOCUMENTS_DIR,
            docx_document_dir: str = settings.DOCUMENTS_DIR
    ) -> DocumentData:
        """Генерация документа pdf.

        :param pdf_documents_dir: абсолютный путь к директории, в которой необходимо создавать pdf документ
        :param docx_document_dir: абсолютный путь к директории, в которой необходимо создавать docx документ
        :param remove_docx: удалять документ docx после создания pdf документа
        :return: данные сгенерированного документа
        """
        if self.docx_document is None:
            self.generate_docx(docx_document_dir)
        result_code = subprocess.call(
            [
                'libreoffice',
                '--headless',
                '--convert-to',
                'pdf',
                self.docx_document.full_path
            ],
            cwd=pdf_documents_dir,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        try:
            if result_code == 0:
                return DocumentData(
                    name=self.docx_document.name,
                    path=join(relpath(pdf_documents_dir, settings.BASE_DIR), f'{self.docx_document.name}.pdf'),
                    full_path=join(pdf_documents_dir, f'{self.docx_document.name}.pdf')
                )
            else:
                raise DocumentGeneratorException(
                    f'Не удалось сформировать pdf документ. LibreOffice вернул код {result_code}'
                )
        finally:
            if remove_docx:
                remove(self.docx_document.full_path)
                self.docx_document = None


__all__ = [
    'DocumentData',
    'DocumentGenerator'
]
