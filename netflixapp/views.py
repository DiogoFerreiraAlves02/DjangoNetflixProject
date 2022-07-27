from django.shortcuts import redirect, render
from django.views import View
import imp
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ProfileForm
from requests import request
from .models import Movie, Profile

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('netflixapp:profile-list')
        return render(request, 'index.html')


method_decorator(login_required, name='dispatch')
class ProfileList(View):
    def get(self, request, *args, **kwargs):
        try:
            profiles = request.user.profiles.all()
            context = {
                'profiles':profiles
            }
            return render(request, 'profilelist.html',context)
        except:
            return redirect('netflixapp:Home')

method_decorator(login_required, name='dispatch')
class ProfileCreate(View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm()
        context = {
            'form':form
        }
        return render(request, 'profilecreate.html',context)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        
        if form.is_valid():
            profile=Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect('netflixapp:profile-list')
                
        context = {
            'form':form
        }
        return render(request, 'profilecreate.html',context)

method_decorator(login_required, name='dispatch')
class MovieList(View):
    def get(self, request, profile_id, *args, **kwargs):
        try:
            profile = Profile.objects.get(uuid=profile_id)
            if profile not in request.user.profiles.all():
                return redirect('netflixapp:profile-list')

            if profile.age_limit == "All" :
                movies = Movie.objects.filter()
            else:
                 movies = Movie.objects.filter(age_limit=profile.age_limit)

            context = {
            'movies':movies
            }

            return render(request, 'movielist.html', context)
        except Profile.DoesNotExist:
            return redirect('netflixapp:profile-list') 

method_decorator(login_required, name='dispatch')
class MovieDetail(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            num_visits = request.session.get('num_visits', 1)
            request.session['num_visits'] = num_visits + 1
            context = {
                'movie':movie,
                'num_visits': num_visits
            }

            return render(request, 'moviedetail.html', context)
        except Movie.DoesNotExist:
            return redirect('netflixapp:profile-list')

method_decorator(login_required, name='dispatch')
class PlayMovie(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            movie = movie.video.values()
            
            context = {
                'movie':list(movie)
            }

            return render(request, 'playmovie.html', context)
        except Movie.DoesNotExist:
            return redirect('netflixapp:profile-list')

method_decorator(login_required, name='dispatch')
class PlayMovieLow(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            movie = movie.lowVideo.values()
            
            context = {
                'movie':list(movie)
            }

            return render(request, 'playmovielow.html', context)
        except Movie.DoesNotExist:
            return redirect('netflixapp:profile-list')