from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404, \
    HttpResponse, HttpResponseServerError
from django.urls import reverse
from django.conf import settings
from django.core.files import File
from .models import BalanceSheet
from .utils import convert_pdf_to_csv, save_dataframe_to_db
from django.views.decorators.csrf import csrf_exempt

import os


def home(request):
    return render(request, 'balance_sheeter/home.html')


@csrf_exempt
def save_and_return(request):
    try:
        var = str(request.POST['query_variable'])
        year = int(request.POST['query_year'])
        file = request.FILES['file']
    except KeyError:
        return HttpResponseBadRequest("Missing data")
    except (ValueError, SyntaxError):
        return HttpResponseBadRequest("Incorrect data")

    temp_file = os.path.join(settings.MEDIA_ROOT, 'temp')
    with open(temp_file, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # Create csv
    df, csv_file_name = convert_pdf_to_csv(temp_file)

    if df is None:
        return HttpResponseBadRequest("Incorrect data")

    if csv_file_name is None:
        return HttpResponseServerError("File saving failed. Please try again.")

    # Save data to db
    save_dataframe_to_db(df)

    # Query db for required value
    var = var.lower()
    b = BalanceSheet.objects.filter(variable__iexact=var, year=year).first()

    if not b:
        return Http404("Variable and year combination not found")

    url_params = '?' + 'value=' + b.value + '&' + 'filename=' + csv_file_name
    return HttpResponseRedirect(reverse('results') + url_params)


def results(request):
    try:
        context = {
            'value': request.GET['value'],
            'filename': request.GET['filename']
        }
    except KeyError:
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'balance_sheeter/results.html', context)


def download(request):
    filename = request.GET['filename']
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    f = File(open(filepath, 'r'))
    response = HttpResponse(f, content_type='application/force-download')
    response[
        'Content-Disposition'] = 'attachment; filename=' + filename + '.csv'
    return response
