from django.conf.urls import include,url
from django.contrib.auth.decorators import login_required, permission_required
from . import views

app_name = 'music'


urlpatterns = [
    # /music/
    url('^$', views.index, name='index'),

    # /music/register
    url('^register/$', views.UserFormView.as_view(), name='register'),
    # /music/721/
    url('^(?P<pk>[0-9]+)/$',login_required(views.DetailView.as_view()), name='detail'),

    # /music/song/add
    url('^song/add/$',login_required(views.SongCreate.as_view()), name='song-add'),

    # /music/album/add/
    url('album/add/$', login_required(views.AlbumCreate.as_view()), name='album-add'),

    # /music/album/2/
    url('album/(?P<pk>[0-9]+)/$', login_required(views.AlbumUpdate.as_view()), name='album-update'),

    # /music/album/2/delete
    url('album/(?P<pk>[0-9]+)/delete/$', login_required(views.AlbumDelete.as_view()), name='album-delete'),

    # /music/song/2/delete
    url('song/(?P<song_id>[0-9]+)/delete/$', views.song_delete, name='song-delete'),

    #/music/song/1/download
    url('song/(?P<song_id>[0-9]+)/download/$',views.download, name='download'),

    #/music/song/1/
    url('song/(?P<song_id>[0-9]+)/$',views.play, name='play'),

    # /music/login
    url('^login/$', views.login_user, name='login'),

    # /music/logout
    url('^logout/$', views.logout_user, name='logout'),
]