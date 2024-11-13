from app import models

def popular_tags(request):
    popular_tags = models.Tag.objects.get_popular_tags()
   
    return {'popular_tags': popular_tags}