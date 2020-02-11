# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from board.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets={
            "text":forms.Textarea(attrs={'placeholder':'배려와 매너가 밝은 커뮤니티를 만듭니다.','class':'form-control','rows':5}),
        }
        labels={
            "text":""
        }