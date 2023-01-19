"""Controllers of the model"""
from datetime import date

from own_framework.templator import render
from all_patterns.creational import Engine, Logger
from all_patterns.structural import Router, Debug
from all_patterns.behavioral import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer
from architectural_system_pattern_unit_of_work import UnitOfWork

site = Engine()
logger = Logger('common')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

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
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course(course_kind, name, category)

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

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

            nc = site.create_category(name)
            site.categories.append(nc)

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


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug()
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
