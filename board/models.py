# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Article(models.Model):
    title      = models.CharField('제목', max_length=126, null=False)
    content    = models.TextField('내용', null=False)
    #author     = models.CharField('작성자', max_length=16, null=False)
    author     = models.ForeignKey('accounts.User', related_name='articles', on_delete=models.CASCADE)
    created_at = models.DateTimeField('작성일', default=timezone.now)
    created_at.editable = True  #create의 editable 속성에 True를 설정               //원래 False

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)
    #def __unicode__(self):
    #    return u'[{}] {}' %(self.id, self.title)

@python_2_unicode_compatible
class Comment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    post = models.ForeignKey('board.Article', related_name='comments', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text