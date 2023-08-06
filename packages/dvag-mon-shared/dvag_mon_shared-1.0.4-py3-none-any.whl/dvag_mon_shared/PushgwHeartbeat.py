import logging
from azure.keyvault.secrets import SecretClient
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, generate_latest
from prometheus_client.exposition import default_handler
from dataclasses import dataclass


@dataclass
class PushgwHeartbeat:
    client: SecretClient = None

    def sendtopushgateway(self, success: str, error: str, function_name: str = None, environment: str = None):
        pushgw_user: str = self.client.get_secret(
            'PUSHGATEWAY-AUTH-USER').value
        pushgw_token: str = self.client.get_secret(
            'PUSHGATEWAY-AUTH-TOKEN').value
        url_pushgateway: str = self.client.get_secret('PUSHGATEWAY-URL').value
        # Handler that implements HTTP/HTTPS connections with Custom Header Authentification

        def token_auth_handler(url, method, timeout, headers, data):
            def handle():
                if pushgw_user is not None and pushgw_token is not None:
                    headers.append(('Auth-User', pushgw_user))
                    headers.append(('Auth-Token', pushgw_token))
                default_handler(url, method, timeout, headers, data)()
            return handle

        success = str(success)
        registry = CollectorRegistry()
        g = Gauge('dvag_e2e_heartbeat', 'last time the function was executed successfully', [
                  'instance', 'platform', 'environment', 'product', 'error'], registry=registry)
        g.labels(instance=function_name, platform='azure',
                 environment=environment, product='monitoring', error=error).set(success)
        # Generate the metric data in the Prometheus text format and print it
        try:
            push_to_gateway(url_pushgateway, job='aktives-monitoring', grouping_key={
                            'instance': function_name}, registry=registry, handler=token_auth_handler)
        except Exception as e:
            logging.error(
                f"Exception occurred while posting to pushgateway: {e}")
        logging.info(
            f"Send metric to pushgateway {url_pushgateway}: {generate_latest(registry).decode('utf-8')}")
