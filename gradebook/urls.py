from os import path

from django.urls import include
from rest_framework.routers import DefaultRouter

from gradebook.views import LecturerViewSet, ClassViewSet, index

router = DefaultRouter()
router.register('lecturer', LecturerViewSet, "lecturer")
router.register('class', ClassViewSet, "class")
router.register('course', ClassViewSet, "course")
router.register('semester', ClassViewSet, "semester")
router.register('student', ClassViewSet, "student")
router.register('studentEnrolment', ClassViewSet, "studentEnrolment")
urlpatterns = router.urls



