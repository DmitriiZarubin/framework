import copy
import quopri


class User:
    """
    абстрактный класс пользователь
    """
    pass


class Teacher(User):
    """
    класс преподаватель
    """
    pass


class Student(User):
    """
    класс студент
    """
    pass


class UserFactory:
    """
    порождающий паттерн Абстрактная фабрика - фабрика пользователей
    """
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class CoursePrototype:
    """
    порождающий паттерн Прототип - Курс
    """

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):
    """
    класс курс
    """

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


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
    def create_user(type_):
        return UserFactory.create(type_)

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

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

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

    def __init__(self, name):
        self.name = name

    def log(self, text):
        with open(self.name, 'a') as f:
            f.write(text)
            f.write('\n')

