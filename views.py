"""Controllers of the model"""
from own_framework.templator import render


class Index:
    def __call__(self):
        return '200 OK', render('index.html', title='Главная страница')


class Contact:
    def __call__(self):
        return '200 OK', render('contact.html', title='Контакты')


class Page:
    def __call__(self):
        return '200 OK', render('page.html', title='Пример страницы')


class Examples:
    def __call__(self):
        return '200 OK', render('examples.html', title='Примеры контента')


class AnotherPage:
    def __call__(self):
        return '200 OK', render('another_page.html', title='Еще одна страница')


class Css:
    def __call__(self):
        return '200 OK', render('/style/style.css', title='Пример страницы')
