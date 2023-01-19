from jsonpickle import dumps, loads
from enum import Enum, auto

from own_framework.templator import render


class Observer:

    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print(f'SMS ---> we are glad to invite a new student {subject.students[1].name}')


class EmailNotifier(Observer):

    def update(self, subject):
        print(f'Email ---> we are glad to invite a new student {subject.students[1].name}')


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        if 'css' not in template_name:
            mime = 'text/html'
        else:
            mime = 'text/css'
        return '200 OK', render(template_name, **context), mime

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


class ConsoleWriter:
    @staticmethod
    def write(text):
        print(text)


class OutputFormat(Enum):
    FILE = auto()
    CONSOLE = auto()


class WriteStrategy(ABC):
    @staticmethod
    def write(text):
        pass


class ConsoleWriteStrategy(WriteStrategy):
    @staticmethod
    def write(text):
        print(text)


class FileWriteStrategy(WriteStrategy):
    @staticmethod
    def write(text):
        with open('log.log', 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')


class TextProcessor:
    def __init__(self, write_strategy=ConsoleWriteStrategy):
        self.write_strategy = write_strategy

    def set_output_format(self, output_format):
        if output_format == OutputFormat.CONSOLE:
            self.write_strategy = ConsoleWriteStrategy()
        elif output_format == OutputFormat.FILE:
            self.write_strategy = FileWriteStrategy(path='log.log')

    def write(self, info):
        self.write_strategy.write(info)
