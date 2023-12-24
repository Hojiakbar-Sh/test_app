from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from variant.models import Subject, Variant, Exercise, Topic, Result, Teacher


# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Variant)
class VariantAdmin(TranslationAdmin):
    list_display = ('title',)
    list_filter = ["subject"]
    group_fieldsets = True

    def get_queryset(self, request):
        # Foydalanuvchiga faqat o'zi yaratgan postlarni o'zgartirish va o'chirishga ruxsat berish
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(teacher__user=request.user)
        return qs

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['teacher'].queryset = Teacher.objects.filter(user=request.user)
        context['adminform'].form.fields['subject'].queryset = Subject.objects.filter(teacher__user=request.user)
        return super(VariantAdmin, self).render_change_form(request, context, *args, **kwargs)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Exercise)
class ExerciseAdmin(TranslationAdmin):
    list_filter = ["variant"]
    group_fieldsets = True

    def get_object(self, request, *args, **kwargs):
        request._admin_obj = super(ExerciseAdmin, self).get_object(*args, **kwargs)
        return request._admin_obj

    def get_queryset(self, request):
        # Foydalanuvchiga faqat o'zi yaratgan postlarni o'zgartirish va o'chirishga ruxsat berish
        qs = super().get_queryset(request)
        return qs.filter(variant__teacher__user=request.user)

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['variant'].queryset = Variant.objects.filter(
            subject__teacher__user=request.user)
        context['adminform'].form.fields['topic'].queryset = Topic.objects.filter(subject__teacher__user=request.user)
        return super(ExerciseAdmin, self).render_change_form(request, context, *args, **kwargs)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_filter = ["subject"]

    def get_queryset(self, request):
        print(request)
        # Foydalanuvchiga faqat o'zi yaratgan postlarni o'zgartirish va o'chirishga ruxsat berish
        qs = super().get_queryset(request)
        return qs.filter(subject__teacher__user=request.user)

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['subject'].queryset = Subject.objects.filter(teacher__user=request.user)
        return super(TopicAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
