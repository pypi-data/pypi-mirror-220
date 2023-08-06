"""State module for managing Kubernetes Deployment."""
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
    """create/update a Deployment

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict): Standard object's metadata.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.>`_
        spec(dict): Specification of the desired behavior of the Deployment.
        timeout(dict, Optional): Timeout configuration for resource creation.

          * create (dict) -- Timeout configuration for resource creation
                * delay(int, Optional) -- The amount of time in seconds to wait between attempts. Defaults to 15
                * max_attempts(int, Optional)  -- Customized timeout configuration containing delay and max attempts. Defaults to 40.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              k8s.apps.v1.deployment.present:
              - metadata:
                  name: nginx-deployment
                  namespace: default
              - spec:
                  replicas: 1
                  selector:
                    match_labels:
                      app: nginx
                  strategy:
                    rolling_update:
                      max_surge: 25%
                      max_unavailable: 25%
                    type: RollingUpdate
                  template:
                    metadata:
                      labels:
                        app: nginx
                    spec:
                      containers:
                      - image: nginx:1.14.2
                        image_pull_policy: IfNotPresent
                        name: nginx
                        ports:
                        - container_port: 80
                          protocol: TCP
                        termination_message_path: /dev/termination-log
                        termination_message_policy: File
                      restart_policy: Always

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Get namespace
    namespace = metadata.get("namespace") if "namespace" in metadata else "default"
    metadata["namespace"] = namespace

    # Check for existing deployment by name in namespace
    before = None
    if resource_id:
        deployment = await hub.exec.k8s.client.AppsV1Api.read_namespaced_deployment(
            ctx, name=resource_id, namespace=namespace
        )
        if not deployment["result"]:
            result["comment"] = deployment["comment"]
            result["result"] = deployment["result"]
            return result
        before = deployment["ret"]

    # Update current state
    current_state = (
        hub.tool.k8s.apps.v1.deployment_utils.convert_raw_deployment_to_present(
            deployment=before
        )
    )
    result["old_state"] = current_state

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "metadata": metadata,
        "spec": spec,
    }

    desired_state = hub.tool.k8s.apps.v1.deployment_utils.handle_default_values(
        desired_state=desired_state
    )

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )

    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.apps.v1.deployment", name=name
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
                resource_type="k8s.apps.v1.deployment", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.apps.v1.deployment", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1Deployment"
    )
    if before:
        ret = await hub.exec.k8s.client.AppsV1Api.replace_namespaced_deployment(
            ctx, name=resource_id, namespace=namespace, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.apps.v1.deployment", name=name
        )
    else:
        ret = await hub.exec.k8s.client.AppsV1Api.create_namespaced_deployment(
            ctx, namespace=namespace, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.apps.v1.deployment", name=name
        )

    # Custom waiter for create/update
    waiter_config = hub.tool.k8s.waiter_utils.create_waiter_config(
        timeout_config=timeout.get("create") if timeout else None,
    )

    def create_acceptor(status: bool, data: Dict = None, comment: Tuple = None) -> bool:
        conditions = data.get("conditions") if data.get("conditions") else []
        for condition in conditions:
            if (
                condition.get("type") == "Progressing"
                and bool(condition.get("status"))
                and condition.get("reason") == "NewReplicaSetAvailable"
            ):
                return True
            if condition.get("type") == "Progressing" and not bool(
                condition.get("status")
            ):
                raise RuntimeError(
                    f"reason : {condition.get('reason')}, message: {condition.get('message')}"
                )

        return False

    arguments = {"name": resource_id, "namespace": namespace}
    result_arguments = {"conditions": "status.conditions"}
    deployment_waiter = hub.tool.k8s.waiter_utils.create_waiter(
        api_class_name="AppsV1Api",
        operation="read_namespaced_deployment",
        arguments=arguments,
        result_arguments=result_arguments,
        acceptor_function=create_acceptor,
    )
    try:
        await hub.tool.k8s.custom_waiter.wait(
            ctx,
            waiter=deployment_waiter,
            waiter_config=waiter_config,
            err_graceful=False,
        )
    except Exception as e:
        message = f"Deployment resource {name} is unavailable."
        result["comment"] = result["comment"] + (str(e),) + (message,)

    # Fetch the updated resource and update new_state
    deployment = await hub.exec.k8s.client.AppsV1Api.read_namespaced_deployment(
        ctx, name=resource_id, namespace=namespace
    )
    if not deployment["result"]:
        result["comment"] = result["comment"] + deployment["comment"]
        result["result"] = deployment["result"]
        return result
    after = deployment["ret"]
    result[
        "new_state"
    ] = hub.tool.k8s.apps.v1.deployment_utils.convert_raw_deployment_to_present(
        deployment=after
    )
    return result


async def absent(
    hub,
    ctx,
    name: str,
    metadata: Dict = dict(namespace="default"),
    resource_id: str = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """Delete a Deployment

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict, Optional): Standard object's metadata.
            Defaults to metadata with 'default' namespace, in case of value not provided in absent state.
            More info: `Kubernetes reference <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.>`_
        timeout(dict, Optional): Timeout configuration for resource deletion.

            * delete(dict) -- Timeout configuration for resource deletion
                * delay(int, Optional) -- The amount of time in seconds to wait between attempts. Defaults to 15
                * max_attempts(int, Optional) -- Customized timeout configuration containing delay and max attempts. Defaults to 40.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              k8s.apps.v1.deployment.absent:
                - name: value
                - metadata: value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    namespace = metadata.get("namespace") if "namespace" in metadata else "default"

    before = None
    if resource_id:
        deployment = await hub.exec.k8s.client.AppsV1Api.read_namespaced_deployment(
            ctx, name=resource_id, namespace=namespace
        )
        if deployment and deployment["result"]:
            before = deployment["ret"]
            result[
                "old_state"
            ] = hub.tool.k8s.apps.v1.deployment_utils.convert_raw_deployment_to_present(
                deployment=before
            )

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.apps.v1.deployment", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.apps.v1.deployment", name=name
        )
    else:
        ret = await hub.exec.k8s.client.AppsV1Api.delete_namespaced_deployment(
            ctx, name=resource_id, namespace=namespace
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
                    f"Error while waiting for delete deployment : {comment[0]}"
                )
            return False

        arguments = {"name": resource_id, "namespace": namespace}
        result_arguments = {"condition": "status.condition"}

        deployment_waiter = hub.tool.k8s.waiter_utils.create_waiter(
            api_class_name="AppsV1Api",
            operation="read_namespaced_deployment",
            arguments=arguments,
            result_arguments=result_arguments,
            acceptor_function=delete_acceptor,
        )
        try:
            await hub.tool.k8s.custom_waiter.wait(
                ctx,
                waiter=deployment_waiter,
                waiter_config=waiter_config,
                err_graceful=True,
            )
        except Exception as e:
            result["comment"] = result["comment"] + (str(e),)
            result["result"] = False
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.apps.v1.deployment", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    List objects of kind Deployment in all namespaces

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe k8s.apps.v1.deployment

    """
    ret = await hub.exec.k8s.client.AppsV1Api.list_deployment_for_all_namespaces(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe deployment {ret['comment']}")
        return {}

    result = {}
    for deployment in ret["ret"].items:
        deployment_resource = (
            hub.tool.k8s.apps.v1.deployment_utils.convert_raw_deployment_to_present(
                deployment=deployment
            )
        )
        result[deployment.metadata.name] = {
            "k8s.apps.v1.deployment.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in deployment_resource.items()
            ]
        }
    return result
