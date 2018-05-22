from django.shortcuts import render,redirect
from repository import models
import os
import json
from django.db import transaction
from django.shortcuts import HttpResponse
from backend.auth.auth import check_login
from backend.auth.forms import ArticleForm,Base_info,Tag
# Create your views here.

@check_login
def index(request):
    return render(request,'backend_index.html')

@check_login
def base_info(request):
    blog_id = request.session['user_info']['nid']
    ret = {'status':False,'error':None}
    if request.method == 'GET':
        img_obj = models.UserInfo.objects.filter(nid=blog_id).values_list('avatar').first()
        # print(img_obj[0])
        return render(request,'backend_base_info.html',{'img_obj':img_obj})
    # elif request.method == 'POST':
    #     form = Base_info(request=request,data=request.POST)
    #     if form.is_valid():
    #         # with transaction.atomic():
    #         nickname = form.cleaned_data.pop('nickname')
    #         models.Blog.objects.create(**form.cleaned_data,user_id=blog_id)
    #         models.UserInfo.objects.filter(nid=blog_id).update(nickname=nickname)
    #         ret['status'] = True
    #     else:
    #         ret['error'] = form.errors.as_json()
    #     return HttpResponse(json.dumps(ret))
    elif request.method == 'POST':
        print(request.POST)
        print(blog_id)
        nickname = request.POST.get('nickname')
        site = request.POST.get('site')
        title = request.POST.get('title')
        models.UserInfo.objects.filter(nid=blog_id).update(nickname=nickname)
        v = models.Blog.objects.filter(user_id=blog_id).count()
        if v :
            models.Blog.objects.filter(user_id=blog_id).update(site=site,title=title)
        else:
            models.Blog.objects.create(site=site, title=title,user_id=blog_id)
        ret['status'] = True
        return HttpResponse(json.dumps(ret))
@check_login
def upload_avatar(request):
    nid = request.session['user_info']['nid']
    ret = {'status':False,'data':None}
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar_img')
        if file_obj:
            file_path = os.path.join('static/imgs/avatar/',file_obj.name)
            with open(file_path,'wb') as f:
                for chunks in file_obj:
                    f.write(chunks)
            ret['status'] = True
            ret['data'] = file_path
            models.UserInfo.objects.filter(nid=nid).update(avatar=file_path)
        else:
            pass
        return HttpResponse(json.dumps(ret))

@check_login
def tag(request):
    blog_id = request.session['user_info']['blog__nid']
    print(blog_id)
    if request.method == 'GET':
        obj = models.Tag.objects.filter(blog_id=blog_id)
        return render(request,'backend_tag.html',{'obj':obj})

    if request.method == 'POST':
        addtag = request.POST.get('newtag')
        models.Tag.objects.create(title=addtag,blog_id=blog_id)
        return redirect('/backend/tag.html')

@check_login
def tag_edit(request,nid):
    if request.method == 'GET':
        obj = models.Tag.objects.filter(nid=nid).first()
        form = Tag(instance=obj)
        return render(request,'tag_edit.html',{'form':form})

@check_login
def category(request):
    ret={'status':False,'data':None}
    nid = request.session['user_info']['blog__nid']
    if request.method == 'GET':
        obj = models.Category.objects.filter(blog_id=nid)
        return render(request,'backend_category.html',{'obj':obj})
    elif request.method == 'POST':
        print(request.POST,nid)
        title = request.POST.get('category')
        models.Category.objects.create(title=title,blog_id=nid)
        ret['status'] = True
        return HttpResponse(json.dumps(ret))

@check_login
def article(request,*args,**kwargs):
    blog_id = request.session['user_info']['blog__nid']
    obj = models.Article.objects.filter(blog_id=blog_id)
    return render(request,'backend_article.html',{'result':obj})

@check_login
def add_article(request):
    if request.method == 'GET':
        form = ArticleForm(request=request)
        return render(request,'backend_add_article.html',{'form':form})
    elif request.method =='POST':
        print(request.POST)
        form = ArticleForm(request=request,data=request.POST)
        if form.is_valid():

            with transaction.atomic():
                tags = form.cleaned_data.pop('tags')
                content = form.cleaned_data.pop('content')
                form.cleaned_data['blog_id'] = request.session['user_info']['blog__nid']
                obj = models.Article.objects.create(**form.cleaned_data)
                models.ArticleDetail.objects.create(content=content,article=obj)
                tag_list = []
                for tag in tags:
                    tag = int(tag)
                    tag_list.append(models.Article2Tag(article_id=obj.nid,tag_id=tag))
                models.Article2Tag.objects.bulk_create(tag_list)
            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_add_article.html', {'form': form})
    else:
        return redirect('/')
@check_login
def edit_article(request,nid):
    blog_id = request.session['user_info']['blog__nid']
    if request.method == 'GET':
        obj = models.Article.objects.filter(blog_id=blog_id,nid=nid).first()
        if not obj:
            pass
        tags = obj.tags.values_list('nid')

        if tags:
            tags = list(zip(*tags))[0]
        content = obj.articledetail_set.all().values('content').first()
        print(content)
        init_dict = {
            'nid':obj.nid,
            'title':obj.title,
            'summary':obj.summary,
            'category_id':obj.category_id,
            'article_type_id':obj.article_type_id,
            'content':content['content'],
            'tags':tags,
        }
        form = ArticleForm(request=request,data=init_dict)
        return render(request,'backend_edit_article.html',{'form':form,'nid':nid})

    if request.method == 'POST':
        form = ArticleForm(request=request,data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            obj = models.Article.objects.filter(nid=nid,blog_id=blog_id).first()
            if not obj:
                pass
            with transaction.atomic():
                content = form.cleaned_data.pop('content')
                tags = form.cleaned_data.pop('tags')
                models.Article.objects.filter(nid=obj.nid).update(**form.cleaned_data)
                models.ArticleDetail.objects.filter(article=obj).update(content=content)
                models.Article2Tag.objects.filter(article=obj).delete()
                tag_list = []
                for tag in tags:
                    tag = int(tag)
                    tag_list.append(models.Article2Tag(article_id=obj.nid,tag_id=tag))
                models.Article2Tag.objects.bulk_create(tag_list)
            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_edit_article.html', {'form': form, 'nid': nid})


