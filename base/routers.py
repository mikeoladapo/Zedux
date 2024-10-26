from rest_framework.routers import DefaultRouter
from .views import CustomUserViewset,InstructorViewset

router = DefaultRouter()
router.register(r"users",CustomUserViewset,basename="custom-users")
router.register(r"instructors",InstructorViewset,basename="instructors")
urlpatterns = router.urls 