import os

from app.utils import report_analysis
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response


class DocumentView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        if file := request.FILES['myfile']:
            name, extension = os.path.splitext(file.name)
            if extension != '.xlsx':
                return Response(
                    {'error': 'Принимает только xlsx формат.'},
                    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                )
            path_filename, filename, file = report_analysis(file)

            try:
                with open(path_filename, 'rb') as file:
                    response = HttpResponse(file.read(), content_type='xlsx', charset='utf-8')
                    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
                    response['Content-Length'] = os.path.getsize(path_filename)
                    return response
            finally:
                os.remove(path_filename)

        return render(request, 'index.html')
