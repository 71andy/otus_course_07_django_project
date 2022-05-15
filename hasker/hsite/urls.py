from django.urls import path, re_path
from .views import *


# app_name = 'hsite'
urlpatterns = [
    path('', IndexView.as_view(), {'order': 'date'}, name='main-page'),
    re_path(r'^date/$', IndexView.as_view(), {'order': 'date'}, name='home-by-date'),
    re_path(r'^votes/$', IndexView.as_view(), {'order': 'votes'}, name='home-by-votes'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('logout-page', logout_page, name='logout-page'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path("question/<int:pk>", QuestionView.as_view(), name="question"),
    path("question/<int:pk>/ans", post_answer, name="answer"),
    path('ask/', AskView.as_view(), name='ask'),
]
