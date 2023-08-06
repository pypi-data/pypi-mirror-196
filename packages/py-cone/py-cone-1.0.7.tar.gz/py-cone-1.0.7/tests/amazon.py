from sp_api.api import Reports, CatalogItems, Catalog
from sp_api.api import Feeds
from sp_api.util.load_all_pages import load_all_pages
from sp_api.base import SellingApiException, SellingApiBadRequestException
from sp_api.base.reportTypes import ReportType


# 获取亚马逊利润报表
def get_amazon_profit_report():
    # 获取亚马逊利润报表
    try:
        report_type = ReportType.PROFITABILITY_REPORT
        report = Reports().request_report(report_type)
        report_id = report.payload['reportId']
        report = Reports().get_report(report_id)
        return report.payload
    except SellingApiBadRequestException as e:
        print(e)
        return None
    except SellingApiException as e:
        print(e)
        return None

# 获取亚马逊交易报表
def get_amazon_transaction_report():
    # 获取亚马逊交易报表
    try:
        report_type = ReportType.FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL
        report = Reports().request_report(report_type)
        report_id = report.payload['reportId']
        report = Reports().get_report(report_id)
        return report.payload
    except SellingApiBadRequestException as e:
        print(e)
        return None
    except SellingApiException as e:
        print(e)
        return None

# ReportType.FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL

# 获取亚马逊交易范围报表
def get_amazon_transaction_range_report(start_date, end_date):
    # 获取亚马逊交易范围报表
    try:
        report_type = ReportType.FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL
        report = Reports().request_report(report_type, start_date=start_date, end_date=end_date)
        report_id = report.payload['reportId']
        report = Reports().get_report(report_id)
        return report.payload
    except SellingApiBadRequestException as e:
        print(e)
        return None
    except SellingApiException as e:
        print(e)
        return None
  

# amazon sqs client
def get_amazon_sqs_client():
    # 获取亚马逊sqs client
    try:
        sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        return sqs
    except Exception as e:
        print(e)
        return None



# 获取亚马逊数据报告 广告报告
def get_amazon_advertising_report():
    # 获取亚马逊广告报告
    try:
        report_type = ReportType.ADVERTISING_PERFORMANCE_REPORT
        report = Reports().request_report(report_type)
        report_id = report.payload['reportId']
        report = Reports().get_report(report_id)
        return report.payload
    except SellingApiBadRequestException as e:
        print(e)
        return None
    except SellingApiException as e:
        print(e)
        return None


# 亚马逊广告api
def get_amazon_advertising_api():
    # 获取亚马逊广告api
    try:
        advertising_api = Advertising()
        return advertising_api
    except SellingApiBadRequestException as e:
        print(e)
        return None
    except SellingApiException as e:
        print(e)
        return None

# request amazon advertising api
def request_amazon_advertising_api(advertising_api, report_type, start_date, end_date):
    # 请求亚马逊广告api
    try:
        report = advertising_api.request_report(report_type, start_date=start_date, end_date=end_date)
        report_id = report.payload['reportId']
        report = advertising_api.get_report(report_id)
        return report.payload
    except SellingApiBadRequestException as e:
        print(e)
        return None
    except SellingApiException as e:
        print(e)
        return None


