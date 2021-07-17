from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import loader
from django.urls import reverse
from tpblite import TPB
from tpblite import ORDERS, CATEGORIES
import requests
from django.conf import settings
from django.shortcuts import redirect
from .forms import SearchForm, DownloadForm
from synology_api import downloadstation
from djangobay.settings import SYNOLOGY


@login_required
def search(request, genre=None):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            t = TPB()
            title = form.cleaned_data['title']
            if genre == "movies":
                torrents = t.search(title, order=ORDERS.SEEDERS.DES, category=CATEGORIES.VIDEO.HD_MOVIES)
            if genre == "series":
                torrents = t.search(title, order=ORDERS.SEEDERS.DES, category=CATEGORIES.VIDEO.HD_TV_SHOWS)
            return render(request, 'torrents/search.html', {'form': form, 'torrents': serialize_torrents(torrents), 'genre': genre})
    else:
        form = SearchForm()
    

    return render(request, 'torrents/search.html', {'form': form})


@login_required
def download(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DownloadForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            dwn = downloadstation.DownloadStation(SYNOLOGY['host'], SYNOLOGY['port'], SYNOLOGY['username'], SYNOLOGY['password'])
            magnet = form.cleaned_data['magnet']
            destination = '/homes/aixemple/downloads/'+form.cleaned_data['genre']
            dwn.create_uri_task(magnet,{'destination':destination})
        else:
            print(form.errors)
    return HttpResponseRedirect(reverse('torrents:downloading'))


@login_required
def downloading(request):
    dwn = downloadstation.DownloadStation(SYNOLOGY['host'], SYNOLOGY['port'], SYNOLOGY['username'], SYNOLOGY['password'])
    tasks_list = dwn.tasks_list()['data']['tasks']
    return render(request, 'torrents/downloading.html', {'tasks_list':tasks_list})


def logout_view(request):
    logout(request)
    return redirect('%s' % (settings.LOGIN_URL))

def view_404(request, exception=None):
    return redirect('/')

def serialize_torrents(torrents):
    torrents_json = []
    for torrent in torrents:
        row = {
            "title": torrent.title,
            "seeds": torrent.seeds,
            "leeches": torrent.leeches,
            "upload_date": torrent.upload_date,
            "uploader": torrent.uploader,
            "filesize": torrent.filesize,
            "byte_size": torrent.byte_size,
            "magnetlink": torrent.magnetlink,
            "url": torrent.url,
            "is_trusted": torrent.is_trusted,
            "is_vip": torrent.is_vip,
            "infohash": torrent.infohash,
            "category": torrent.category
        }
        torrents_json.append(row)
    return torrents_json