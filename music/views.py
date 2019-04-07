from django.shortcuts import render, get_object_or_404
from . models import Album, Song
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AlbumForm, SongForm, UserForm
from django.views.generic import UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='music:login')
def index(request):
    albums = Album.objects.all()
    return render(request, 'music/index.html', {'albums': albums})

def detail(request, album_id):
     album = get_object_or_404(Album, pk=album_id)
     return render(request, 'music/detail.html', {'album': album})


def create_album(request):
    form = AlbumForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        albums = Album.objects.all()
        for album in albums:
            if album.album_name == form.cleaned_data.get('album_name'):
                context = {
                    'form': form,
                    'message': 'Album already exists'
                }
                return render(render,'music/create_album.html', context())
        album = form.save(commit=False)
        album.album_cover = request.FILES['album_cover']
        album.save()
        return render(request, 'music/detail.html', {'album': album})
    return render(request, 'music/create_album.html', {'form': form})

class AlbumUpdateView(UpdateView):
    model = Album
    fields = ['album_name', 'artist_name', 'album_genre']
    template_name = 'music/create_album.html'




def album_delete(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    album.delete()
    return redirect('/')

def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        for s in album.song_set.all():
            if s.song_name == form.cleaned_data('song_name'):
                contex = {
                    'form': form,
                    'message': 'Song already exist'
                }
                return render(render, 'music/create_song.html', contex())
        song = form.save(commit=False)
        song.album = album
        song.song_audio = request.FILES['song_audio']
        song.save()
        contex = {
            'album': album,
            'message': 'Song Created Successfully'
        }
        return render(request, 'music/detail.html', {'album': album})


    return render(request, 'music/create_song.html', {'form':form})



class SongUpdateView(UpdateView):
    model = Song
    fields = ['song_name', 'song_audio']
    template_name = 'music/create_song.html'

def delete_song(request,album_id, song_id):
        album = get_object_or_404(Album, pk=album_id)
        song = get_object_or_404(Song, pk=song_id)
        song.delete()
        context = {
            'album': album,
            'message': 'Song Deleted Successfully'

        }
        return render(request, 'music/detail.html', context())



def signup(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('music:index')
    return render(request, 'registration/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        # if user.is_active:
        login(request, user)
        return redirect('music:index')
       # return render(request, 'registraion/login.html', {'message': 'Account deactivate'})
    return render(request, 'registration/login.html')


def logout_user(request):
    logout(request)
    context = {
        'message': 'Logged Out'
    }
    return render(request,'registration/login.html')