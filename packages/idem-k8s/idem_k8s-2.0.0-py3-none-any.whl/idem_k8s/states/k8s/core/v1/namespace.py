"""State module for managing Kubernetes Namespace."""
import copy
from typing import Any
from typing import Dict
from typing import Tuple

from dict_tools import differ

__contracts__ = ["resource"]


async def present(
    hub, ctx, name: str, metadata: Dict, resource_id: str = None
) -> Dict[str, Any]:
    """Create a Namespace

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict): Standard object's metadata.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.>`_

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              k8s.core.v1.namespace.present:
              - name: idem-test
              - metadata:
                  name: idem-test
                  labels:
                    example-label-name: example-label-value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Check for existing namespace by name
    before = None
    if resource_id:
        namespace = await hub.exec.k8s.client.CoreV1Api.read_namespace(
            ctx, name=resource_id
        )
        if not namespace["result"]:
            result["comment"] = namespace["comment"]
            result["result"] = namespace["result"]
            return result
        before = namespace["ret"]

    # Update current state
    current_state = (
        hub.tool.k8s.core.v1.namespace_utils.convert_raw_namespace_to_present(
            namespace=before
        )
    )
    result["old_state"] = current_state

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "metadata": metadata,
    }

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )

    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.core.v1.namespace", name=name
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
                resource_type="k8s.core.v1.namespace", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.core.v1.namespace", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1Namespace"
    )
    if before:
        ret = await hub.exec.k8s.client.CoreV1Api.replace_namespace(
            ctx, name=resource_id, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.core.v1.namespace", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.create_namespace(ctx, body=body)
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.core.v1.namespace", name=name
        )

    # Fetch the updated resource and update new_state
    namespace = await hub.exec.k8s.client.CoreV1Api.read_namespace(
        ctx, name=resource_id
    )
    if not namespace["result"]:
        result["comment"] = result["comment"] + namespace["comment"]
        result["result"] = namespace["result"]
        return result
    after = namespace["ret"]
    result[
        "new_state"
    ] = hub.tool.k8s.core.v1.namespace_utils.convert_raw_namespace_to_present(
        namespace=after
    )
    return result


async def absent(
    hub, ctx, name: str, resource_id: str = None, timeout: Dict = None
) -> Dict[str, Any]:
    """Delete a Namespace

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        timeout(dict, Optional): Timeout configuration for resource deletion.

            * delete (dict) -- Timeout configuration for resource deletion
                * delay(int, Optional) -- The amount of time in seconds to wait between attempts. Defaults to 15
                * max_attempts(int, Optional) -- Customized timeout configuration containing delay and max attempts. Defaults to 40.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              k8s.core.v1.namespace.absent:
                - name: value
                - resource_id: value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    before = None
    if resource_id:
        namespace = await hub.exec.k8s.client.CoreV1Api.read_namespace(
            ctx, name=resource_id
        )
        if namespace and namespace["result"]:
            before = namespace["ret"]
            result[
                "old_state"
            ] = hub.tool.k8s.core.v1.namespace_utils.convert_raw_namespace_to_present(
                namespace=before
            )

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.core.v1.namespace", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.core.v1.namespace", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.delete_namespace(
            ctx, name=resource_id
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        # Custom waiter for delete
        waiter_config = hub.tool.k8s.waiter_utils.create_waiter_config(
            timeout_config=timeout.get("delete") if timeout else None,
        )

        def delete_acceptor(
            status: bool, data: Dict = None, comment: Tuple = None
        ) -> bool:
            if not status and '"reason":"NotFound"' in comment[0]:
                return True
            if not status:
                raise RuntimeError(
                    f"Error while waiting for delete namespace : {comment[0]}"
                )
            return False

        arguments = {"name": resource_id}
        result_arguments = {"condition": "status.condition"}

        namespace_waiter = hub.tool.k8s.waiter_utils.create_waiter(
            api_class_name="CoreV1Api",
            operation="read_namespace",
            arguments=arguments,
            result_arguments=result_arguments,
            acceptor_function=delete_acceptor,
        )
        try:
            await hub.tool.k8s.custom_waiter.wait(
                ctx,
                waiter=namespace_waiter,
                waiter_config=waiter_config,
                err_graceful=True,
            )
        except Exception as e:
            result["comment"] = result["comment"] + (str(e),)
            result["result"] = False
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.core.v1.namespace", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    List or watch objects of kind Namespace.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe k8s.core.v1.namespace

    """
    ret = await hub.exec.k8s.client.CoreV1Api.list_namespace(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe namespace {ret['comment']}")
        return {}

    result = {}
    for namespace in ret["ret"].items:
        namespace_resource = (
            hub.tool.k8s.core.v1.namespace_utils.convert_raw_namespace_to_present(
                namespace=namespace
            )
        )
        result[namespace.metadata.name] = {
            "k8s.core.v1.namespace.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in namespace_resource.items()
            ]
        }
    return result
