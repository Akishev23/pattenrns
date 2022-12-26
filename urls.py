from datetime import date

from views import Index, StudyPrograms, CourseList, CategoryList, CreateCourse, \
    CreateCategory, CopyCourse, Css


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/course-list/': CourseList(),
    '/study-programs/': StudyPrograms(),
    '/category-list/': CategoryList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/copy-course/': CopyCourse(),
    '/css/': Css(),
}
