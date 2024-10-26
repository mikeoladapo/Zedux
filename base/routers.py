from rest_framework.routers import DefaultRouter
from .views import CustomUserViewset

router = DefaultRouter()
router.register(r"users",CustomUserViewset,basename="users")
urlpatterns = router.urls 