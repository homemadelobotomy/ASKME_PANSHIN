from app import models
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--ratio', type=int)
        super().add_arguments(parser)    

    def handle(self, *args, **options):
        ratio = options['ratio']
        
        
        users = [User(username=f'User {i}', email=f'user{i}@gmail.com') for i in range(ratio)]
        User.objects.bulk_create(users)
        users = User.objects.filter(username__startswith='User')
        
        profiles = [models.Profile(user=user, nickname=user.username, email=user.email) for user in users]
        models.Profile.objects.bulk_create(profiles)
        profiles = list(models.Profile.objects.all())

        
        tags = [models.Tag(name=f'Tag #{i}') for i in range(ratio)]
        models.Tag.objects.bulk_create(tags)
        tags = list(models.Tag.objects.all())
        
       
        questions = [
            models.Question(
                title=f'Title for question {i}',
                text=f'This is text for question {i}',
                author=profiles[i % ratio],
            ) for i in range(ratio * 10)
        ]
        models.Question.objects.bulk_create(questions)
        
    
        questions = list(models.Question.objects.select_related('author').prefetch_related('tags').all())
        tags_len = len(tags)
        for item in range(len(questions)) :
            selected_tags = [tags[item % tags_len],tags[(item + 1) % tags_len],tags[(item + 1) % tags_len]]
            questions[item].tags.set(selected_tags)

        for j in range (10):

            answers = [
                models.Answer(
                    text=f'This is text for answer {i}',
                    author=profiles[i % ratio],
                    question=questions[i % (ratio * 10)],
                    status='c' if i % 10 == 4 else 'w',
                ) for i in range(j * ratio * 10,(j+1) * ratio * 10)
            ]
            models.Answer.objects.bulk_create(answers)
            print(f"{j} part of answers has been uploaded")

        answers = list(models.Answer.objects.select_related('author', 'question').all())

        question_likes = [
            models.QuestionLike(
                user=profiles[i // (ratio * 10)],
                question=questions[i % (ratio * 10)],
            ) for i in range(ratio * 9 * 10)
        ]
        models.QuestionLike.objects.bulk_create(question_likes,batch_size = 1000)

        
        answer_likes = [
            models.AnswerLike(
                user=profiles[i // (ratio * 100)],
                answer=answers[i % (ratio * 100)],
            ) for i in range(ratio * 10 * 13)
        ]
        models.AnswerLike.objects.bulk_create(answer_likes,batch_size = 1000)

        question_like_ids = list(models.QuestionLike.objects.values_list('id', flat=True))
        random.shuffle(question_like_ids)
        random_likes_ids = question_like_ids[:ratio * 10]
        models.QuestionLike.objects.filter(id__in=random_likes_ids).delete()
   
