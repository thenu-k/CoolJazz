from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.createPage, name="create"),
    path("logout", views.logoutView, name="logout"),
    path("createArticle", views.createArticle, name="createArticle"),
    path("article/<int:article_id>", views.articlePage, name="article"),
    path("delete/<int:article_id>", views.deletePage, name="deletePage"),
    path("dangerous/delete/<int:article_id>", views.deleteArticle, name="deleteArticle"),
    path("edit/<int:article_id>", views.editPage, name="editPage"),
    path("editArticle/<int:article_id>", views.editArticle, name="editArticle"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
