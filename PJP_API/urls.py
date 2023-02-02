from django.urls import path
from . import views

urlpatterns = [


    path('', views.apiOverview, name="api-overview"),

    path('message_list', views.messageList, name='message_list'),
    path('message_list/<str:pk>', views.messageDetail, name='message_list'),
    path('message_create', views.messageCreate, name='message_create'),
    path('message_update/<str:pk>', views.messageUpdate, name='message_update'),
    path('message_delete/<str:pk>', views.messageDelete, name='message_delete'),

    path('ai_list', views.aiList, name='ai_list'),
    path('ai_list/<str:pk>', views.aiDetail, name='ai_list'),
    path('ai_create', views.aiCreate, name='ai_create'),
    path('ai_update/<str:pk>', views.aiUpdate, name='ai_update'),
    path('ai_delete/<str:pk>', views.aiDelete, name='ai_delete'),

    path('ai_signal', views.AiSignal, name='ai_signal'),

    path('mes_ai', views.myAiList, name='mes_ai'),

    path('ai_search/', views.aiSearch, name='ai_search'),
    path('ai_search_mixte/', views.aiSearchMixte, name='ai_search_mixte'),

    path('favories_list', views.favorieList, name='favories_list'),

    path("login", views.logIn, name='log in'),
    path("signup", views.signUp, name='Sign Up')
]
