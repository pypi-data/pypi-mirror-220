import requests
import json

from requests.exceptions import HTTPError
from ..models.datasetRefreshScheduleModel import datasetRefreshSchedule


class DatasetService:
    groups_snippet = "groups"
    datasets_snippet = "datasets"
    refreshes_snippet = "refreshes"
    refresh_schedule_snippet = "refreshSchedule"

    def __init__(self, client):
        self.client = client
        self.base_url = f"{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}"

    def refresh_dataset_in_group(self, dataset_id, group_id):
        url = (
            self.base_url
            + f"/{self.groups_snippet}/{group_id}/{self.datasets_snippet}/{dataset_id}/{self.refreshes_snippet}"
        )
        headers = self.client.auth_header
        response = requests.post(url, headers=headers)

        if response.status_code != 202:
            raise HTTPError(
                response,
                f"Failed when trying to refresh dataset {dataset_id}:\n{response.json()}",
            )

    def get_refresh_schedule(self, dataset_id):
        url = (
            self.base_url
            + f"/{self.datasets_snippet}/{dataset_id}/{self.refresh_schedule_snippet}"
        )
        headers = self.client.auth_header
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPError(
                response,
                f"Get Refresh Schedule request for dataset {dataset_id} returned http error: {response.json()}",
            )

        return self.refresh_schedules_from_get_refresh_schedule_response(
            response, dataset_id
        )

    @classmethod
    def refresh_schedules_from_get_refresh_schedule_response(cls, response, dataset_id):
        """
        Creates a list of refresh schedules from a http response object
        :param response:
            The http response object
        :return: list
            The list of refresh schedules
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        refreshables = []

        # go through entries returned from API
        refreshables.append(datasetRefreshSchedule.from_dict(response_dict, dataset_id))

        return refreshables
