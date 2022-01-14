'''
To render html web pages
'''

from django.http import HttpResponse
import random
from articles.models import Article
from django.template.loader import render_to_string

#MVT Model Views Template
def HomeView(request): 
    # 'request' is standard in django

    '''
    taje in a request (django sends request)
    return html as a response (we pick to return the response)
    '''

    name = 'Homayoon' 
    # what about something from the database??
    main_title = 'Main Page'
    main_content = 'Articles:'
    object_list = Article.objects.all() # This is called a QuerySet not a List

    # Django Templates 
    context = {
        'title' : main_title,
        'content' : main_content,
        'object_list' : object_list
    }
    html_string = render_to_string('HomeView.html', context=context)
    # html_string = '<h1>{title}, {id}, {content}</h1>'.format(**context)

    return HttpResponse(html_string)

