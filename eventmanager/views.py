from django.contrib import auth
import datetime
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.utils import translation
from django.shortcuts import redirect
from django.conf import settings

from django.http import JsonResponse, HttpResponse


from . import forms
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import permission_required


@permission_required('project.can_mark_returned', raise_exception=True)
def test(request):
    return HttpResponse(request.user.has_perm('project.can_mark_returned'))


# @cache_page(60 * 1)
# def test2(request):
#     return HttpResponse('cached-'+datetime.datetime.now() )


class LoginViewExt(auth_views.LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['langs'] = settings.LANGUAGES
        context['lang'] = translation.get_language()
        return context

 
    def post(self, request, *args, **kwargs):
        set_language(request)
        return super().post(request, *args, **kwargs)
 


class LogoutViewExt(auth_views.LogoutView):
    template_name = 'registration/logged_out.html'


def index(request):
    if request.user and request.user.is_authenticated:
        return redirect('/app')

    return redirect('/accounts/login')  # login(request)

def set_language(request):
    #django.views.i18n.set_language()
    user_language = request.POST.get(
        'lang', request.GET.get('lang', settings.LANGUAGE_CODE))
 
    if translation.check_for_language(user_language):
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        #request.COOKIES[settings.LANGUAGE_COOKIE_NAME] = user_language
        return ''
 
    return 'Lang not defined'


# def logout(request):
#     #if request.user and request.user.is_authenticated:
#     auth.logout(request)
#     return redirect('/')


# def login(request):
#     form = None

#     has_err = True
#     msg = ''

#     try:
#         if request.method == 'POST':

#             form = forms.LoginForm(request.POST)
#             if form.is_valid():
#                 username = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password')

#                 user = auth.authenticate(username=username, password=password)
#                 if user is not None:
#                     auth.login(request, user)
#                     return redirect('/') #go to main again or may be to menu
#                 else:
#                     msg = 'User Name or Password not valid'

#             else:
#                msg = form.errors.get('__all__')[0]
#         else:
#             has_err = False
#             form = forms.LoginForm()
#     except:
#         msg = 'Error'
#     finally:
#         pass

#     if has_err and not msg:
#         msg = 'Log In Error'

#     form.message = msg

#     return render(request, 'login.html', {'form': form})

@login_required(login_url='/accounts/login', redirect_field_name='')
def app(request):
    return render(request, 'app.html', {'username': request.user.username})
