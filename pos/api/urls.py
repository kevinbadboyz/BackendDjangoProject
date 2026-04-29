from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    # Using class APIVIEW
    path('api/table-restos', views.TableRestoListCreateAPIView.as_view()),
    path('api/table-resto-detail/<id>', views.TableRestoDetailAPIView.as_view()),

    # Using generics class
    path('api/v2/table-resto-list', views.TableRestoListAPIView.as_view()),
    path('api/v2/table-resto-create', views.TableRestoCreateAPIView.as_view()),
    path('api/v2.table-resto-info/<pk>', views.TableRestoInfoAPIView.as_view()),

    path('api/categories', views.CategoryListAPIView.as_view()),
    path('api/menu-restos', views.MenuRestoListAPIView.as_view()),
    path('api/menu-resto-filter/', views.MenuRestoFilterApi.as_view()),

    path('api/login', views.LoginView.as_view()),
    path('api/register', views.RegisterView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)