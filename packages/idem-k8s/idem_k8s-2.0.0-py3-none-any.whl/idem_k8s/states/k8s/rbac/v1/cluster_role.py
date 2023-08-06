"""State module for managing Kubernetes ClusterRole."""
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
    aggregation_rule: Dict = None,
    rules: List = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create a ClusterRole

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        aggregation_rule(dict, Optional):
            AggregationRule is an optional field that describes how to build the Rules for this ClusterRole.
            If AggregationRule is set, then the Rules are controller managed and direct changes to Rules
            will be stomped by the controller.
        metadata(dict): Standard object's metadata.
        rules(list, Optional): Rules holds all the PolicyRules for this ClusterRole.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              k8s.rbac.v1.cluster_role.present:
              - name: value
              - metadata:
                  name: idem-test-cluster-role
              - rules:
                - api_groups:
                  - test.com
                  resources:
                  - vaconfigs
                  verbs:
                  - get
                  - list
                  - watch

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Check for existing cluster_role by name
    before = None
    if resource_id:
        cluster_role = (
            await hub.exec.k8s.client.RbacAuthorizationV1Api.read_cluster_role(
                ctx, name=resource_id
            )
        )
        if not cluster_role["result"]:
            result["comment"] = cluster_role["comment"]
            result["result"] = cluster_role["result"]
            return result
        before = cluster_role["ret"]

    # Update current state
    current_state = (
        hub.tool.k8s.rbac.v1.cluster_role_utils.convert_raw_cluster_role_to_present(
            cluster_role=before
        )
    )
    result["old_state"] = current_state

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "metadata": metadata,
    }

    if aggregation_rule:
        desired_state["aggregation_rule"] = aggregation_rule
    if rules:
        desired_state["rules"] = rules

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )

    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.rbac.v1.cluster_role", name=name
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
                resource_type="k8s.rbac.v1.cluster_role", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.rbac.v1.cluster_role", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1ClusterRole"
    )
    if before:
        ret = await hub.exec.k8s.client.RbacAuthorizationV1Api.replace_cluster_role(
            ctx, name=resource_id, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.rbac.v1.cluster_role", name=name
        )
    else:
        ret = await hub.exec.k8s.client.RbacAuthorizationV1Api.create_cluster_role(
            ctx, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.rbac.v1.cluster_role", name=name
        )

    # Fetch the updated resource and update new_state
    cluster_role = await hub.exec.k8s.client.RbacAuthorizationV1Api.read_cluster_role(
        ctx, name=resource_id
    )
    if not cluster_role["result"]:
        result["comment"] = result["comment"] + cluster_role["comment"]
        result["result"] = cluster_role["result"]
        return result
    after = cluster_role["ret"]
    result[
        "new_state"
    ] = hub.tool.k8s.rbac.v1.cluster_role_utils.convert_raw_cluster_role_to_present(
        cluster_role=after
    )
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Delete a ClusterRole

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              k8s.rbac.v1.cluster_role.absent:
                - name: value
                - resource_id: value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    before = None
    if resource_id:
        cluster_role = (
            await hub.exec.k8s.client.RbacAuthorizationV1Api.read_cluster_role(
                ctx, name=resource_id
            )
        )
        if cluster_role and cluster_role["result"]:
            before = cluster_role["ret"]
            result[
                "old_state"
            ] = hub.tool.k8s.rbac.v1.cluster_role_utils.convert_raw_cluster_role_to_present(
                cluster_role=before
            )

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.rbac.v1.cluster_role", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.rbac.v1.cluster_role", name=name
        )
    else:
        ret = await hub.exec.k8s.client.RbacAuthorizationV1Api.delete_cluster_role(
            ctx, name=resource_id
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.rbac.v1.cluster_role", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    List or watch objects of kind ClusterRole.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe k8s.rbac.v1.cluster_role

    """
    ret = await hub.exec.k8s.client.RbacAuthorizationV1Api.list_cluster_role(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe cluster_role {ret['comment']}")
        return {}

    result = {}
    for cluster_role in ret["ret"].items:
        cluster_role_resource = (
            hub.tool.k8s.rbac.v1.cluster_role_utils.convert_raw_cluster_role_to_present(
                cluster_role=cluster_role
            )
        )
        result[cluster_role.metadata.name] = {
            "k8s.rbac.v1.cluster_role.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in cluster_role_resource.items()
            ]
        }
    return result
