from django.urls import path

from . import views

urlpatterns = [
    path("", views.CaseView.as_view(), name = 'lol'),
    path("about/", views.IndexView.as_view(), name = 'about'),
    path("contract/", views.IndexView1.as_view(), name = 'contract'),
    path("addbalance/", views.IndexView2.as_view(), name = 'addbalance'),
    path("caseout/", views.IndexView3.as_view(), name = 'caseout'),
    path("loginsteam/", views.IndexView5.as_view(), name = 'loginsteam'),
    path("faq/", views.IndexView6.as_view(), name = 'faq'),
    path("coockie/", views.IndexView7.as_view(), name = 'coockie'),
    path("agreement/", views.IndexView8.as_view(), name = 'agreement'),
    path("contacts/", views.ContactsView.as_view(), name = 'contacts'),
    path("livetrade/", views.IndexView9.as_view(), name = 'livetrade'),
    path("register/", views.RegisterView.as_view(), name = 'register'),
    path("login/", views.LoginView.as_view(), name = 'login'),
    path("user/<str:pk>/", views.UserDetailView.as_view(), name = 'user_detail'),
    path("item/<slug:slug>/", views.ItemView.as_view(), name = 'item_detail'),
    path("case/<slug:slug>/", views.CaseDetailView.as_view(), name="case_detail"),
    path("myprofile/", views.Profilevies.as_view(), name = 'me'),
    path("logout/", views.LogoutView.as_view(), name = 'logout'),
]