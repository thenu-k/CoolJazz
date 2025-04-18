from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from django.core import serializers

def index(request):
    articles = Article.objects.filter(deleted=False).order_by("-created")
    return render(request, "index.html", {
        "articles": articles,
        "pageName": "Cool Jazz"
    })

def createPage(request):
    return render(request, "create.html", {
        "pageName": "Create Article",
        "edit": False
    })

def reloadPage(request):
    return HttpResponseRedirect()

def createArticle(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        title = data.get("title", "")
        content = data.get("content", "")
        abstract = data.get("abstract", "")
        user = request.user
        article = Article(title=title, content=content, abstract=abstract, userKey=user)
        article.save()
        return JsonResponse({"status": 'success', "article_id": article.id})
    
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def articlePage(request, article_id):
    article = Article.objects.get(id=article_id)
    username = article.userKey.username
    return render(request, "article.html", {
        "article": article,
        "username": username,
        "pageName": article.title
    })


def deletePage(request, article_id):
    if request.user.is_authenticated:
        article = Article.objects.get(id=article_id)
        if request.user == article.userKey:
            previousURL = request.META.get('HTTP_REFERER')
            if previousURL == None:
                previousURL = "/"
            confirmation = {
                "title": "CONFIRMATION OF DELETION",
                "message": "Are you sure you want to delete this article? This action cannot be undone.",
                "extra": article.title,
                "options": [["YES", f"/dangerous/delete/{article.id}", "red"], ["NO", previousURL]]
            }
            return render(request, "confirmation.html", {
                "confirmation": confirmation,
                "pageName": "Delete Article"
            })
        else:
            return HttpResponseRedirect(reverse("admin:index"))
    else:
        return HttpResponseRedirect(reverse("admin:index"))
        
def deleteArticle(request, article_id):
    if request.user.is_authenticated:
        article = Article.objects.get(id=article_id)
        if request.user == article.userKey:
            article.deleted = True
            article.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("admin:index"))
    else:
        return HttpResponseRedirect(reverse("admin:index"))
    
def editPage(request, article_id):
    if request.user.is_authenticated:
        article = Article.objects.get(id=article_id)
        if request.user == article.userKey:
            return render(request, "create.html", {
                "article": article,
                "edit": True,
                "pageName": "Edit Article"
            })
        else:
            return HttpResponseRedirect(reverse("admin:index"))
    else:
        return HttpResponseRedirect(reverse("admin:index"))
    
def editArticle(request, article_id):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        title = data.get("title", "")
        content = data.get("content", "")
        abstract = data.get("abstract", "")
        user = request.user
        article = Article.objects.get(id=article_id)
        if user == article.userKey:
            article.title = title
            article.content = content
            article.abstract = abstract
            article.save()
            return JsonResponse({"status": 'success'})
        else:
            return HttpResponseRedirect(reverse("admin:index"))
    else:
        return HttpResponseRedirect(reverse("admin:index"))
    
def search(request):
    title = request.GET.get("title")
    abstract = request.GET.get("abstract")
    content = request.GET.get("content")
    articles = Article.objects.filter(title__icontains=title, abstract__icontains=abstract, content__icontains=content, deleted=False).order_by("-created")
    return render(request, "searchResults.html", {
        "articles": articles,
        "pageName": "Search Results",
        "title": title,
        "abstract": abstract,
        "content": content,
        "fullSearch": True
    })

def randomArticle(request):
    articles = Article.objects.filter(deleted=False)
    if len(articles) > 0:
        article = articles.order_by("?").first()
        return HttpResponseRedirect(reverse("article", args=[article.id]))
    else:
        return HttpResponseRedirect(reverse("index"))
    
def confirmLogout(request):
    if request.user.is_authenticated:
        previousURL = request.META.get('HTTP_REFERER')
        if previousURL == None:
            previousURL = "/"
        confirmation = {
            "title": "CONFIRMATION OF LOGOUT",
            "message": "Are you sure you want to logout?",
            "options": [["YES", "/logout", "red"], ["NO", previousURL]]
        }
        return render(request, "confirmation.html", {
            "confirmation": confirmation,
            "pageName": "Logout"
        })
    else:
        return HttpResponseRedirect(reverse("index"))