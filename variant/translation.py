# from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions, register

from .models import Subject, Variant, Topic, Exercise, Result


@register(Subject)
class SubjectTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Variant)
class VariantTranslationOptions(TranslationOptions):
    fields = ('title',)

# translator.register(Variant, VariantTranslationOptions)


@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Exercise)
class ExerciseTranslationOptions(TranslationOptions):
    fields = ('text', 'answer_a', 'answer_b', 'answer_c', 'answer_d')


@register(Result)
class ExerciseTranslationOptions(TranslationOptions):
    pass
