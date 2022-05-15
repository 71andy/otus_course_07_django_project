# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
# from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.db.models import Count, Value, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.views.decorators.http import require_http_methods
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *


class IndexView(generic.ListView):
    template_name = 'hsite/index.html'
    context_object_name = 'questions_list'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_by_date'] = self.kwargs.get('order') == 'date'
        return context

    def get_queryset(self):
        order_by = {'date': '-pub_date', 'votes': '-votes'}
        order = self.kwargs.get('order')
        if order not in order_by.keys():
            order = 'date'
        q = (
            Question.objects.annotate(votes=(Count('likes', distinct=True) - Count('dislikes', distinct=True)))
            .annotate(answers=Count('answer', distinct=True))
            .order_by(order_by[order])
        )

        return q


class QuestionView(generic.DetailView):
    model = Question
    template_name = 'hsite/question.html'
    # context_object_name = 'answers_list'
    # pk_url_kwarg = 'question_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        question = kwargs['object']
        q = Answer.objects.filter(question=question.pk)
        q = q.annotate(votes=(Count('likes', distinct=True) - Count('dislikes', distinct=True)))
        q = q.order_by('-votes', '-pub_date')
        context['answers_list'] = q
        context['answer_form'] = AnswerForm()
        return context

    def get(self, request, *args, **kwargs):
        vote = self.request.GET.get('vote')
        answer_pk = self.request.GET.get('answer')
        question_pk = self.request.GET.get('question')
        if vote:
            try:
                pk = int(answer_pk) if answer_pk else int(question_pk)
                mode = 'answer' if answer_pk else 'question'
                self.update_vote(pk, vote, mode)
            except ValueError:
                pass

        return super().get(request, *args, **kwargs)

    def update_vote(self, pk, vote, mode):
        mode_map = {'answer': Answer, 'question': Question}

        user = self.request.user
        if not user.is_authenticated:
            return

        objects = mode_map[mode].objects
        obj = objects.get(pk=pk)

        likes = obj.likes.all()
        dislikes = obj.dislikes.all()
        if vote == 'dislike':
            if user in likes:
                obj.likes.remove(user)
            elif user not in dislikes:
                obj.dislikes.add(user)
        elif vote == 'like':
            if user in dislikes:
                obj.dislikes.remove(user)
            elif user not in likes:
                obj.likes.add(user)


class AskView(LoginRequiredMixin, generic.CreateView):
    form_class = AskForm
    template_name = 'hsite/ask.html'  # Указание имени темплейта
    success_url = reverse_lazy('main-page')
    # Настройка поведения LoginRequiredMixin
    login_url = reverse_lazy('login')  # Переход на URL если пользователь не авторизован
    # raise_exception = True  # Показывать страницу 403 неавторизованным пользователям

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ask a question'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AskView, self).form_valid(form)


@login_required
@require_http_methods(["POST"])
def post_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            Answer.objects.create(user=request.user, question=question, **form.cleaned_data)

    return redirect('question', pk)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'hsite/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            print("RegisterView post")
            user = form.save()
            # Автоматический вход при успешной регистрации
            login(self.request, user)
            return redirect('main-page')

        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the main-page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect('main-page')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'hsite/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('logout-page')

        # else process dispatch as it otherwise normally would
        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main-page')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def logout_page(request):
    if request.method == 'POST':
        return logout_user(request)
    else:
        return render(request, 'hsite/logout.html')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'hsite/profile.html', {'user_form': user_form, 'profile_form': profile_form})
