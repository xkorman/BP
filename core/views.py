from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from core.models import Questions

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .forms import RequestInfoForm

class InfoView(TemplateView):
    template_name = 'home.html'


def index(request):
    return HttpResponse(template='index.html')


def faq(request):
    questions = Questions.objects.all().order_by('id')
    return render(request, 'faq.html', {'questions': questions})


def render_pdf_view(data):
    html_string = render_to_string('ziadost_info.html', {'data': data})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="mypdf.pdf"'
        return response
    return response


def get_request_data(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RequestInfoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.data
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render_pdf_view(data)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = RequestInfoForm()

    return render(request, 'ziadost_info_get_data.html', {'form': form})