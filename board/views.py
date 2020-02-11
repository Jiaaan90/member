# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView
from board.models import Article, Comment
from board.forms import CommentForm

from django.utils.decorators import method_decorator
#from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages

from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404

from django.views.decorators.http import require_POST

from django.shortcuts import render

#from django.urls import reverser_lazy

#댓글
def post_create(request):
    return render(request, 'article_comment.html')
def article_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('article_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'article_detail.html', {'post': post, 'form': form})

class ArticleListView(TemplateView):         # 게시글 목록
    #template_name = 'base.html'
    #queryset = Article.objects.all()         # 모든 게시글
    template_name = 'article_list.html'       #뷰 전용 템플릿 생성 , 상속받아서 이렇게 쓰면됨
    
    def get(self, request, *args, **kwargs):
        print(request.GET)
        queryset = Article.objects.all()
        print(queryset)
        ctx = {
            #'view': self.__class__.__name__, # 클래스의 이름
            #'data': self.queryset            # 검색 결과
            
            #'articles' : self.queryset

            'articles' : queryset
        }                             
        return self.render_to_response(ctx)
    
    def get_queryset(self):
        if not self.queryset:
            self.queryset = Article.objects.all()
        return self.queryset
    ''' 
    template_name = 'article_list.html'    # 뷰 전용 템플릿 생성.
    queryset = None

    def get(self, request, *args, **kwargs):
        ctx = {
            'view': self.__class__.__name__, # 클래스의 이름
            'articles': self.get_queryset()
        }
        return self.render_to_response(ctx)

    def get_queryset(self):
        if not self.queryset:
            self.queryset = Article.objects.all()
        return self.queryset
    '''
    #댓글 FBV

class ArticleDetailView(TemplateView):
    #template_name = 'base.html'
    template_name = 'article_detail.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'                 # 검색데이터의 primary key를 전달받을 이름

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset     # queryset 파라미터 초기화
        pk = self.kwargs.get(self.pk_url_kwargs) # pk는 모델에서 정의된 pk값, 즉 모델의 id
        return queryset.get(pk=pk)    # pk로 검색된 데이터가 있다면 그 중 첫번째 데이터 없다면 None 반환
    
    def get(self, request, *args, **kwargs):
        article = self.get_object()
        #if not article:
        #    raise Http404('invalid article_id')  # 검색된 데이터가 없다면 에러 발생
        ctx = {
            #'view': self.__class__.__name__,
            #'data': article
            'article' : article
        }
        return self.render_to_response(ctx)


    ######게시글삭제
    def post(self, request, *args, **kwargs): # 액션
        queryset = self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        action = request.POST.get('action')           # request.POST 객체에서 데이터 얻기
        article = self.get_object()
        #print(action)
        if action == 'delete' and  article.author == self.request.user:          
            queryset.get(pk=pk).delete()
            messages.success(self.request, '게시글이 삭제 되었습니다') # 메시지 저장
        else:
            messages.error(self.request, '본인이 작성한 글이 아닙니다.', extra_tags='danger')         #error 레벨로 메시지 저장

        return HttpResponseRedirect('/article/')


 

#@method_decorator(csrf_exempt, name='dispatch') #모든 핸들러 예외 처리
class ArticleCreateUpdateView(LoginRequiredMixin, TemplateView):  # 게시글 추가, 수정
    login_url = settings.LOGIN_URL

    template_name = 'article_update.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        return queryset.filter(pk=pk).first()

        #if pk and not article:
        #    raise Http404('invalid pk')
        #elif article.author != self.request.user:                             # 작성자가 수정하려는 사용자와 다른 경우
        #    raise Http404('invalid user')
        #return article
    def get(self, request, *args, **kwargs):    #화면 요청
        article = self.get_object()
        #if not article:
        #   raise Http404('invalid article_id')
        ctx = {
            #'view': self.__class__.__name__,
            #'data': article
            'article' : article
        }
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs): # 액션
        print(request.POST)
        action = request.POST.get('action')           # request.POST 객체에서 데이터 얻기
        #post_data = {key: request.POST.get(key) for key in ('title', 'content', 'author')}
        post_data = {key: request.POST.get(key) for key in ('title', 'content')}
        print(post_data)
        for key in post_data:                         # 세가지 데이터 모두 있어야 통과 --> #2가지로 변경
            if not post_data[key]:
                #raise Http404('no data for {}'.format(key))
                messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger') # error 레벨로 메시지 저장
        
        post_data['author'] = self.request.user                                  # 작성자를 현재 사용자로 설정

        if len(messages.get_messages(request)) == 0:      #메세지가 있다면 아무것도 처리하지 않음
            
            if action == 'create':                        # action이 create일 경우
                #article = Article.objects.create(title=title, content=content, author=author)
                article = Article.objects.create(**post_data)
                messages.success(self.request, '게시글이 저장 되었습니다')    # success 레벨로 메세지 저장
            elif action == 'update':                      # action이 update일 경우
                article = self.get_object()
                if article.author == self.request.user:
                    #article = self.get_object()
                    #if not article:
                    #    raise Http404('invalid article_id')
                    for key, value in post_data.items():
                        setattr(article, key, value)
                    article.save()
                    messages.success(self.request, '게시글이 저장되었습니다.')
                else:
                    messages.error(self.request, '본인이 작성한 글이 아닙니다' , extra_tags='danger')
            else:                                         # action이 없거나 create, update 중 하나가 아닐 경우
                #raise Http404('invalid action')
                messages.error(self.request, '알 수 없는 요청입니다.', extra_tags='danger')         #error 레벨로 메시지 저장
            
            return HttpResponseRedirect('/article/') # 정상적인 저장이 완료되면 '/articles/'로 이동됨

        ctx = {
            #'view':self.__class__.__name__,
            #'data':article
            'article' : self.get_object() if action == 'update' else None                   # if else 삼항 문법
        }
        return self.render_to_response(ctx)
        

#class ArticleDeleteView(DeleteView):
#    model = Article
#    success_url = reverser_lazy("/")
#    template_name = 'article_update.html'


#def hello(request, to):
#    return HttpResponse('Hello {}.'.format(to))






''' < -------------------------------- FBV 방식 ----------------------------------->
def hello(request, to):
    return HttpResponse('Hello {}.'.format(to))

def list_article(request):                          # 목록보기
    return HttpResponse('list')

def detail_article(request, article_id):            # 상세보기, 상세보기할 article의 id 필요
    return HttpResponse('detail {}'.format(article_id))

def create_or_update_article(request, article_id):  # 생성 및 수정하기, 수정할 때는 article의 id 필요
    if article_id: # 수정하기
        if request.method == 'GET':
            return HttpResponse('update {}'.format(article_id))
        elif request.method == 'POST':
            return do_create_article(request)
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])
    else:          # 생성하기
        if request.method == 'GET':
            return HttpResponse('create')
        elif request.method == 'POST':
            return do_update_article(request)
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])


def do_create_article(request):
    return HttpResponse(request.POST)

def do_update_article(request):
    return HttpResponse(request.POST)
'''