from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length = 255)
    avatar = models.ImageField(blank = True, null = True)
    email = models.EmailField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.nickname

class TagManager(models.Manager):

    def get_popular_tags(self, number = 8):
        tags = Tag.objects.all().annotate(question_count = Count("question")).order_by('-question_count')
        
        return [{'name':tag.name } for tag in tags[:number]]    
    
class Tag(models.Model):
    name = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TagManager()

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
     
    def create_list(self, sort_by = 'created_at',tag = "none"):
        if sort_by == 'likes':
            ordering = '-like_count'  
        else:
            ordering = '-created_at'
        
        if tag == 'none':
            questions = (Question.objects.all().annotate(like_count = Count('questionlike')).order_by(ordering))
        else:
            questions = (Question.objects.filter(tags__name = tag).annotate(like_count = Count('questionlike')).order_by(ordering))

        return [
        {  
           'author' : question.author.nickname,
            'likes' :question.like_count,
            "title": question.title,
            "id": question.id,
            "text": question.text,
            "tags": list(question.tags.all().values_list('name',flat = True)),
        } for question in questions.filter(author__nickname__startswith = "User")
  ]


class Question(models.Model):
    title = models.CharField(max_length = 255)
    text = models.CharField(max_length = 1024)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = QuestionManager()
    def __str__(self):
        return self.title



# Table answer{
#   id int [pk]
#   author varchar
#   text varchar
#   correct bool
#   question_id int
#   created_at datetime
#   updated_at datetime

class AnswerManager(models.Manager):
     
    def create_list(self,question_id):
        question = Question.objects.get(id=question_id)
        answers = (Answer.objects.filter(question = question).annotate(like_count = Count('answerlike')).order_by('-like_count'))

        return [
        {  
           'author' : answer.author.nickname,
            'likes' :answer.like_count,
            "id": answer.id,
            "text": answer.text,
            "status" : answer.status,
            'question': question,
        } for answer in answers.filter(author__nickname__startswith = "User")
        ]
    
    def get_question(self,question_id):
        question = (Question.objects.all().annotate(like_count = Count('questionlike'))).get(id = question_id)
        return {  
           'author' : question.author.nickname,
            'likes' :question.like_count,
            "title": question.title,
            "id": question.id,
            "text": question.text,
            "tags": list(question.tags.all().values_list('name',flat = True)),
        }

class Answer(models.Model):
    STATUS_CHOISES = [
        ('c','Corrrect'),
        ('w', 'Wrong'),
    ]
    text = models.TextField(max_length = 1024)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    status = models.CharField(max_length = 10, choices = STATUS_CHOISES)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = AnswerManager()
    def __str__(self):
        return f"Answer by {self.author.nickname} to {self.question.title}"



# }
# Table tag{
#   id int [pk]
#   name varchar
#   count int

#   created_at datetime
#   updated_at datetime
# }

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        unique_together = ('user','answer')


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        unique_together = ('user','question')
    
   

# Table like{
#   id int [primary key]
#   question_id int
#   user_id int

#   created_at datetime
#   updated_at datetime
# }


# Table tag_question{
#   tag_id int 
#   question_id int 
# }

