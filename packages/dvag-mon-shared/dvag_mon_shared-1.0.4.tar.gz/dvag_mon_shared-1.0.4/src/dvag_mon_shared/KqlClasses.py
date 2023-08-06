import time
from azure.monitor.query import LogsQueryClient, LogsQueryStatus, LogsQueryResult, LogsQueryPartialResult
import logging
from datetime import datetime, timedelta
from dateutil import parser as du_parser
from pytimeparse import parse as pt_parse
from pandas import DataFrame
from azure.core.exceptions import HttpResponseError, ResourceExistsError
import re
import base64
import urllib
import zlib
from dvag_mon_shared.mapping_const import environment_dict, subscription_dict
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from prometheus_client.exposition import default_handler
import json
from typing import Callable
from dataclasses import dataclass
from azure.storage.blob import BlobServiceClient
import os


@dataclass
class KQLQueryResponse:
    """Result of a KQLQuery"""
    ok: bool
    status_code: int
    result: LogsQueryResult | dict


def map_environment(env: str) -> str:
    ENVIRONMENT_MAP = {
        "ent":      "Entwicklung",
        "dev":      "Entwicklung",
        "int":      "Integration",
        "prd":      "Produktion",
        "prod":     "Produktion",
        "abn":      "Abnahme",
        "preprod":  "Abnahme",
        "id":       "Innendienst"
    }
    return ENVIRONMENT_MAP.get(env, "Entwicklung")


def result_to_pandas(data: LogsQueryResult, error: bool = False) -> DataFrame:
    table = data.tables[0]
    df = DataFrame(columns=table.columns, data=table.rows)
    return df


def export_rawjson(data: LogsQueryResult, indent: int | None = None) -> str:
    out: dict[str, list] = {'tables': []}
    for table in data.tables:
        typed_columns = [{'name': name, 'type': type}
                         for name, type in zip(table.columns, table.columns_types)]
        rows = [list(row) for row in table.rows]
        table_entry = {
            'name': table.name,
            'columns': typed_columns,
            'rows': rows
        }
        out['tables'].append(table_entry)
    return json.dumps(out, indent=indent, default=str)


def export_pdjson(data: LogsQueryResult, indent: int | None = None) -> str:
    df = result_to_pandas(data)
    return df.to_json(indent=indent)


def export_pdjson_rec(data: LogsQueryResult, indent: int | None = None) -> str:
    df = result_to_pandas(data)
    return df.to_json(orient='records', indent=indent)


def export_pdstring(data: LogsQueryResult) -> str:
    df = result_to_pandas(data)
    return df.to_string()


exporters = {
    'rawjson': export_rawjson,
    'pdjson': export_pdjson,
    'pdjson_rec': export_pdjson_rec,
    'pdstring': export_pdstring,
    'string': export_pdstring
}


def get_exporter(format: str) -> Callable[[LogsQueryResult], str]:
    return exporters.get(format, export_rawjson)

# postprocessing save to blob storage


def save_to_blob_storage(converted_result: KQLQueryResponse, filename: str, url: str, container_name: str) -> None:
    try:
        blob_client = BlobServiceClient.from_connection_string(url)
        blob_client = blob_client.get_blob_client(
            container=container_name, blob=f'{filename}-{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}')
        blob_client.upload_blob(converted_result)
        logging.info('Blob %s created',
                     filename)
    except ResourceExistsError:
        logging.info('Blob %s already exists', filename)
        pass

# TODO: implement with ABC as different parameters are used


def post_processing(format: str, converted_result: KQLQueryResponse, filename: str, url: str, container_name: str) -> None:
    match format:
        case 'blob_storage':
            return save_to_blob_storage(converted_result, filename, url, container_name)
        case 'adx':
            # TODO: implement ADX post processing
            raise NotImplementedError('ADX post processing not implemented')
        case 'prometheus':
            # TODO: implement prometheus post processing
            raise NotImplementedError(
                'Prometheus post processing not implemented')
        case _:
            logging.warning('No post processing executed')


def make_timespan(start: str | None = None, end: str | None = None, duration: str = '24h') -> tuple[datetime, datetime]:
    """Creates a datetime-tuple (start,end) that can be used by LogsQueryClient.query_resource"""
    logging.info(f'function call: make_timespan({start},{end},{duration})')

    duration = '24h' if not duration else duration
    duration_td = timedelta(seconds=pt_parse(duration))

    if not start and not end:
        return (datetime.now() - duration_td, datetime.now())

    if start and end:
        parsed_start = du_parser.parse(start)
        parsed_end = du_parser.parse(end)
        logging.info(f'make_timespan: start->{parsed_start}')
        logging.info(f'make_timespan: end->{parsed_end}')
        return (parsed_start, parsed_end)

    if start:
        parsed_start = du_parser.parse(start)
        logging.info(f'make_timespan: start->{parsed_start}')
        logging.info(f'make_timespan: duration->{duration_td}')
        return (parsed_start, parsed_start + duration_td)

    if end:
        parsed_end = du_parser.parse(end)
        logging.info(f'make_timespan: end->{parsed_end}')
        return (parsed_end - duration_td, parsed_end)


class KQLQuery:
    """Performs login, Executes a query to a single or multiple workspaces, returns resultset """

    def __init__(self, creds, resourceId) -> None:
        self.creds = creds  # Credentials to access the log resource or LAW
        # ResourceId can be the GUID of a Log Analytics Workspace (e.g. 'dd78a9b0-366b-48a8-a717-264ddd5aeca4') or the ResourceId of a specific resource (e.g. /subscriptions/4b011a26-7412-4c17-94b0-4be1ef3262f6/resourceGroups/rg-vertraege-ffm-ent/providers/microsoft.insights/components/appi-vertraege-ffm-ent)
        self.resourceId = resourceId
        self.resourceMode = resourceId.find("/") == 0

    def execute(self, myquery, span: tuple[datetime, datetime] | None = None) -> KQLQueryResponse:
        response = None

        try:
            log_client = LogsQueryClient(self.creds)
            if self.resourceMode:  # Using query_resource to access only specified resource log data
                result = log_client.query_resource(self.resourceId,
                                                   query=myquery,
                                                   timespan=span)
            else:
                result = log_client.query_workspace(self.resourceId,
                                                    query=myquery,
                                                    timespan=span)
            if type(result) == LogsQueryResult:
                return KQLQueryResponse(True, 200, result)
            else:
                return KQLQueryResponse(False, 500, {"error": "LogsQueryPartialResult returned", "type": "PartialResult", "reason": "unknown", "code": 500})
        except HttpResponseError as e:
            logging.info(f"Failure during LAW Query {e}")
            message = {
                "error": e.message,
                "type": e.exc_type,
                "reason": e.reason,
                "code": e.status_code
            }
            return KQLQueryResponse(False, e.status_code, message)

    def generate_portal_link(self, myquery):
        # Generate Portal link (only used if environment PORTAL_LINK is set to true )
        logging.info("generate_portal_link")
        base_url = "https://portal.azure.com#@930d042f-8145-48e6-871e-7659c17b56da/blade/Microsoft_Azure_Monitoring_Logs/LogsBlade/source/Alerts.EmailLinks/scope/%7B%22resources%22%3A%5B%7B%22resourceId%22%3A%22%2Fsubscriptions%2Feea48e9a-9c6e-418f-8c52-1581eee4de07%2FresourceGroups%2Frg-monitoring-prod%2Fproviders%2Fmicrosoft.operationalinsights%2Fworkspaces%2Flog-monitoring-prod-01%22%7D%5D%7D/q/eJyVUcFKw0AQvfcrxj0lkGoaqKCQgxb1UqsEQfAStrtDuyTZLTuziqUf76ZpqR5EXOYwPN6%2BeW%2Bmad2K6tl8tIOPNXqEOb5jC8ZCIu6q6qkSGYjXm2ohUpBWg2yoVm0gRl9b2WFNUJYgNt7p0LBx9uLU5hMx2g2qj0gkVwhnylmWxhKIZ%2B865DUGEsfZR9aJNHPWomJg06EGF1iA80AsVVOzl6qf%2Fxf7V9Vo8X%2FC5seHuDIKXSe92SLc47pFXyoXLCdpBrdoA28jogcoUFwYpbD8hKWxteTkJQo9oEUvGXUG0y4DHdtePynyohjnV%2BN8%2BjKZXBexLs%2Fz4b2lUX0RN0%2Bb6LJswhK9RUban2MPHg6TQbTdB4guvtEOqU73izGc597ZEAI0kvoC/prettify/1/timespan/"
        compressed_value = zlib.compress(myquery.encode('utf-8'))
        base64_bytes = base64.b64encode(compressed_value)
        base64_message = base64_bytes.decode('ascii')
        safe_string = urllib.parse.quote(base64_message)
        safe_string = safe_string.replace("/", "%2F")
        href = re.sub('(.+7D\/q\/)(.+)(\/prettify.+)',
                      f"\\1{safe_string}\\3", base_url)
        return href


class KQLResult:
    """Receives an Azure KQL resultset and converts this resultset to a dataframe with one line for every metric.
       This can be exported to various formats, e.g. Prometheus Metrics export for push gateway"""

    def __init__(self, result) -> None:
        # Accept various result set formats, e.g. Log Analytics Queries, App Insights, ADX, Resource Graph Explorer
        # result can be any resultset-like type, currently only LogsQueryResult is supported, todo: AppInsights, ADX, Resource Graph Explorer
        self.dfArray = []
        self.dfIndex = -1
        self.result = ''
        self.CurrentType = ''
        self.metric_list = []

        # Process the results of a Log Analytics Workspace Query
        if type(result).__name__ == "LogsQueryResult":
            self.dfIndex = len(self.dfArray)

            # For mapping of LogsQueryResult to a Pandas dataframe see
            # https://docs.microsoft.com/en-us/python/api/overview/azure/monitor-query-readme?view=azure-python
            for datatable in result.tables:
                self.dfArray.append(
                    DataFrame(data=datatable.rows, columns=datatable.columns))

    def setcurrentDataFrame(self, index: int = 0) -> DataFrame:
        """Sets the number of the current dataframe, beginning with 0"""
        self.dfIndex = index
        return self.currentDataFrame()

    def currentDataFrame(self) -> DataFrame:
        """Retrieves the current dataframe"""
        return self.dfArray[self.dfIndex]

    def checkIfMetricExist(self, MetricsName) -> bool:
        if MetricsName not in self.metric_list:
            self.metric_list.append(MetricsName)
            return True
        return False

    def toCsv(self) -> DataFrame:
        df = self.currentDataFrame()
        return df.to_csv(sep=',')

    def remove(self, text) -> str:
        return re.sub(r'[^\w\s]+', '', re.sub(r'\n', '  ', text).replace("'", "").replace('"', '').replace('\n', ''))

    def toPrometheus(self, client, type, GRAFANA_DASHBOARD_ID) -> bool:
        is_success = True

        # Get KV Secrets
        try:
            PUSHGATEWAY_URL = (client.get_secret('PUSHGATEWAY-URL').value)
            PUSHGATEWAY_AUTH_USER = (
                client.get_secret('PUSHGATEWAY-AUTH-USER').value)
            PUSHGATEWAY_AUTH_TOKEN = (
                client.get_secret('PUSHGATEWAY-AUTH-TOKEN').value)
        except Exception as e:
            logging.info(f"Unable to fetch KV Secret {e}")

        def token_auth_handler(url, method, timeout, headers, data):
            def handle():
                if PUSHGATEWAY_AUTH_USER is not None and PUSHGATEWAY_AUTH_TOKEN is not None:
                    headers.append(('Auth-User', PUSHGATEWAY_AUTH_USER))
                    headers.append(('Auth-Token', PUSHGATEWAY_AUTH_TOKEN))
                default_handler(url, method, timeout, headers, data)()
            return handle

        """Convert current DataFrame to Prometheus exposition format"""

        # For Prometheus exposition formats see https://github.com/prometheus/docs/blob/main/content/docs/instrumenting/exposition_formats.md
        # If the query includes a timestamp it can be converted with
        # unix_time = int((row.get('TimeGenerated') - datetime(1970, 1, 1)).total_seconds()) * 1000

        # convert column level metrics to single rows for each metrics (preparation for Prometheus exposition format)
        # see https://stackoverflow.com/questions/28654047/convert-columns-into-rows-with-pandas

        if type == 'url-rtf':
            newdf = self.currentDataFrame().melt(id_vars=["rtname", "environment", "AppRoleName", "resourcegroup",
                                                          "subscription", "failuredetails", "result"], var_name="MetricsName", value_name="MetricsValue")
        elif type == 'heartbeat':
            newdf = self.currentDataFrame().melt(id_vars=[
                "rtname", "environment", "resourcegroup", "AppRoleName", "subscription"], var_name="MetricsName", value_name="MetricsValue")

        for group_index, group_row in newdf.groupby(["rtname", "environment"]):
            registry = CollectorRegistry()
            self.metric_list = []
            for index, row in group_row.iterrows():
                # Using f-strings to format Prometheus output line by line
                # Alternately newdf.to_string(columns = ["MetricsName", "rtname", "Environ", "AppRoleName", "MetricsValue"], header=False, index=False, col_space=0)
                # could be used with column formatters
                # result += f'{row["MetricsName"].lower()}{{rtname="{row["rtname"]}",Environ="{row["Environ"]}",AppRoleName="{row["AppRoleName"]}"}} {row["MetricsValue"]}\n'

                # Mapping for environment
                if row["environment"] in environment_dict:
                    environment = environment_dict.get(row["environment"])
                else:
                    environment = 'Für alle Umgebungen'
                # Mapping for subscription
                if row["subscription"] in subscription_dict:
                    subscription = subscription_dict.get(row["subscription"])
                else:
                    subscription = ''
                # We need to seperate the querys as we have different labels
                if type == 'url-rtf':
                    # remove special characters out of failuredetails row
                    row["failuredetails"] = self.remove(row["failuredetails"])
                    if self.checkIfMetricExist(row["MetricsName"]):
                        g = Gauge(f'dvag_e2e_{row["MetricsName"].lower()}', '', ['environment', 'app_role_name', 'subscription',
                                  'resource_group', 'instance', 'hostname', 'type', 'grafana_id', 'failuredetails'], registry=registry)
                    g.labels(environment=environment, app_role_name=row["AppRoleName"], subscription=subscription, resource_group=row["resourcegroup"], instance=row[
                             "rtname"], hostname=row["rtname"], failuredetails=row["failuredetails"], type='rtf', grafana_id=GRAFANA_DASHBOARD_ID).set(row["MetricsValue"])
                elif type == 'heartbeat':
                    # remove the .01 out of the heartbeat rt name
                    try:
                        row["rtname"] = re.search(
                            r'(.+timetrigger(dynamic|url)).01', row["rtname"]).group(1)
                    except:
                        logging.info("Couldnt remove heartbeat counter")
                        pass
                    if self.checkIfMetricExist(row["MetricsName"]):
                        heartbeat = Gauge(f'dvag_e2e_{row["MetricsName"].lower()}', 'last time the function was executed successfully', [
                                          'environment', 'subscription', 'app_role_name', 'resource_group', 'instance', 'hostname', 'type'], registry=registry)
                    heartbeat.labels(environment=environment, subscription=subscription, app_role_name=row["AppRoleName"], resource_group=row[
                                     "resourcegroup"], instance=row["rtname"], hostname=row["rtname"], type='heartbeat').set(row["MetricsValue"])
                self.CurrentType = row["MetricsName"]
            try:
                push_to_gateway(PUSHGATEWAY_URL, job='aktives-monitoring', grouping_key={
                                'name': row["rtname"], 'environment': environment}, registry=registry, handler=token_auth_handler)
                registry = CollectorRegistry.unregister
            except Exception as e:
                is_success = False
                logging.error(
                    f"Exception occurred while posting to pushgateway: {e}")
            logging.info(
                f"{row['rtname']} - {environment} metrics sent to {PUSHGATEWAY_URL}")
        return is_success
