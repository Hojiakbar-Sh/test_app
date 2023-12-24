from django import forms
from django.forms import Form, ModelForm, inlineformset_factory, Textarea, TextInput, Select
from modeltranslation.forms import TranslationModelForm
from modeltranslation.utils import get_translation_fields

from config import settings
from variant.models import Variant, Exercise


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        # fields = ('title',)
        fields = ('title', 'title_uz', 'title_ru', 'title_en',)

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ('topic', 'text', 'answer_a', 'answer_b', 'answer_c', 'answer_d', 'answer')

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


ExerciseFormSet = inlineformset_factory(
    Variant,
    Exercise,
    # fields=('topic', 'text', 'answer_a', 'answer_b', 'answer_c', 'answer_d', 'answer'),
    exclude=('id', 'variant',),
    extra=3,
    can_delete=False,
)
