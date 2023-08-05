import json.decoder

import requests
from packaging.version import Version

from akinoncli.core.exc import AkinonCLIError
from akinoncli.core.version import get_version


class AkinonResponse:
    def __init__(self, is_succeed, status_code, data=None):
        data = data or {}
        self.is_succeed = is_succeed
        self.status_code = status_code
        self.data = data


class AkinonCloudClient:
    URLS = {
        "base": "",
        "apps": "applications/",
        "app_detail": "applications/{app_id}/",
        "app_build": "applications/{app_id}/build/",
        "app_versions": "applications/{app_id}/versions/",
        "app_version_logs": "applications/{app_id}/versions/{v_id}/logs",
        "app_version_detail": "applications/{app_id}/versions/{v_id}/",
        "application_types": "applications/application_types/",
        "application_types_admin": "admin/application_types/",
        "application_types_admin_detail": "admin/application_types/{application_type_id}/",
        "login": "users/login/",
        "projects": "projects/",
        "project_detail": "projects/{p_id}/",
        "project_apps": "projects/{p_id}/project_apps/",
        "project_app_detail": "projects/{p_id}/project_apps/{pa_id}/",
        "project_app_custom_env": "projects/{p_id}/project_apps/{pa_id}/custom_env/",
        "project_app_deploy": "projects/{p_id}/project_apps/{pa_id}/deploy/",
        "project_app_deploy_multiple": "applications/{app_id}/deploy_multiple_project_apps/",
        "project_app_deployments": "projects/{p_id}/project_apps/{pa_id}/deployments/",
        "project_app_deployment_log": "projects/{p_id}/project_apps/{pa_id}/deployments/{deployment_id}/logs",
        "project_apps_logs": "projects/{project_id}/project_apps/{project_app_id}/logs/",
        "project_apps_export_logs": "projects/{project_id}/project_apps/{project_app_id}/logs/export",
        "relatable_project_apps": "projects/{project_id}/applications/{app_id}/relatable-project-apps/",
        "public_keys": "users/public_keys/",
        "public_key_detail": "users/public_keys/{pk_id}/",
        "register": "users/register/",
        "domains": "accounts/domains/",
        "certificates": "accounts/domains/{domain_id}/certificates/",
        "attach_certificate": "projects/{p_id}/project_apps/attach_certificate/",
    }

    def __init__(self, base_url, token):
        self.token = token
        self.URLS['base'] = base_url

    def _send_request(self, method, url, params=None, data=None, headers=None, qs=None, response_format='json'):
        params = params or {}
        data = data or {}
        headers = headers or {}
        qs = qs or {}
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = f"akinoncli {Version(get_version())}"

        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        url = f"{self.URLS['base']}{self.URLS[url]}".format(**params)
        response = requests.request(method=method, url=url, json=data, headers=headers, params=qs)
        if response.status_code >= 500:
            raise AkinonCLIError("An error has occurred on our side. We'll fix that.", response=response)
        elif response.status_code == 401:
            raise AkinonCLIError("Unauthenticated request, please log in with your credentials.", response=response)
        elif response.status_code == 403:
            raise AkinonCLIError(
                "You do not have access to do this action. Please contact your account owner.", response=response
            )
        elif not response.ok:
            raise AkinonCLIError(
                f'API returned an unsuccessful status code. HTTP {response.status_code}: {response.reason}',
                response=response,
            )

        data = response.content
        if response_format == 'json':
            try:
                data = response.json()
            except json.decoder.JSONDecodeError:
                data = {}

        return AkinonResponse(is_succeed=response.ok, status_code=response.status_code, data=data)

    def login(self, data):
        return self._send_request("POST", "login", data=data)

    def get_projects(self, qs: dict):
        return self._send_request("GET", "projects", qs=qs)

    def create_project(self, data):
        return self._send_request("POST", "projects", data=data)

    def update_project(self, p_id, data):
        response = self._send_request("PATCH", "project_detail", params={"p_id": p_id}, data=data)
        if response.status_code == 404:
            raise AkinonCLIError("Project could not found.")
        return response

    def get_applications(self, qs: dict):
        """
        return account's applications
        """
        return self._send_request("GET", "apps", params=qs)

    def get_application(self, app_id: int):
        """
        Gets details of an application
        """
        return self._send_request("GET", "app_detail", params={"app_id": app_id})

    def create_application(self, data):
        return self._send_request("POST", "apps", data=data)

    def update_application(self, app_id, data):
        response = self._send_request("PATCH", "app_detail", params={"app_id": app_id}, data=data)
        if response.status_code == 404:
            raise AkinonCLIError("Application could not found.")
        return response

    def build_application(self, app_id, data):
        response = self._send_request("POST", "app_build", params={"app_id": app_id}, data=data)
        if response.status_code == 404:
            raise AkinonCLIError("Application could not found.")
        return response

    def get_app_versions(self, app_id):
        return self._send_request("GET", "app_versions", params={"app_id": app_id})

    def get_app_version_logs(self, app_id, version_id):
        return self._send_request("GET", "app_version_logs", params={"app_id": app_id, "v_id": version_id})

    def get_application_types(self, qs: dict):
        return self._send_request("GET", "application_types", qs=qs)

    def get_project_apps(self, p_id, qs: dict):
        return self._send_request("GET", "project_apps", params={"p_id": p_id}, qs=qs)

    def get_project_app(self, p_id, pa_id):
        return self._send_request("GET", "project_app_detail", params={"p_id": p_id, "pa_id": pa_id})

    def update_project_app(self, p_id, pa_id, data):
        response = self._send_request("PATCH", "project_app_detail", params={"p_id": p_id, "pa_id": pa_id}, data=data)
        if response.status_code == 404:
            raise AkinonCLIError("Project App could not found.")
        return response

    def delete_project_app_custom_env(self, p_id, pa_id, data):
        response = self._send_request(
            "POST", "project_app_custom_env", params={"p_id": p_id, "pa_id": pa_id}, data=data
        )
        if response.status_code == 404:
            raise AkinonCLIError("Project App could not found.")
        return response

    def update_project_app_custom_env(self, p_id, pa_id, data):
        response = self._send_request("PUT", "project_app_custom_env", params={"p_id": p_id, "pa_id": pa_id}, data=data)
        if response.status_code == 404:
            raise AkinonCLIError("Project App could not found.")
        return response

    def get_project_app_logs(self, project_id, project_app_id, data):
        return self._send_request(
            "POST", "project_apps_logs", params={"project_id": project_id, "project_app_id": project_app_id}, data=data
        )

    def get_relatable_project_apps(self, app_id, project_id):
        return self._send_request("GET", "relatable_project_apps", params={"project_id": project_id, "app_id": app_id})

    def export_project_app_logs(
        self, project_id, project_app_id, start_date=None, end_date=None, dates=None, applications=None
    ):
        data = {}

        if start_date:
            data['start_date'] = start_date

        if end_date:
            data['end_date'] = end_date

        if dates:
            data['dates'] = dates.split(',')

        if applications:
            data['applications'] = applications.split(',')

        return self._send_request(
            'POST',
            'project_apps_export_logs',
            params={"project_id": project_id, "project_app_id": project_app_id},
            data=data,
        )

    def create_project_app(self, p_id, data):
        return self._send_request("POST", "project_apps", params={"p_id": p_id}, data=data)

    def attach_certificate(self, project_id: str, data: dict):
        response = self._send_request("POST", "attach_certificate", params={"p_id": project_id}, data=data)
        if response.status_code == 404:
            if response.data is None:
                raise AkinonCLIError("Project App could not found.")
            raise AkinonCLIError(str(response.data))

        return response

    def deploy_project_app(self, p_id: int, pa_id: int, data: dict) -> AkinonResponse:
        response = self._send_request(
            "POST",
            "project_app_deploy",
            params={
                "p_id": p_id,
                "pa_id": pa_id,
            },
            data=data,
        )
        if response.status_code == 404:
            raise AkinonCLIError("Project App could not be found.")
        return response

    def deploy_multiple_project_apps(self, app_id: int, data: dict) -> AkinonResponse:
        response = self._send_request(
            "POST",
            "project_app_deploy_multiple",
            params={
                "app_id": app_id,
            },
            data=data,
        )
        if response.status_code == 404:
            raise AkinonCLIError("App could not be found.")
        return response

    def get_project_app_deployments(self, p_id, pa_id):
        return self._send_request("GET", "project_app_deployments", params={"p_id": p_id, "pa_id": pa_id})

    def get_project_app_deployment_logs(self, p_id, pa_id, deployment_id):
        return self._send_request(
            "GET", "project_app_deployment_log", params={"p_id": p_id, "pa_id": pa_id, "deployment_id": deployment_id}
        )

    def get_public_keys(self, qs: dict):
        return self._send_request("GET", "public_keys", qs=qs)

    def create_public_key(self, data):
        return self._send_request("POST", "public_keys", data=data)

    def remove_public_key(self, pk_id):
        return self._send_request("DELETE", "public_key_detail", params={"pk_id": pk_id})

    def get_domains(self, qs: dict):
        return self._send_request("GET", "domains", qs=qs)

    def create_domain(self, data):
        return self._send_request("POST", "domains", data=data)

    def get_certificates(self, domain_id, qs: dict):
        return self._send_request("GET", "certificates", params={"domain_id": domain_id}, qs=qs)

    def create_certificate(self, domain_id, data):
        return self._send_request("POST", "certificates", data=data, params={'domain_id': domain_id})
