import os
import io
import lasio
import base64
import urllib
import numpy as np
import matplotlib.pyplot as plt

from django.views.generic import TemplateView
from django.http import HttpResponse

DATA_ROOT = '/home/apgcegeohack/notebooks/data/'
LAS_ROOT = DATA_ROOT + 'PETROPHYSICS/'
SEGY_ROOT = DATA_ROOT + 'SEISMIC/'

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_folder'] = os.listdir(DATA_ROOT)
        return context

def generate_las_data():
    all_las_files = os.listdir(LAS_ROOT)
    return sorted(all_las_files)

class LasView(TemplateView):
    template_name = 'las.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filename = self.request.GET.get('select', None)
        if filename:
            las = lasio.read(LAS_ROOT + filename)
            plt.plot(las["GR"], las.index)
            fig = plt.gcf()
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            context['chart'] = uri

        context['las_data'] = generate_las_data()
        return context

def get_segy_folders():
    all_segy_folders = dict()
    file_option_string = ''
    list_dir = os.listdir(SEGY_ROOT)
    for l in list_dir:
        all_files = os.listdir(SEGY_ROOT + '/' + l)
        for f in all_files:
            file_option_string += '<option value="{}">{}</option>'.format(f, f)
        all_segy_folders[l] = file_option_string
    print('segy_folders: {}'.format(all_segy_folders))
    return all_segy_folders

class SegyView(TemplateView):
    template_name = 'segy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print('segy root: {}'.format(SEGY_ROOT))
        context['segy_folders'] = get_segy_folders()
        return context