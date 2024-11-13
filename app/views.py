from django.http import HttpResponse
from django.shortcuts import render
import copy
from django.core.paginator import Paginator
from app import models

# Create your views here.




def pagination(list, request, per_page = 5):
    
    page_num = request.GET.get('page',1)

    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1
    
    paginator = Paginator(list,per_page)
    page = paginator.page(page_num)

    elided_page_range = page.paginator.get_elided_page_range(number = page.number,on_each_side = 1, on_ends = 1)
    return {'list': page.object_list, 
                   'page_obj' : page,
                   'elided_page_range' : elided_page_range,
                   'ELLIPSIS' : paginator.ELLIPSIS}
    
    


def index (request):
    QUESTIONS = models.Question.objects.create_list()
    return render(request, template_name = 'index.html',
        context = pagination(QUESTIONS,request,5)
        )

def hot(request):
    HOT_QUESTIONS = models.Question.objects.create_list(sort_by = "likes")
    
    return render(request,template_name = 'hot.html',
                  context = pagination(HOT_QUESTIONS,request,5))


def one_question(request, question_id):
    ANSWERS = models.Answer.objects.create_list(question_id = question_id)
    context = pagination(ANSWERS,request,per_page = 5)
    context['question'] = models.Answer.objects.get_question(question_id = question_id)
    return render(request, template_name = 'one_question.html',
                  context = context )

def ask(request):
    return render(request, template_name= 'ask.html'
                  )

def tag(request,tag):
    QUESTIONS = models.Question.objects.create_list(tag = tag)
    context = pagination(QUESTIONS,request,10)
    context['tag'] = str(tag)
    return render(request,  template_name='tag.html',
                  context = context)

def profile(request):
    return render(request,template_name="profile.html",
                  )
def login(request):
    return render(request,template_name="login.html",
                  )

def sigup(request):
    return render(request,template_name="signup.html",
                    )