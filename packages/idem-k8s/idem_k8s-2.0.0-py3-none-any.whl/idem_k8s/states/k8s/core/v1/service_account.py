"""State module for managing Kubernetes ServiceAccount."""
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
    automount_service_account_token: bool = True,
    image_pull_secrets: List = None,
    secrets: List = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create a ServiceAccount

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        automount_service_account_token(bool, Optional):
            AutomountServiceAccountToken indicates whether pods running as this service account should have
            an API token automatically mounted. Can be overridden at the pod level.
        image_pull_secrets(list, Optional):
            ImagePullSecrets is a list of references to secrets in the same namespace to use for pulling any
            images in pods that reference this ServiceAccount. ImagePullSecrets are distinct from Secrets
            because Secrets can be mounted in the pod, but ImagePullSecrets are only accessed by the
            kubelet. More info: `Kubernetes reference <https://kubernetes.io/docs/concepts/containers/images/#specifying-
            imagepullsecrets-on-a-pod>`_.
        metadata(dict): Standard object's metadata.
            More info: `Kubernetes metadata reference <https://git.k8s.io/community/contributors/devel/sig-
            architecture/api-conventions.md#metadata.>`_.
        secrets(list, Optional): Secrets is the list of secrets allowed to be used by pods running using this ServiceAccount.
            More info: `Kubernetes secret reference <https://kubernetes.io/docs/concepts/configuration/secret.>`_.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              k8s.core.v1.service_account.present:
                - name: value
                - metadata:
                  name: idem-service-account-test
                  namespace: default
                  labels:
                    example-label-name: example-label-value
                - automount_service_account_token: false

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Get namespace
    namespace = metadata.get("namespace") if "namespace" in metadata else "default"
    metadata["namespace"] = namespace

    # Check for existing service_account by name in namespace
    before = None
    if resource_id:
        service_account = (
            await hub.exec.k8s.client.CoreV1Api.read_namespaced_service_account(
                ctx, name=resource_id, namespace=namespace
            )
        )
        if not service_account["result"]:
            result["comment"] = service_account["comment"]
            result["result"] = service_account["result"]
            return result
        before = service_account["ret"]

    # Update current state
    current_state = hub.tool.k8s.core.v1.service_account_utils.convert_raw_service_account_to_present(
        service_account=before
    )
    result["old_state"] = current_state

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "automount_service_account_token": automount_service_account_token,
        "metadata": metadata,
    }

    if image_pull_secrets:
        desired_state["image_pull_secrets"] = image_pull_secrets

    # For the brownfield scenario, if ESM does not contain service_account information and secrets are None in the
    # SLS file, existing secrets of the service account should be used.
    if secrets:
        desired_state["secrets"] = secrets
    elif current_state:
        desired_state["secrets"] = current_state.get("secrets")

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )
    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.core.v1.service_account", name=name
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
                resource_type="k8s.core.v1.service_account", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.core.v1.service_account", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1ServiceAccount"
    )
    if before:
        ret = await hub.exec.k8s.client.CoreV1Api.replace_namespaced_service_account(
            ctx, name=resource_id, namespace=namespace, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.core.v1.service_account", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.create_namespaced_service_account(
            ctx, namespace=namespace, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.core.v1.service_account", name=name
        )

    # Fetch the updated resource and update new_state
    service_account = (
        await hub.exec.k8s.client.CoreV1Api.read_namespaced_service_account(
            ctx, name=resource_id, namespace=namespace
        )
    )
    if not service_account["result"]:
        result["comment"] = result["comment"] + service_account["comment"]
        result["result"] = service_account["result"]
        return result
    after = service_account["ret"]
    result[
        "new_state"
    ] = hub.tool.k8s.core.v1.service_account_utils.convert_raw_service_account_to_present(
        service_account=after
    )
    return result


async def absent(
    hub,
    ctx,
    name: str,
    metadata: Dict = dict(namespace="default"),
    resource_id: str = None,
) -> Dict[str, Any]:
    """Delete a ServiceAccount

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict, Optional): Standard object's metadata.
            Defaults to metadata with 'default' namespace, in case of value not provided in absent state.
            More info: `Kubernetes metadata reference <https://git.k8s.io/community/contributors/devel/sig-
            architecture/api-conventions.md#metadata.>`_

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              k8s.core.v1.service_account.absent:
                - name: value
                - metadata: value
                - resource_id: value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    namespace = metadata.get("namespace") if "namespace" in metadata else "default"

    before = None
    if resource_id:
        service_account = (
            await hub.exec.k8s.client.CoreV1Api.read_namespaced_service_account(
                ctx, name=resource_id, namespace=namespace
            )
        )
        if service_account and service_account["result"]:
            before = service_account["ret"]
            result[
                "old_state"
            ] = hub.tool.k8s.core.v1.service_account_utils.convert_raw_service_account_to_present(
                service_account=before
            )

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.core.v1.service_account", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.core.v1.service_account", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.delete_namespaced_service_account(
            ctx, name=resource_id, namespace=namespace
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.core.v1.service_account", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    List or watch objects of kind ServiceAccount.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe k8s.core.v1.service_account

    """
    ret = await hub.exec.k8s.client.CoreV1Api.list_service_account_for_all_namespaces(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe service_account {ret['comment']}")
        return {}

    result = {}
    for service_account in ret["ret"].items:
        service_account_resource = hub.tool.k8s.core.v1.service_account_utils.convert_raw_service_account_to_present(
            service_account=service_account
        )
        result[service_account.metadata.name] = {
            "k8s.core.v1.service_account.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in service_account_resource.items()
            ]
        }
    return result
