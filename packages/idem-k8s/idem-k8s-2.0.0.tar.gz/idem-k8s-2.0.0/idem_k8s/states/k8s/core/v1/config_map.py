"""State module for managing Kubernetes ConfigMap."""
import copy
from typing import Any
from typing import Dict

from dict_tools import differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    metadata: Dict,
    immutable: bool = False,
    data: Dict = None,
    binary_data: Dict = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create a ConfigMap

    Args:
        name(str): An Idem name of the resource.
        metadata(dict): Standard object's metadata.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.>`_
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        binary_data(dict, Optional): BinaryData contains the binary data. Each key must consist of alphanumeric characters, '-', '_'
            or '.'. BinaryData can contain byte sequences that are not in the UTF-8 range. The keys stored
            in BinaryData must not overlap with the ones in the Data field, this is enforced during
            validation process. Using this field will require 1.10+ apiserver and kubelet.
        data(dict, Optional): Data contains the configuration data. Each key must consist of alphanumeric characters, '-', '_'
            or '.'. Values with non-UTF-8 byte sequences must use the BinaryData field. The keys stored in
            Data must not overlap with the keys in the BinaryData field, this is enforced during validation
            process.
        immutable(bool, Optional): Immutable, if set to true, ensures that data stored in the ConfigMap cannot be updated (only
            object metadata can be modified). If not set to true, the field can be modified at any time.
            Defaulted to nil.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              k8s.core.v1.config_map.present:
                - name: idem-config-map-test
                - data:
                      adminRoles: test-admin
                      clientType: test-clientType
                      viewerRoles: test-viewerRoles
                - metadata:
                      annotations:
                        meta.helm.sh/release-name: test-release
                        meta.helm.sh/release-namespace: test-release-default
                      labels:
                        app: test-app
                        environment: test-environment
                        product: test-product
                      name: idem-config-map-test
                      namespace: default

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Get namespace
    namespace = metadata.get("namespace") if "namespace" in metadata else "default"
    metadata["namespace"] = namespace

    # Check for existing config_map by name in namespace
    before = None
    if resource_id:
        config_map = await hub.exec.k8s.client.CoreV1Api.read_namespaced_config_map(
            ctx, name=resource_id, namespace=namespace
        )
        if not config_map["result"]:
            result["comment"] = config_map["comment"]
            result["result"] = config_map["result"]
            return result
        before = config_map["ret"]

    # Update current state
    current_state = (
        hub.tool.k8s.core.v1.config_map_utils.convert_raw_config_map_to_present(
            config_map=before
        )
    )
    result["old_state"] = current_state

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "metadata": metadata,
        "immutable": immutable,
    }

    if data:
        desired_state["data"] = data
    if binary_data:
        desired_state["binary_data"] = binary_data

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )
    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.core.v1.config_map", name=name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result

    # Handle test behaviour
    if ctx.get("test", False):
        result["new_state"] = hub.tool.k8s.test_state_utils.generate_test_state(
            enforced_state=current_state,
            desired_state=desired_state,
        )
        result["comment"] = (
            hub.tool.k8s.comment_utils.would_update_comment(
                resource_type="k8s.core.v1.config_map", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.core.v1.config_map", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1ConfigMap"
    )
    if before:
        ret = await hub.exec.k8s.client.CoreV1Api.replace_namespaced_config_map(
            ctx, name=resource_id, namespace=namespace, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.core.v1.config_map", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.create_namespaced_config_map(
            ctx, namespace=namespace, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.core.v1.config_map", name=name
        )

    # Fetch the updated resource and update new_state
    config_map = await hub.exec.k8s.client.CoreV1Api.read_namespaced_config_map(
        ctx, name=resource_id, namespace=namespace
    )
    if not config_map["result"]:
        result["comment"] = result["comment"] + config_map["comment"]
        result["result"] = config_map["result"]
        return result
    after = config_map["ret"]
    result[
        "new_state"
    ] = hub.tool.k8s.core.v1.config_map_utils.convert_raw_config_map_to_present(
        config_map=after
    )
    return result


async def absent(
    hub,
    ctx,
    name: str,
    metadata: Dict = dict(namespace="default"),
    resource_id: str = None,
) -> Dict[str, Any]:
    """Delete a ConfigMap

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict, Optional): Standard object's metadata.
            Defaults to metadata with 'default' namespace, in case of value not provided in absent state.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.>`_

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              k8s.core.v1.config_map.absent:
                - name: value
                - metadata: value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    namespace = metadata.get("namespace") if "namespace" in metadata else "default"

    before = None
    if resource_id:
        config_map = await hub.exec.k8s.client.CoreV1Api.read_namespaced_config_map(
            ctx, name=resource_id, namespace=namespace
        )
        if config_map and config_map["result"]:
            before = config_map["ret"]
            result[
                "old_state"
            ] = hub.tool.k8s.core.v1.config_map_utils.convert_raw_config_map_to_present(
                config_map=before
            )

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.core.v1.config_map", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.core.v1.config_map", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.delete_namespaced_config_map(
            ctx, name=resource_id, namespace=namespace
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.core.v1.config_map", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    List or watch objects of kind ConfigMap

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe k8s.core.v1.config_map

    """
    ret = await hub.exec.k8s.client.CoreV1Api.list_config_map_for_all_namespaces(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe config_map {ret['comment']}")
        return {}

    result = {}
    for config_map in ret["ret"].items:
        config_map_resource = (
            hub.tool.k8s.core.v1.config_map_utils.convert_raw_config_map_to_present(
                config_map=config_map
            )
        )
        result[config_map.metadata.name] = {
            "k8s.core.v1.config_map.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in config_map_resource.items()
            ]
        }
    return result
