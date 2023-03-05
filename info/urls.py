from django.urls import path
from .views import info_detail, examples_by_language


urlpatterns = [
    path('<slug:slug>/', info_detail, name='info_detail'),
      path('language/<int:language_id>/examples/', examples_by_language , name="Examples by language"),

]
