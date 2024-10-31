from rest_framework.routers import DefaultRouter
from .views import MyCartViewSet,MyCourseViewSet,MyProfileViewSet
from django.urls import path ,include

router = DefaultRouter()
router.register(r'my-cart',MyCartViewSet,basename='my-cart')
router.register(r'my-courses',MyCourseViewSet,basename='my-courses')
router.register(r'',MyProfileViewSet,basename='my-profile')

custom_urls = [
    path('my-courses/add/<int:course_id>/', MyCourseViewSet.as_view({'post': 'add_to_my_courses'}), name='add-to-my-courses'),
    path('my-cart/add/<int:course_id>/', MyCartViewSet.as_view({'post': 'add_to_cart'}), name='add-to-cart'),
]
urlpatterns = [
    path('',include(router.urls)),
    path('',include(custom_urls))
]