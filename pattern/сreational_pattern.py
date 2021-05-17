import copy
import quopri
from pattern.behavior_pattern import ConsoleWriter, Subject


class User:
    """
    абстрактный класс пользователь
    """

    def __init__(self, name):
        self.name = name


class Teacher(User):
    """
    класс преподаватель
    """
    pass


class Student(User):
    def __init__(self, name):
        """
        класс студент
        """
        self.courses = []
        super().__init__(name)


class UserFactory:
    """
    порождающий паттерн Абстрактная фабрика - фабрика пользователей
    """
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class CoursePrototype:
    """
    порождающий паттерн Прототип - Курс
    """

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype, Subject):
    """
    класс курс
    """

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        """
        Добавление студента на курс
        :param student:
        """
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    """
    класс Интерактивный курс
    """
    pass


class RecordCourse(Course):
    """
    класс Курс в записи
    """
    pass


class Category:
    """
    класс Категории
    """
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


class CourseFactory:
    """
    порождающий паттерн Абстрактная фабрика - фабрика курсов
    """
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Engine:
    """
    класс - Основной интерфейс проекта
    """

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, category_id):
        for item in self.categories:
            print('item', item.id)
            if item.id == category_id:
                return item
        raise Exception(f'Нет категории с id = {category_id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    """
    порождающий паттерн Синглтон
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    """
    класс - логирование
    """

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
