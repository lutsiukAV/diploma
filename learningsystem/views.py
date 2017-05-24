from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from learningsystem.models import Profile
import json
from networkx import *

from learningsystem.tree.binary import BinaryTree, AvlTree
from learningsystem.expression.expression import *

# Create your views here.
def layout(request):
    return HttpResponse(render(request, 'layout.html'))

@login_required(login_url="/login/")
def index(request):
    return HttpResponse(render(request, 'home.html'))

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
        if not request.user.id is None:
            return HttpResponse(render(request, 'home.html'))
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
        if not request.user.id is None:
            return HttpResponse(render(request, 'home.html'))
        return HttpResponse(render(request, 'login.html'))

@login_required(login_url="/login/")
def out(request):
    logout(request)
    return HttpResponse(render(request,'login.html'))

@login_required(login_url="/login/")
def shortestPath(request):
    return HttpResponse(render(request, 'shortestpath.html'))

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def minimalSpanningTree(request):
    return HttpResponse(render(request,'minimalspanningtree.html'))

@login_required(login_url="/login/")
def MSTresult(request):
    graph = json.loads(request.POST['result'])
    g = Graph()
    for v in graph["vertices"]:
        g.add_node(v)
    for e in graph["edges"]:
        g.add_edge(e["from"],e["to"], weight = e["weight"])
    mst = minimum_spanning_tree(g, 'weight')
    gr = json.dumps(graph)
    return HttpResponse(render(request, 'mstresult.html', context={'graph': gr, 'mst': [list(elem) for elem in mst.edges()]}))

@login_required(login_url="/login/")
def eulerianCurcuit(request):
    return HttpResponse(render(request, 'euleriancircuit.html'))

@login_required(login_url="/login/")
def ECresult(request):
    graph = json.loads(request.POST['result'])
    g = Graph()
    for v in graph["vertices"]:
        g.add_node(v)
    for e in graph["edges"]:
        g.add_edge(e["from"], e["to"])
    if is_eulerian(g):
            circuit = list(eulerian_circuit(g))
            gr = json.dumps(graph)
            return HttpResponse(render(request, 'euleriancurcuitresult.html', context={'graph': gr, 'circuit': [list(elem) for elem in circuit]}))
    gr = json.dumps(graph)
    lst = []
    return HttpResponse(render(request, 'euleriancurcuitresult.html', context={'graph': gr,'circuit': [list(elem) for elem in lst] ,'message': "Non-eulerian"}))

@login_required(login_url="/login/")
def isomorphic(request):
    return HttpResponse(render(request, "isomorphic.html"))

@login_required(login_url="/login/")
def isomorphicresult(request):
    graph1 = json.loads(request.POST['result1'])
    g1 = Graph()
    for v in graph1["vertices"]:
        g1.add_node(v)
    for e in graph1["edges"]:
        g1.add_edge(e["from"], e["to"])

    graph2 = json.loads(request.POST['result2'])
    g2 = Graph()
    for v in graph2["vertices"]:
        g2.add_node(v)
    for e in graph2["edges"]:
        g2.add_edge(e["from"], e["to"])

    gr1 = json.dumps(graph1)
    gr2 = json.dumps(graph2)

    if is_isomorphic(g1, g2):
        return HttpResponse(render(request, 'isomorphicresult.html', context={'graph1': gr1, 'graph2': gr2, 'message': "Isomorphic"}))

    return HttpResponse(render(request, 'isomorphicresult.html', context={'graph1': gr1, 'graph2': gr2, 'message': "Non-isomorphic"}))

@login_required(login_url="/login/")
def truthTable(request):
    return HttpResponse(render(request, 'truthtable.html'))

@login_required(login_url="/login/")
def truthTableHandler(request):
    expression = request.POST['expr']
    pstfx = postfix(expression)
    g, v = generate(pstfx)
    result = base(pstfx, g, v)
    return HttpResponse(render(request, 'truthtableresult.html', context={'result': result}))


@login_required(login_url="/login/")
def binaryTree(request):
    return HttpResponse(render(request, 'binarytree.html'))

@login_required(login_url="/login/")
def bintreeHandler(request):
    t = json.loads(request.POST['keys'])
    T = BinaryTree()
    for key in t:
        T.insert(key)
    tr = json.dumps(T.toTreantConfig())

    return HttpResponse(render(request, 'bintreeresult.html', context={'tree': tr}))


@login_required(login_url="/login/")
def avlTree(request):
    return HttpResponse(render(request, 'avltree.html'))

@login_required(login_url="/login/")
def avltreeHandler(request):
    t = json.loads(request.POST['keys'])
    T = AvlTree()
    for key in t:
        T.insert(key)
    tr = json.dumps(T.toTreantConfig())

    return HttpResponse(render(request, 'avlresult.html', context={'tree': tr}))