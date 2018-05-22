from django import forms
from django.forms import fields
from django.forms import widgets as django_widgets
from repository import models
import repository

class ArticleForm(forms.Form):
    def __init__(self,request,*args,**kwargs):
        super(ArticleForm,self).__init__(*args,**kwargs)
        blog_id = request.session['user_info']['blog__nid']
        self.fields['category_id'].choices = models.Category.objects.filter(blog_id=blog_id).values_list('nid','title')
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=blog_id).values_list('nid','title')


    title = fields.CharField(error_messages={'required':'必填'},
        widget=django_widgets.TextInput(attrs={'class':'form-control'}))
    summary = fields.CharField(widget=django_widgets.TextInput(attrs={'class':'form-control'}))
    content = fields.CharField(widget=django_widgets.Textarea(attrs={'class':'form-control'}))
    category_id = fields.ChoiceField(choices=[],widget=django_widgets.RadioSelect)
    tags = fields.MultipleChoiceField(choices=[],widget=django_widgets.CheckboxSelectMultiple)
    article_type_id = fields.IntegerField(widget=django_widgets.RadioSelect(choices=models.Article.type_choices))


class Base_info(forms.Form):
    def __init__(self,request,*args,**kwargs):
        self.request = request
        super(Base_info,self).__init__(*args,**kwargs)
    nickname = fields.CharField(error_messages={'required':'必填'})
    site = fields.CharField(error_messages={'required':'必填'})
    title = fields.CharField(error_messages={'required':'必填'})

class Tag(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['title',]




