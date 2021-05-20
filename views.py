from datetime import date

from framework.templator import render
from pattern.сreational_pattern import Engine, Logger, MapperRegistry
from pattern.struct_pattern import ApplicationRoute, Debug
from pattern.behavior_pattern import EmailNotifier, SmsNotifier, \
    ListView, CreateView, BaseSerializer
from pattern.unit_of_work_pattern import UnitOfWork

site = Engine()
logger = Logger('main_log.txt')
routes = {}
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@ApplicationRoute(routes=routes, url='/')
class Index:
    """
    класс для шаблона index
    """

    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@ApplicationRoute(routes=routes, url='/about/')
class About:
    """
    класс для шаблона about
    """

    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


@ApplicationRoute(routes=routes, url='/contact/')
class Contact:
    """
    класс для шаблона contact
    """

    @Debug(name='contact')
    def __call__(self, request):
        return '200 OK', render('contact.html')


class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@ApplicationRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    """
    класс - Расписание
    """

    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study_programs.html', data=date.today())


@ApplicationRoute(routes=routes, url='/courses-list/')
class CoursesList:
    """
    класс - список курсов
    """

    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@ApplicationRoute(routes=routes, url='/create-course/')
class CreateCourse:
    """
    класс - создание курса
    """
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@ApplicationRoute(routes=routes, url='/create-category/')
class CreateCategory:
    """
    класс - создатькатегорию
    """

    @Debug(name='CreateCategory')
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
                                    objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


@ApplicationRoute(routes=routes, url='/category-list/')
class CategoryList:
    """
    класс - список категорий
    """

    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


@ApplicationRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    """
    класс - копировать курс
    """

    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_course_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_course_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html',
                                    objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@ApplicationRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'stud_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@ApplicationRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_stud.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@ApplicationRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_stud.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        mapper = MapperRegistry.get_current_mapper('student')
        site.students = mapper.all()
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


@ApplicationRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
