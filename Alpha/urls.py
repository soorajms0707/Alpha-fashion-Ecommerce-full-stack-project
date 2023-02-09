from django.urls import path
from .views import *

urlpatterns = [
    path('',index),
    path('contact/',contact),
    path('about/',about),
    path('registration/',registration),
    path('login/',login),
    path('shop/<username>',shop),
    path('upload/<username>',upload),
    path('uploaddisplay/',uploaddisplay),
    path('uploaddelete/<int:id>',uploaddelete),
    path('uploadedit/<int:id>',uploadedit),
    path('profileedit/<username>', profileedit),
    path('userreg/',userreg),
    path('verify/<auth_token>', verify),
    path('userlogin/',userlogin),
    path('user/<username>',user),
    path('cart/<username>/<int:id>',cart),
    path('cartdisplay/<username>',cartdisplay),
    path('cartdelete/<username>/<int:id>',cartdelete),
    path('buy/<username>/<int:id>',buy),
    path('useredit/<username>',useredit),
    path('email/',email_send)




]