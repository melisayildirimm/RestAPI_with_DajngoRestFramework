from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from . import views
#from .views import list_users
from rest_framework.routers import DefaultRouter


"""router = DefaultRouter()
router.include_format_suffixes = False
router.register('user', views.userInfoViewSet, basename='user')"""


urlpatterns = [
    #path('users/', views.list_users),
    path('users/', views.userInfoList.as_view()),
    #path('users/<int:pk>/', views.user_detail),
    path('users-detail/<int:id>', views.userInfoDetail.as_view()),
    #path('generic/users/<int:id>/', views.GenericAPIView.as_view()),
    #path('viewset/', include(router.urls)),
    #path('viewset/<int:pk>/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', obtain_auth_token, name='obtain-token'),
    #path('users/<str:content_type>/', views.ListItem.as_view()),
    path('users-listitems/emails/', views.FetchEmailsView.as_view()),
    path('users-filter/<str:data>/', views.Filter.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
