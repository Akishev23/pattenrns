from os.path import join
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: str, template name
    :param folder: str, template folder
    :param kwargs: kwargs sending to template
    :return:
    """
    file_path = join(folder, template_name)
    with open(file_path, encoding='cp1251') as f:
        template = Template(f.read())
    return template.render(**kwargs)
