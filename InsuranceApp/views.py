from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .models import *
import csv
from django.http import HttpResponse

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
import pandas as pd

@api_view()
@permission_classes((AllowAny, ))
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])

def schema_view(request):
    generator = schemas.SchemaGenerator(title='Rest Swagger')
    return Response(generator.get_schema(request=request))

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """
        retrieve:
        Return the given user.

        list:
        Return a list of all the existing users.

        create:
        Create a new user instance.
        """
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
def detaildata(request):
    try:
        agencyid = request.data.get("agencyid")
    except:
        agencyid = -1
    try:
        month = request.data.get("month")
    except:
        month = -1
    try:
        year = request.data.get("year")
    except:
        year = -1
    try:
        state = request.data.get("state")
    except:
        state = -1
    if agencyid == -1 or agencyid == '' or agencyid is None \
        or month == -1 or month == '' or year is None\
        or year == -1 or year == '' or year is None\
        or state == -1 or state == '' or state is None :
        return Response({'result': 'Error! Please provide valid agencyid, month, year, and state'}, status=HTTP_400_BAD_REQUEST)

    data = FactInsurance.objects.filter(AGENCY_DETAILS_ID__AGENCY_ID=agencyid, PERIOD_ID__MONTHS=month, PERIOD_ID__STAT_PROFILE_DATE_YEAR=year, PROD_DETAILS_ID__STATE_ABBR=state)
    result = list(data.values())
    return Response({'result': result}, status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
def detailagencydata(request):
    try:
        agencyid = request.data.get("agencyid")
    except:
        agencyid = -1

    if agencyid == -1 or agencyid == '' or agencyid is None:
        return Response({'result': 'Error! Please provide valid agencyid.'}, status=HTTP_400_BAD_REQUEST)

    data = FactInsurance.objects.filter(AGENCY_DETAILS_ID__AGENCY_ID=agencyid)
    result = list(data.values())
    return Response({'result': result}, status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
def vendorpremium(request):
    try:
        vendor = request.data.get("vendor")
    except:
        vendor = -1
    if vendor == -1:
        return Response({'result': 'Error! Please provide valid vendor.'}, status=HTTP_400_BAD_REQUEST)

    return Response({'result': SummaryVendorwiseInfo(vendor)}, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def stateproductionlinepremium(request):
    return Response({'result': SummaryStateByProductionLineInfo()}, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def csvreportexport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csvreportexport.csv"'

    try:
        startdate = request.query_params.get("startdate")
    except:
        startdate = '1900-01-01'

    try:
        enddate = request.query_params.get("enddate")
    except:
        enddate = '2100-01-01'

    print(startdate)
    print(enddate)

    writer = csv.writer(response)
    writer.writerow(['Production Line', 'Agency Id' 'NB_WRTN_PREM_AMT', 'WRTN_PREM_AMT', 'PREV_WRTN_PREM_AMT', 'PRD_ERND_PREM_AMT'])
    result_temp = FactInsurance.objects.all()
    result = list(result_temp.values('PROD_DETAILS_ID__PROD_LINE', 'AGENCY_DETAILS_ID__AGENCY_ID', 'PERIOD_ID__STAT_PROFILE_DATE_YEAR', 'PERIOD_ID__MONTHS', 'NB_WRTN_PREM_AMT', 'WRTN_PREM_AMT', 'PREV_WRTN_PREM_AMT', 'PRD_ERND_PREM_AMT'))

    df = pd.DataFrame(result)
    print(df.head(5))
    df["PERIOD_ID__MONTHS"] = df.PERIOD_ID__MONTHS.map("{:02}".format)
    df['PERIOD'] = df["PERIOD_ID__STAT_PROFILE_DATE_YEAR"].map(str) + '-' + df["PERIOD_ID__MONTHS"].map(str) + '-01'
    df['PERIOD'] = pd.to_datetime(df['PERIOD'])

    report = df[(df['PERIOD'] >= str(startdate)) & (df['PERIOD'] <= str(enddate))].groupby(['PROD_DETAILS_ID__PROD_LINE', 'AGENCY_DETAILS_ID__AGENCY_ID'])[
        ['NB_WRTN_PREM_AMT', 'WRTN_PREM_AMT', 'PREV_WRTN_PREM_AMT', 'PRD_ERND_PREM_AMT']].sum()
    #print(report.head())

    for index, item in df.head(2000).iterrows():
        writer.writerow([item['PROD_DETAILS_ID__PROD_LINE'], item['AGENCY_DETAILS_ID__AGENCY_ID'], item['NB_WRTN_PREM_AMT'], item['WRTN_PREM_AMT'], item['PREV_WRTN_PREM_AMT'], item['PRD_ERND_PREM_AMT']])

    return response