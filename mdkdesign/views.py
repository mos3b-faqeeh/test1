from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from sklearn.feature_extraction.text import CountVectorizer


import requests
import json
import pandas as pd
import numpy as np

import pdb;



def mdkHome(request):
    return render (request,'mdkHome.html')

