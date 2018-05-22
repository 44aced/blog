from django.urls import path,re_path
from backend import views
urlpatterns = [
    path('index.html',views.index),
    path('base_info.html',views.base_info),
    path('upload_avatar.html', views.upload_avatar),
    path('tag.html',views.tag),
    re_path('tag_edit_(\d+).html',views.tag_edit),
    path('category.html',views.category),
    re_path('article-(\d+)-(\d+).html',views.article),
    path('add_article.html',views.add_article),
    re_path('edit-article-(\d+).html',views.edit_article)
]