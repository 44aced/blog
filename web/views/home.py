from django.shortcuts import render,redirect,reverse
from repository import models

def index(request, *args, **kwargs):
    """
    博客首页，展示全部博文
    :param request:
    :return:
    """

    article_type_list = models.Article.objects.all()

    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index',kwargs=kwargs)
    else:
        article_type_id = None
        base_url = '/'

    data_count = article_list = models.Article.objects.filter(**kwargs).count()


    # page_obj = Pagination(request.GET.get('p'),data_count)
    article_list = models.Article.objects.filter(**kwargs).values_list('title','blog__user__avatar',
                   'blog__user__nickname','create_time' ,'summary' ).order_by('-nid')
    # page_str = page_obj.page_str(base_url)


    return render(
        request,
        'index.html',
        {
            'article_list': article_list,
            'article_type_id': article_type_id,
            'article_type_list': article_type_list,
            # 'page_str': page_str,
            # 'userinfo':userinfo,
        }
    )

def home(request,site):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    article_list = models.Article.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid,count(nid) as num , strftime("%Y-%m",create_time) as ctime from  repository_article group by strftime("%Y-%m",create_time)')

    return render(request,'home.html',
                  {'blog':blog,'tag_list':tag_list,
                   'category_list':category_list,
                   'article_list':article_list,'date_list':date_list })

def detail(request,site,nid):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.filter(blog=blog).raw(
        'select nid,count(nid) as num , strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    article = models.Article.objects.filter(blog=blog,nid=nid).first()
    content = models.Article.objects.filter(blog=blog,nid=nid).values_list('articledetail__content').first()


    return render(request,'home_detail.html',
                  {'tag_list':tag_list,'nid':nid,'blog':blog,
                 'category_list':category_list,'date_list':date_list,
                 'article':article,'content':content})

def filter(request,site,condition,val):
    blog = models.Blog.objects.filter(site=site).select_related('user')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    template_name = 'home_summary_list.html'
    if condition == 'tag':
        template_name = 'home_title_list.html'
        article_list = models.Article.objects.filter(tags=val,blog=blog).all()
    elif condition == 'category':
        article_list = models.Article.objects.filter(category_id=val, blog=blog).all()
    elif condition == 'date':
        # article_list = models.Article.objects.filter(blog=blog).extra(
        # where=['date_format(create_time,"%%Y-%%m")=%s'], params=[val, ]).all()

        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
        # select * from article where strftime("%Y-%m",create_time)=2017-02
    else:
        article_list = []

    return render(
        request,
        template_name,
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list
        }
    )