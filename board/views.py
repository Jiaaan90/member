# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView, UpdateView, DeleteView
from board.models import Article, Comment
from board.forms import CommentForm, ArticleForm

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#from django.utils.decorators import method_decorator
#from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect

from django.views.decorators.http import require_POST

from django.shortcuts import render

#from django.urls import reverser_lazy

DEFAULT_ARTICLE = 62


#댓글
#화면이동
#한페이지 내에서 잘 안됨
def post_create(request):
    
    return render(request, 'article_comment.html')

def index_get(request):

    return render(request, 'article_index.html')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('.', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'article_comment.html', {'post': post, 'form': form})


########댓글 수정 삭제##########
class CommentUpdate(UpdateView): 
    # asdasdasdasd
    # asdasdasd
    # asdasdasd
    # asdasd
    # asdasd
    #a asdasdasdasdasdasd
    #asdasdasd
    # asdasasdasd
    #/asdaasdasdasdasd
    model = Comment
    #fields = ['text']
    form_class = CommentForm
    template_name = 'comment_update.html'
    article = Article()
    # success_url = '/'
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
            # 삭제 페이지에서 권한이 없다! 라고 띄우거나
            # detail페이지로 들어가서 삭제에 실패했습니다. 라고 띄우거나
        
        if request.method == "POST":
            form = CommentForm(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                messages.success(request, '댓글이 수정 되었습니다.')
                return redirect('/article/' + str(article.id) + '/comment/')
            else:
                form = CommentForm(instance=self.get_object())
        else:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)

class CommentDelete(DeleteView):
    model = Comment
    template_name = 'comment_delete.html' 
    success_url = '/article/' 

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/article/')
        else:
            return super(CommentDelete, self).dispatch(request, *args, **kwargs)
        
class ArticleListView(TemplateView):         # 게시글 목록
    #template_name = 'base.html'
    template_name = 'article_list.html'       #뷰 전용 템플릿 생성 , 상속받아서 이렇게 쓰면됨
    #queryset = Article.objects.all()         # 모든 게시글
    #pk_url_kwargs = 'article_id' 
    
    def get_object(self, queryset=None):
        queryset = queryset or self.queryset     # queryset 파라미터 초기화
        pk = self.kwargs.get(self.pk_url_kwargs) # pk는 모델에서 정의된 pk값, 즉 모델의 id
        return queryset.get(pk=pk)    # pk로 검색된 데이터가 있다면 그 중 첫번째 데이터 없다면 None 반환
    
    def get(self, request, *args, **kwargs):
       
        #페이징
        #article = get_object_or_404(Article, pk=pk)
        PAGE_ROW_COUNT=15
        PAGE_DISPLAY_COUNT=5
        total_list=  Article.objects.all().exclude(pk=DEFAULT_ARTICLE)
        paginator=Paginator(total_list, PAGE_ROW_COUNT)
        pageNum=request.GET.get('pageNum')
        totalPageCount=paginator.num_pages # 전체 페이지 갯수 

        #if not request.user.is_authenticated():
        #    return redirect('/article/create/')             # url aritle 막기
        
        try:
            article_list=paginator.page(pageNum)
        except PageNotAnInteger:
            article_list=paginator.page(1)
            pageNum=1
        except EmptyPage:
            article_list=paginator.page(paginator.num_pages)
            pageNum=paginator.num_pages

        pageNum=int(pageNum)
        startPageNum=1+((pageNum-1)//PAGE_DISPLAY_COUNT)*PAGE_DISPLAY_COUNT
        endPageNum=startPageNum+PAGE_DISPLAY_COUNT-1
        
        if totalPageCount < endPageNum:
            endPageNum=totalPageCount
            
        bottomPages=range(startPageNum, endPageNum+1)
   
        print(article_list)
   
        ctx = {
            #'view': self.__class__.__name__, # 클래스의 이름
            #'data': self.queryset            # 검색 결과
            #'articles' : self.queryset
            'articles' : article_list,
            'pageNum':pageNum,
            'bottomPages':bottomPages,
            'totalPageCount':totalPageCount,
            'startPageNum':startPageNum,
            'endPageNum':endPageNum,
            #'post': post,
            #'form': form
            #'comment' : comment
            #'comment' : comments
        }        
        try:
            comments = Comment.objects.filter(pk=articles)
            ctx['comments'] = comments
            print(comments)   
        except:
            print('pass')
            pass
        return self.render_to_response(ctx)
    
    ##없어도 됨
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
        #form = CommentForm() 
        # comments = Comment.objects.filter(Article=article_id)
        form = CommentForm()

        ctx = {
            #'view': self.__class__.__name__,
            #'data': article
            'form' : form,
            'article' : article,
            #'comments' : comments
            #'post' : post,
         #   'form' : form
        }

        try:
            comments = Comment.objects.filter(post=article)
            ctx['comments'] = comments
            # todo 코멘트에 대한 view 생성, ctx에 추가
        except:
            pass
            # 흘리기

        #post = get_object_or_404(Post, pk=pk)    
        #if request.method == "POST":
        #    form = CommentForm(request.POST)
        #    if form.is_valid():
        #        comment = form.save(commit=False)
        #        comment.author = request.user
        #        comment.post = post
        #        comment.save()
        #        return redirect('article_detail', pk=pk)
        #else:
        #    form = CommentForm()
        
#        pk = self.kwargs.get(self.pk_url_kwargs)
#        comments = Comment.objects.all()
#        comment = comments.get(pk=pk)
        #if not article:
        #    raise Http404('invalid article_id')  # 검색된 데이터가 없다면 에러 발생

        return self.render_to_response(ctx)

    ######게시글삭제
    def post(self, request, *args, **kwargs): # 액션
        queryset = self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        action = request.POST.get('action')           # request.POST 객체에서 데이터 얻기
        article = self.get_object()
        #print(action)
        
        if request.user.is_authenticated :  
            if action == 'delete' and  article.author == self.request.user:          
                queryset.get(pk=pk).delete()
                messages.success(self.request, '게시글이 삭제 되었습니다.') # 메시지 저장
            else:
                messages.error(self.request, '본인이 작성한 글이 아닙니다.', extra_tags='danger')#error 레벨로 메시지 저장
        else:
            if action == 'delete':
                queryset.get(pk=pk).delete()
                messages.success(self.request, '게시글이 삭제 되었습니다.')
        
        
        return HttpResponseRedirect('/article/')

#@method_decorator(csrf_exempt, name='dispatch') #모든 핸들러 예외 처리
class ArticleCreateUpdateView(TemplateView):  # 게시글 추가, 수정
    #LoginRequiredMixin
    #login_url = settings.LOGIN_URL # 원래 로그인 안한사람들 막으려면 써야되는것 LoginRequireMixin 과 같이
    template_name = 'article_update.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        print(queryset.filter(pk=pk).first())
        return queryset.filter(pk=pk).first()
        #if pk and not article:
        #    raise Http404('invalid pk')
        #elif article.author != self.request.user:                             # 작성자가 수정하려는 사용자와 다른 경우
        #    raise Http404('invalid user')
        #return article
    def get(self, request, *args, **kwargs):    #화면 요청
        article = self.get_object()
        flag = article
        if article is None:
            article = self.queryset.filter(pk=DEFAULT_ARTICLE).first()
    
        form = ArticleForm(instance = article) #######이렇게 하면 편집기에 나옴.....instance라는 속성에 위에서 미리 지정해놓은 글의 객체를 설정

        ctx = {
            'article' : flag,
            'form' : form
        }
        
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs): # 액션
        form = ArticleForm()
        #print(request.POST)
        action = request.POST.get('action')           # request.POST 객체에서 데이터 얻기
 
        ##### 로그인 안되면 3개 로그인 되어있으면 2개 넘기면 될듯
        if not request.user.is_authenticated :
            #print(request.POST.get('content'))
            post_data = {key: request.POST.get(key) for key in ('title', 'content','author')}

            for key in post_data:
                if not post_data[key]:
                    messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger')
                    return HttpResponseRedirect('.')

            if len(messages.get_messages(request)) == 0:
                if action == 'create':
                    article = Article.objects.create(**post_data)                    
                    messages.success(self.request, '게시글이 저장되었습니다.')
                elif action == 'update':
                    article = self.get_object()
                    for key, value in post_data.items():
                        setattr(article, key, value)

                        article.save()
                    messages.success(self.request, '게시글이 저장되었습니다.')
                else:
                    messages.error(self.request, '알 수 없는 요청입니다.', extra_tags='danger')

                return HttpResponseRedirect('/article/' + str(article.id) + '/update/') # 정상적인 저장이 완료되면 '/article/'로 이동됨

            ctx = {
                'article': self.get_object() if action == 'update' else None,
                'form' : form
            }
        else:
            post_data = {key: request.POST.get(key) for key in ('title', 'content')}
            post_data['author'] = self.request.user
            print(post_data)
            for key in post_data:                         # 세가지 데이터 모두 있어야 통과 --> #2가지로 변경
                if not post_data[key]:
                #raise Http404('no data for {}'.format(key))
                    messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger') # error 레벨로 메시지 저장
            
                                        # 작성자를 현재 사용자로 설정

            if len(messages.get_messages(request)) == 0:      #메세지가 있다면 아무것도 처리하지 않음
                
                if action == 'create':                        # action이 create일 경우
                    #article = Article.objects.create(title=title, content=content, author=author)
                    article = Article.objects.create(**post_data)
                    messages.success(self.request, '게시글이 저장 되었습니다')    # success 레벨로 메세지 저장
                    return HttpResponseRedirect('/article/')
                elif action == 'update':                      # action이 update일 경우
                    article = self.get_object()
                    if article.author == self.request.user:
                        #article = self.get_object()
                        #if not article:
                        #    raise Http404('invalid article_id')
                        for key, value in post_data.items():
                            setattr(article, key, value)
                        #article = form.save()
                        article.save()
                        messages.success(self.request, '게시글이 저장되었습니다.')
                    else:
                        messages.error(self.request, '본인이 작성한 글이 아닙니다' , extra_tags='danger')
                else:                                         # action이 없거나 create, update 중 하나가 아닐 경우
                    #raise Http404('invalid action')
                    messages.error(self.request, '알 수 없는 요청입니다.', extra_tags='danger')         #error 레벨로 메시지 저장
                
                return HttpResponseRedirect('.') # 정상적인 저장이 완료되면 '/articles/'로 이동됨

            ctx = {
                #'view':self.__class__.__name__,
                #'data':article
                'action' : 'update',
                'article' : self.get_object() if action == 'update' else None,                   # if else 삼항 문법
                'form' : form
            }
            

        return self.render_to_response(ctx)
        
#class IndexView(ListView):  # 페이징
#    models = Article
#    paginate_by = 10

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