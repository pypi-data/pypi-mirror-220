""" Python client for Eagle Eye Networks APIv3 """
__version__ = "0.0.4"


import json
import logging
import requests
from .settings import *

from datetime import datetime, timedelta
from pytz import timezone

from io import BytesIO

logging.basicConfig(level=logging.INFO)



class EagleEyev3():
    """
    Class representing the EagleEyev3 client.
    """

    __version__ = "0.0.4"
    __all__ = ['EagleEyev3', 'Device', 'Camera']

    def __init__(self, config=None):
        """
        Initializes the EagleEyev3 client object.
        """
        self.client_id = None
        self.client_secret = None
        self.access_token = None
        self.refresh_token = None
        self.redirect_uri = None

        keys_to_check = ['client_id', 'client_secret', 'server_protocol', 'server_host', 'server_port', 'server_path']
        if config and all([name in config for name in keys_to_check]):
            self._load_vars_from_settings(config)
        else:
            if config is None:
                logging.warn("config is None or was not passed into constructor")
            else:
                logging.error("config is missing keys")

        self.user_base_url = None
        self.current_user = None
        self.users = []
        self.bridges = []
        self.cameras = []
        self.switches = []
        self.users = []
        self.accounts = []
        self.user_tz_obj = None

        self.lazy_login = False

        if self.lazy_login:
            try:
                self._load_access_token()
            except FileNotFoundError as e:
                logging.warn("self.lazy_login is set to {self.lazy_login} but could not find .lazy_login file to load")

    def _load_vars_from_settings(self, config={}):
        """
        Load variables from the settings module.
        """
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.server_protocol = config['server_protocol']
        self.server_host = config['server_host']
        self.server_port = config['server_port']
        self.server_path = config['server_path']

        # Combine server_protocol, server_host, and server_port to make the redirect_uri
        # Note: Please see the note in settings.py about trailing slashes and modify this line if needed
        
        self.redirect_uri = f"{self.server_protocol}://{self.server_host}:{self.server_port}/{self.server_path}"


    def _save_access_token(self):
        with open(".lazy_login", "w") as json_file:
            json.dump({
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'current_user': self.current_user
            }, json_file)

    def _load_access_token(self):
        with open(".lazy_login", "r") as json_file:
            saved = json.load(json_file)
            if 'access_token' in saved:
                self.access_token = saved['access_token']
            if 'refresh_token' in saved:
                self.refresh_token = saved['refresh_token']

        self.get_base_url(cascade=True)


    def time_now(self):
        return datetime.now(tz=self.user_tz_obj).isoformat(timespec='milliseconds')


    def time_before(self, ts=None, hours=6):
        if ts == None:
            ts = datetime.now(tz=self.user_tz_obj)

        if type(ts) == str:
            ts = datetime.fromisoformat(ts)

        return (ts - timedelta(hours=hours)).isoformat(timespec='milliseconds')



    def login_tokens(self, code=None, cascade=True):
        """
        Obtains login tokens using the authorization code.

        Args:
            code (str): The authorization code.
            cascade (bool): Indicates whether to cascade and get the base URL and current user information.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, data, and current user information.
        """
        baseUrl = "https://auth.eagleeyenetworks.com/oauth2/token"
        pathUrl = f"?grant_type=authorization_code&scope=vms.all&code={code}&redirect_uri={self.redirect_uri}" # Note the trailing slash, make sure it matches the whitelist
        url = baseUrl + pathUrl

        # Send a POST request to obtain login tokens
        response = requests.post(url, auth=(self.client_id, self.client_secret))
        response_json = response.json()

        logging.info(f"{response.status_code} in login_tokens")

        if response.status_code == 200:
            success = True
            self.access_token = response_json['access_token']
            self.refresh_token = response_json['refresh_token']

            if self.lazy_login:
                self._save_access_token()

            if cascade:
                self.get_base_url()
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json,
            'current_user': self.current_user
        }

    def logout(self):
        """
        Revokes token.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = "https://auth.eagleeyenetworks.com/oauth2/revoke"

        payload = {
            "token": self.access_token,
            "token_type_hint": "access_token"
        }

        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json",
                    "Content-type": "application/json"
                }

        # Send a POST request to obtain the base URL
        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in logout")

        if response.status_code == 200:
            success = True
        else:
            success = False
            logging.info(f"call to logout: {response_json}")

        self.access_token = None
        self.refresh_token = None

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_base_url(self, cascade=True):
        """
        Obtains the base URL for the user.

        Args:
            cascade (bool): Indicates whether to cascade and get the current user information.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = "https://api.eagleeyenetworks.com/api/v3.0/clientSettings"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        # Send a GET request to obtain the base URL
        response = requests.get(url, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in get_base_url")

        if response.status_code == 200:
            success = True
            if 'httpsBaseUrl' in response_json and 'hostname' in response_json['httpsBaseUrl']:
                self.user_base_url = response_json['httpsBaseUrl']['hostname']
                if cascade:
                    self.get_current_user()
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_current_user(self):
        """
        Obtains the information of the current user.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/users/self?include=timeZone"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        # Send a GET request to obtain the current user information
        response = requests.get(url, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in get_current_user")

        if response.status_code == 200:
            success = True
            self.current_user = response_json
            self.user_tz_obj = timezone(response_json['timeZone']['timeZone'])
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_users(self):
        """
        Obtains the list of users.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/users?include=timeZone"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        response = requests.get(url, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in get_list_of_users")

        if response.status_code == 200:
            success = True
            self.users = [i for i in response_json['results']]
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_cameras(self):
        """
        Obtains the list of cameras.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/cameras?include=status"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        response = requests.get(url, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in get_list_of_cameras")

        if response.status_code == 200:
            success = True
            self.cameras = [
                    Camera(id=i['id'],\
                           name=i['name'],\
                           status=i['status'],\
                           account_id=i['accountId'],\
                           bridge_id=i['bridgeId'],\
                           user_base_url=self.user_base_url,\
                           een_instance=self)
                           for i in response_json['results']]
            for camera in self.cameras:
                camera.user_base_url = self.user_base_url
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_bridges(self):
        """
        Obtains the list of bridges.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/bridges"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        response = requests.get(url, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in get_list_of_bridges")

        if response.status_code == 200:
            success = True
            self.bridges = [i for i in response_json['results']]
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_switches(self):
        """
        Obtains the list of switches.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/switches"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        response = requests.get(url, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in get_list_of_switches")

        if response.status_code == 200:
            success = True
            self.switches = [i for i in response_json['results']]
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_available_devices(self, deviceType__in="camera"):
        """
        Obtains the list of available devices.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/availableDevices?deviceType__in={deviceType__in}"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        response = requests.get(url, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in get_list_of_available_devices")

        if response.status_code == 200:
            success = True
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_multi_cameras(self):
        """
        Obtains the list of multi-cameras.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/multiCameras"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        response = requests.get(url, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in get_list_of_multi_cameras")

        if response.status_code == 200:
            success = True
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_feeds(self):
        """
        Obtains the list of feeds.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/feeds"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        response = requests.get(url, headers=headers)
        response_json = response.json()

        logging.info(f"{response.status_code} in get_list_of_feeds")

        if response.status_code == 200:
            success = True
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }


    def get_camera_by_id(self, esn):
        found_camera = None
        for camera in self.cameras:
            if camera.id == esn:
                found_camera = camera
                break

        if found_camera == None:
            camera = Camera()

        logging.debug(f"returning camera {camera} for search query {esn}")
        return camera




class Device():

    def __init__(self, id=None, name=None, status=None, account_id=None, user_base_url=None, een_instance=None):

        self.id = id
        self.name = name
        self.status = status
        self.account_id = account_id
        self.user_base_url = user_base_url,
        self.een_instance = een_instance

    def get_id(self):
        return self.id

    def get_status(self):
        if 'connectionStatus' in self.status:
            return self.status['connectionStatus']
        return None

    def is_online(self):
        if 'connectionStatus' in self.status:
            return self.status['connectionStatus'] == "online"
        return None

    def is_offline(self):
        if 'connectionStatus' in self.status:
            return self.status['connectionStatus'] == "deviceOffline" \
                or self.status['connectionStatus'] == "bridgeOffline" \
                or self.status['connectionStatus'] == "error"
        return None

    def __repr__(self):
        if self.is_online():
            online = '✅'
        elif self.is_offline():
            online = '❌'
        else:
            online = '？'
        return f"{online} [{self.id}] - {self.name}"



class Camera(Device):

    def __init__(self, id=None, name=None, status=None, account_id=None, bridge_id=None, user_base_url=None, een_instance=None):
        super().__init__(id=id, name=name, status=status, account_id=account_id, user_base_url=user_base_url, een_instance=een_instance)
        self.bridge_id = bridge_id
        self.previews = []
        self.videos = []
        self.events = {
                'status': [],
                'motion': []
                } 
    
    
    def get_list_of_events(self, start_timestamp=None, end_timestamp=None):
        """
        Obtains the list of events.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """

        if start_timestamp == None or end_timestamp == None:
            logging.debug(f"get_list_of_events called without timestamp")
            return {
                "success": False,
                "response_http_status": None,
                "data": { 'msg': 'get_list_of_events called without required args, needs start_timestamp, end_timestamp' }
            }

        url = f"https://{self.user_base_url}/api/v3.0/events?pageSize=100&include=een.deviceCloudStatusUpdate.v1&startTimestamp__gte={start_timestamp}&endTimestamp__lte={end_timestamp}&actor=camera%3A{self.id}&type__in=een.deviceCloudStatusUpdateEvent.v1"

        headers = { 
                    "Authorization": f"Bearer {self.een_instance.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=(3, 5))
            response_json = response.json()

            logging.debug(f"{response.status_code} returned from {url} with {headers} and {response.text}")
            logging.info(f"{response.status_code} in get_list_of_events")

            if response.status_code == 200:
                success = True
                # filter events by type
                [self.events['status'].append(i) for i in response.json()['results'] if i['type'] == 'een.deviceCloudStatusUpdateEvent.v1']
                [self.events['motion'].append(i) for i in response.json()['results'] if i['type'] == 'een.motionDetectionEvent.v1']

                # remove duplicates
                seen = set()
                self.events['status'] = [event for event in self.events['status'] if event['endTimestamp'] and event['id'] not in seen and not seen.add(event['id'])]
                seen = set()
                self.events['motion'] = [event for event in self.events['motion'] if event['id'] not in seen and not seen.add(event['id'])]

                # sort by event startTimestamp descending
                self.events['status'] = sorted(self.events['status'], key=lambda x: x['startTimestamp'], reverse=True)
                self.events['motion'] = sorted(self.events['motion'], key=lambda x: x['startTimestamp'], reverse=True)
            else:
                success = False

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for {self.id} get_list_of_events()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }
            

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }


    def get_live_preview(self):

        url = f"https://{self.user_base_url}/api/v3.0/media/liveImage.jpeg?deviceId={self.id}&type=preview"

        headers = { 
                    "Authorization": f"Bearer {self.een_instance.access_token}", 
                    "Accept": "image/jpeg"
                }

        try:
            response = requests.get(url, headers=headers, timeout=(3, 5))
            logging.info(f"{response.status_code} in get_live_preview")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for {self.id} get_live_preview()")
            response = None
        except requests.exceptions.RequestException as e:
            logging.warn(e)
            response = None
        
        return response








