from django.db import models
from django.db import connection, connections
import json
from datetime import datetime
from sqlserver_ado.fields import LegacyDateTimeField
import urllib3
import urllib.request

class DimPeriod(models.Model):
    PERIOD_ID = models.BigIntegerField(primary_key=True)
    STAT_PROFILE_DATE_YEAR = models.IntegerField()
    MONTHS = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'DimPeriod'

class DimProd(models.Model):
    PROD_DETAILS_ID = models.BigIntegerField(primary_key=True)
    PROD_ABBR = models.CharField(max_length=500)
    PROD_LINE = models.CharField(max_length=500)
    STATE_ABBR = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'DimProd'

class DimVendor(models.Model):
    VENDOR_ID = models.BigIntegerField(primary_key=True)
    VENDOR_IND = models.CharField(max_length=500)
    VENDOR = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'DimVendor'

class DimAgencyDetails(models.Model):
    AGENCY_DETAILS_ID = models.BigIntegerField(primary_key=True)
    AGENCY_ID = models.IntegerField()
    PRIMARY_AGENCY_ID = models.IntegerField()
    AGENCY_APPOINTMENT_YEAR = models.IntegerField()
    ACTIVE_PRODUCERS = models.IntegerField()
    MAX_AGE = models.IntegerField()
    MIN_AGE = models.IntegerField()
    PL_START_YEAR = models.IntegerField()
    PL_END_YEAR = models.IntegerField()
    COMMISIONS_START_YEAR = models.IntegerField()
    COMMISIONS_END_YEAR = models.IntegerField()
    CL_START_YEAR = models.IntegerField()
    CL_END_YEAR = models.IntegerField()
    ACTIVITY_NOTES_START_YEAR = models.IntegerField()
    ACTIVITY_NOTES_END_YEAR = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'DimAgencyDetails'

class FactInsurance(models.Model):
    COMPOSITE_ID = models.CharField(max_length=100, primary_key=True)
    AGENCY_DETAILS_ID = models.ForeignKey(DimAgencyDetails, db_column='AGENCY_DETAILS_ID', on_delete=models.CASCADE)
    POLICY_DETAILS_ID = models.BigIntegerField()
    PERIOD_ID = models.ForeignKey(DimPeriod, db_column='PERIOD_ID', on_delete=models.CASCADE)
    PROD_DETAILS_ID = models.ForeignKey(DimProd, db_column='PROD_DETAILS_ID', on_delete=models.CASCADE)
    VENDOR_ID = models.ForeignKey(DimVendor, db_column='VENDOR_ID', on_delete=models.CASCADE)
    RETENTION_POLY_QTY = models.FloatField()
    POLY_INFORCE_QTY = models.FloatField()
    PREV_POLY_INFORCE_QTY = models.FloatField()
    NB_WRTN_PREM_AMT = models.FloatField()
    WRTN_PREM_AMT = models.FloatField()
    PREV_WRTN_PREM_AMT = models.FloatField()
    PRD_ERND_PREM_AMT = models.FloatField()
    PRD_INCRD_LOSSES_AMT = models.FloatField()
    RETENTION_RATIO = models.FloatField()
    LOSS_RATIO = models.FloatField()
    LOSS_RATIO_3YR = models.FloatField()
    GROWTH_RATE_3YR = models.FloatField()

    class Meta:
        managed = False
        db_table = 'FactInsurance'



def dictfetchall(cur):
    dataset = cur.fetchall()
    columns = [col[0] for col in cur.description]
    return [
        dict(zip(columns, row))
        for row in dataset
        ]

def SummaryVendorwiseInfo(vendor):
    cur = connections['default'].cursor()
    if vendor == '':
        whereclause = ''
    else:
        whereclause = "WHERE Vendor = '" + str(vendor) + "'"
    query = """SELECT [VENDOR_IND]
                  ,[VENDOR]
                  ,SUM([RETENTION_POLY_QTY]) [RETENTION_POLY_QTY]
                  ,SUM([POLY_INFORCE_QTY]) [POLY_INFORCE_QTY]
                  ,SUM([WRTN_PREM_AMT]) [WRTN_PREM_AMT]
                  ,AVG([RETENTION_RATIO]) [RETENTION_RATIO]
              FROM [dbo].[DimVendor] VEN INNER JOIN [dbo].[FactInsurance] INS
              ON VEN.[VENDOR_ID] = INS.[VENDOR_ID]
              """ + whereclause + """
              GROUP BY [VENDOR_IND]
                  ,[VENDOR]"""
    cur.execute(query)
    results = dictfetchall(cur)
    cur.close()
    return results

def SummaryStateByProductionLineInfo():
    cur = connections['default'].cursor()
    query = """SELECT [STATE_ABBR]
                  ,[PROD_LINE]
                  ,SUM([RETENTION_POLY_QTY]) [RETENTION_POLY_QTY]
                  ,SUM([POLY_INFORCE_QTY]) [POLY_INFORCE_QTY]
                  ,SUM([WRTN_PREM_AMT]) [WRTN_PREM_AMT]
                  ,AVG([RETENTION_RATIO]) [RETENTION_RATIO]
              FROM [dbo].[DimProd] PROD INNER JOIN [dbo].[FactInsurance] INS
              ON PROD.[PROD_DETAILS_ID] = INS.[PROD_DETAILS_ID]
              GROUP BY [STATE_ABBR]
                  ,[PROD_LINE]"""
    cur.execute(query)
    results = dictfetchall(cur)
    cur.close()
    return results

def AgencyProductLinebyDate():
    cur = connections['default'].cursor()
    query = """SELECT [STATE_ABBR]
                  ,[PROD_LINE]
                  ,SUM([RETENTION_POLY_QTY]) [RETENTION_POLY_QTY]
                  ,SUM([POLY_INFORCE_QTY]) [POLY_INFORCE_QTY]
                  ,SUM([WRTN_PREM_AMT]) [WRTN_PREM_AMT]
                  ,AVG([RETENTION_RATIO]) [RETENTION_RATIO]
              FROM [dbo].[DimProd] PROD INNER JOIN [dbo].[FactInsurance] INS
              ON PROD.[PROD_DETAILS_ID] = INS.[PROD_DETAILS_ID]
              GROUP BY [STATE_ABBR]
                  ,[PROD_LINE]"""
    cur.execute(query)
    results = dictfetchall(cur)
    cur.close()
    return results

