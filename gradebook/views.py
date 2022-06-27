from django.shortcuts import render
from django.http import HttpResponse
from django.urls  import reverse_lazy

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from gradebook.models import Lecturer, Class, Course, Semester, Student, StudentEnrolment
from gradebook.serializers import LecturerSerializer, ClassSerializer, CourseSerializer, StudentSerializer, StudentEnrolmentSerializer


def index(request):
    context = {'title': 'Gradebook Home', 'content': 'Welcome to the Gradebook'}
    return render(request, 'index.html', context)


def updateSemesterForm(request, id):
    semester = Semester.objects.get(id=id)
    context = {'semester': semester}
    return render(request, "update_semester.html", context)


def createSemesterForm(request, id):
    semester = Semester.objects.get(id=id)
    context = {'semester': semester}
    return render(request, "update_semester.html", context)

class ListSemester(ListView):
    model = Semester
    template_name = 'list_semester.html'
    ordering = ['year']


class SemesterDetail(DetailView):
    model = Semester
    template_name = 'semester_detail.html'


class CreateSemester(CreateView):
    model = Semester
    fields = '__all__'
    # form_class = 'CreateSemesterForm'
    template_name = "create_semester.html"


class UpdateSemester(UpdateView):
    model = Semester
    fields = '__all__'
    # form_class = 'UpdateSemesterForm'
    template_name = "update_semester.html"


class DeleteSemester(DeleteView):
    model = Semester
    # form_class = 'DeleteSemesterForm'
    template_name = "delete_semester.html"
    success_url = reverse_lazy("list_semester")


class ListCourse(ListView):
    model = Course
    template_name = 'list_course.html'
    ordering = ['code']


class CourseDetail(DetailView):
    model = Course
    template_name = 'course_detail.html'


class CreateCourse(CreateView):
    model = Course
    fields = '__all__'
    # form_class = 'CreateCourseForm'
    template_name = "create_course.html"


class UpdateCourse(UpdateView):
    model = Course
    fields = '__all__'
    # form_class = 'UpdateCourseForm'
    template_name = "update_course.html"


class DeleteCourse(DeleteView):
    model = Course
    # form_class = 'DeleteCourseForm'
    template_name = "delete_course.html"
    success_url = reverse_lazy("list_course")


class ListClass(ListView):
    model = Class
    template_name = 'list_class.html'


class ClassDetail(DetailView):
    model = Class
    template_name = 'class_detail.html'


class CreateClass(CreateView):
    model = Class
    fields = '__all__'
    # form_class = 'CreateClassForm'
    template_name = "create_class.html"


class UpdateClass(UpdateView):
    model = Class
    fields = '__all__'
    # form_class = 'UpdateClassForm'
    template_name = "update_class.html"


class DeleteClass(DeleteView):
    model = Class
    # form_class = 'DeleteClassForm'
    template_name = "delete_class.html"
    success_url = reverse_lazy("list_class")


class ListLecturer(ListView):
    model = Lecturer
    template_name = 'list_lecturer.html'


class LecturerDetail(DetailView):
    model = Lecturer
    template_name = 'lecturer_detail.html'


class CreateLecturer(CreateView):
    model = Lecturer
    fields = '__all__'
    # form_class = 'CreateLecturerForm'
    template_name = "create_lecturer.html"


class UpdateLecturer(UpdateView):
    model = Lecturer
    fields = '__all__'
    # form_class = 'UpdateLecturerForm'
    template_name = "update_lecturer.html"


class DeleteLecturer(DeleteView):
    model = Lecturer
    # form_class = 'DeleteLecturerForm'
    template_name = "delete_lecturer.html"
    success_url = reverse_lazy("list_lecturer")


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer

    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, IsAdminUser]


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, IsAdminUser]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, IsAdminUser]


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = ClassSerializer

    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, IsAdminUser]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, IsAdminUser]


class StudentEnrolmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrolment.objects.all()
    serializer_class = StudentEnrolmentSerializer

    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_superuser:
            serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        is_lecture = False
        groups = user.groups.all()
        if groups.filter(name='lecturer').exists():
            is_lecture = True
        if user.is_superuser or is_lecture:
            serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            studentenrollments = StudentEnrolment.objects.all()
            return studentenrollments
        is_lecture = False
        groups = user.groups.all()
        if groups.filter(name='lecturer').exists():
            is_lecture = True
        if is_lecture:
        # 1. lecture's class
            lectureclasses = Class.objects.filter(Lecturer__User=user)

            enrollments = []
            for lectureclass in lectureclasses:
                classenrollments = StudentEnrolment.objects.filter(Class_id=lectureclass.id)
                enrollments += classenrollments
            return enrollments

        # 2. enrollments of this class
        # 3. list all enrollments in this class out
        is_student = False
        groups = user.groups.all()
        if groups.filter(name='student').exists():
            is_student = True
        if is_student:
            #filter out the results belongs to the student
            #print(user)
            #groups = user.groups.all()

            studentenrollments = StudentEnrolment.objects.filter(Student_id = user.id)
            return studentenrollments



    # filter out the results belongs to the student











