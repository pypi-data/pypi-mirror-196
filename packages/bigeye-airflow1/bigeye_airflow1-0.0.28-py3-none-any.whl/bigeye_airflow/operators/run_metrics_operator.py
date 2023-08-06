import logging
import json

from airflow.hooks.http_hook import HttpHook
from airflow.models import BaseOperator


class RunMetricsOperator(BaseOperator):

    def __init__(self,
                 connection_id,
                 warehouse_id,
                 schema_name,
                 table_name,
                 metric_ids=None,
                 *args,
                 **kwargs):
        super(RunMetricsOperator, self).__init__(*args, **kwargs)
        self.connection_id = connection_id
        self.warehouse_id = warehouse_id
        self.schema_name = schema_name
        self.table_name = table_name
        self.metric_ids = metric_ids

    def execute(self, context):
        metric_ids_to_run = []
        hook = self.get_hook('GET')
        if self.metric_ids is None:
            table = self._get_table_for_name(self.schema_name, self.table_name)
            if table is None or table.get("id") is None:
                raise Exception("Could not find table: ", self.schema_name, self.table_name)
            table_id = table.get("id")
            result = hook.run("api/v1/metrics?warehouseIds={warehouse_id}&tableIds={table_id}"
                              .format(warehouse_id=self.warehouse_id,
                                      table_id=table_id),
                              headers={"Accept": "application/json"})
            metrics = result.json()
            metric_ids_to_run = [m['id'] for m in metrics]
        else:
            metric_ids_to_run = self.metric_ids
        num_failing_metrics = 0
        for m in metric_ids_to_run:
            logging.debug("Running metric: %s", m)
            metric_result = hook.run(
                f"api/v1/metrics/run/{m}",
                headers={"Content-Type": "application/json", "Accept": "application/json"}).json()
            
            failed_metric_statuses = ['METRIC_RUN_STATUS_UNSPECIFIED', 'METRIC_RUN_STATUS_UNKNOWN', 'METRIC_RUN_STATUS_MUTABLE_UNKNOWN', 'METRIC_RUN_STATUS_GROUPS_LIMIT_FAILED']
            if metric_result.get('status') in failed_metric_statuses:
                logging.error("Metric is not OK: %s", m)
                logging.error("Metric result: %s", metric_result)

        if num_failing_metrics > 0:
            error_message = "There are {num_failing} failing metrics; see logs for more details"
            raise ValueError(error_message.format(num_failing=num_failing_metrics))

    def get_hook(self, method) -> HttpHook:
        return HttpHook(http_conn_id=self.connection_id, method=method)

    def _get_table_for_name(self, schema_name, table_name):
        post_hook = self.get_hook('POST')
        schema_result = post_hook.run("api/v1/schemas/fetch",
                                        headers={"Content-Type": "application/json", "Accept": "application/json"},
                                        data=json.dumps({"sourceIds": [self.warehouse_id],"search": schema_name}))
        schemas = schema_result.json().get("schemas")
        if len(schemas) == 0 or schemas is None:
            raise Exception("Could not find schema: ", schema_name)
        else:
            schema_id = schemas[0].get("id")

        tables_result = post_hook.run("api/v1/tables/fetch",
                                        headers={"Content-Type": "application/json", "Accept": "application/json"},
                                        data=json.dumps({"schemaIds": [schema_id], "ignoreFields": False}))
        tables = tables_result.json().get("tables")
        for t in tables:
            if t['name'].lower() == table_name.lower():
                return t 
        
        return None