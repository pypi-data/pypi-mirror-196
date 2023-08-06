# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2023  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

class Subscription():

    def __init__(self, subscription):
        subscription = subscription or {}

        # Data sources
        self.explain_queue_ds = DataSource(
            subscription.get("explain_queue_ds", {}))
        self.explain_result_ds = DataSource(
            subscription.get("explain_result_ds", {}))
        self.payload_ds = DataSource(
            subscription.get("payload_data_source", {}))
        self.scored_training_ds = DataSource(
            subscription.get("scored_training_ds", {}))

        # Subscription details
        self.data_mart_id = subscription.get("data_mart_id")
        self.subscription_id = subscription.get("subscription_id")
        self.binding_id = subscription.get("binding_id")

        asset = subscription.get("asset") or {}
        self.asset_name = asset.get("name")
        self.asset_id = asset.get("id")

        deployment = subscription.get("deployment") or {}
        self.deployment_name = deployment.get("name")
        self.deployment_id = deployment.get("id")

        self.scoring_id_column = subscription.get("scoring_id_column")
        self.scoring_timestamp_column = subscription.get(
            "scoring_timestamp_column")


class DataSource():
    """Class representing datasource"""

    def __init__(self, data_source):
        self.connection = data_source.get("connection", {})
        self.credentials = data_source.get("credentials", {})
        self.connection_type = self.connection.get("type")
        self.database = data_source.get("database_name")
        self.schema = data_source.get("schema_name")
        self.table = data_source.get("table_name")
        self.partition_column = data_source.get("partition_column")
        self.num_partitions = data_source.get("num_partitions")

    def __str__(self):
        ds_dict = vars(self).copy()
        del ds_dict["connection"]
        del ds_dict["credentials"]
        return str(ds_dict)
