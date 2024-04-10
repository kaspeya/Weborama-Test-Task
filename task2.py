import fileinput
import os.path

from bs4 import BeautifulSoup
from ebooklib import epub

BOOK_REPORT_FIELDS = ['title', 'creator', 'publisher', 'date']


def get_book_metadata_joined(
        book, field_name, scope='DC', delimiter=', ') -> str:

    """Эта функция возвращает строку с соответствующем полем."""

    metadata = book.get_metadata(scope, field_name)
    if not metadata:
        return '<Not mentioned>'
    return delimiter.join([f'{e[0]}' for e in metadata])


def get_epub_report_str(file_path, fields=None,
                        delimiter='\n',
                        epub_read_options=None) -> str:

    """Эта функция получает нужные поля и возвращает строку."""

    if epub_read_options is None:
        epub_read_options = {'ignore_ncx': True}
    if fields is None:
        fields = BOOK_REPORT_FIELDS
    try:
        book = epub.read_epub(file_path, options=epub_read_options)
        # removes warning about future versions
    except epub.EpubException:
        return f'Cannot open epub file: {file_path}'
    except FileNotFoundError:
        return f'Cannot find epub file: {file_path}'

    return delimiter.join([
        f'{field.capitalize()}: {get_book_metadata_joined(book, field)}'
        for field in fields])


def get_fb2_report_str(file_path) -> str:

    """Эта функция получает на входе input с названием файла,
        открывает файл в режиме двоичного чтения,
        парсит данные по тегам и добавляет их в словарь.
    """

    field_dict = {field: [] for field in BOOK_REPORT_FIELDS}

    with open(file_path, 'rb') as file:
        soup = BeautifulSoup(file.read(), 'xml')
        title_info = soup.find('title-info')
        if title_info:
            authors = title_info.find_all('author')
            for author in authors:
                field_dict['creator'].append('')

                if author.find('first-name'):
                    field_dict[
                        'creator'][-1] += author.find('first-name').text + ' '
                if author.find('middle-name'):
                    field_dict[
                        'creator'][-1] += author.find('middle-name').text + ' '
                if author.find('last-name'):
                    field_dict['creator'][-1] += author.find('last-name').text

            titles = title_info.find_all('book-title')

            for title in titles:
                field_dict['title'].append(title.text)

        publish_info = soup.find('publish-info')
        if publish_info:
            publishers = publish_info.find_all('publisher')
            for publisher in publishers:
                field_dict['publisher'].append(publisher.text)

            years = publish_info.find_all('year')
            for year in years:
                field_dict['date'].append(year.text)
    return '\n'.join([f"{k.capitalize()}: {','.join(v)}"
                      for k, v in field_dict.items()])


def get_target_file() -> fileinput:

    """Получение и проверка файла из инпута."""

    user_input = input('Enter file name: ')
    if not os.path.isfile(user_input):
        print(f'Error!\nFile {user_input} not found\n')
    else:
        print(f'\nReading file {user_input}...\n')
    return user_input


def main():
    ins = get_target_file()
    try:
        if ins.endswith('.fb2'):
            print(get_fb2_report_str(ins))
        elif ins.endswith('.epub'):
            print(get_epub_report_str(ins))
    except Exception as e:
        print(f'Cannot parse {ins} file in case of unexpected reason: \n{e}')


if __name__ == '__main__':
    main()

"""Сначала я посмотрела, что из себя изнутри представляют epub и fb2 файлы.
    Если fb2 оказался текстовым, то epub оказался де-факто zip-архивом.
    Я нашла удобную библиотеку ebooklib, которой парсился epub.
    Так как fb2 более простой текстовый формат,
    для парсинга я воспользовалась bs4.

    Для проверки работоспособности программы я протестила по сотне файлов
    каждого типа, причем fb2 файлы имели разные энкодинги.
"""
