from rest_framework.routers import DefaultRouter
from .views import MyCartViewSet,MyCourseViewSet
from django.urls import path ,include

router = DefaultRouter()
router.register(r'my-cart',MyCartViewSet,basename='my-cart')
router.register(r'my-course',MyCourseViewSet,basename='my-course')

custom_urls = [
    path('my-course/add/<int:course_id>/', MyCourseViewSet.as_view({'post': 'add_to_my_course'}), name='add-to-my-course'),
    path('my-cart/add/<int:course_id>/', MyCartViewSet.as_view({'post': 'add_to_cart'}), name='add-to-cart'),
]
urlpatterns = [
    path('',include(router.urls)),
    path('',include(custom_urls))
]