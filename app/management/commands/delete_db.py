from django.core.management.base import BaseCommand, CommandError
from app import models
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        User.objects.all().filter(username__startswith = "User").delete()
        models.Question.objects.all().delete()
        models.Tag.objects.all().delete()
        models.Answer.objects.all().delete()
        models.AnswerLike.objects.all().delete()
        models.QuestionLike.objects.all().delete()

        