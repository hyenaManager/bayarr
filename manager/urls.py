from django.urls import path

from . import views

urlpatterns = [
    path('home',views.home,name='home'),
    path('login',views.login_view,name='login'),
    path('register',views.register_form,name='register'),
    path('graph<str:monthInput>',views.graph,name='graph'),
    path('data',views.data,name='data'),
    path('getStart',views.getStart,name='getStarted'),
    path('register_user',views.register_user,name='register_user'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('login_user',views.login_user,name='login_user'),
    path('addData',views.addData,name='addData'),
    path('dataDel',views.dataDel,name='dataDel'),
    path('dataToEdit<int:id>',views.dataToEdit,name='dataToEdit'),
    path('updateExData',views.updateExData,name='updateExData'),
    path('history',views.history,name='history'),
    #path('sendMail',views.sendMail,name='sendmail'),
    path('resetPassword',views.reset_password,name='reset_password'),
    path('addPswd',views.addPswd,name='addPswd'),
    path('idUser',views.idUser,name='idUser'),
    path('dataEdit',views.dataEdit,name='dataEdit'),
    path('dataToFill<int:id>',views.dataToFill,name='dataToFill'),
    path('dataFill',views.dataFill,name='dataFill'),
    path('delOp<int:id>',views.del_op,name='delOption'),
    path('csv_data',views.csv_data,name='cvsData'),
    path('developerContact',views.devContact,name='developerContact')
]