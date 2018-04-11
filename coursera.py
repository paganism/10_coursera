import requests
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
import argparse
import os


def get_courses_list(record_count):
    xml = requests.get(
        "https://www.coursera.org/sitemap~www~courses.xml"
    ).content
    root = etree.fromstring(xml)
    url_list = []
    for element in root.getchildren():
        for i in element.getchildren():
            url_list.append(i.text)
    return url_list[:record_count]


def get_course_info(course):
    course_info = []
    html_content = requests.get(course).content
    soup = BeautifulSoup(html_content, 'html.parser')
    try:
        course_info.append(soup.find_all('h2')[0].get_text())
    except IndexError:
        course_info.append("No name yet")
    try:
        course_info.append(soup.find_all('div', 'rc-Language')[0].get_text())
    except IndexError:
        course_info.append("No Lang yet")
    try:
        course_info.append(soup.find_all(
            'div', 'rc-StartDateString'
        )[0].get_text())
    except IndexError:
        course_info.append("No Date yet")
    try:
        course_info.append(soup.find_all('div', 'rc-BasicInfo')[0].get_text())
    except:
        course_info.append("No Info yet")
    try:
        course_info.append(soup.find_all('div', 'ratings-text')[0].get_text())
    except IndexError:
        course_info.append("No rating yet")
    return course_info


def output_courses_info_to_xlsx(course_info, filepath):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Coursera courses info'
    ws['A1'] = 'Course Title'
    ws['B1'] = 'Language'
    ws['C1'] = 'Start Date'
    ws['D1'] = 'Continouation'
    ws['E1'] = 'Rating'
    for each in course_info:
        ws.append(each)
    wb.save(filepath)


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        dest='path',
        required=True,
        help='Path to file'
    )
    return parser.parse_args()


if __name__ == "__main__":
    record_count = 20
    url_list = get_courses_list(record_count)
    course_list = []
    arg = parse_argument()
    filepath = arg.path
    for each_course in url_list:
        info = get_course_info(each_course)
        course_list.append(info)
    output_courses_info_to_xlsx(course_list, filepath)
