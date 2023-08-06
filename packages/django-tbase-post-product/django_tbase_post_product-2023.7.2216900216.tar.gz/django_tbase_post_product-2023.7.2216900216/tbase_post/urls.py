from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from .sitemaps import PostSitemap
from . import views
sitemaps = {
    'posts': PostSitemap,
}
urlpatterns = [
    path('', cache_page(60 * 15)(views.IndexView.as_view()), name='detail_index'),
    path('detail/<int:pk>/', cache_page(60 * 15)(views.DetailView.as_view()), name='detail_view'),
    path('tag/<int:pk>/',
         cache_page(60 * 60)(views.TagListView.as_view()),
         name='article_list_by_tag'),
    path('sitemap.xml', 
         sitemap, 
         {'sitemaps': sitemaps}, 
         name='django.contrib.sitemaps.views.sitemap'),  # 网站地图 
    # path('detail/<int:pk>', views.DetailView.as_view(), name='post_view'),
    # path('<int:pk>/', views.PostView.as_view(), name='post'),
]