from django.urls import path
from .views import *


urlpatterns = [
    ###### SERIES RELATED #####
    #path('series/<str:slug>/', SeriesDetail.as_view(), name="series_detail"),
    ###### SERIES RELATED END HERE ######

    ###### BLOG RELATED #########
    path('create-blog/', BlogCreate.as_view(), name="blog_create"),
    path('', BlogList.as_view(), name="blog_list"),#Blog List
    path('<int:pk>/', BlogDetail.as_view(), name="blog_detail"),#Blog Details
    path('category/<str:slug>/', BlogCategory.as_view(), name="blog_category"),#Category
    
    path('<int:pk>/update/', BlogUpdate.as_view(), name="blog_update"),# Blog Update
    path('<int:pk>/delete/', blogDelete, name="blog_delete"),#Blog Delete
    path('<int:pk>/like/', likeBlog, name="likeBlog"),#Upvote/Like Blog
    path('<int:pk>/dislike/', disLikeBlog, name="disLikeBlog"),#DownVote/dislike
]