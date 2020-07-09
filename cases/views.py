from django.conf import settings
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
import os
from random import choices

from roulete.settings import BASE_DIR
from .models import Case, Items, User_info, Category, Casesitems, Useritems


def handle_uploaded_file(f):
    with open('../media/avatars/newava.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class CaseView(ListView):
    model = Case
    context_object_name = 'all'
    template_name = "case_list.html"

    def get_queryset(self):
        queryset = {'cases': Case.objects.all(),
                    'category': Category.objects.all()}
        return queryset

class IndexView(View):
    def get(self,request):
        return render(request, 'about.html')

    def post(self, request):
        if request.is_ajax():
            qs = Case.objects.all().distinct().values("name","case_image")
            queryset = list(qs)
            return JsonResponse({"casesse": queryset}, safe=False)

class IndexView1(View):
    def get(self,request):
        return render(request, 'contract.html')

    def post(self, request):
        if request.is_ajax():
            chto =  request.POST.get('id')
            case = Casesitems.objects.filter(case=chto).all()
            items = []
            weightes = []
            for el in case:
                items.append(el.item)
                weightes.append(el.item_droprate)
            items_name = []
            for el in items:
                items_name.append(el.name)
            a = choices(items_name, weightes)
            #----часть рандома--------#
            casepr = Case.objects.get(id=chto).price
            m = User_info.objects.get(user_id=request.user.id).balance
            new_balance = m - casepr
            user = User_info.objects.get(user_id=request.user.id)
            user.balance = new_balance
            user.save()
            #---изменение баланса---#
            vaipitem = Items.objects.get(name=a[0])
            f = vaipitem.id
            prcs = Casesitems.objects.get(case=chto,item=f)
            am = prcs.amount
            neam = am - 1
            if neam == 0:
                prcs.delete()
            else:
                prcs.amount = neam
                prcs.save()
            #-----Уменьшнние колва------#
            try:
                vaipitem = Items.objects.get(name=a[0])
                f = Useritems.objects.get(user=request.user.user_info,item=vaipitem)
                am = f.amount
                newam = am + 1
                f.amount = newam
                f.save()
            except Exception as E:
                print(E)
                Useritems.objects.create(user=request.user.user_info,item=vaipitem,amount=1)
            #-----Добавление предмета-----#
            item = Items.objects.get(name=a[0])
            #-----Данные итема-----#
            opacha = []
            rtm = Casesitems.objects.filter(case=chto).all()
            for el in rtm:
                opacha.append(el.item.name)
            ind = opacha.index(a[0])
            print(a)
            return JsonResponse({'name':a,'newbalance':new_balance,'img':item.item_image.url,'price':item.price,'ind':ind   },safe=False)


class IndexView2(View):
    def get(self,request):
        return render(request, 'balance.html')

    def post(self, request):
        if request.is_ajax():
            itm = Items.objects.get(name=request.POST['name'])
            item = Useritems.objects.get(user=request.user.user_info,item=itm)
            casepr = item.item.price
            m = User_info.objects.get(user_id=request.user.id).balance
            new_balance = m + casepr
            user = User_info.objects.get(user_id=request.user.id)
            user.balance = new_balance
            user.save()
            #-----Увеличить баланс-----#
            if int(item.amount) == 1:
                item.delete()
            else:
                a = item.amount - 1
                item.amount = a
                item.save()
            return JsonResponse('asd',safe=False)

class IndexView3(View):
    def get(self,request):
        return render(request, 'caseout.html')

class ContactsView(View):
    def get(self,request):
        return render(request, 'contact.html')

    def post(self, request):
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('from_email', '')
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ['goloslana245@gmail.com'])
                messages.add_message(request, messages.INFO, 'Ваше сообщение успешно отправлено!\nОжидайте ответа')
                return redirect('lol')
            except Exception as E:
                E = str(E)
                f = E.find(']')
                f = int(f) + 1
                E = E[f:]
                messages.add_message(request, messages.INFO, 'Что-то пошло не так!\n'+str(E))
                return redirect('contacts')
        else:
            messages.add_message(request, messages.INFO, 'Заполните все поля!')
            return redirect('contacts')

class IndexView5(View):
    def get(self,request):
        return render(request, 'about.html')

class IndexView6(View):
    def get(self,request):
        return render(request, 'faq.html')

class IndexView7(View):
    def get(self,request):
        return render(request, 'coockies.html')

class IndexView8(View):
    def get(self,request):
        return render(request, 'agreement.html')

class IndexView9(View):
    def get(self,request):
        return render(request, 'livetrades.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if username == '' and password == '':
            messages.add_message(request, messages.INFO, 'Введите логин и пароль!')
            return redirect('login')
        elif username == '':
            messages.add_message(request, messages.INFO, 'Введите логин!')
            return render(request, 'login.html')
        elif password == '':
            messages.add_message(request, messages.INFO, 'Введите пароль!')
            return render(request, 'login.html')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.INFO, 'Вы успешно вошли')
                return redirect('lol')
            else:
                messages.add_message(request, messages.INFO, 'Проверьте правильность введенных данных!')
                return redirect('login')

class Profilevies(View):
    def get(self, request):
        if str(request.user) == 'AnonymousUser':
            messages.add_message(request, messages.INFO, 'Чтобы смотреть профиль зарегестрируйтесь или войдите!')
            return redirect('register')
        else:
            return render(request, 'me.html')

    def post(self, request):
        try:
            f = request.FILES['ava']
            f = str(f)
            if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.psd'):
                m = User_info.objects.get(user_id=request.user.id)
                m.avatar = request.FILES['ava']
                m.save()
                messages.add_message(request, messages.INFO, 'Аватарка успешно добавлена!')
                return redirect('me')
            else:
                messages.add_message(request, messages.INFO, 'Неподдерживаемый формат!\nПоддерживаются: png,jpg,jpeg,psd')
                return redirect('me')
        except Exception as E:
            print(E)
            username = request.POST['username']
            mdl = User.objects.filter(username=username).all()
            if username == '':
                messages.add_message(request, messages.INFO, 'Введите логин!')
                return redirect('me')
            elif str(username) == request.user.username:
                messages.add_message(request, messages.INFO, 'Это ваш текущий логин!')
                return redirect('me')
            elif int(len(str(username))) > 149:
                messages.add_message(request, messages.INFO, 'Максимальная длинна логин 150 символов!')
                return redirect('me')
            elif not str(mdl) == '<QuerySet []>':
                messages.add_message(request, messages.INFO, 'Логин уже занят!Используйте другой логин!')
                return redirect('me')
            else:
                user = User.objects.select_for_update().filter(username=request.user.username).update(username=username)
                messages.add_message(request, messages.INFO, 'Логин успешно изменен!')
                return redirect('me')

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.INFO, 'Вы успешно вышли')
        return redirect('lol')

class RegisterView(View):
    def get(self, request):
            return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        mdl = User.objects.filter(username=username).all()
        if username == '' and password1 == '':
            messages.add_message(request, messages.INFO, 'Введите логин и пароль!')
            return redirect('register')
        elif username == '':
            messages.add_message(request, messages.INFO, 'Введите логин!')
            return redirect('register')
        elif not str(mdl) == '<QuerySet []>':
            messages.add_message(request, messages.INFO, 'Логин уже занят!Используйте другой логин!')
            return redirect('register')
        elif password1 == '':
            messages.add_message(request, messages.INFO, 'Введите пароль!')
            return redirect('register')
        elif str(password1) != str(password2):
            messages.add_message(request, messages.INFO, 'Пароли не совпадают!')
            return redirect('register')
        else:
            user = User.objects.create_user(username, '',password1)
            user.save()
            user_info = User_info.objects.create(avatar=None,balance=0,user=user)
            user_info.save()
            messages.add_message(request, messages.INFO, 'Регистрация прошла успешно!Теперь войдите в аккаунт!')
            return redirect('login')

class CaseDetailView(DetailView):
    """Полное описание фильма"""
    model = Case
    queryset = Case.objects.all()
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UserDetailView(DetailView):
    """Полное описание фильма"""
    model = User
    queryset = User.objects.all()
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ItemView(DetailView):
    """Полное описание фильма"""
    model = Items
    queryset = Items.objects.all()
    template_name = 'item_detail.html'
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
