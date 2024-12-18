from rest_framework.routers import DefaultRouter
from .views import CustomUserViewset,InstructorViewset,CourseViewset,CategoryViewset,CourseMaterialViewset,LoginViewset

router = DefaultRouter()
router.register(r"users",CustomUserViewset,basename="custom-users")
router.register(r"instructors",InstructorViewset,basename="instructors")
router.register(r"courses",CourseViewset,basename="courses")
router.register(r"categories",CategoryViewset,basename="categories")
router.register(r"course-materials",CourseMaterialViewset,basename="course-materials")
router.register(r"auth",LoginViewset,basename="auth")
urlpatterns = router.urls 