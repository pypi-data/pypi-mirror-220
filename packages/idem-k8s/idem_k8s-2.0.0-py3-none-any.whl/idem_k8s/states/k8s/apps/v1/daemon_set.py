"""State module for managing Kubernetes DaemonSet."""
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
    """Create a DaemonSet.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict): Standard object's metadata.
            More info: `Kubernetes metadata reference <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.>`_
        spec(dict): The desired behavior of this daemon set. More info:
            More info: `Kubernetes spec reference <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-
            status.>`_
        timeout(dict, Optional): Timeout configuration for resource creation.

           * create(dict) -- Timeout configuration for resource creation
              * delay(int, Optional) -- The amount of time in seconds to wait between attempts. Defaults to 15
              * max_attempts(int, Optional) -- Customized timeout configuration containing delay and max attempts. Defaults to 40.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              k8s.apps.v1.daemon_set.present:
                - name: daemon_set_1
                - metadata: value
                - spec: value


            resource_is_present:
              k8s.apps.v1.daemon_set.present:
              - metadata:
                  name: nginx-ds
                  namespace: default
              - spec:
                  selector:
                    match_labels:
                      name: nginx
                  update_strategy:
                    rolling_update:
                      max_unavailable: 1
                    type: RollingUpdate
                  template:
                    metadata:
                      labels:
                        name: nginx
                    spec:
                      containers:
                      - image: nginx:1.14.2
                        image_pull_policy: IfNotPresent
                        name: nginx
                        resources:
                          limits:
                            memory: 200Mi
                          requests:
                            cpu: 100m
                            memory: 200Mi
                        termination_message_path: /dev/termination-log
                        termination_message_policy: File
                      restart_policy: Always

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Get namespace
    namespace = metadata.get("namespace") if "namespace" in metadata else "default"
    metadata["namespace"] = namespace

    # Check for existing daemon_set by name in namespace
    before = None
    if resource_id:
        daemon_set = await hub.exec.k8s.client.AppsV1Api.read_namespaced_daemon_set(
            ctx, name=resource_id, namespace=namespace
        )
        if not daemon_set["result"]:
            result["comment"] = daemon_set["comment"]
            result["result"] = daemon_set["result"]
            return result
        before = daemon_set["ret"]

    # Update current state
    current_state = (
        hub.tool.k8s.apps.v1.daemon_set_utils.convert_raw_daemon_set_to_present(
            daemon_set=before
        )
    )
    result["old_state"] = current_state

    # Handle no change behaviour
    desired_state = {"resource_id": resource_id, "metadata": metadata, "spec": spec}

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )

    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.apps.v1.daemon_set", name=name
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
                resource_type="k8s.apps.v1.daemon_set", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.apps.v1.daemon_set", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1DaemonSet"
    )
    if before:
        ret = await hub.exec.k8s.client.AppsV1Api.replace_namespaced_daemon_set(
            ctx, name=resource_id, namespace=namespace, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.apps.v1.daemon_set", name=name
        )
    else:
        ret = await hub.exec.k8s.client.AppsV1Api.create_namespaced_daemon_set(
            ctx, namespace=namespace, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.apps.v1.daemon_set", name=name
        )

    # Custom waiter for create/update
    waiter_config = hub.tool.k8s.waiter_utils.create_waiter_config(
        timeout_config=timeout.get("create") if timeout else None,
    )

    def create_acceptor(status: bool, data: Dict = None, comment: Tuple = None) -> bool:
        availability = data.get("availability") if data.get("availability") else None
        return True if availability else False

    arguments = {"name": resource_id, "namespace": namespace}
    result_arguments = {"availability": "status.number_available"}

    daemon_set_waiter = hub.tool.k8s.waiter_utils.create_waiter(
        api_class_name="AppsV1Api",
        operation="read_namespaced_daemon_set",
        arguments=arguments,
        result_arguments=result_arguments,
        acceptor_function=create_acceptor,
    )
    try:
        await hub.tool.k8s.custom_waiter.wait(
            ctx,
            waiter=daemon_set_waiter,
            waiter_config=waiter_config,
            err_graceful=False,
        )
    except Exception as e:
        message = f"DaemonSet resource {name} is unavailable."
        result["comment"] = result["comment"] + (str(e),) + (message,)

    # Fetch the updated resource and update new_state
    daemon_set = await hub.exec.k8s.client.AppsV1Api.read_namespaced_daemon_set(
        ctx, name=resource_id, namespace=namespace
    )
    if not daemon_set["result"]:
        result["comment"] = result["comment"] + daemon_set["comment"]
        result["result"] = daemon_set["result"]
        return result

    after = daemon_set["ret"]
    result[
        "new_state"
    ] = hub.tool.k8s.apps.v1.daemon_set_utils.convert_raw_daemon_set_to_present(
        daemon_set=after
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
    """Delete a DaemonSet.

    Args:
        name(str, Optional): An Idem name of the resource.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        metadata(dict, Optional): Standard object's metadata.
            Defaults to metadata with 'default' namespace, in case of value not provided in absent state.
            More info: `Kubernetes metadata reference <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.>`_
        timeout(dict, Optional): Timeout configuration for resource deletion.

            * delete(dict) -- Timeout configuration for resource deletion
                * delay(int, Optional) -- The amount of time in seconds to wait between attempts. Defaults to 15
                * max_attempts(int, Optional) -- Customized timeout configuration containing delay and max attempts. Defaults to 40.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              k8s.apps.v1.daemon_set.absent:
                - name: value
                - metadata: value
                - resource_id: value

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    namespace = metadata.get("namespace") if "namespace" in metadata else "default"

    before = None
    if resource_id:
        daemon_set = await hub.exec.k8s.client.AppsV1Api.read_namespaced_daemon_set(
            ctx, name=resource_id, namespace=namespace
        )
        if daemon_set and daemon_set["result"]:
            before = daemon_set["ret"]
            result[
                "old_state"
            ] = hub.tool.k8s.apps.v1.daemon_set_utils.convert_raw_daemon_set_to_present(
                daemon_set=before
            )

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.apps.v1.daemon_set", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.apps.v1.daemon_set", name=name
        )
    else:
        ret = await hub.exec.k8s.client.AppsV1Api.delete_namespaced_daemon_set(
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
                    f"Error while waiting for delete daemon_set : {comment[0]}"
                )
            return False

        arguments = {"name": resource_id, "namespace": namespace}
        result_arguments = {"availability": "status.number_available"}

        daemon_set_waiter = hub.tool.k8s.waiter_utils.create_waiter(
            api_class_name="AppsV1Api",
            operation="read_namespaced_daemon_set",
            arguments=arguments,
            result_arguments=result_arguments,
            acceptor_function=delete_acceptor,
        )
        try:
            await hub.tool.k8s.custom_waiter.wait(
                ctx,
                waiter=daemon_set_waiter,
                waiter_config=waiter_config,
                err_graceful=True,
            )
        except Exception as e:
            result["comment"] = result["comment"] + (str(e),)
            result["result"] = False
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.apps.v1.daemon_set", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    list or watch objects of kind DaemonSet.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe k8s.apps.v1.daemon_set

    """
    ret = await hub.exec.k8s.client.AppsV1Api.list_daemon_set_for_all_namespaces(
        ctx,
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe daemon_set {ret['comment']}")
        return {}

    result = {}
    for daemon_set in ret["ret"].items:
        daemon_set_resource = (
            hub.tool.k8s.apps.v1.daemon_set_utils.convert_raw_daemon_set_to_present(
                daemon_set=daemon_set
            )
        )
        result[daemon_set.metadata.name] = {
            "k8s.apps.v1.daemon_set.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in daemon_set_resource.items()
            ]
        }
    return result
