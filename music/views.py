from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Album,Song
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
import os
from django.http import Http404
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/music/login/')
def index(request):
	all_albums = Album.objects.all()
	return render(request,'music/index.html', {'all_albums': all_albums})


class DetailView(generic.DetailView):
	model = Album
	template_name = 'music/detail.html'

class AlbumCreate(CreateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']

class SongCreate(CreateView):
	model = Song
	fields = ['album', 'song_title', 'song']

class AlbumUpdate(UpdateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
	model = Album
	success_url= reverse_lazy('music:index')


# register a new user
class UserFormView(View):
	form_class = UserForm
	template_name = 'music/registration_form.html'

	def get(self,request):
		form = self.form_class(None)
		return render(request, self.template_name,{'form': form})

	
	def post(self,request):
		form = self.form_class(request.POST)
	
		if form.is_valid():

			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()


			user = authenticate(username = username, password = password)

			if user is not None:

				if user.is_active :
					login(request, user)
					all_albums = Album.objects.all
					return redirect('music:index')
	
		
		return render(request, self.template_name,{'form': form})

# download a song
def download(request, song_id):
	song = Song.objects.get(pk=song_id)
	path = song.filename()
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="mp3")
			response['Content-Type'] = 'audio/mp3'
			response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
			return response
	raise Http404

# play a song
def play(request, song_id):
	song = Song.objects.get(pk=song_id)	
	path = song.filename()
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="mp3")
			response['Content-Type'] = 'audio/mp3'
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	raise Http404

# delete a song
def song_delete(request, song_id):
	instance = Song.objects.get(pk=song_id)	
	album_id = instance.album.pk
	path = instance.filename()
	instance.delete()
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	os.remove(file_path)
	return redirect('music:detail',  pk = album_id)

# login form
def login_user(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(username = username, password = password)

		if user is not None:
			if user.is_active:
				login(request, user)
				all_albums = Album.objects.all
				return redirect('music:index')
			else:
				return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'music/login.html', {'error_message': 'Invalid login'})
	return render(request, 'music/login.html')



# logout user
def logout_user(request):
	logout(request)

	return render(request, 'music/login.html')


#index
#def index(request):
	#all_albums = Album.objects.filter(user=request.user)
	#return render(request,'music/index.html', {'all_abums': all_albums})

	
#	class IndexView(generic.ListView):
#		template_name ='music/index.html'
#		context_object_name = 'all_albums'
#		def get_queryset(self):
#			return Album.objects.filter(user=request.user)

