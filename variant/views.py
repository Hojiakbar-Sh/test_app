from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic.edit import BaseCreateView

from variant.forms import VariantForm, ExerciseFormSet
from variant.models import Subject, Variant, Exercise, Result, UserAnswer, Teacher


# Create your views here.


def index_view(request):
    return render(request, 'pages/home_page.html')


def subject_list_view(request):
    user = request.user
    if user.is_authenticated:
        subject_list = Subject.objects.all()
        if user.is_staff:
            subject_list = subject_list.filter(teacher__user=user)
        context = {
            'subject_list': subject_list
        }
        return render(request, 'pages/subject_page.html', context)
    return redirect('account:login')


def subject_view(request, pk):
    variant_list = Variant.objects.filter(subject_id=pk)
    subject = Subject.objects.get(id=pk)
    context = {
        'subject': subject,
        'variant_list': variant_list
    }
    return render(request, 'pages/variant_page.html', context)


@login_required
def variant_view(request, pk):
    exercise_list = Exercise.objects.filter(variant_id=pk)
    variant = Variant.objects.get(id=pk)
    if request.method == 'GET':
        template = 'pages/exercise_page.html'
        if request.user.is_staff:
            template = 'pages/variant_edit.html'
        context = {
            'variant': variant,
            'exercise_list': exercise_list,
        }
        return render(request, template_name=template, context=context)

    if request.method == 'POST':
        data = request.POST
        result = Result.objects.create(user=request.user, variant=variant)
        for exercise in exercise_list:
            user_answer = UserAnswer(result=result, exercise=exercise)
            if data.get(str(exercise.id)) is not None:
                user_answer.user_answer = data.get(str(exercise.id))
                if exercise.answer == data.get(str(exercise.id)):
                    user_answer.is_True = True
            user_answer.save()
        return redirect('test:result', pk=result.id)


def result_view(request, pk):
    result = Result.objects.get(id=pk, user=request.user)
    ua = UserAnswer.objects.filter(result=result, is_True=True)

    object_list = []
    for exercise in result.variant.exercises.all():
        object_list.append({
            'exercise': exercise,
            'user_answer': exercise.user_answers.get(result=result).user_answer,
            'is_True': exercise.user_answers.get(result=result).is_True
        })

    context = {
        'object_list': object_list,
        'ball': len(ua),
        'count': len(result.variant.exercises.all())
    }

    return render(request, 'pages/result_page.html', context=context)


class VariantCreateView(View):
    def get(self, request):
        print(request.GET.get('subject'))
        context = {
            'variant_form': VariantForm(),
            'formset': ExerciseFormSet(instance=Variant())
        }

        return render(request, 'pages/variant_create.html', context=context)

    def post(self, request):
        variant_form = VariantForm(request.POST)
        formset = ExerciseFormSet(request.POST, instance=Variant())

        if variant_form.is_valid() and formset.is_valid():
            variant = variant_form.save()
            formset.instance = variant
            formset.save()
            return redirect('home')
# class VariantCreateView(LoginRequiredMixin, CreateView):
# model = Variant
# fields = ["title"]
# template_name = 'pages/variant_create.html'
# success_url = reverse_lazy('test:subject_list')
#
# def form_valid(self, form):
#     subject_id = self.request.GET.get('subject')
#     form.instance.teacher = Teacher.objects.get(user=self.request.user, subject_id=subject_id)
#     form.instance.subject = Subject.objects.get(id=subject_id)
#     return super(VariantCreateView, self).form_valid(form)
