from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from learningsystem.models import Profile
import json
from networkx import *

# Create your views here.
def layout(request):
    return HttpResponse(render(request, 'layout.html'))

def signup(request):
    if request.method == 'POST':
        users = User.objects.filter(email=request.POST['email'])
        if len(users) == 0:
            user = User.objects.create_user(email=request.POST['email'], username=request.POST['username'], password=request.POST['password'])
            user.save()
            profile = Profile.objects.create(birthday=request.POST['birthday'], avatar=request.POST['avatar'], user_id=user.id)
            profile.save()
            return HttpResponse(render(request, 'login.html'))
        else:
            return HttpResponse(render(request, 'signup.html', context={'message': 'Your email has been already used!'}))
    else:
        return HttpResponse(render(request, 'signup.html'))

def home(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponse(render(request, 'home.html'))
        else:
            return HttpResponse(render(request, 'login.html', context={'message': 'Fail to login!'}))
    else:
        return HttpResponse(render(request, 'login.html'))

def out(request):
    logout(request)
    return HttpResponse(render(request,'login.html'))

def shortestPath(request):
    return HttpResponse(render(request, 'shortestpath.html'))

def findShortestPath(request):
    graph = json.loads(request.POST['result'])
    g = Graph()
    for v in graph["vertices"]:
        g.add_node(v)
    for e in graph["edges"]:
        g.add_edge(e["from"],e["to"], weight = e["weight"])
    path = dijkstra_path(g, int(request.POST['FROM']), int(request.POST['TO']))
    gr = json.dumps(graph)
    return HttpResponse(render(request, "shortestpathresult.html", context={'graph': gr, 'path': path}))
