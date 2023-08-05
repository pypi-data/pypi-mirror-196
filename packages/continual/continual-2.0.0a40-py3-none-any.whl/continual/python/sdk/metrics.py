from __future__ import annotations
from typing import List, Optional, Any, Union
from datetime import datetime

from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager


class MetricsManager(Manager):
    """Manages metric resources."""

    # the name pattern for metrics depends on the resource it was created for
    name_pattern: str = ""

    def create(
        self,
        id: str,
        display_name: str = "",
        direction: str = "UNSPECIFIED",
        tags: Optional[dict[str, str]] = None,
        replace_if_exists: bool = False,
    ) -> Metric:
        """Create a Metric.

        Arguments:
            id: identifier for the metric (e.g. "accuracy")
            display_name: the display name of the metric
            direction: direction of the metric (e.g. "HIGHER", "LOWER", or "UNSPECIFIED")
            tags: a dict of tags to add to this metric
            replace_if_exists: if the metric exists and this is true, update the current metric and return, else raise an error if the metric already exists

        Returns:
            A new metric.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> mape_metric = model_version.metrics.create(id="accuracy", display_name="my accuracy")
            >>> mape_metric.log(value=0.1, group_name="test")
            >>> model_version.metrics.get("accuracy")
            <Metric object {'name': 'projects/test_project/environments/my_environment/models/my_model/versions/cerkggdvn3d3cn5absgg/metrics/accuracy', 'display_name': 'my accuracy', 'create_time': '2023-01-05T21:59:30.214316Z', 'update_time': '2023-01-05T21:59:30.214316Z', 'values': [{'name': 'projects/test_project/environments/production/models/test_model/versions/cerkggdvn3d3cn5absgg/metrics/mape/metricValues/cerkgglvn3d3cn5abss0', 'value': 0.1, 'timestamp': '0001-01-01T00:00:00Z', 'create_time': '2023-01-05T21:59:30.223377Z', 'created_by': 'projects/test_project/apikeys/ceeeg5lvn3d2lroffjv0', 'run': '', 'step': '0', 'group': ''}], 'created_by': 'projects/test_project/apikeys/ceeeg5lvn3d2lroffjv0', 'run': '', 'direction': 'UNSPECIFIED'}>
        """

        req = management_pb2.CreateMetricRequest(
            metric=Metric(
                display_name=display_name,
                direction=direction,
                run=self.run_name,
                tags=tags,
                current_run=self.run_name,
            ).to_proto(),
            metric_id=id,
            parent=self.parent,
            replace_if_exists=replace_if_exists,
        )

        resp = self.client._management.CreateMetric(req)
        return Metric.from_proto(resp, client=self.client, current_run=self.run_name)

    def log(
        self,
        metric_name: str,
        value: Any,
        group: str = "",
        timestamp: Union[str, datetime] = None,
        step: int = 0,
        label: str = "",
        replace_if_exists: bool = False,
    ):
        """Log a Metric Value.

        Arguments:
            metric_name: the name of the metric to log this value for
            value: value of the metric
            group: [Optional] name of the group to which this metric belongs (e.g. "train")
            timestamp: [Optional] timestamp for which the value has been logged for
            step: [Optional] step at which the metric was logged, allows metrics to be grouped into a sequence
            label: [Optional] a label that describes the value
            replace_if_exists: if the metric value exists and this is true, update the current metric value and return, else raise an error if the metric value already exists
        Returns:

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> mape_metric = model_version.metrics.create(id="accuracy", display_name="my accuracy")
            >>> mape_metric.log(value=0.1, group_name="test")
            >>> model_version.metrics.get("accuracy")
            <Metric object {'name': 'projects/test_project/environments/my_environment/models/my_model/versions/cerkggdvn3d3cn5absgg/metrics/accuracy', 'display_name': 'my accuracy', 'create_time': '2023-01-05T21:59:30.214316Z', 'update_time': '2023-01-05T21:59:30.214316Z', 'values': [{'name': 'projects/test_project/environments/production/models/test_model/versions/cerkggdvn3d3cn5absgg/metrics/mape/metricValues/cerkgglvn3d3cn5abss0', 'value': 0.1, 'timestamp': '0001-01-01T00:00:00Z', 'create_time': '2023-01-05T21:59:30.223377Z', 'created_by': 'projects/test_project/apikeys/ceeeg5lvn3d2lroffjv0', 'run': '', 'step': '0', 'group': ''}], 'created_by': 'projects/test_project/apikeys/ceeeg5lvn3d2lroffjv0', 'run': '', 'direction': 'UNSPECIFIED'}>
        """
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        req = management_pb2.LogMetricRequest(
            parent=self.name(
                metric_name, self.parent, f"{self.parent}/metrics/{metric_name}"
            ),
            value=types.MetricValue(
                value=float(value) if isinstance(value, int) else value,
                group=group,
                step=step,
                timestamp=timestamp,
                run=self.run_name,
                label=label,
            ).to_proto(),
            replace_if_exists=replace_if_exists,
        )
        self.client._management.LogMetric(req)
        return

    def get(self, id: str) -> Metric:
        """Get metric.

        Arguments:
            name: Metric name or id.
            key: Metric key.
            group_name: Metric group name.
            step: Metric step for sequences.

        Returns
            A Metric.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> metric_keys = ['accuracy', 'precision', 'recall']
            >>> metrics = [model_version.metrics.create(key=key, value=0.9, direction="HIGHER", group_name="train") for key in metric_keys]
            >>> model_version.metrics.get(name=metrics[1].name).key                     # get by name
            'precision'
            >>> model_version.metrics.get(key="accuracy", group_name="train").key       # get by key and group_name
            'accuracy'
        """
        req = management_pb2.GetMetricRequest(
            name=self.name(
                id=id,
                parent=self.parent,
                name_pattern=self.parent + "/metrics/{metric}",
            ),
        )
        metric = self.client._management.GetMetric(req)
        return Metric.from_proto(metric, client=self.client, current_run=self.run_name)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: str = None,
        default_sort_order: str = "ASC",
    ) -> List[Metric]:
        """List metrics.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.

        Returns:
            A list of metrics.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> metric_keys = ['accuracy', 'precision', 'recall']
            >>> metrics = [model_version.metrics.create(key=key, value=0.9, direction="HIGHER", group_name="train") for key in metric_keys]
            >>> [m.key for m in model_version.metrics.list(page_size=3)]
            ['recall', 'precision', 'accuracy']
            >>> [m.key for m in model_version.metrics.list(page_size=3, order_by="key")]
            ['accuracy', 'precision', 'recall']
        """
        req = management_pb2.ListMetricsRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            default_sort_order=default_sort_order,
        )
        resp = self.client._management.ListMetrics(req)
        return [
            Metric.from_proto(x, client=self.client, current_run=self.run_name)
            for x in resp.metrics
        ]

    def list_all(self) -> Pager[Metric]:
        """List all metrics.

        Pages through all metrics using an iterator.

        Returns:
            A iterator of all metrics.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> metric_keys = ['accuracy', 'precision', 'recall']
            >>> metrics = [model_version.metrics.create(key=key, value=0.9, direction="HIGHER", group_name="train") for key in metric_keys]
            >>> [m.key for m in model_version.metrics.list_all()]
            ['accuracy', 'precision', 'recall']
        """

        def next_page(next_page_token):
            req = management_pb2.ListMetricsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListMetrics(req)
            return (
                [
                    Metric.from_proto(x, client=self.client, current_run=self.run_name)
                    for x in resp.metrics
                ],
                resp.next_page_token,
            )

        return Pager(next_page)

    def update(
        self,
        paths: List[str],
        metric: Metric,
    ) -> Metric:
        """Update Metric.

        Arguments:
            paths: A list of paths to be updated.
            metric: Metric object containing updated fields.

        Returns:
            An updated Metric.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
        """

        req = management_pb2.UpdateMetricRequest(
            metric=metric.to_proto(),
            update_paths=paths,
            run=self.run_name,
        )
        resp = self.client._management.UpdateMetric(req)
        return Metric.from_proto(resp, client=self.client, current_run=self.run_name)


class Metric(Resource, types.Metric):
    """Metric resource."""

    # the name pattern for metrics depends on the resource it was created for
    name_pattern: str = ""

    _manager: MetricsManager
    """Metrics manager."""

    def _init(self):
        self._manager = MetricsManager(
            parent=self.parent, client=self.client, run_name=self.current_run
        )

    def log(
        self,
        value: Any,
        group: str = "",
        timestamp: Union[str, datetime] = None,
        step: int = 0,
        label: str = "",
        replace_if_exists: bool = False,
    ):
        """Log a Metric Value for the current Metric.

        Arguments:
            value: value of the metric
            group: [Optional] name of the group to which this metric belongs (e.g. "train")
            timestamp: [Optional] timestamp for which the value has been logged for
            step: [Optional] step at which the metric was logged, allows metrics to be grouped into a sequence
            label: [Optional] a label that describes the value
            replace_if_exists: if the metric value exists and this is true, update the current metric value and return, else raise an error if the metric value already exists

        Returns:

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(display_name="my_model", description="Customer churn model")
            >>> model_version = model.model_versions.create()
            >>> mape_metric = model_version.metrics.create(id="accuracy", display_name="my accuracy")
            >>> mape_metric.log(value=0.1, group_name="test")
            >>> model_version.metrics.get("accuracy")
            <Metric object {'name': 'projects/test_project/environments/production/models/test_model/versions/cerkggdvn3d3cn5absgg/metrics/accuracy', 'display_name': 'my accuracy', 'create_time': '2023-01-05T21:59:30.214316Z', 'update_time': '2023-01-05T21:59:30.214316Z', 'values': [{'name': 'projects/test_project/environments/production/models/test_model/versions/cerkggdvn3d3cn5absgg/metrics/mape/metricValues/cerkgglvn3d3cn5abss0', 'value': 0.1, 'timestamp': '0001-01-01T00:00:00Z', 'create_time': '2023-01-05T21:59:30.223377Z', 'created_by': 'projects/test_project/apikeys/ceeeg5lvn3d2lroffjv0', 'run': '', 'step': '0', 'group': ''}], 'created_by': 'projects/test_project/apikeys/ceeeg5lvn3d2lroffjv0', 'run': '', 'direction': 'UNSPECIFIED'}>
        """
        self._manager.log(
            metric_name=self.name,
            value=value,
            group=group,
            step=step,
            timestamp=timestamp,
            label=label,
            replace_if_exists=replace_if_exists,
        )

    def update(self, paths: List[str]) -> Metric:
        """Update Metric.

        Arguments:
            paths: A list of paths to be updated.

        Returns:
            An updated Metric.

        Examples:
            >>> ...
        """
        return self._manager.update(paths=paths, metric=self)

    def add_tags(self, tags: dict[str, str]) -> Metric:
        """add tags.

        Arguments:
            tags: A dictionary of tag key/tag value

        Returns:
            An updated Metric.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> metric = model_version.metrics.get(id="metric1")
            >>> metric.add_tags({"color": "blue", "fruit": "apple"})
        """
        for key in tags:
            self.tags[key] = tags[key]
        return self._manager.update(self, paths=["tags"])

    def remove_tags(self, tags: List[str]) -> Metric:
        """remove tags.

        Arguments:
            tags: A list of tag keys

        Returns:
            An updated Metric.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> metric = model_version.metrics.get(id="metric1")
            >>> metric.remove_tags({"color", "fruit"})
        """
        for key in tags:
            self.tags.pop(key, -1)
        return self._manager.update(self, paths=["tags"])
