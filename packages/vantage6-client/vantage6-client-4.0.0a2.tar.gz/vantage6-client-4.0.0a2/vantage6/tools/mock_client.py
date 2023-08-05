import pandas as pd
import json
import logging

from typing import Any
from importlib import import_module
from copy import deepcopy

from vantage6.tools.wrappers import select_wrapper
from vantage6.tools.util import info

module_name = __name__.split('.')[1]


class MockAlgorithmClient:
    """
    The MockAlgorithmClient mimics the behaviour of the AlgorithmClient. It
    can be used to mock the behaviour of the AlgorithmClient and its
    communication with the server.

    Parameters
    ----------
    datasets : list[list[dict]]
        A list that contains the datasets that are used in the mocked
        algorithm. The inner list contains the datasets for each organization;
        the outer list is for each organization. A single dataset should be
        described as a dictionary with the same keys as in a node
        configuration:

        - database: str (path to file or SQL connection string) or pd.DataFrame
        - type (str, e.g. "csv" or "sql")
        - input_data (dict). The input data that is normally passed to the
          algorithm wrapper, e.g. a worksheet for an excel database.

        Note that if the database is a pandas DataFrame, the type and
        input_data keys are not required.
    module : str
        The name of the module that contains the algorithm.
    collaboration_id : int, optional
        Sets the mocked collaboration id to this value. Defaults to 1.
    organization_ids : list[int], optional
        Set the organization ids to this value. The first value is used for
        this organization, the rest for child tasks. Defaults to [0, 1, 2, ..].
    node_ids: list[int], optional
        Set the node ids to this value. The first value is used for this node,
        the rest for child tasks. Defaults to [0, 1, 2, ...].
    """
    def __init__(
        self, datasets: list[dict], module: str, collaboration_id: int = None,
        organization_ids: int = None, node_ids: int = None,
    ) -> None:
        self.log = logging.getLogger(module_name)
        self.n = len(datasets)

        if organization_ids and len(organization_ids) == self.n:
            self.all_organization_ids = organization_ids
        else:
            default_organization_ids = list(range(self.n))
            if organization_ids:
                self.log.warning(
                    "The number of organization ids (%s) does not match the "
                    "number of datasets (#=%s), using default values (%s) "
                    "instead",
                    organization_ids,
                    self.n,
                    default_organization_ids,
                )
            self.all_organization_ids = default_organization_ids

        self.organization_id = self.all_organization_ids[0]

        if node_ids and len(node_ids) == self.n:
            self.all_node_ids = node_ids
        else:
            default_node_ids = list(range(self.n))
            if node_ids:
                self.log.warning(
                    "The number of node ids (%s) does not match the number of "
                    "datasets (#=%s), using default values (%s) instead",
                    node_ids,
                    self.n,
                    default_node_ids,
                )
            self.all_node_ids = default_node_ids
        self.node_id = self.all_node_ids[0]

        self.datasets_per_org = {}
        self.organizations_with_data = []
        for idx, org_datasets in enumerate(datasets):
            org_id = self.all_organization_ids[idx]
            self.organizations_with_data.append(org_id)
            org_data = []
            for dataset in org_datasets:
                if isinstance(dataset["database"], pd.DataFrame):
                    org_data.append(dataset["database"])
                else:
                    wrapper = select_wrapper(dataset["type"])
                    org_data.append(
                        wrapper.load_data(
                            dataset["database"],
                            dataset["input_data"] if "input_data" in dataset
                            else {}
                        )
                    )
            self.datasets_per_org[org_id] = org_data

        self.collaboration_id = collaboration_id if collaboration_id else 1
        self.module_name = module
        self.tasks = []
        self.runs = []
        self.results = []

        self.image = 'mock_image'
        self.database = 'mock_database'

        self.task = self.Task(self)
        self.result = self.Result(self)
        self.organization = self.Organization(self)
        self.collaboration = self.Collaboration(self)
        self.node = self.Node(self)

    def wait_for_results(self, task_id: int, *args, **kwargs) -> list:
        """
        Mock waiting for results - just return the results as tasks are
        completed synchronously in the mock client.

        Parameters
        ----------
        task_id: int
            ID of the task for which the results should be obtained.

        Returns
        -------
        list
            List of task results.
        """
        info('Mocking waiting for results')
        return self.result.from_task(task_id)

    class SubClient:
        """
        Create sub groups of commands using this SubClient

        Parameters
        ----------
        parent : MockAlgorithmClient
            The parent client
        """
        def __init__(self, parent) -> None:
            self.parent: MockAlgorithmClient = parent

    class Task(SubClient):
        """
        Task subclient for the MockAlgorithmClient
        """
        def __init__(self, parent) -> None:
            super().__init__(parent)
            self.last_result_id = 0

        def create(
            self, input_: dict, organizations: list[int],
            name: str = "mock", description: str = "mock", *args, **kwargs
        ) -> int:
            """
            Create a new task with the MockProtocol and return the task id.

            Parameters
            ----------
            input_ : dict
                The input data that is passed to the algorithm. This should at
                least  contain the key 'method' which is the name of the method
                that should be called. Another often used key is 'master' which
                indicates that this container is a master container. Other keys
                depend on the algorithm.
            organizations : list[int]
                A list of organization ids that should run the algorithm.
            name : str, optional
                The name of the task, by default "mock"
            description : str, optional
                The description of the task, by default "mock"

            Returns
            -------
            int
                The id of the task.
            """
            if not len(organizations):
                raise ValueError(
                    "No organization ids provided. Cannot create a task for "
                    "zero organizations."
                )

            module = import_module(self.parent.module_name)

            # extract method from lib and input
            method_name = input_.get("method")
            method = getattr(module, method_name)

            # get input
            args = input_.get("args", [])
            kwargs = input_.get("kwargs", {})

            # get data for organization
            for org_id in organizations:
                # When creating a child task, pass the parent's datasets and
                # client to the child. By passing also the client, the child
                # has access to the same IDs specified
                data = self.parent.datasets_per_org[org_id]
                client_copy = deepcopy(self.parent)
                client_copy.node_id = self._select_node(org_id)
                client_copy.organization_id = org_id
                result = method(
                    mock_client=self.parent,
                    mock_data=data,
                    *args, **kwargs
                )

                self.last_result_id += 1
                self.parent.results.append({
                    "id": self.last_result_id,
                    "result": json.dumps(result),
                    "run": {
                        "id": self.last_result_id,
                        "link": f"/api/run/{self.last_result_id}",
                        "methods": ["GET", "PATCH"]
                    },
                })
                self.parent.runs.append({
                    "id": self.last_result_id,
                    "started_at": "2021-01-01T00:00:00.000000",
                    "assigned_at": "2021-01-01T00:00:00.000000",
                    "finished_at": "2021-01-01T00:00:00.000000",
                    "log": "mock_log",
                    "ports": [],
                    "status": "completed",
                    "input": json.dumps(input_),
                    "results": {
                        "id": self.last_result_id,
                        "link": f"/api/result/{self.last_result_id}",
                        "methods": ["GET", "PATCH"]
                    },
                    "node": {
                        "id": org_id,
                        "ip": None,
                        "name": "mock_node",
                        "status": "online",
                    },
                    "organization": {
                        "id": org_id,
                        "link": f"/api/organization/{org_id}",
                        "methods": ["GET", "PATCH"]
                    },
                    "task": {
                        "id": len(self.parent.tasks),
                        "link": f"/api/task/{len(self.parent.tasks)}",
                        "methods": ["GET", "PATCH"]
                    },
                })

            id_ = len(self.parent.tasks)
            collab_id = self.parent.collaboration_id
            task = {
                "id": id_,
                "runs": f"/api/run?task_id={id_}",
                "status": "completed",
                "name": name,
                "databases": ["mock"],
                "description": description,
                "image": "mock_image",
                "init_user": {
                    "id": 1,
                    "link": "/api/user/1",
                    "methods": ["GET", "DELETE", "PATCH"]
                },
                "init_org": {
                    "id": self.parent.organization_id,
                    "link": f"/api/organization/{self.parent.organization_id}",
                    "methods": ["GET", "PATCH"]
                },
                "parent": None,
                "collaboration": {
                    "id": collab_id,
                    "link": f"/api/collaboration/{collab_id}",
                    "methods": ["DELETE", "PATCH", "GET"]
                },
                "job_id": 1,
                "children": None,
            }
            self.parent.tasks.append(task)
            return task

        def get(self, task_id: int) -> dict:
            """
            Return the task with the given id.

            Parameters
            ----------
            task_id : int
                The id of the task.

            Returns
            -------
            dict
                The task details.
            """
            if task_id >= len(self.parent.tasks):
                return {
                    "msg": f"Could not find task with id {task_id}"
                }
            return self.parent.tasks[task_id]

        def _select_node(self, org_id: int) -> int:
            """
            Select a node for the given organization id.

            Parameters
            ----------
            org_id : int
                The organization id.

            Returns
            -------
            int
                The node id.
            """
            if not self.parent.all_node_ids or \
                    not self.parent.all_organization_ids or \
                    org_id not in self.parent.all_organization_ids:
                return org_id
            org_idx = self.parent.all_organization_ids.index(org_id)
            return self.parent.all_node_ids[org_idx]

    class Run(SubClient):
        """
        Run subclient for the MockAlgorithmClient
        """
        def get(self, id_: int) -> dict:
            """
            Get mocked run by ID

            Parameters
            ----------
            id_ : int
                The id of the run.

            Returns
            -------
            dict
                A mocked run.
            """
            for run in self.parent.runs:
                if run.get("id") == id_:
                    return run
            return {
                "msg": f"Could not find run with id {id_}"
            }

        def from_task(self, task_id: int) -> list[dict]:
            """
            Get mocked runs by task ID

            Parameters
            ----------
            task_id : int
                The id of the task.

            Returns
            -------
            list[dict]
                A list of mocked runs.
            """
            runs = []
            for run in self.parent.runs:
                if run.get("task").get("id") == task_id:
                    runs.append(run)
            return runs

    class Result(SubClient):
        """
        Result subclient for the MockAlgorithmClient
        """
        def get(self, id_: int) -> Any:
            """
            Get mocked result by ID

            Parameters
            ----------
            id_ : int
                The id of the result.

            Returns
            -------
            Any
                A mocked result.
            """
            for result in self.parent.results:
                if result.get("id") == id_:
                    return json.loads(result.get("result"))
            return {
                "msg": f"Could not find result with id {id_}"
            }

        def from_task(self, task_id: int) -> list[Any]:
            """
            Return the results of the task with the given id.

            Parameters
            ----------
            task_id : int
                The id of the task.

            Returns
            -------
            list[Any]
                The results of the task.
            """
            results = []
            for task in self.parent.tasks:
                if task.get("id") == task_id:
                    for result in task.get("results"):
                        results.append(json.loads(result.get("result")))
            return results

    class Organization(SubClient):
        """
        Organization subclient for the MockAlgorithmClient
        """
        def get(self, id_) -> dict:
            """
            Get mocked organization by ID

            Parameters
            ----------
            id_ : int
                The id of the organization.

            Returns
            -------
            dict
                A mocked organization.
            """
            if not id_ == self.parent.organization_id and \
                    id_ not in self.parent.organizations_with_data:
                return {
                    "msg": f"Organization {id_} not found."
                }
            return {
                "id": id_,
                "name": f"mock-{id_}",
                "domain": f"mock-{id_}.org",
                "address1": "mock",
                "address2": "mock",
                "zipcode": "mock",
                "country": "mock",
                "public_key": "mock",
                "collaborations": f"/api/collaboration?organization_id={id_}",
                "users": f"/api/user?organization_id={id_}",
                "tasks": f"/api/task?init_org_id={id_}",
                "nodes": f"/api/node?organization_id={id_}",
                "runs": f"/api/run?organization_id={id_}"
            }

        def list(self) -> list[dict]:
            """
            Get mocked organizations in the collaboration.

            Returns
            -------
            list[dict]
                A list of mocked organizations in the collaboration.
            """
            organizations = []
            for i in self.parent.all_organization_ids:
                organizations.append(self.get(i))
            return organizations

    class Collaboration(SubClient):
        """
        Collaboration subclient for the MockAlgorithmClient
        """
        def get(self, is_encrypted: bool = True) -> dict:
            """
            Get mocked collaboration

            Parameters
            ----------
            is_encrypted : bool
                Whether the collaboration is encrypted or not. Default True.

            Returns
            -------
            dict
                A mocked collaboration.
            """
            collab_id = self.parent.collaboration_id
            return {
                "id": collab_id,
                "name": "mock-collaboration",
                "encrypted": is_encrypted,
                "tasks": f"/api/task?collaboration_id={collab_id}",
                "nodes": f"/api/node?collaboration_id={collab_id}",
                "organizations":
                    f"/api/organization?collaboration_id={collab_id}"
            }

    class Node(SubClient):
        """
        Node subclient for the MockAlgorithmClient
        """
        def get(self, is_online: bool = True) -> dict:
            """
            Get mocked node

            Parameters
            ----------
            is_online : bool
                Whether the node is online or not. Default True.

            Returns
            -------
            dict
                A mocked node.
            """
            node_id = self.parent.node_id
            collab_id = self.parent.collaboration_id
            return {
                "id": node_id,
                "name": "mock-node",
                "status": "online" if is_online else "offline",
                "ip": "1.2.3.4",
                "config": {
                    "key": "value",
                },
                "collaboration": {
                    "id": collab_id,
                    "link": f"/api/collaboration/{collab_id}",
                    "methods": [
                        "DELETE",
                        "PATCH",
                        "GET"
                    ]
                },
                "last_seen": "2021-01-01T00:00:00.000000",
                "type": "node",
                "organization": {
                    "id": node_id,
                    "link": f"/api/organization/{node_id}",
                    "methods": [
                        "GET",
                        "PATCH"
                    ]
                },
            }

    # TODO implement the get_addresses method before using this part
    # class VPN(SubClient):
    #     """
    #     VPN subclient for the MockAlgorithmClient
    #     """
    #     def get_addresses(
    #         self, only_children: bool = False, only_parent: bool = False,
    #         include_children: bool = False, include_parent: bool = False,
    #         label: str = None
    #     ) -> list[dict] | dict:
    #         """
    #         Mock VPN IP addresses and ports of other algorithm containers in
    #         the current task.

    #         Parameters
    #         ----------
    #         only_children : bool, optional
    #             Only return the IP addresses of the children of the current
    #             task, by default False. Incompatible with only_parent.
    #         only_parent : bool, optional
    #             Only return the IP address of the parent of the current task,
    #             by default False. Incompatible with only_children.
    #         include_children : bool, optional
    #             Include the IP addresses of the children of the current task,
    #             by default False. Incompatible with only_parent, superseded
    #             by only_children.
    #         include_parent : bool, optional
    #             Include the IP address of the parent of the current task, by
    #             default False. Incompatible with only_children, superseded by
    #             only_parent.
    #         label : str, optional
    #             The label of the port you are interested in, which is set
    #             in the algorithm Dockerfile. If this parameter is set, only
    #             the ports with this label will be returned.

    #         Returns
    #         -------
    #         list[dict] | dict
    #             List of dictionaries containing the IP address and port number,
    #             and other information to identify the containers. If obtaining
    #             the VPN addresses from the server fails, a dictionary with a
    #             'message' key is returned instead.
    #         """
    #         pass

    #     def get_parent_address(self) -> dict:
    #         """
    #         Get the IP address and port number of the parent of the current
    #         task.

    #         Returns
    #         -------
    #         dict
    #             Dictionary containing the IP address and port number, and other
    #             information to identify the containers. If obtaining the VPN
    #             addresses from the server fails, a dictionary with a 'message'
    #             key is returned instead.
    #         """
    #         return self.get_addresses(only_parent=True)

    #     def get_child_addresses(self) -> list[dict]:
    #         """
    #         Get the IP addresses and port numbers of the children of the
    #         current task.

    #         Returns
    #         -------
    #         List[dict]
    #             List of dictionaries containing the IP address and port number,
    #             and other information to identify the containers. If obtaining
    #             the VPN addresses from the server fails, a dictionary with a
    #             'message' key is returned instead.
    #         """
    #         return self.get_addresses(only_children=True)
