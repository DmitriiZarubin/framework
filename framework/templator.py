from jinja2 import Template
import os


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: название шаблона
    :param folder: каталог для поиска шаблона
    :param kwargs: аргументы
    :return:
    """
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
