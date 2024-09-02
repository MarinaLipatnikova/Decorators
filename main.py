import datetime
import os


def logger(old_function):

    def new_function(*args, **kwargs):
        with open('main.log', 'a', encoding='utf-8') as file:
            file.write(
                f'{datetime.datetime.now()}: отработала функция {old_function.__name__} с аргументами {args}, {kwargs}. Функция возвращает: {(old_function(*args, **kwargs))}\n')
            file.close()
            result = old_function(*args, **kwargs)
        return result
    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()


def logger2(path):

    def __logger(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'a', encoding='utf-8') as file:
                file.write(
                    f'{datetime.datetime.now()}: отработала функция {old_function.__name__} с аргументами {args}, {kwargs}. Функция возвращает: {(old_function(*args, **kwargs))}\n')
                file.close()
                result = old_function(*args, **kwargs)

            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger2(path)
        def hello_world():
            return 'Hello World'

        @logger2(path)
        def summator(a, b=0):
            return a + b

        @logger2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()



class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.main_cursor = 0
        self.cursor = 0
        return self

    def __next__(self):

        if len(self.list_of_list) <= self.main_cursor:
            raise StopIteration

        item = self.list_of_list[self.main_cursor][self.cursor]
        self.cursor += 1

        if len(self.list_of_list[self.main_cursor]) == self.cursor:
            self.main_cursor += 1
            self.cursor = 0

        return item


def test_3():
    path = ('log_iter.log')
    if os.path.exists(path):
        os.remove(path)

    @logger2(path)
    def list_of_lists(l):
        return FlatIterator(l).list_of_list

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    list_of_lists(list_of_lists_1)


if __name__ == '__main__':
    test_3()