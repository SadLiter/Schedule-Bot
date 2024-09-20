import pdfplumber
import pandas as pd
import requests
import re

def split_and_invert(text):
    if text is None or not isinstance(text, str):
        return text

    return text[::-1]

def invert_numbers(text):
    if text is None or not isinstance(text, str):
        return text
    
    match = re.match(r'(\d+)', text)
    if match:
        number_part = match.group(1)
        inverted_number_part = number_part[::-1]
        return inverted_number_part
    return text

def pdf_to_excel(pdf_path, excel_path):
    """
    Конвертирует PDF в Excel, исправляя опечатки/пропуски
    или случайные переносы строки в исходном файле.
    """
    correction_dict = {
        'паIр а': 'пара I',
        'паIIр а': 'пара II',
        'паIрI а': 'пара II',
        'IIIпара': 'пара III',
        'III\nпара': 'пара III',
        'пIаIрIа': 'пара III',
        'пIаVр а': 'пара IV',
        'пIаVра': 'пара IV',
        'паVр а': 'пара V',
        'пVарIа': 'пара VI',
        'пVаIрIа': 'пара VII',
        'пVарIIа': 'пара VII',
        'пVаIрIаI': 'пара VIII',
        'ырап№': 'пара №',
        'енибакт': 'кабинет',
        'тенибак': 'кабинет',
        'акдащолп.тропс': 'спорт.площадка',
        '.тропсакдащолп': 'спорт.площадка',
        '.тропс': 'спорт.площадка',
        'акдащолп\n.тропс': 'спорт.площадка',
        'ямерв': 'время'
    }

    with pdfplumber.open(pdf_path) as pdf:
        all_data = []

        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                for row in table:
                    corrected_row = []
                    
                    for col_idx, cell in enumerate(row):
                        if isinstance(cell, str):
                            cell = correction_dict.get(cell, cell)
                            
                            if col_idx == 0:
                                cell = split_and_invert(cell)
                            
                            elif col_idx >= 4 and (col_idx - 4) % 2 == 0:
                                cell = invert_numbers(cell)
                            
                        corrected_row.append(cell)
                    all_data.append(corrected_row)

    df = pd.DataFrame(all_data)

    df.at[24, 0] = 'СРЕДА'

    df.to_excel(excel_path, index=False, header=False)

    print(f"PDF успешно конвертирован в {excel_path}")

def download_pdf(url, save_path):
    """
    Скачивает PDF-файл с указанного URL и сохраняет его на диск.

    :param url: URL PDF-файла
    :param save_path: Путь для сохранения файла (включая имя и расширение .pdf)
    """
    try:
        response = requests.get(url)
        response.raise_for_status() 
        
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        print(f'PDF файл успешно скачан и сохранен по адресу: {save_path}')
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при скачивании PDF файла: {e}')
