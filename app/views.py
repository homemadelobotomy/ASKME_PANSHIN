from django.http import HttpResponse
from django.shortcuts import render
import copy
from django.core.paginator import Paginator


# Create your views here.

QUESTIONS = [
    {
      "title": f'Question # {i}',
      "id": i,
      "text": f'This is text for question #{i}'
    } for i in range(1,1000)
  ]

# ANSWERS = [
#     {
#       "title": f'Question # {i}',
#       "id": i,
#       "text": f"This is answer number #{i} for question"
#     } for i in range(1,100)
#   ]


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
    
    return render(request, template_name = 'index.html',
        context = pagination(QUESTIONS,request,5)
        )

def hot(request):
    HOT_QUESTIONS = copy.deepcopy(QUESTIONS)
    HOT_QUESTIONS.reverse()
    return render(request,template_name = 'hot.html',
                  context = pagination(HOT_QUESTIONS,request,5))


def one_question(request, question_id):
    one_question = QUESTIONS[question_id-1]
    ANSWERS = []
    
    for i in range(1,100):
        ANSWERS.append({
        "id" : i,
        "text": f"This is answer number #{i} for question {one_question['id']}"
    })
        
    
    context = pagination(ANSWERS,request,per_page=10)
    context['question'] = one_question
    return render(request, template_name = 'one_question.html',
                  context = context )

def ask(request):
    return render(request, template_name= 'ask.html'
                  )

def tag(request,tag):
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