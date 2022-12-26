"""Controllers of the model"""
from datetime import date

from own_framework.templator import render
from all_patterns.creational import Engine, Logger

site = Engine()
logger = Logger('common')


class Index:
    def __call__(self, request, *args, **kwargs):
        return '200 OK', render('index.html',
                                title='Главная страница',
                                objects=site.categories
                                ), 'text/html'


class StudyPrograms:
    def __call__(self, request, *args, **kwargs):
        return '200 OK', render('study-programs.html',
                                title='Учебные программы',
                                date=date.today()
                                ), 'text/html'


class NotFound404:
    def __call__(self, request):
        return '404 Not Found', render('404.html',
                                       title='Страница не найдена'
                                       ), 'text/html'


class CourseList:
    def __call__(self, request):
        logger.log('COURSE LIST ASKED')

        cat = request.get('request_params').get('given_id')
        if cat:
            cat = int(cat)
            category = site.find_category_by_id(cat)
            return '200 OK', render('course-list.html',
                                    title='Список курсов',
                                    objects=category.courses,
                                    name=category.name,
                                    given_id=category.id
                                    ), 'text/html'
        return '200 OK', 'No courses have been found', 'text/html'


class CategoryList:
    def __call__(self):
        logger.log('List of categories asked')
        return '200 OK', render('category-list.html',
                                title='Список категорий',
                                objects=site.categories), 'text/html'


class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('recorded', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id,
                                    title='Список курсов'), 'text/html'

        else:
            self.category_id = int(request.get('request_params').get('id'))
            if self.category_id and self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id,
                                        title='Создать курс'), 'text/html'

            return '200 OK', 'No categories have been found', 'text/html'


class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html',
                                    objects_list=site.categories,
                                    title='Главная страница'), 'text/html'
        else:
            categories = site.categories
            return '200 OK', render('create-category.html',
                                    categories=categories,
                                    title='Создать категорию'), 'text/html'


class CopyCourse:
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
                site.courses.append(new_course)

            return '200 OK', render('course_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name), 'text/html'
        except KeyError:
            return '200 OK', 'No courses have been found', 'text/html'


class Css:
    def __call__(self, request):
        return '200 OK', render('/style/style.css'), 'text/css'
