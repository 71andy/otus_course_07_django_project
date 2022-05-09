from django.urls import path
from .views import *


# app_name = 'hsite'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('logout-page', logout_page, name='logout-page'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path("question/<int:pk>", QuestionView.as_view(), name="question"),
    path("question/<int:pk>/ans", post_answer, name="answer"),
    path('ask/', AskView.as_view(), name='ask'),
]
