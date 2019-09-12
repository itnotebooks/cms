#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-12 下午9:59
# @Version        : 1.0
# @File           : k8s
# @Software       : PyCharm

from kubernetes.client import Configuration, ApiClient, CoreV1Api, AppsV1Api, BatchV1Api, RbacAuthorizationV1Api
from kubernetes.stream import stream
from kubernetes.client.rest import RESTClientObject


class K8SAPI:
    '''

    '''

    def __init__(self, cluster):
        self.cluster = cluster

    def get_api_client(self):
        configuration = Configuration()
        configuration.verify_ssl = False
        configuration.host = self.cluster.api
        configuration.api_key['authorization'] = self.cluster.token
        configuration.api_key_prefix['authorization'] = 'Bearer'
        api_client = ApiClient(configuration)
        return api_client

    def get_core_v1_api(self):
        """
        获取CoreV1Api
        :return:
        """
        client = self.get_api_client()
        core_v1_api = CoreV1Api(client)
        return core_v1_api

    def get_app_v1_api(self):
        """
        AppsV1Api
        :return:
        """
        client = self.get_api_client()
        app_v1_api = AppsV1Api(client)
        return app_v1_api

    def get_batch_v1_api(self):
        """
        BatchV1Api
        :return:
        """
        client = self.get_api_client()
        batch_v1_api = BatchV1Api(client)
        return batch_v1_api

    def get_rbacauthorization_v1_api(self):
        """
        RbacAuthorizationV1Api
        :return:
        """
        client = self.get_api_client()
        rbacauthorization_v1_api = RbacAuthorizationV1Api(client)
        return rbacauthorization_v1_api

    def test_pod_connect(self, pod, namespace, command=None, container=None):
        """
        测试链接pod
        :param pod:
        :param namespace:
        :param command:
        :param container:
        :return:
        """
        if not command:
            command = [
                "/bin/sh",
                "-c",
                'TERM=xterm-256color; export TERM; [ -x /bin/bash ] '
                '&& ([ -x /usr/bin/script ] '
                '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
                '|| exec /bin/sh']

        core_v1_api = self.get_core_v1_api()
        if stream(core_v1_api.connect_get_namespaced_pod_exec, pod, namespace, command=command,
                  container=container,
                  stderr=True, stdin=False,
                  stdout=True, tty=False):
            return True
        else:
            return False

    def get_pods_exec(self, pod, namespace, command=None, container=None):
        core_v1_api = self.get_core_v1_api()
        if not command:
            command = [
                "/bin/sh",
                "-c",
                'TERM=xterm-256color; export TERM; [ -x /bin/bash ] '
                '&& ([ -x /usr/bin/script ] '
                '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
                '|| exec /bin/sh']

        if container:
            container_stream = stream(core_v1_api.connect_get_namespaced_pod_exec, pod, namespace, command=command,
                                      container=container,
                                      stderr=True,
                                      stdin=True,
                                      stdout=True,
                                      tty=True,
                                      _preload_content=False)
        else:
            container_stream = stream(core_v1_api.connect_get_namespaced_pod_exec, pod, namespace, command=command,
                                      stderr=True,
                                      stdin=True,
                                      stdout=True,
                                      tty=True,
                                      _preload_content=False)
        return container_stream


class K8SRestAPI:
    '''

    '''

    def __init__(self, cluster):
        self.cluster = cluster

    def get_rest_client(self):
        configuration = Configuration()
        configuration.verify_ssl = False
        configuration.host = self.cluster.api
        configuration.api_key['authorization'] = self.cluster.token
        configuration.api_key_prefix['authorization'] = 'Bearer'
        rest_client = RESTClientObject(configuration)

        return rest_client
