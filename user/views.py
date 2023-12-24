from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView

from user.forms import RegisterForm
from user.models import User


# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'pages/register_page.html', {'form': form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'pages/register_page.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


class DetailProfileView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'pages/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        result_list = []
        for res in user.results.all():
            result_list.append({
                'result': res,
                'count_exersice': len(res.variant.exercises.all()),
                'signpost': round(len(res.user_answers.filter(is_True=True)) * 100 / len(res.variant.exercises.all()),
                                  2),
                'count_correct': len(res.user_answers.filter(is_True=True)),
                'count_incorrect': len(res.variant.exercises.all()) - len(res.user_answers.filter(is_True=True))
            })
        context["result_list"] = result_list
        return context


class EditProfileView(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'avatar']
    template_name = 'pages/edit_profile_page.html'

    def get_success_url(self):
        return reverse_lazy('account:profile_detail', kwargs={'pk': self.object.pk})


class DeleteProfileView(DeleteView):
    model = User
    template_name = 'pages/delete_profile_page.html'

    def get_success_url(self):
        return reverse_lazy('home')


