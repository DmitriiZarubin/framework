from datetime import date
from views import Index, About, Contact, \
    StudyPrograms, CoursesList, \
    CreateCourse, CreateCategory, CategoryList, CopyCourse


def date_front(request):
    request['date'] = date.today()


fronts = [date_front]

# routes = {
#     '/': Index(),
#     '/about/': About(),
#     '/contact/': Contact(),
#     '/study_programs/': StudyPrograms(),
#     '/courses-list/': CoursesList(),
#     '/create-course/': CreateCourse(),
#     '/create-category/': CreateCategory(),
#     '/category-list/': CategoryList(),
#     '/copy-course/': CopyCourse()
# }
