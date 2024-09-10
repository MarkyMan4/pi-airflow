from typing import Any, Dict

import dlt
from dlt.sources.helpers.rest_client.auth import OAuth2ClientCredentials
from rest_api import RESTAPIConfig, rest_api_resources


class OAuth2ClientCredentialsStrava(OAuth2ClientCredentials):
    def build_access_token_request(self) -> Dict[str, Any]:
        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "json": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                **self.access_token_request_data,
            },
        }


@dlt.source
def strava_source() -> Any:
    auth = OAuth2ClientCredentials(
        access_token_url=dlt.secrets["sources.strava.access_token_url"],
        client_id=dlt.secrets["sources.strava.client_id"],
        client_secret=dlt.secrets["sources.strava.client_secret"],
        access_token_request_data={
            "grant_type": "refresh_token",
            "refresh_token": dlt.secrets["sources.strava.refresh_token"],
        },
    )
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://www.strava.com/api/v3",
            "auth": auth,
        },
        # The default configuration for all resources and their endpoints
        "resource_defaults": {
            # "primary_key": "id",
            "write_disposition": "merge",
            "endpoint": {
                "params": {
                    "per_page": 100,
                },
            },
        },
        "resources": [
            {
                "name": "athlete",
                "endpoint": {
                    "path": "/athlete",
                },
            },
            {
                "name": "activities",
                "endpoint": {
                    "path": "/athlete/activities",
                    # Query parameters for the endpoint
                    # api docs https://developers.strava.com/docs/reference/#api-Activities-getLoggedInAthleteActivities
                    "params": {
                        "after": 1725160601
                        # Define `since` as a special parameter
                        # to incrementally load data from the API.
                        # This works by getting the updated_at value
                        # from the previous response data and using this value
                        # for the `since` query parameter in the next request.
                        # "since": {
                        #     "type": "incremental",
                        #     "cursor_path": "updated_at",
                        #     "initial_value": "2024-01-25T11:21:28Z",
                        # },
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_strava() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="strava_api",
        destination="duckdb",
        dataset_name="strava",
    )

    load_info = pipeline.run(strava_source())
    print(load_info)


if __name__ == "__main__":
    load_strava()
