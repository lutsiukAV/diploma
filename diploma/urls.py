"""diploma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from learningsystem.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^layout/',layout),
    url(r'^index/',index),
    url(r'^signup/',signup),
    url(r'^login/',home),
    url(r'^logout/',out),
    url(r'^shortest/',shortestPath),
    url(r'^shortestpathresult/',findShortestPath),
    url(r'^minimalspanningtree/',minimalSpanningTree),
    url(r'^mstresult/',MSTresult),
    url(r'^euleriancurcuit/',eulerianCurcuit),
    url(r'^ecresult/',ECresult),
    url(r'^isomorphic/',isomorphic),
    url(r'^isomorphicresult/',isomorphicresult),
    url(r'^binary/',binaryTree),
    url(r'^bintreehandler/',bintreeHandler),
    url(r'^avl/',avlTree),
    url(r'^avlhandler/',avltreeHandler),
    url(r'^truthtable/',truthTable),
    url(r'^truthtableresult/',truthTableHandler),
    url(r'^sequential/',sequential),
    url(r'^sequentialresult/',sequentialHandler),
    url(r'^resolution/',resolution),
    url(r'^resolutionresult/',resolutionHandler),
    url(r'^btree/',bTree),
    url(r'^btreehandler',bTreeHandler),
    url(r'^rbtree',rbtree),
    url(r'^rbhandler',rbHandler)
]
