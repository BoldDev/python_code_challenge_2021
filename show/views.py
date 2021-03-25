from datetime import datetime

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
import json

import requests

from show.models import Show, Episode, Season




def index(request):
    return render(request, 'index.html')
