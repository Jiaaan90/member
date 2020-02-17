# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from board.models import Article, Comment

from django_summernote.widgets import SummernoteWidget

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets={
            "text":forms.Textarea(attrs={'placeholder':'리눅스웨어에 오신걸 환영합니다.','class':'form-control','rows':5}),
        }
        labels={
            "text":""
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['content']
        widgets = {
            'content' : SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '560px','class':'form-control',
             'name':'content','value':'{{article.content}}'}}),
        }
        labels={
            "내용":""
        }
