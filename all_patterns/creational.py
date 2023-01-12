from copy import deepcopy
from quopri import decodestring
import enum

from behavioral import PropertyObservable, Subject


class User:
    def __init__(self, name):
        self.name = name


class Tutor(User):
    pass


class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    pass


class StudentFactory(UserFactory, PropertyObservable):

    def __init__(self):
        super().__init__()

    def create(self, name):
        if name:
            return Student(name)


class TutorFactory(UserFactory):
    @staticmethod
    def create(name):
        return Tutor(name)


class UserMachine:
    class AvailableKindsOfUsers(enum.Enum):
        TUTOR = 1
        STUDENT = 2

    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
        for u in self.AvailableKindsOfUsers:
            user_def = u.name.capitalize()
            factory_name = user_def + "Factory"
            factory_instance = eval(factory_name)()
            self.factories.append((user_def, factory_instance))

    @staticmethod
    def create_user(kind, name):
        factory = [i[1] for i in UserMachine.factories if kind.capitalize() == i[0]][0]
        return factory.create(name)


class Course(Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    pass


class RecordedCourse(Course):
    pass


class CourseFactory:
    interactive_course_proto = InteractiveCourse('base_of_python', 'python')
    recorded_course_proto = RecordedCourse('english for programmers', 'others')

    @staticmethod
    def __new_course(proto, name, category):
        new_course = deepcopy(proto)
        new_course.name = name
        new_course.category = category
        return new_course

    @staticmethod
    def _new_interactive_course(name, category):
        return CourseFactory.__new_course(CourseFactory.interactive_course_proto, name, category)

    @staticmethod
    def _new_recorded_course(name, category):
        return CourseFactory.__new_course(CourseFactory.recorded_course_proto, name, category)

    @staticmethod
    def create_course(kind, name, category):
        return eval(f'CourseFactory._new_{kind}_course')(name, category)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Engine:

    def __init__(self):
        self.tutors = []
        self.students = []
        self.courses = []
        self.categories = []
        self.cat_count = {}

    def create_user(self, kind, name):
        usr = UserMachine()
        if kind == 'tutor':
            self.tutors.append(usr)
        else:
            self.students.append(usr)
        return usr.create_user(kind, name)

    def create_category(self, name, category=None):
        cat = Category(name, category)
        self.categories.append(cat)
        self.cat_count[cat] = 0
        return cat

    def find_category_by_id(self, given_id):
        for item in self.categories:
            if item.id == given_id:
                return item
        raise Exception(f'there is no category with given id {given_id}')

    def create_course(self, kind, name, category):
        course = CourseFactory.create_course(kind, name, category)
        self.courses.append(course)
        if not self.categories.count(category):
            self.categories.append(category)
        try:
            self.cat_count[category] += 1
        except KeyError:
            self.cat_count[category] = 1
        return course

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        raise Exception(f'there is no course with name {name}')

    def course_count(self, cat_name):
        return self.cat_count[cat_name]

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class Logger:

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print(self.name, 'log------->', text)
