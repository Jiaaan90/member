# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Article(models.Model):
    title      = models.CharField('제목', max_length=126, null=False)
    content    = models.TextField('내용', null=False)
    author     = models.CharField('작성자', max_length=16, null=False)
    #author     = models.ForeignKey('accounts.User', related_name='articles', on_delete=models.CASCADE)
    anonymous_author = models.CharField('작성자', max_length=100, null=True)
    created_at = models.DateTimeField('작성일', default=timezone.now)
    article_hit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)
    
    class Meta:
        ordering = ['-created_at']          ##게시글 순서

    @property
    def update_counter(self):
        self.article_hit = self.article_hit + 1
        self.save()
        return self.article_hit

    #def __unicode__(self):
    #    return u'[{}] {}' %(self.id, self.title)

@python_2_unicode_compatible
class Comment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    post = models.ForeignKey('board.Article', related_name='comments', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

   