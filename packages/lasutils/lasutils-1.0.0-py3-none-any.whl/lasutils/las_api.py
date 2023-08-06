import logging
from datetime import datetime
from lasutils import settings
from lasutils.api_poller import create_poller

CONF_LAS_API_URL = "api.url"
CONF_LAS_SITE_ID = "site.id"
API_SITE_ID = "site-id"

log = logging.getLogger(__name__)


class LasApi:
    # --- Internals ---
    def __init__(
        self,
        site_id: str = None,
        api_url: str = None,
        poll_retry_time: int = 60,
        las_config: dict = None,
        las_user: str = None,
        las_pwd: str = None,
    ):
        if las_config:
            self._api_url = las_config[CONF_LAS_API_URL]
            self._site_id = las_config[CONF_LAS_SITE_ID]
        else:
            self._site_id = site_id
            self._api_url = api_url

        if las_user and las_pwd:
            user = las_user
            pwd = las_pwd
        else:
            user = settings.LAS_USER
            pwd = settings.LAS_PWD
        self._poll_retry_time = poll_retry_time
        self._poller = self._create_poller(self._api_url, user, pwd)

    def _create_poller(self, api_url: str, las_usr: str, las_pwd: str):
        bo_auth_config = {
            "auth.token.url": f"{api_url}/user/login",
            "auth.content.type": "json",
            "auth.token.name": "jwt_token",
            "auth.payload": {
                "userName": f"{las_usr}",
                "password": f"{las_pwd}",
            },
        }
        bo_api_config = {
            "api.type": "rest",
            "api.format": "json",
            "api.url": f"{api_url}",
            "api.dataPath": "",
        }
        return create_poller(auth_config=bo_auth_config, api_config=bo_api_config)

    def _get_api_time_format(self, dt: datetime):
        return dt.isoformat(timespec="milliseconds") + "Z"

    # Generic POST
    def post(self, resource: str = None, payload: dict = None):
        return self._poller.post(
            resource, payload=payload, fail_retry_time=self._poll_retry_time
        )

    # Generic GET. Handles both paged and unpaged data
    def poll(self, resource: str = None, params: dict = None, page_size: int = 0):
        params = {} if not params else params
        if page_size == 0:
            # Get unpaged data
            return self._poller.poll(
                resource,
                params=params,
                fail_retry_time=self._poll_retry_time,
            )
        else:
            # Get paged data
            page_index = 0
            params = {"page-index": page_index, "page-size": page_size, **params}

            batch = self._poller.poll(
                resource,
                params=params,
                fail_retry_time=self._poll_retry_time,
            )
            result = batch
            while len(batch) >= page_size:
                page_index += 1
                params["page-index"] = page_index
                batch = self._poller.poll(
                    resource,
                    params=params,
                    fail_retry_time=self._poll_retry_time,
                )
                result.extend(batch)
                log.info(f"Polled {len(result)} items")
            return result

    # --- API ---
    # Broadcast
    def get_broadcasts(self, start_from: datetime, start_to: datetime):
        params = {
            API_SITE_ID: self._site_id,
            "start-from": self._get_api_time_format(start_from),
            "start-to": self._get_api_time_format(start_to),
        }
        return self.poll("broadcast", params=params)

    def get_broadcast_by_ext_id(self, match_id: str):
        params = {
            API_SITE_ID: self._site_id,
            "external-broadcast-id": match_id,
        }
        return self.poll("broadcast", params=params)

    def get_broadcast_by_id(self, broadcast_id: str):
        params = {
            API_SITE_ID: self._site_id,
            "broadcastId": broadcast_id,
        }
        return self.poll("broadcast/internal", params=params)

    def get_broadcast(self, broadcast_id: str):
        params = {
            API_SITE_ID: self._site_id,
        }
        return self.poll(f"broadcast/{broadcast_id}", params=params)

    # Video
    def get_video(self, id: str):
        params = {
            API_SITE_ID: self._site_id,
        }
        return self.poll(f"broadcast/video/{id}", params=params)

    def get_download_list(
        self, access_token: str, competition_id: str, start_from: datetime
    ):
        if not start_from:
            log.error(f'Get download-list. Missing "start_from" param')
            return None
        params = {
            "competition-id": competition_id,
            "access-token": access_token,
            "start-to": self._get_api_time_format(start_from),
            "sort-column": "start",
            "sort-order": "Descending",
        }
        try:
            self._poller.set_header_field("site-id", self._site_id)
            result = self.poll(f"broadcast/download-list", params=params, page_size=25)
        except Exception as err:
            self._poller.äset_header_field("site-id", "BACKOFFICE")
            log.error(f"Failed to get download list. Error: {err}")

    def get_download_access_token(self, competition_id: str):
        params = {
            "target-id": competition_id,
            "target": "COMP",
        }
        return self.poll(f"user/access-token", params=params)

    def create_download_access_token(self, competition_id: str):
        data = {
            "targetId": competition_id,
            "target": "COMP",
            "note": f"Python SDK ({settings.LAS_USER})",
            "anonymous": "true",
            "siteId": self._site_id,
        }
        return self.post(f"user/access-token", payload=data)

    # Venue
    def get_venue(self, venue_id: str):
        params = {
            API_SITE_ID: self._site_id,
        }
        return self.poll(f"venue/{venue_id}", params=params)

    def get_venues(self, site_id: str = None):
        site_id = site_id if site_id else self._site_id
        params = {
            API_SITE_ID: site_id,
        }
        return self.poll(f"venue", params=params)

    # Sites
    def get_sites_custom(self):
        params = {
            "site-type": "CUSTOM",
        }
        return self.poll(f"site/config/settings", params=params)

    def get_sites_common(self):
        params = {
            "site-type": "COMMON",
        }
        return self.poll(f"site/config/settings", params=params)

    # Cameras
    def get_cameras(self):
        return self.poll(f"venue/camera", page_size=200)

    # Groups
    def get_groups(self):
        params = {
            API_SITE_ID: self._site_id,
        }
        return self.poll("group", params=params)

    # Payment
    def get_payment_config(self):
        params = {
            API_SITE_ID: self._site_id,
        }
        return self.poll(f"payment/v2/config", params=params)

    def get_payment_transactions(self, start: datetime, stop: datetime):
        params = {
            API_SITE_ID: self._site_id,
            "from": self._get_api_time_format(start),
            "to": self._get_api_time_format(stop),
        }
        return self.poll(f"payment/v2/transactions", params=params)

    # Users
    def get_users(self):
        return self.poll(f"user/get-users-by-site-id/{self._site_id}", page_size=200)

    def get_user(self, user_id):
        return self.poll(f"user/{user_id}")

    # Player Account
    def get_player_account(self, user_id):
        params = {API_SITE_ID: self._site_id, "user-id": user_id}

        return self.poll(
            f"player-account",
            params=params,
        )
