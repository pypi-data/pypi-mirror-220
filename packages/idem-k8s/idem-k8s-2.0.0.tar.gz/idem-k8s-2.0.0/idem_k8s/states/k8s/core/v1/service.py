"""State module for managing Kubernetes Service."""
import copy
from typing import Any
from typing import Dict
from typing import Tuple

from dict_tools import differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    metadata: Dict,
    spec: Dict,
    resource_id: str = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """create a Service

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict): Standard object's metadata.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-
            architecture/api-conventions.md#metadata.>`_
        spec(dict): Spec defines the behavior of a service.
            More info: `Kubernetes Spec reference <https://git.k8s.io/community/contributors/devel/sig-
            architecture/api-conventions.md#spec-and-status.>`_
        timeout(dict, Optional): Timeout configuration for resource creation.

            * create (dict) -- Timeout configuration for resource creation
                * delay(int, Optional) -- The amount of time in seconds to wait between attempts.
                  Defaults to 15 in case of None.
                * max_attempts(int, Optional) -- Customized timeout configuration containing delay and max attempts.
                  Defaults to 40 in case of None.

    Request Syntax:
        .. code-block:: sls

            [service-name]:
              k8s.core.v1.service.present:
                - name: "string"
                - metadata: "Dict"
                - spec: "Dict"
                - resource_id: "string"
                - timeout: "Dict"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              k8s.core.v1.service.present:
                - name: idem-test-service
                - metadata:
                    name: idem-test-secret
                    namespace: default
                - spec:
                    type: NodePort
                    selector:
                      app: echo-hostname
                    ports:
                      - nodePort: 30163
                        port: 8080
                        targetPort: 80

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Get namespace
    namespace = metadata.get("namespace") if "namespace" in metadata else "default"
    metadata["namespace"] = namespace

    # Check for existing service by name in namespace
    before = None
    if resource_id:
        service = await hub.exec.k8s.core.v1.service.get(
            ctx, name=name, resource_id=resource_id, namespace=namespace
        )
        if not service["result"] or not service["ret"]:
            result["result"] = False
            result["comment"] = tuple(service["comment"])
            return result
        before = service["ret"]

    # Update current state
    result["old_state"] = before

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "metadata": metadata,
        "spec": spec,
        "timeout": timeout,
    }
    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )

    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.core.v1.service", name=name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result

    # Handle test behaviour
    if ctx.get("test", False):
        result["new_state"] = hub.tool.k8s.test_state_utils.generate_test_state(
            enforced_state=result["old_state"],
            desired_state=desired_state,
        )
        result["comment"] = (
            hub.tool.k8s.comment_utils.would_update_comment(
                resource_type="k8s.core.v1.service", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.core.v1.service", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1Service"
    )
    if before:
        ret = await hub.exec.k8s.client.CoreV1Api.replace_namespaced_service(
            ctx, name=resource_id, namespace=namespace, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.core.v1.service", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.create_namespaced_service(
            ctx, namespace=namespace, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.core.v1.service", name=name
        )

    # Custom waiter for create/update
    waiter_config = hub.tool.k8s.waiter_utils.create_waiter_config(
        default_delay=15,
        default_max_attempts=40,
        timeout_config=timeout.get("create") if timeout else None,
    )

    def create_acceptor(status: bool, data: Dict = None, comment: Tuple = None) -> bool:
        service_type = data.get("type")
        if service_type == "LoadBalancer":
            load_balancer = (
                data.get("load_balancer") if data.get("load_balancer") else {}
            )
            if load_balancer:
                ingress = load_balancer.get("ingress") or []
                if ingress and (not ingress[0].get("hostname")):
                    hub.log.debug(
                        f"'status.load_balancer.ingress[0].hostname' is still empty for service: "
                        f"{data.get('resource_id')}"
                    )
                    return False
        return True

    arguments = {"name": resource_id, "namespace": namespace}
    result_arguments = {
        "load_balancer": "status.load_balancer",
        "type": "spec.type",
        "resource_id": "metadata.name",
    }
    service_waiter = hub.tool.k8s.waiter_utils.create_waiter(
        api_class_name="CoreV1Api",
        operation="read_namespaced_service",
        arguments=arguments,
        result_arguments=result_arguments,
        acceptor_function=create_acceptor,
    )
    try:
        await hub.tool.k8s.custom_waiter.wait(
            ctx, waiter=service_waiter, waiter_config=waiter_config, err_graceful=False
        )
    except Exception as e:
        result["comment"] += (str(e),)
        result["result"] = False
        return result

    # Fetch the updated resource and update new_state
    service = await hub.exec.k8s.core.v1.service.get(
        ctx, name=name, resource_id=resource_id, namespace=namespace
    )
    if not service["result"]:
        result["comment"] += service["comment"]
        result["result"] = service["result"]
        return result
    after = service["ret"]
    result["new_state"] = after
    return result


async def absent(
    hub,
    ctx,
    name: str,
    metadata: Dict = dict(namespace="default"),
    resource_id: str = None,
) -> Dict[str, Any]:
    """delete a Service

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict, Optional): Standard object's metadata.
            Defaults to metadata with 'default' namespace, in case of value not provided in absent state.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-
            architecture/api-conventions.md#metadata.>`_

    Request Syntax:
      .. code-block:: sls

           [service-name]:
              k8s.core.v1.service.absent:
                - name: 'string'
                - metadata: 'Dict'
                - resource_id: 'string'

    Returns:
      Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              k8s.core.v1.service.absent:
                - name: value
                - metadata: value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    namespace = metadata.get("namespace") if "namespace" in metadata else "default"

    before = None
    if resource_id:
        service = await hub.exec.k8s.core.v1.service.get(
            ctx, name=name, resource_id=resource_id, namespace=namespace
        )
        if service and service["result"]:
            before = service["ret"]
            result["old_state"] = before

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.core.v1.service", name=name
        )
    else:
        if ctx.get("test", False):
            result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
                resource_type="k8s.core.v1.service", name=name
            )
            return result
        else:
            ret = await hub.exec.k8s.client.CoreV1Api.delete_namespaced_service(
                ctx, name=resource_id, namespace=namespace
            )
            if not ret["result"]:
                result["result"] = False
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
                resource_type="k8s.core.v1.service", name=name
            )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    List or watch objects of kind Service

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe k8s.core.v1.service

    """
    ret = await hub.exec.k8s.client.CoreV1Api.list_service_for_all_namespaces(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe service {ret['comment']}")
        return {}

    result = {}
    for service in ret["ret"].items:
        service_resource = (
            hub.tool.k8s.core.v1.service_utils.convert_raw_service_to_present(
                service=service
            )
        )
        result[service.metadata.name] = {
            "k8s.core.v1.service.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in service_resource.items()
            ]
        }
    return result
