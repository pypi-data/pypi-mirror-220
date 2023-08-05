from typing import Any, Dict, List, Optional

from pydantic import Field

from phidata.infra.resource import InfraResource
from phidata.k8s.api_client import K8sApiClient
from phidata.k8s.constants import DEFAULT_K8S_NAMESPACE
from phidata.k8s.enums.api_version import ApiVersion
from phidata.k8s.enums.kind import Kind
from phidata.k8s.resource.meta.v1.object_meta import ObjectMeta
from phidata.utils.cli_console import print_info
from phidata.utils.log import logger


class K8sObject(InfraResource):
    def get_k8s_object(self) -> Any:
        """Returns the K8sObject definition"""
        logger.error("@get_k8s_object method not defined")


class K8sResource(K8sObject):
    """Base class for K8s Resources"""

    ## Common fields for all K8s Resources
    # Which version of the Kubernetes API you're using to create this object
    # Note: we use an alias "apiVersion" so that the K8s manifest generated by this resource
    #       has the correct key
    api_version: ApiVersion = Field(..., alias="apiVersion")
    # What kind of object you want to create
    kind: Kind
    # Data that helps uniquely identify the object, including a name string, UID, and optional namespace
    metadata: ObjectMeta

    ## Fields used in api calls
    # async_req bool: execute request asynchronously
    async_req: bool = False
    # pretty: If 'true', then the output is pretty printed.
    pretty: bool = True

    # List of fields to include from the K8sResource class when generating the
    # K8s manifest. Subclasses must add fields to include in the fields_for_k8s_manifest list
    fields_for_k8s_manifest_base: List[str] = [
        "api_version",
        "apiVersion",
        "kind",
        "metadata",
    ]
    # List of fields to include from Subclasses
    # This should be defined by the Subclass
    fields_for_k8s_manifest: List[str] = []

    # Used for running post-create, post-update and post-delete steps
    resource_available: bool = False
    resource_updated: bool = False
    resource_deleted: bool = False

    def is_valid(self) -> bool:
        # SubResources can use this function to add validation checks
        return True

    def get_namespace(self) -> str:
        if self.metadata and self.metadata.namespace:
            return self.metadata.namespace
        return DEFAULT_K8S_NAMESPACE

    def get_label_selector(self) -> str:
        labels = self.metadata.labels
        if labels:
            label_str = ",".join([f"{k}={v}" for k, v in labels.items()])
            return label_str
        return ""

    def get_k8s_object(self) -> Any:
        """Creates a K8sObject for this resource.
        Eg:
            * For a Deployment resource, it will return the V1Deployment object.
        """
        logger.error("@get_k8s_object method not defined")
        return None

    def get_resource_name(self) -> str:
        if self.name:
            return self.name
        return self.metadata.name or self.__class__.__name__

    @staticmethod
    def get_from_cluster(
        k8s_client: K8sApiClient, namespace: Optional[str] = None, **kwargs
    ) -> Any:
        """Gets all resources of this type from the K8s Cluster

        Args:
            k8s_client: The K8sApiClient for the current Cluster
            namespace: Namespace to use.
        """
        logger.error(f"@get_from_cluster method not defined")
        return None

    def _create(self, k8s_client: K8sApiClient) -> bool:
        logger.error(f"@_create method not defined for {self.__class__.__name__}")
        return False

    def create(self, k8s_client: K8sApiClient) -> bool:
        """Creates the resource on the K8s Cluster

        Args:
            k8s_client: The K8sApiClient for the current Cluster
        """
        if not self.is_valid():
            return False
        if self.use_cache and self.is_active_on_cluster(k8s_client):
            self.resource_available = True
            print_info(
                f"{self.get_resource_type()} {self.get_resource_name()} already active."
            )
            return True
        else:
            self.resource_available = self._create(k8s_client)
        if self.resource_available:
            print_info(
                f"{self.get_resource_type()} {self.get_resource_name()} created."
            )
            return self.post_create(k8s_client)
        return self.resource_available

    def post_create(self, k8s_client: K8sApiClient) -> bool:
        # return True because this function is not used for most resources
        return True

    def _read(self, k8s_client: K8sApiClient) -> Any:
        logger.error(f"@_read method not defined for {self.__class__.__name__}")
        return False

    def read(self, k8s_client: K8sApiClient) -> Any:
        """Reads the resource from the K8s Cluster
        Eg:
            * For a Deployment resource, it will return the V1Deployment object
            currently running on the cluster.

        Args:
            k8s_client: The K8sApiClient for the current Cluster
        """
        if not self.is_valid():
            return None
        if self.use_cache and self.active_resource is not None:
            return self.active_resource
        return self._read(k8s_client)

    def _update(self, k8s_client: K8sApiClient) -> Any:
        logger.error(f"@_update method not defined for {self.__class__.__name__}")
        return False

    def update(self, k8s_client: K8sApiClient) -> bool:
        """Updates the resource on the K8s Cluster

        Args:
            k8s_client: The K8sApiClient for the current Cluster
        """
        if not self.is_valid():
            return False
        if self.is_active_on_cluster(k8s_client):
            self.resource_updated = self._update(k8s_client)
        else:
            print_info(
                f"{self.get_resource_type()} {self.get_resource_name()} does not exist."
            )
            return True
        if self.resource_updated:
            return self.post_update(k8s_client)
        return self.resource_updated

    def post_update(self, k8s_client: K8sApiClient) -> bool:
        # return True because this function is not used for most resources
        return True

    def _delete(self, k8s_client: K8sApiClient) -> Any:
        logger.error(f"@_delete method not defined for {self.__class__.__name__}")
        return False

    def delete(self, k8s_client: K8sApiClient) -> bool:
        """Deletes the resource from the K8s Cluster

        Args:
            k8s_client: The K8sApiClient for the current Cluster
        """
        if not self.is_valid():
            return False
        if self.is_active_on_cluster(k8s_client):
            self.resource_deleted = self._delete(k8s_client)
        else:
            print_info(
                f"{self.get_resource_type()} {self.get_resource_name()} does not exist."
            )
            return True
        if self.resource_deleted:
            return self.post_delete(k8s_client)
        return self.resource_deleted

    def post_delete(self, k8s_client: K8sApiClient) -> bool:
        # return True because this function is not used for most resources
        return True

    def is_active_on_cluster(self, k8s_client: K8sApiClient) -> bool:
        """Returns True if the resource is running on the K8s Cluster"""
        active_resource = self.read(k8s_client=k8s_client)
        if active_resource is not None:
            return True
        return False

    ######################################################
    ## Building the k8s_manifest
    ######################################################

    def get_k8s_manifest_dict(self) -> Optional[Dict[str, Any]]:
        """Returns the K8s Manifest for this Object as a dict"""

        from itertools import chain

        k8s_manifest: Dict[str, Any] = {}
        all_attributes: Dict[str, Any] = self.dict(exclude_defaults=True, by_alias=True)
        # logger.debug("All Attributes: {}".format(all_attributes))
        for attr_name in chain(
            self.fields_for_k8s_manifest_base, self.fields_for_k8s_manifest
        ):
            if attr_name in all_attributes:
                k8s_manifest[attr_name] = all_attributes[attr_name]
        # logger.debug(f"k8s_manifest:\n{k8s_manifest}")
        return k8s_manifest

    def get_k8s_manifest_yaml(self, **kwargs) -> Optional[str]:
        """Returns the K8s Manifest for this Object as a yaml"""
        import yaml

        k8s_manifest_dict = self.get_k8s_manifest_dict()

        if k8s_manifest_dict is not None:
            return yaml.safe_dump(k8s_manifest_dict, **kwargs)
        return None

    def get_k8s_manifest_json(self, **kwargs) -> Optional[str]:
        """Returns the K8s Manifest for this Object as a json"""
        import json

        k8s_manifest_dict = self.get_k8s_manifest_dict()

        if k8s_manifest_dict is not None:
            return json.dumps(k8s_manifest_dict, **kwargs)
        return None
