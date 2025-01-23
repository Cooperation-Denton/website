from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from blog import views
from .feeds import BlogFeeds

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('new_post/', views.new_post, name='new_post'),
    path('delete_blog_post/<slug:slug>/',
         views.delete_post, name='delete_blog_post'),
    path('blog/<slug:slug>', views.post_details, name='post_details'),
    path('rss.xml', BlogFeeds(), name="blog_feed"),
    path('contact/', views.contact, name='contact'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
