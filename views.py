"""Controllers of the model"""
from datetime import date

from own_framework.templator import render
from all_patterns.creational import Engine, Logger
from all_patterns.structural import Router, Debug

site = Engine()
logger = Logger('common')

routs = {}


@Router(routs, '/')
class Index:
    @Debug()
    def __call__(self, request, *args, **kwargs):
        return '200 OK', render('index.html',
                                title='Главная страница',
                                objects=site.categories,
                                count=site.cat_count
                                ), 'text/html'


@Router(routs)
class StudyPrograms:
    @Debug()
    def __call__(self, request, *args, **kwargs):
        return '200 OK', render('study-programs.html',
                                title='Учебные программы',
                                date=date.today()
                                ), 'text/html'


class NotFound404:
    @Debug()
    def __call__(self, request):
        return '404 Not Found', render('404.html',
                                       title='Страница не найдена'
                                       ), 'text/html'


@Router(routs)
class CourseList:
    @Debug()
    def __call__(self, request):
        logger.log('COURSE LIST ASKED')
        return '200 OK', render('course-list.html',
                                title='Список курсов',
                                objects=site.courses,
                                ), 'text/html'


@Router(routs)
class CategoryList:
    @Debug()
    def __call__(self, request):
        logger.log('List of categories asked')
        return '200 OK', render('category-list.html',
                                title='Список категорий',
                                objects=site.categories,
                                counts=site.cat_count
                                ), 'text/html'


@Router(routs)
class CreateCourse:
    category_id = -1

    @Debug()
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data.get('name')
            name = site.decode_value(name)
            try:
                cat_id = int(data.get('cat'))
            except TypeError:
                pass
            else:
                self.category_id = cat_id
            course_kind = data.get('kind')
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                site.create_course(course_kind, name, category)

            return '200 OK', render('course-list.html',
                                    objects=site.courses,
                                    title='Список доступных курсов'), 'text/html'

        else:

            return '200 OK', render('create-course-without-category.html',
                                    names=site.categories,
                                    title='Создать курс'), 'text/html'


@Router(routs)
class CreateCategory:
    @Debug()
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            site.create_category(name)

            return '200 OK', render('index.html',
                                    objects=site.categories,
                                    count=site.cat_count,
                                    title='Главная страница'), 'text/html'
        else:
            categories = site.categories
            return '200 OK', render('create-category.html',
                                    categories=categories,
                                    title='Создать категорию'), 'text/html'


@Router(routs)
class CopyCourse:
    @Debug()
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_of_{name}'
                old_course_kind = old_course.__class__.__name__.strip('Course').lower()
                new_course = site.create_course(old_course_kind, new_name,
                                                old_course.category)
                new_course.name = new_name

            return '200 OK', render('course-list.html',
                                    objects=site.courses,
                                    title='Список доступных курсов'), 'text/html'
        except KeyError:
            return '200 OK', 'No courses have been found', 'text/html'


@Router(routs)
class Css:
    def __call__(self, request):
        return '200 OK', render('/style/style.css'), 'text/css'
