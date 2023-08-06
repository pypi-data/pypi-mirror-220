"""State module for managing Kubernetes StorageClass."""
import copy
from typing import Any
from typing import Dict
from typing import List

from dict_tools import differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    metadata: Dict,
    provisioner: str,
    allow_volume_expansion: bool = True,
    allowed_topologies: List = None,
    mount_options: List = None,
    parameters: Dict = None,
    reclaim_policy: str = None,
    volume_binding_mode: str = "Immediate",
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create a StorageClass.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        allow_volume_expansion(bool, Optional): AllowVolumeExpansion shows whether the storage class allow volume
            expand.
        allowed_topologies(list, Optional): Restrict the node topologies where volumes can be dynamically provisioned.
            Each volume plugin defines its own supported topology specifications.
            An empty TopologySelectorTerm list means there is no topology restriction.
            This field is only honored by servers that enable the VolumeScheduling feature.
        metadata(dict): Standard object's metadata.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-
            architecture/api-conventions.md#metadata.>`_
        mount_options(list, Optional): Dynamically provisioned PersistentVolumes of this storage class are created with
            these mountOptions, e.g. ["ro", "soft"]. Not validated - mount of the PVs will simply fail if one is
            invalid.
        parameters(dict, Optional): Parameters holds the parameters for the provisioner that should create volumes of
            this storage class.
        provisioner(str): Provisioner indicates the type of the provisioner.
        reclaim_policy(str, Optional): Dynamically provisioned PersistentVolumes of this storage class are created with
            this reclaimPolicy. Defaults to Delete.
        volume_binding_mode(str, Optional): VolumeBindingMode indicates how PersistentVolumeClaims should be
            provisioned and bound. When unset, VolumeBindingImmediate is used. This field is only honored by servers
            that enable the VolumeScheduling feature.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              k8s.storage_k8s_io.v1.storage_class.present:
                - name: storage_class_1
                - allow_volume_expansion: true
                - allowed_topologies:
                    - match_label_expressions:
                        - key: "failure-domain.beta.kubernetes.io/zone"
                          values: ["us-west-2a"]
                - metadata:
                    name: "storage_class_1"
                - mount_options: ["soft"]
                - parameters:
                    type: "gp2"
                    iopsPerGB: "10"
                - provisioner: "kubernetes.io/aws-ebs"
                - reclaim_policy: "Retain"
                - volume_binding_mode: "WaitForFirstConsumer"

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Check for existing storage_class by name
    before = None
    if resource_id:
        storage_class = await hub.exec.k8s.client.StorageV1Api.read_storage_class(
            ctx, name=resource_id
        )
        if not storage_class["result"]:
            result["comment"] = storage_class["comment"]
            result["result"] = storage_class["result"]
            return result
        before = storage_class["ret"]

    # Update current state
    current_state = hub.tool.k8s.storage_k8s_io.v1.storage_class_utils.convert_raw_storage_class_to_present(
        storage_class=before
    )
    result["old_state"] = current_state

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "allow_volume_expansion": allow_volume_expansion,
        "metadata": metadata,
        "provisioner": provisioner,
        "reclaim_policy": reclaim_policy,
        "volume_binding_mode": volume_binding_mode,
    }

    if allowed_topologies:
        desired_state["allowed_topologies"] = allowed_topologies
    if mount_options:
        desired_state["mount_options"] = mount_options
    if parameters:
        desired_state["parameters"] = parameters

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )
    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.storage_k8s_io.v1.storage_class", name=name
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
                resource_type="k8s.storage_k8s_io.v1.storage_class", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.storage_k8s_io.v1.storage_class", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1StorageClass"
    )
    if before:
        ret = await hub.exec.k8s.client.StorageV1Api.replace_storage_class(
            ctx, name=resource_id, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.storage_k8s_io.v1.storage_class", name=name
        )
    else:
        ret = await hub.exec.k8s.client.StorageV1Api.create_storage_class(
            ctx, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.storage_k8s_io.v1.storage_class", name=name
        )

    # Fetch the updated resource and update new_state
    storage_class = await hub.exec.k8s.client.StorageV1Api.read_storage_class(
        ctx, name=resource_id
    )
    if not storage_class["result"]:
        result["comment"] = result["comment"] + storage_class["comment"]
        result["result"] = storage_class["result"]
        return result
    after = storage_class["ret"]
    result[
        "new_state"
    ] = hub.tool.k8s.storage_k8s_io.v1.storage_class_utils.convert_raw_storage_class_to_present(
        storage_class=after
    )
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Delete a StorageClass.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              k8s.storage_k8s_io.v1.storage_class.absent:
                - name: value
                - resource_id: value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    before = None
    if resource_id:
        storage_class = await hub.exec.k8s.client.StorageV1Api.read_storage_class(
            ctx, name=resource_id
        )
        if storage_class and storage_class["result"]:
            before = storage_class["ret"]
            result[
                "old_state"
            ] = hub.tool.k8s.storage_k8s_io.v1.storage_class_utils.convert_raw_storage_class_to_present(
                storage_class=before
            )

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.storage_k8s_io.v1.storage_class", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.storage_k8s_io.v1.storage_class", name=name
        )
    else:
        ret = await hub.exec.k8s.client.StorageV1Api.delete_storage_class(
            ctx, name=resource_id
        )
        result["result"] = ret["result"]
        result["comment"] = (
            hub.tool.k8s.comment_utils.delete_comment(
                resource_type="k8s.storage_k8s_io.v1.storage_class", name=name
            )
            if result["result"]
            else ret["comment"]
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    List or watch objects of kind StorageClass.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe k8s.storage_k8s_io.v1.storage_class

    """
    ret = await hub.exec.k8s.client.StorageV1Api.list_storage_class(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe storage_class {ret['comment']}")
        return {}

    result = {}
    for storage_class in ret["ret"].items:
        storage_class_resource = hub.tool.k8s.storage_k8s_io.v1.storage_class_utils.convert_raw_storage_class_to_present(
            storage_class=storage_class
        )
        result[storage_class.metadata.name] = {
            "k8s.storage_k8s_io.v1.storage_class.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in storage_class_resource.items()
            ]
        }
    return result
