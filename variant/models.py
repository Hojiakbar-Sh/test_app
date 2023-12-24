from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Teacher(models.Model):
    user = models.ForeignKey(to='user.User', related_name='teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey(to='variant.Subject', related_name='teacher', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.subject}'


class Subject(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Variant(models.Model):
    subject = models.ForeignKey(to=Subject, related_name='variants', on_delete=models.CASCADE)
    teacher = models.ForeignKey(to='variant.Teacher', related_name='variants', on_delete=models.CASCADE)
    title = models.CharField(_('Variant title'), max_length=30)

    def __str__(self):
        return self.title


class Topic(models.Model):
    subject = models.ForeignKey(to=Subject, related_name='topics', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    topic = models.ForeignKey(to=Topic, related_name='exercises', on_delete=models.CASCADE, null=True)
    variant = models.ForeignKey(to=Variant, related_name='exercises', on_delete=models.CASCADE)
    text = models.TextField()
    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    answer_d = models.TextField()
    answer = models.CharField(max_length=20, choices=[
        ('answer_a', "A variant"),
        ('answer_b', "B variant"),
        ('answer_c', "C variant"),
        ('answer_d', "D variant")
    ])

    def __str__(self):
        return self.text


class Result(models.Model):
    user = models.ForeignKey(to='user.User', related_name='results', on_delete=models.CASCADE)
    variant = models.ForeignKey(to='Variant', related_name='results', on_delete=models.CASCADE)
    date_completed = models.DateTimeField(_("Bajarilgan vaqt"), default=timezone.now)

    def __str__(self):
        return self.variant.title


class UserAnswer(models.Model):
    result = models.ForeignKey(to='Result', related_name='user_answers', on_delete=models.CASCADE)
    exercise = models.ForeignKey(to='Exercise', related_name='user_answers', on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=20, null=True, blank=True)
    is_True = models.BooleanField(default=False)

    def __str__(self):
        return self.exercise.text
