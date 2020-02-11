# -*- coding: utf-8 -*-

#from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from accounts.models import User

from accounts.forms import UserRegistrationForm, LoginForm

from django.contrib import messages

from django.contrib.auth.forms import UserChangeForm


#def index_view(request):                                                       -> 바로 url 넘기는 방법 
#    return HttpResponseRedirect('/accounts/login/')

class UserRegistrationView(CreateView):                                         #회원가입
    #model = User                                                               # 자동생성 폼에서 사용할 모델
    #fields = ('email', 'name', 'password','phone','birth_date','date_joined')  # 자동생성 폼에서 사용할 필드
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = '/article/'

class UserLoginView(LoginView):                                                 # 로그인
    authentication_form = LoginForm
    template_name = 'accounts/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super(UserLoginView,self).form_invalid(form) ############# python2에서 super(UserLoginView,self) 넣어줘야된다!!!! 아니면 안됨!
                                                            # python3에서는 super안에() 이렇게 해주면됨!




#FCV
#def update(request):
#    user_change_form = UserChangeForm(instance = request.user)
#    return render(request, 'accounts/mypage_form.html', {'user_change_form':user_change_form})



    