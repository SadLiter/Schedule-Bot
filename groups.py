import pandas as pd
import re
from convert import pdf_to_excel, download_pdf


download_pdf('http://www.krstc.ru/files/raspis/s1', 'files/testpd.pdf')
pdf_to_excel('files/testpd.pdf', 'files/testxl.xlsx')

df = pd.read_excel("files/testxl.xlsx", sheet_name="Sheet1", header=None)

def get_student_groups(df):
    number = 3
    student_groups = {}
    first_row = df.iloc[0]
    for line in first_row:
        if re.search(r'\d{2}К$', str(line)):
            line = line.upper()
            student_groups[line] = number
            number += 2

    return student_groups

student_groups = get_student_groups(df)

def get_schedule(df, student_group, today_day):
    offset = 11
    week = {'пн': offset*0, 'вт': offset*1, 'ср': offset*2, 'чт': offset*3, 'пт': offset*4}
    format_week = {'пн': 'понедельник', 'вт': 'вторник', 'ср': 'среда', 'чт': 'четверг', 'пт': 'пятница'}

    j = student_groups[student_group]
    i = 3 # начальное значение индекса
    data = []
    corp = df[j][i+week[today_day]-1]

    while i < (len(df)+2):
        key = df[2][i+week[today_day]]
        value = df[j][i+week[today_day]]
        cab = df[j+1][i+week[today_day]]
        day = today_day
        group = student_group
        
        key = '' if pd.isna(key) else key
        value = '' if pd.isna(value) else value
        cab = '' if pd.isna(cab) else cab

        if (not key or not value or not cab) and data:
            break

        if isinstance(key, str):
            key = re.sub(r'-(\s*)\n', '-', key)
        if isinstance(value, str):
            value = value.replace('\n', ' ')
        if isinstance(cab, str):
            cab = cab.replace('\n', ' ')
        
        if key and value and cab:
            data.append([key, value, cab])
        
        i += 1 

    result = "\n".join(f"🎓{row[0]}: {row[1]}: каб. {row[2]}" for row in data)
    result = f'  {group}\n{format_week[day]}\n{corp}\n\n{result}'

    return result
