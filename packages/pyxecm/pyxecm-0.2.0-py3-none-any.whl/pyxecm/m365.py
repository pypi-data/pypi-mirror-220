"""
M365 Module to interact with the MS Graph API
See also https://learn.microsoft.com/en-us/graph/ 

Class: M365
Methods:

__init__ : class initializer
config : returns config data set
credentials: returns the token data
requestHeader: request header for MS Graph API calls
parseRequestResponse: process result into Json
existResultItem: check if an dict item is in the response
                 of the Graph REST API call
getResultValue: check if a defined value (based on a key) is in the Graph API response
parseRequestResponse: parse the REST API responses and convert
                      them to Python dict in a safe way

authenticate : authenticates at M365 Graph API

getUsers: Get list all all users in M365 tenant 
getUser: Get a M365 User based on its email
getGroups: Get list all all groups in M365 tenant
getGroup: Get a M365 Group based on its name
addGroup: Add a M365 Group
addUser: Add a M365 User
hasTeam: Check if a M365 Group has a M365 Team connected or not
addTeam: Add a M365 Team (based on an existing group)
deleteTeams: Delete MS teams with a given name
getUserLicenses: Get the assigned license SKUs of a user
assignLicenseToUser: Add an M365 license to a user (e.g. to use Office 365)
getUserPhoto: Retriev the photo of a M365 user
updateUserPhoto: Update a user with a profile photo (which must be in local file system)
getGroupMembers: Get members (users and groups) of the specified group
getGroupOwners: Get owners (users) of the specified group
addGroupMember: Add a user or group to a target group
isMember: Check whether a M365 user is already in a M365 group
addGroupOwner: Add a user as owner to a group
purgeDeletedItems: Purge all deleted users and groups in the organization
purgeDeletedItem: Help function that purges a single user or group
getTeamsApps: Get a list of MS Teams apps in catalog that match a given filter criterium
uploadTeamsApp: Upload a new app package to the catalog of MS Teams apps
removeTeamsApp: Remove MS Teams App for the app catalog
assignTeamsAppToUser: Assign (add) a MS teams app to a M365 user.
upgradeTeamsAppOfUser: Upgrade a MS teams app for a user.
addSensitivityLabel: Assign a existing sensitivity label to a user.
                     THIS IS CURRENTLY NOT WORKING!
assignSensitivityLabelToUser: Create a new sensitivity label in M365
                              THIS IS CURRENTLY NOT WORKING!
"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import json
import logging
import os
import re
import urllib.parse
import zipfile
from urllib.parse import quote

import requests

logger = logging.getLogger("customizer.m365")

requestLoginHeaders = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}


class M365(object):
    """Used to automate stettings in Microsoft 365 via the Graph API."""

    _config: dict
    _access_token = None
    _user_access_token = None

    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        domain: str,
        sku_id: str,
        teams_app_name: str,
    ):
        """Initialize the M365 object

        Args:
            tenant_id (string): M365 Tenant ID
            client_id (string): M365 Client ID
            client_secret (string): M365 Client Secret
            domain (string): M365 domain
            sku_id (string): License SKU for M365 users
            teams_app_name (string): name of the Extended ECM app for MS Teams
        """

        m365Config = {}

        # Set the authentication endpoints and credentials
        m365Config["tenantId"] = tenant_id
        m365Config["clientId"] = client_id
        m365Config["clientSecret"] = client_secret
        m365Config["domain"] = domain
        m365Config["skuId"] = sku_id
        m365Config["teamsAppName"] = teams_app_name
        m365Config[
            "authenticationUrl"
        ] = "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(tenant_id)
        m365Config["graphUrl"] = "https://graph.microsoft.com/v1.0/"
        m365Config["betaUrl"] = "https://graph.microsoft.com/beta/"
        m365Config["directoryObjects"] = m365Config["graphUrl"] + "directoryObjects"

        # Set the data for the token request
        m365Config["tokenData"] = {
            "client_id": client_id,
            "scope": "https://graph.microsoft.com/.default",
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }

        m365Config["groupsUrl"] = m365Config["graphUrl"] + "groups"
        m365Config["usersUrl"] = m365Config["graphUrl"] + "users"
        m365Config["teamsUrl"] = m365Config["graphUrl"] + "teams"
        m365Config["teamsTemplatesUrl"] = m365Config["graphUrl"] + "teamsTemplates"
        m365Config["teamsAppsUrl"] = m365Config["graphUrl"] + "appCatalogs/teamsApps"
        m365Config["directoryUrl"] = m365Config["graphUrl"] + "directory"
        m365Config["securityUrl"] = m365Config["betaUrl"] + "security"

        self._config = m365Config

    def config(self):
        return self._config

    def credentials(self):
        return self.config()["tokenData"]

    def credentialsUser(self, username: str, password: str) -> dict:
        """In some cases MS Graph APIs cannot be called via
            application permissions (client_id, client_secret)
            but requires a token of a user authenticated
            with username + password. This is e.g. the case
            to upload a MS teams app to the catalog.
            See https://learn.microsoft.com/en-us/graph/api/teamsapp-publish

        Args:
            username (string): username
            password (string): password
        Returns:
            dictionary: user credentials for M365
        """

        credentials = {
            "client_id": self.config()["clientId"],
            "scope": "https://graph.microsoft.com/.default",
            "client_secret": self.config()["clientSecret"],
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        return credentials

    # end method definition

    def requestHeader(self, content_type: str = "application/json") -> dict:
        request_header = {
            "Authorization": "Bearer {}".format(self._access_token),
            "Content-Type": content_type,
        }
        return request_header

    # end method definition

    def requestHeaderUser(self, content_type: str = "application/json") -> dict:
        request_header = {
            "Authorization": "Bearer {}".format(self._user_access_token),
            "Content-Type": content_type,
        }
        return request_header

    # end method definition

    def parseRequestResponse(
        self,
        response_object: requests.Response,
        additional_error_message: str = "",
        show_error: bool = True,
    ) -> dict:
        """Converts the request response (JSon) to a Python dict in a safe way
           that also handles exceptions. It first tries to load the response.text
           via json.loads() that produces a dict output. Only if response.text is
           not set or is empty it just converts the response_object to a dict using
           the vars() built-in method.

        Args:
            response_object (object): this is reponse object delivered by the request call
            additional_error_message (string, optional): use a more specific error message
                                                         in case of an error
            show_error (boolean): True: write an error to the log file
                                  False: write a warning to the log file
        Returns:
            dictionary: response information or None in case of an error
        """

        if not response_object:
            return {}

        try:
            if response_object.text:
                dict_object = json.loads(response_object.text)
            else:
                dict_object = vars(response_object)
        except json.JSONDecodeError as e:
            if additional_error_message:
                message = "Cannot decode response as JSon. {}; error -> {}".format(
                    additional_error_message, e
                )
            else:
                message = "Cannot decode response as JSon; error -> {}".format(e)
            if show_error:
                logger.error(message)
            else:
                logger.warning(message)
            return {}
        else:
            return dict_object

    # end method definition

    def existResultItem(
        self, response: dict, key: str, value: str, sub_dict_name: str = ""
    ) -> bool:
        """Check existence of key / value pair in the response properties of an MS Graph API call.

        Args:
            response (dictionary): REST response from an MS Graph REST Call
            key (string): property name (key)
            value (string): value to find in the item with the matching key
            sub_dict_name (string): some MS Graph API calls include nested
                                    dict structures that can be requested
                                    with an "expand" query parameter. In such
                                    a case we use the sub_dict_name to access it.
        Returns:
            boolean: True if the value was found, False otherwise
        """

        if not response:
            return False
        if not "value" in response:
            return False

        values = response["value"]
        if not values or not isinstance(values, list):
            return False

        if not sub_dict_name:
            for item in values:
                if value == item[key]:
                    return True
        else:
            for item in values:
                if not sub_dict_name in item:
                    return False
                if value == item[sub_dict_name][key]:
                    return True
        return False

    # end method definition

    def getResultValue(self, response: dict, key: str, index: int = 0) -> str:
        """Get value of a result property with a given key of an MS Graph API call.

        Args:
            response (dictionary): REST response from an MS Graph REST Call
            key (string): property name (key)
            index (integer, optional): Index to use (1st element has index  0).
                                       Defaults to 0.
        Returns:
            string: value for the key, None otherwise
        """

        if not response:
            return ""
        if not "value" in response:
            return ""

        values = response["value"]
        if not values or not isinstance(values, list) or len(values) - 1 < index:
            return ""

        return values[index][key]

    # end method definition

    def authenticate(self, revalidate: bool = False):
        """Authenticate at M365 Graph API with client ID and client secret.

        Args:
            revalidate (boolean, optional): determinse if a re-athentication is enforced
                                            (e.g. if session has timed out with 401 error)
        Returns:
            Access token. Also stores access token in self._access_token
        """

        # Already authenticated and session still valid?
        if self._access_token and not revalidate:
            return self._access_token

        request_url = self.config()["authenticationUrl"]
        request_header = requestLoginHeaders

        logger.info("Requesting M365 Access Token from -> %s", request_url)

        authenticate_post_body = self.credentials()
        authenticate_response = None

        try:
            authenticate_response = requests.post(
                request_url,
                data=authenticate_post_body,
                headers=request_header,
                timeout=60,
            )
        except requests.exceptions.ConnectionError as e:
            logger.warning(
                "Unable to connect to -> %s : %s", self.config()["authenticationUrl"], e
            )
            return None

        if authenticate_response.ok:
            authenticate_dict = self.parseRequestResponse(authenticate_response)
            if not authenticate_dict:
                return None
            else:
                access_token = authenticate_dict["access_token"]
                logger.debug("Access Token -> %s", access_token)
        else:
            logger.error(
                "Failed to request an M365 Access Token; error -> %s",
                authenticate_response.text,
            )
            return None

        # Store authentication access_token:
        self._access_token = access_token
        return self._access_token

    # end method definition

    def authenticateUser(self, username: str, password: str):
        """Authenticate at M365 Graph API with username and password.

        Args:
            username (string): name (emails) of the M365 user
            password (string): password of the M365 user
        Returns:
            Access token. Also stores access token in self._access_token
        """

        request_url = self.config()["authenticationUrl"]
        request_header = requestLoginHeaders

        logger.info(
            "Requesting M365 Access Token for user -> %s from -> %s",
            username,
            request_url,
        )

        authenticate_post_body = self.credentialsUser(username, password)
        authenticate_response = None

        try:
            authenticate_response = requests.post(
                request_url,
                data=authenticate_post_body,
                headers=request_header,
                timeout=60,
            )
        except requests.exceptions.ConnectionError as e:
            logger.warning(
                "Unable to connect to -> %s with username -> %s: %s",
                self.config()["authenticationUrl"],
                username,
                e,
            )
            return None

        if authenticate_response.ok:
            authenticate_dict = self.parseRequestResponse(authenticate_response)
            if not authenticate_dict:
                return None
            else:
                access_token = authenticate_dict["access_token"]
                logger.debug("User Access Token -> %s", access_token)
        else:
            logger.error(
                "Failed to request an M365 Access Token for user -> %s; error -> %s",
                username,
                authenticate_response.text,
            )
            return None

        # Store authentication access_token:
        self._user_access_token = access_token
        return self._user_access_token

    # end method definition

    def getUsers(self):
        """Get list all all users in M365 tenant

        Returns:
            List of all users.
        """

        request_url = self.config()["usersUrl"]
        request_header = self.requestHeader()

        logger.info("Get list of all users; calling -> %s", request_url)

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to get list of users; status -> %s; error -> %s",
                    response.status_code,
                    response.text,
                )
                return None

    # end method definition

    def getUser(self, user_email: str, show_error: bool = False):
        """Get a M365 User based on its email

        Args:
            user_email (string): M365 user email
        Returns:
            User information (json) or None if the user couldn't be retrieved (e.g. because it doesn't exist).
            Example Output:
            {
                '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#users/$entity',
                'businessPhones': [],
                'displayName': 'Bob Davis',
                'givenName': 'Bob',
                'id': '72c80809-094f-4e6e-98d4-25a736385d10',
                'jobTitle': None,
                'mail': 'bdavis@M365x61936377.onmicrosoft.com',
                'mobilePhone': None,
                'officeLocation': None,
                'preferredLanguage': None,
                'surname': 'Davis',
                'userPrincipalName': 'bdavis@M365x61936377.onmicrosoft.com'
            }
        """

        request_url = self.config()["usersUrl"] + "/" + user_email
        request_header = self.requestHeader()

        logger.info("Get user -> %s; calling -> %s", user_email, request_url)

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get user -> %s; status -> %s; error -> %s",
                        user_email,
                        response.status_code,
                        response.text,
                    )
                else:
                    logger.info("User -> %s not found.", user_email)
                return None

    # end method definition

    def getGroups(self, max_number: int = 250) -> dict:
        """Get list all all groups in M365 tenant

        Args:
            None
        Returns:
            List of all groups.
        """

        request_url = self.config()["groupsUrl"]
        request_header = self.requestHeader()

        logger.info("Get list of all groups; calling -> %s", request_url)

        retries = 0
        while True:
            response = requests.get(
                request_url,
                headers=request_header,
                params={"$top": str(max_number)},
                timeout=60,
            )
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to get list of groups; status -> %s; error -> %s",
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def getGroup(self, group_name: str, show_error: bool = False) -> dict:
        """Get a M365 Group based on its name

        Args:
            group_name (string): M365 Group name
            show_error (boolean): should an error be logged if group is not found.
        Returns:
            dictionary: Group information or None if the group couldn't be created (e.g. because it exisits already).
            Example Output:
            {
                '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#groups',
                'value': [
                    {
                        'id': 'b65f7dba-3ed1-49df-91bf-2bf99affcc8d',
                        'deletedDateTime': None,
                        'classification': None,
                        'createdDateTime': '2023-04-01T13:46:26Z',
                        'creationOptions': [],
                        'description': 'Engineering & Construction',
                        'displayName': 'Engineering & Construction',
                        'expirationDateTime': None,
                        'groupTypes': ['Unified'],
                        'isAssignableToRole': None,
                        'mail': 'Engineering&Construction@M365x61936377.onmicrosoft.com',
                        'mailEnabled': True,
                        'mailNickname': 'Engineering&Construction',
                        'membershipRule': None,
                        'membershipRuleProcessingState': None,
                        'onPremisesDomainName': None,
                        'onPremisesLastSyncDateTime': None,
                        'onPremisesNetBiosName': None,
                        'onPremisesSamAccountName': None,
                        'onPremisesSecurityIdentifier': None,
                        'onPremisesSyncEnabled': None,
                        'preferredDataLocation': None,
                        'preferredLanguage': None,
                        'proxyAddresses': ['SPO:SPO_d9deb3e7-c72f-4e8d-80fb-5d9411ca1458@SPO_604f34f0-ba72-4321-ab6b-e36ae8bd00ec', 'SMTP:Engineering&Construction@M365x61936377.onmicrosoft.com'],
                        'renewedDateTime': '2023-04-01T13:46:26Z',
                        'resourceBehaviorOptions': [],
                        'resourceProvisioningOptions': [],
                        'securityEnabled': False,
                        'securityIdentifier': 'S-1-12-1-3059711418-1239367377-4180393873-2379022234',
                        'theme': None,
                        'visibility': 'Public',
                        'onPremisesProvisioningErrors': []
                    },
                    {
                        'id': '61359860-302e-4016-b5cc-abff2293dff1',
                        ...
                    }
                ]
            }
        """

        query = {"$filter": "displayName eq '" + group_name + "'"}
        encoded_query = urllib.parse.urlencode(query, doseq=True)

        request_url = self.config()["groupsUrl"] + "?" + encoded_query
        request_header = self.requestHeader()

        logger.info("Get group -> %s; calling -> %s", group_name, request_url)

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get group -> %s; status -> %s; error -> %s",
                        group_name,
                        response.status_code,
                        response.text,
                    )
                else:
                    logger.info("Group -> %s not found.", group_name)
                return {}

    # end method definition

    def addGroup(
        self, name: str, security_enabled: bool = False, mail_enabled: bool = True
    ):
        """Add a M365 Group.

        Args:
            name (string): name of the group
            security_enabled (boolean, optional): whether or not this group is used for permission management
            mail_enabled (boolean, optional): whether or not this group is email enabled
        Returns:
            dictionary: Group information or None if the group couldn't be created (e.g. because it exisits already).
            Example Output:
            {
                '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#groups/$entity',
                'id': '28906460-a69c-439e-84ca-c70becf37655',
                'deletedDateTime': None,
                'classification': None,
                'createdDateTime': '2023-04-01T11:40:13Z',
                'creationOptions': [],
                'description': None,
                'displayName': 'Test',
                'expirationDateTime': None,
                'groupTypes': ['Unified'],
                'isAssignableToRole': None,
                'mail': 'Diefenbruch@M365x61936377.onmicrosoft.com',
                'mailEnabled': True,
                'mailNickname': 'Test',
                'membershipRule': None,
                'membershipRuleProcessingState': None,
                'onPremisesDomainName': None,
                'onPremisesLastSyncDateTime': None,
                'onPremisesNetBiosName': None,
                'onPremisesSamAccountName': None,
                'onPremisesSecurityIdentifier': None,
                'onPremisesSyncEnabled': None,
                'onPremisesProvisioningErrors': [],
                'preferredDataLocation': None,
                'preferredLanguage': None,
                'proxyAddresses': ['SMTP:Test@M365x61936377.onmicrosoft.com'],
                'renewedDateTime': '2023-04-01T11:40:13Z',
                'resourceBehaviorOptions': [],
                'resourceProvisioningOptions': [],
                'securityEnabled': True,
                'securityIdentifier': 'S-1-12-1-680551520-1134470812-197642884-1433859052',
                'theme': None,
                'visibility': 'Public'
            }
        """

        group_post_body = {
            "displayName": name,
            "mailEnabled": mail_enabled,
            "mailNickname": name.replace(" ", ""),
            "securityEnabled": security_enabled,
            "groupTypes": ["Unified"],
        }

        request_url = self.config()["groupsUrl"]
        request_header = self.requestHeader()

        logger.info("Adding M365 group -> %s; calling -> %s", name, request_url)
        logger.debug("M365 group attributes -> %s", group_post_body)

        retries = 0
        while True:
            response = requests.post(
                request_url,
                data=json.dumps(group_post_body),
                headers=request_header,
                timeout=60,
            )
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to add M365 group -> %s; status -> %s; error -> %s",
                    name,
                    response.status_code,
                    response.text,
                )
                return None

    # end method definition

    def addUser(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        location: str = "US",
        department: str = "",
    ) -> dict:
        """Add a M365 user.

        Args:
            email (string): email address of the user. This is also the unique identifier
            password (string): password of the user
            first_name (string): first name of the user
            last_name (string): last name of the user
            location (string, optional): country ISO 3166-1 alpha-2 format (e.g. US, CA, FR, DE, CN, ...)
            department (string, optional): department of the user
        Returns:
            dictionary: User information or None if the user couldn't be created (e.g. because it exisits already).
        """

        user_post_body = {
            "accountEnabled": True,
            "displayName": first_name + " " + last_name,
            "givenName": first_name,
            "surname": last_name,
            "mailNickname": email.split("@")[0],
            "userPrincipalName": email,
            "passwordProfile": {
                "forceChangePasswordNextSignIn": False,
                "password": password,
            },
            "usageLocation": location,
        }
        if department:
            user_post_body["department"] = department

        request_url = self.config()["usersUrl"]
        request_header = self.requestHeader()

        logger.info("Adding M365 user -> %s; calling -> %s", email, request_url)

        retries = 0
        while True:
            response = requests.post(
                request_url,
                data=json.dumps(user_post_body),
                headers=request_header,
                timeout=60,
            )
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to add M365 user -> %s; status -> %s; error -> %s",
                    email,
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def hasTeam(self, group_name: str) -> bool:
        """Check if a M365 Group has a M365 Team connected or not

        Args:
            group_name (str): name of the M365 group
        Returns:
            boolean: Returns True if a Team is assigned and False otherwise
        """

        response = self.getGroup(group_name)
        if response is None or not "value" in response or not response["value"]:
            logger.error("M365 group -> %s not found.", group_name)
            return False
        group_id = response["value"][0]["id"]

        request_url = self.config()["groupsUrl"] + "/" + group_id + "/team"
        request_header = self.requestHeader()

        logger.info(
            "Check if group -> %s has a M365 Team connected; calling -> %s",
            group_name,
            request_url,
        )

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)

            if response.status_code == 200:  # Group has a Team assigned!
                logger.info("Group -> %s has has a M365 team connected.", group_name)
                return True
            elif response.status_code == 404:  # Group does not have a Team assigned!
                logger.info("Group -> %s has has no M365 team connected.", group_name)
                return False
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to check if group -> %s has a Team connected; status -> %s; error -> %s",
                    group_name,
                    response.status_code,
                    response.text,
                )
                return False

    # end method definition

    def addTeam(self, name: str, template_name: str = "standard"):
        """Add M365 Team based on an existing M365 Group.

        Args:
            name (string): name of the team. It is assumed that a group with the same name does already exist!
            template_name (string, optional): name of the team template. "standard" is the default value.
        Returns:
            Team information (json - empty text!) or None if the team couldn't be created (e.g. because it exisits already).
        """

        response = self.getGroup(name)
        if response is None or not "value" in response or not response["value"]:
            logger.error(
                "M365 group -> %s not found. It is required for creating a corresponding M365 Team.",
                name,
            )
            return None
        group_id = response["value"][0]["id"]

        response = self.getGroupOwners(name)
        if response is None or not "value" in response or not response["value"]:
            logger.warning(
                "M365 group -> %s has no owners. This is required for creating a corresponding M365 Team.",
                name,
            )
            return None

        team_post_body = {
            "template@odata.bind": "{}('{}')".format(
                self.config()["teamsTemplatesUrl"], template_name
            ),
            "group@odata.bind": "{}('{}')".format(self.config()["groupsUrl"], group_id),
        }

        request_url = self.config()["teamsUrl"]
        request_header = self.requestHeader()

        logger.info("Adding team -> %s; calling -> %s", name, request_url)
        logger.debug("Team Attributes -> %s", team_post_body)

        retries = 0
        while True:
            response = requests.post(
                request_url,
                data=json.dumps(team_post_body),
                headers=request_header,
                timeout=60,
            )
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to add team -> %s; status -> %s; error -> %s",
                    name,
                    response.status_code,
                    response.text,
                )
                return None

    # end method definition

    def deleteTeams(self, name: str) -> bool:
        """Delete Microsoft 365 Teams with a specific name. Microsoft 365 allows
            to have multiple teams with the same name. So this method may delete
            multiple teams if the have the same name. The Graph API we use here
            is the M365 Group API as deleting the group also deletes the associated team.

        Args:
            name (string): name of the Microsoft 365 Team
        Returns:
            boolean: True if teams have been deleted, False otherwise.
        """

        # We need a special handling of team names with single quotes:
        escaped_group_name = name.replace("'", "''")
        encoded_group_name = quote(escaped_group_name, safe="")
        request_url = self.config()[
            "groupsUrl"
        ] + "?$filter=displayName eq '{}'".format(encoded_group_name)

        request_header = self.requestHeader()

        logger.info(
            "Delete all Microsoft 365 Teams with name -> %s; calling -> %s",
            name,
            request_url,
        )

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                existing_teams = self.parseRequestResponse(response)
                break
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to get list of groups; status -> %s; error -> %s",
                    response.status_code,
                    response.text,
                )
                existing_teams = None
                break

        if existing_teams:
            data = existing_teams.get("value")
            if data:
                counter = 0
                for team in data:
                    team_id = team.get("id")
                    request_url = self.config()["groupsUrl"] + "/" + team_id
                    response = requests.delete(
                        request_url, headers=request_header, timeout=60
                    )

                    if not response.ok:
                        logger.error(
                            "Failed to delete team -> %s with ID -> %s", name, team_id
                        )
                        continue
                    counter += 1

                logger.info(
                    "%s teams with name -> %s have been deleted.", counter, name
                )
                return True
            else:
                logger.info("No teams with name -> %s found.", name)
                return False
        else:
            logger.error("Failed to retrieve teams with name -> %s", name)
            return False

    # end method definition

    def deleteAllTeams(self, exception_list: list, pattern_list: list) -> bool:
        """Delete all teams (groups) that are NOT on the exception list AND
           that are matching at least one of the patterns in the provided pattern list.
           This method is used for general cleanup of teams. Be aware that deleted teams
           are still listed under https://admin.microsoft.com/#/deletedgroups

        Args:
            exception_list (list): list of group names that should not be deleted
            pattern_list (list): list of patterns for group names to be deleted
                                 (regular expression)
        Returns:
            boolean: True if teams have been deleted, False otherwise.
        """

        # Get list of all existing M365 groups/teams:
        response = self.getGroups(max_number=500)
        if not "value" in response or not response["value"]:
            return False
        groups = response["value"]
        logger.info(
            "Found -> %s existing M365 groups. Checking which ones should be deleted...",
            len(groups),
        )

        # Process all groups and check if the< should be
        # deleted:
        for group in groups:
            group_name = group["displayName"]
            # Check if group is in exception list:
            if group_name in exception_list:
                logger.info(
                    "Group name -> %s is on the exception list. Skipping.", group_name
                )
                continue
            # Check that at least one pattern is found that matches the group:
            for pattern in pattern_list:
                result = re.search(pattern, group_name)
                if result:
                    logger.info(
                        "Group name -> %s is matching pattern -> %s. Delete it now...",
                        group_name,
                        pattern,
                    )
                    self.deleteTeams(group_name)
                    break
            else:
                logger.info(
                    "Group name -> %s is not matching any delete pattern. Skipping.",
                    group_name,
                )
        return True

    # end method definition

    def getUserLicenses(self, user_id: str) -> dict:
        """Get the assigned license SKUs of a user

        Args:
            user_id (string): M365 GUID of the user (can also be the M365 email of the user)
        Returns:
            dictionary: List of user licenses or None if request fails.
            Example Output:
            {
                '@odata.context': "https://graph.microsoft.com/v1.0/$metadata#users('a5875311-f0a5-486d-a746-bd7372b91115')/licenseDetails",
                'value': [
                    {
                        'id': '8DRPYHK6IUOra-Nq6L0A7GAn38eBLPdOtXhbU5K1cd8',
                        'skuId': 'c7df2760-2c81-4ef7-b578-5b5392b571df',
                        'skuPartNumber': 'ENTERPRISEPREMIUM',
                        'servicePlans': [{...}, {...}, {...}, {...}, {...}, {...}, {...}, {...}, {...}, ...]
                    }
                ]
            }
        """

        request_url = self.config()["usersUrl"] + "/" + user_id + "/licenseDetails"
        request_header = self.requestHeader()

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to get licenses of user -> %s; status -> %s; error -> %s",
                    user_id,
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def assignLicenseToUser(self, user_id: str, sku_id: str) -> dict:
        """Add an M365 license to a user (e.g. to use Office 365)

        Args:
            user_id (string): M365 GUID of the user (can also be the M365 email of the user)
            sku_id (string): M365 GUID of the SKU
                            (e.g. c7df2760-2c81-4ef7-b578-5b5392b571df for E5 and
                                  6fd2c87f-b296-42f0-b197-1e91e994b900 for E3)

        Returns:
            dictionary: response or None if request fails
        """

        request_url = self.config()["usersUrl"] + "/" + user_id + "/assignLicense"
        request_header = self.requestHeader()

        # Construct the request body for assigning the E5 license
        license_post_body = {
            "addLicenses": [
                {
                    "disabledPlans": [],
                    "skuId": sku_id,  # "c42b9cae-ea4f-4a69-9ca5-c53bd8779c42"
                }
            ],
            "removeLicenses": [],
        }

        logger.info(
            "Assign license -> %s to user -> %s; calling -> %s",
            sku_id,
            user_id,
            request_url,
        )

        retries = 0
        while True:
            response = requests.post(
                request_url, json=license_post_body, headers=request_header, timeout=60
            )
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to add license -> %s to user -> %s; status -> %s; error -> %s",
                    sku_id,
                    user_id,
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def getUserPhoto(self, user_id: str, show_error: bool = True):
        """Get the photo of a M365 user

        Args:
            user_id (string): M365 GUID of the user (can also be the M365 email of the user)
            show_error (boolean): whether or not an error should be logged if the user
                                  does not have a photo in M365
        Returns:
            string: Image of the user photo or None if the user photo couldn't be retrieved.
        """

        request_url = self.config()["usersUrl"] + "/" + user_id + "/photo/$value"
        # Set image as content type:
        request_header = self.requestHeader("image/*")

        logger.info("Get photo of user -> %s; calling -> %s", user_id, request_url)

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                return response.content  # this is the actual image - not json!
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get photo of user -> %s; status -> %s; error -> %s",
                        user_id,
                        response.status_code,
                        response.text,
                    )
                else:
                    logger.info("User -> %s does not yet have a photo.", user_id)
                return None

    # end method definition

    def updateUserPhoto(self, user_id: str, photo_path: str) -> dict:
        """Update the M365 user photo

        Args:
            user_id (string): M365 GUID of the user (can also be the M365 email of the user)
            photo_path (string): file system path with the location of the photo
        Returns:
            dictionary: Response of Graph REST API or None if the user photo couldn't be updated.
        """

        request_url = self.config()["usersUrl"] + "/" + user_id + "/photo/$value"
        # Set image as content type:
        request_header = self.requestHeader("image/*")

        # Check if the photo file exists
        if not os.path.isfile(photo_path):
            logger.error("Photo file -> %s not found!", photo_path)
            return {}

        try:
            # Read the photo file as binary data
            with open(photo_path, "rb") as image_file:
                photo_data = image_file.read()
        except OSError as e:
            # Handle any errors that occurred while reading the photo file
            logger.error("Error reading photo file -> %s; error -> %s", photo_path, e)
            return {}

        data = photo_data

        logger.info(
            "Update user -> %s with photo -> %s; calling -> %s",
            user_id,
            photo_path,
            request_url,
        )

        retries = 0
        while True:
            response = requests.put(
                request_url, headers=request_header, data=data, timeout=60
            )
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to update user -> %s with photo -> %s; status -> %s; error -> %s",
                    user_id,
                    photo_path,
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def getGroupMembers(self, group_name: str) -> dict:
        """Get members (users and groups) of the specified group.

        Args:
            group_name (string): name of the group
        Returns:
            dictionary: Response of Graph REST API or None if the REST call fails.
        """

        response = self.getGroup(group_name)
        if not response or not "value" in response or not response["value"]:
            logger.error(
                "Group -> %s does not exist! Cannot retrieve group members.", group_name
            )
            return {}
        group_id = response["value"][0]["id"]

        query = {"$select": "id,displayName,mail,userPrincipalName"}
        encoded_query = urllib.parse.urlencode(query, doseq=True)

        request_url = (
            self.config()["groupsUrl"] + "/" + group_id + "/members?" + encoded_query
        )
        request_header = self.requestHeader()

        logger.info(
            "Get members of group -> %s (%s); calling -> %s",
            group_name,
            group_id,
            request_url,
        )

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to get members of group -> %s (%s); status -> %s; error -> %s",
                    group_name,
                    group_id,
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def getGroupOwners(self, group_name: str) -> dict:
        """Get owners (users) of the specified group.

        Args:
            group_name (string): name of the group
        Returns:
            dictionary: Response of Graph REST API or None if the REST call fails.
        """

        response = self.getGroup(group_name)
        if not response or not "value" in response or not response["value"]:
            logger.error(
                "Group -> %s does not exist! Cannot retrieve group owners.", group_name
            )
            return {}
        group_id = response["value"][0]["id"]

        query = {"$select": "id,displayName,mail,userPrincipalName"}
        encoded_query = urllib.parse.urlencode(query, doseq=True)

        request_url = (
            self.config()["groupsUrl"] + "/" + group_id + "/owners?" + encoded_query
        )
        request_header = self.requestHeader()

        logger.info(
            "Get owners of group -> %s (%s); calling -> %s",
            group_name,
            group_id,
            request_url,
        )

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to get owners of group -> %s (%s); status -> %s; error -> %s",
                    group_name,
                    group_id,
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def addGroupMember(self, group_id: str, member_id: str) -> dict:
        """Add a member (user or group) to a (parent) group

        Args:
            group_id (string): M365 GUID of the group
            member_id (string): M365 GUID of the new member
        Returns:
            dictionary: response of the MS Graph API call or None if the call fails.
        """

        request_url = self.config()["groupsUrl"] + "/" + group_id + "/members/$ref"
        request_header = self.requestHeader()

        group_member_post_body = {
            "@odata.id": self.config()["directoryObjects"] + "/" + member_id
        }

        logger.info(
            "Adding member -> %s to group -> %s; calling -> %s",
            member_id,
            group_id,
            request_url,
        )

        retries = 0
        while True:
            response = requests.post(
                request_url,
                headers=request_header,
                data=json.dumps(group_member_post_body),
                timeout=60,
            )
            if response.ok:
                return self.parseRequestResponse(response)

            # Check if Session has expired - then re-authenticate and try once more
            if response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to add member -> %s to group -> %s; status -> %s; error -> %s",
                    member_id,
                    group_id,
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def isMember(self, group_id: str, member_id: str, show_error: bool = True) -> bool:
        """Checks whether a M365 user is already in a M365 group

        Args:
            group_id (string): M365 GUID of the group
            member_id (string): M365 GUID of the user (member)
            show_error (boolean): whether or not an error should be logged if the user
                                  is not a member of the group
        Returns:
            boolean: True if the user is in the group. False otherwise.
        """

        # don't encode this URL - this has not been working!!
        request_url = (
            self.config()["groupsUrl"]
            + f"/{group_id}/members?$filter=id eq '{member_id}'"
        )
        request_header = self.requestHeader()

        logger.info(
            "Check if user -> %s is in group -> %s; calling -> %s",
            member_id,
            group_id,
            request_url,
        )

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                response = self.parseRequestResponse(response)
                if not "value" in response or len(response["value"]) == 0:
                    return False
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                # MS Graph API returns an error if the member is not in the
                # group. This is typically not what we want. We just return False.
                if show_error:
                    logger.error(
                        "Failed to check if user -> %s is in group -> %s; status -> %s; error -> %s",
                        member_id,
                        group_id,
                        response.status_code,
                        response.text,
                    )
                return False

    # end method definition

    def addGroupOwner(self, group_id: str, owner_id: str) -> dict:
        """Add an owner (user) to a group

        Args:
            group_id (string): M365 GUID of the group
            owner_id (string): M365 GUID of the new member
        Returns:
            dictionary: response of the MS Graph API call or None if the call fails.
        """

        request_url = self.config()["groupsUrl"] + "/" + group_id + "/owners/$ref"
        request_header = self.requestHeader()

        group_member_post_body = {
            "@odata.id": self.config()["directoryObjects"] + "/" + owner_id
        }

        logger.info(
            "Adding owner -> %s to group -> %s; calling -> %s",
            owner_id,
            group_id,
            request_url,
        )

        retries = 0
        while True:
            response = requests.post(
                request_url,
                headers=request_header,
                data=json.dumps(group_member_post_body),
                timeout=60,
            )
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to add owner -> %s to group -> %s; status -> %s; error -> %s",
                    owner_id,
                    group_id,
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def purgeDeletedItems(self):
        """Purge all deleted users and groups.
        Purging users and groups requires administrative rights that typically
        are not provided in Contoso example org.
        """

        request_header = self.requestHeader()

        request_url = (
            self.config()["directoryUrl"] + "/deletedItems/microsoft.graph.group"
        )
        response = requests.get(request_url, headers=request_header, timeout=60)
        deleted_groups = self.parseRequestResponse(response)

        for group in deleted_groups["value"]:
            group_id = group["id"]
            response = self.purgeDeletedItem(group_id)

        request_url = (
            self.config()["directoryUrl"] + "/deletedItems/microsoft.graph.user"
        )
        response = requests.get(request_url, headers=request_header, timeout=60)
        deleted_users = self.parseRequestResponse(response)

        for user in deleted_users["value"]:
            user_id = user["id"]
            response = self.purgeDeletedItem(user_id)

    # end method definition

    def purgeDeletedItem(self, item_id: str):
        """Helper method to purge a single deleted user or group.
           This requires elevated permissions that are typically
           not available via Graph API.

        Args:
            item_id (string): M365 GUID of the user or group to purge
        Returns:
            dictionary: response of the MS Graph API call or None if the call fails.
        """

        request_url = self.config()["directoryUrl"] + "/deletedItems/" + item_id
        request_header = self.requestHeader()

        logger.info("Purging deleted item -> %s; calling -> %s", item_id, request_url)

        retries = 0
        while True:
            response = requests.delete(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to purge deleted item -> %s; status -> %s; error -> %s",
                    item_id,
                    response.status_code,
                    response.text,
                )
                return None

    # end method definition

    def getTeamsApps(self, filter_expression: str = "") -> dict:
        """Get a list of MS Teams apps in catalog that match a given filter criterium

        Args:
            filter_expression (string, optional): filter string see https://learn.microsoft.com/en-us/graph/filter-query-parameter
        Returns:
            dictionary: response of the MS Graph API call or None if the call fails.
        """

        if filter_expression:
            query = {"$filter": filter_expression}
            encoded_query = urllib.parse.urlencode(query, doseq=True)
            request_url = self.config()["teamsAppsUrl"] + "?" + encoded_query
            logger.info(
                "Get list of MS Teams Apps using filter -> %s; calling -> %s",
                filter_expression,
                request_url,
            )
        else:
            request_url = self.config()["teamsAppsUrl"]
            logger.info("Get list of all MS Teams Apps; calling -> %s", request_url)

        request_header = self.requestHeader()

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to get list of MS Teams apps; status -> %s; error -> %s",
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def getTeamsAppsOfUser(self, user_id: str, filter_expression: str = "") -> dict:
        """Get a list of MS Teams apps of a user that match a given filter criterium

        Args:
            user_id (string): M365 GUID of the user (can also be the M365 email of the user)
            filter_expression (string, optional): filter string see https://learn.microsoft.com/en-us/graph/filter-query-parameter
        Returns:
            dictionary: response of the MS Graph API call or None if the call fails.
        """

        query = {"$expand": "teamsAppDefinition"}
        if filter_expression:
            query["$filter"] = filter_expression

        encoded_query = urllib.parse.urlencode(query, doseq=True)
        request_url = (
            self.config()["usersUrl"]
            + "/"
            + user_id
            + "/teamwork/installedApps?"
            + encoded_query
        )
        logger.info(
            "Get list of MS Teams Apps for user -> %s using query -> %s; calling -> %s",
            user_id,
            query,
            request_url,
        )

        request_header = self.requestHeader()

        retries = 0
        while True:
            response = requests.get(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to get list of MS Teams for user -> %s; status -> %s; error -> %s",
                    user_id,
                    response.status_code,
                    response.text,
                )
                return {}

    # end method definition

    def uploadTeamsApp(
        self, app_path: str, update_existing_app: bool = False, app_id: str = ""
    ) -> dict:
        """Upload a new app package to the catalog of MS Teams apps.
            This is not possible with client secret credentials
            but requires a token of a user authenticated
            with username + password.
            See https://learn.microsoft.com/en-us/graph/api/teamsapp-publish
            (permissions table on that page)

        Args:
            app_path (string): file path (with directory) to the app package to upload
        Returns:
            dictionary: Response of the MS GRAPH API REST call or None if the request fails
        """

        if update_existing_app and not app_id:
            logger.error(
                "To update an existing app you need to provide the existing App ID!"
            )
            return {}

        if not os.path.exists(app_path):
            logger.error("Teams App file -> {} does not exist!")
            return {}

        # Ensure that the app file is a zip file
        if not app_path.endswith(".zip"):
            logger.error("Teams App file -> {} must be a zip file!")
            return {}

        request_url = self.config()["teamsAppsUrl"]
        if update_existing_app:
            request_url += "/" + app_id + "/appDefinitions"
        # Here we need the credentials of an authenticated user!
        # (not the application credentials (client_id, client_secret))
        request_header = self.requestHeaderUser("application/zip")

        # upload_files = {'file': open(app_path, 'rb')}

        with open(app_path, "rb") as f:
            app_data = f.read()

        with zipfile.ZipFile(app_path) as z:
            # Ensure that the app file contains a manifest.json file
            if "manifest.json" not in z.namelist():
                logger.error(
                    "Teams App file -> {} does not contain a manifest.json file!"
                )
                return {}

        logger.info(
            "Upload Teams App -> %s to the MS Teams catalog; calling -> %s",
            app_path,
            request_url,
        )

        retries = 0
        while True:
            response = requests.post(
                request_url, headers=request_header, data=app_data, timeout=60
            )
            if response.ok:
                return self.parseRequestResponse(response)

            # Check if Session has expired - then re-authenticate and try once more
            if response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                if update_existing_app:
                    logger.warning(
                        "Failed to update existing MS teams app -> %s (may be because it is not a new version); status -> %s; error -> %s",
                        app_path,
                        response.status_code,
                        response.text,
                    )

                else:
                    logger.error(
                        "Failed to upload new MS teams app -> %s; status -> %s; error -> %s",
                        app_path,
                        response.status_code,
                        response.text,
                    )
                return {}

    # end method definition

    def removeTeamsApp(self, app_id: str):
        """Remove MS Teams App for the app catalog

        Args:
            app_id (string): Microsoft 365 GUID of the MS Teams app
        """

        request_url = self.config()["teamsAppsUrl"] + "/" + app_id
        # Here we need the credentials of an authenticated user!
        # (not the application credentials (client_id, client_secret))
        request_header = self.requestHeaderUser()

        # Make the DELETE request to remove the app from the app catalog
        response = requests.delete(request_url, headers=request_header, timeout=60)

        # Check the status code of the response
        if response.status_code == 204:
            logger.info(
                "The app with ID -> %s has been successfully removed from the app catalog.",
                app_id,
            )
        else:
            logger.error(
                "An error occurred while removing the app from the app catalog. Status code -> %s. Error message -> %s",
                response.status_code,
                response.text,
            )

    # end method definition

    def assignTeamsAppToUser(self, user_id: str, app_name: str) -> dict:
        """Assigns (adds) a MS teams app to a M365 user.

        Args:
            user_id (string): M365 GUID of the user (can also be the M365 email of the user)
            app_name (string): exact name of the app
        Returns:
            dictionary: response of the MS Graph API call or None if the call fails.
        """

        app = self.getTeamsApps(f"contains(displayName, '{app_name}')")
        if not app or not app["value"]:
            logger.error("App -> %s not found!", app_name)
            return {}
        app_id = self.getResultValue(app, "id", 0)

        request_url = (
            self.config()["usersUrl"] + "/" + user_id + "/teamwork/installedApps"
        )
        request_header = self.requestHeader()

        post_body = {
            "teamsApp@odata.bind": self.config()["teamsAppsUrl"] + "/" + app_id
        }

        logger.info(
            "Assign teams app -> %s (%s) to user -> %s; calling -> %s",
            app_name,
            app_id,
            user_id,
            request_url,
        )

        retries = 0
        while True:
            response = requests.post(
                request_url, json=post_body, headers=request_header, timeout=60
            )
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to assign teams app -> {} ({}) to user -> {}; status -> {}; error -> {}".format(
                        app_name, app_id, user_id, response.status_code, response.text
                    )
                )
                return {}

    # end method definition

    def upgradeTeamsAppOfUser(self, user_id: str, app_name: str) -> dict:
        """Upgrade a MS teams app for a user. The call will fail if the user does not
            already have the app assigned. So this needs to be checked before
            calling this method.

        Args:
            user_id (string): M365 GUID of the user (can also be the M365 email of the user)
            app_name (string): exact name of the app
        Returns:
            dictionary: response of the MS Graph API call or None if the call fails.
        """

        app = self.getTeamsAppsOfUser(
            user_id, "contains(teamsAppDefinition/displayName, '{}')".format(app_name)
        )
        if not app or not app["value"]:
            logger.error("App -> {} not found!".format(app_name))
            return {}
        app_id = self.getResultValue(app, "id", 0)

        request_url = (
            self.config()["usersUrl"]
            + "/"
            + user_id
            + "/teamwork/installedApps/"
            + app_id
            + "/upgrade"
        )
        request_header = self.requestHeader()

        logger.info(
            "Upgrade teams app -> {} ({}) of user -> {}; calling -> {}".format(
                app_name, app_id, user_id, request_url
            )
        )

        retries = 0
        while True:
            response = requests.post(request_url, headers=request_header, timeout=60)
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to upgrade teams app -> {} ({}) of user -> {}; status -> {}; error -> {}".format(
                        app_name, app_id, user_id, response.status_code, response.text
                    )
                )
                return {}

    # end method definition

    def addSensitivityLabel(
        self,
        name: str,
        display_name: str,
        description: str = "",
        color: str = "red",
        enabled: bool = True,
        admin_description: str = "",
        user_description: str = "",
        enable_encryption: bool = False,
        enable_marking: bool = False,
    ):
        """Create a new sensitivity label in M365
            THIS IS CURRENTLY NOT WORKING!

        Args:
            name (string): _description_
            display_name (string): _description_
            description (string, optional): _description_. Defaults to "".
            color (string, optional): _description_. Defaults to "red".
            enabled (boolean, optional): _description_. Defaults to True.
            admin_description (string, optional): _description_. Defaults to "".
            user_description (string, optional): _description_. Defaults to "".
            enable_encryption (boolean, optional): _description_. Defaults to False.
            enable_marking (boolean, optional): _description_. Defaults to False.

        Returns:
            Request reponse or None if the request fails.
        """

        # Prepare the request body
        payload = {
            "displayName": display_name,
            "description": description,
            "isEnabled": enabled,
            "labelColor": color,
            "adminDescription": admin_description,
            "userDescription": user_description,
            "encryptContent": enable_encryption,
            "contentMarking": enable_marking,
        }

        request_url = self.config()["securityUrl"] + "/sensitivityLabels"
        request_header = self.requestHeader()

        logger.info(
            "Create sensitivity label -> {}; calling -> {}".format(name, request_url)
        )

        # Send the POST request to create the label
        response = requests.post(
            request_url, headers=request_header, data=json.dumps(payload), timeout=60
        )

        # Check the response status code
        if response.status_code == 201:
            logger.info("Label -> {} has been created successfully!".format(name))
            return response
        else:
            logger.error(
                "Failed to create the label -> {}! Response status code: {}".format(
                    name, response.status_code
                )
            )
            return None

    # end method definition

    def assignSensitivityLabelToUser(self, user_email: str, label_name: str):
        """Assigns a existing sensitivity label to a user.
            THIS IS CURRENTLY NOT WORKING!

        Args:
            user_email (string): email address of the user (as unique identifier)
            label_name (string): name of the label (need to exist)

        Returns:
            Return the request response or None if the request fails.
        """

        # Set up the request body with the label name
        body = {"labelName": label_name}

        request_url = (
            self.config()["usersUrl"] + "/" + user_email + "/assignSensitivityLabels"
        )
        request_header = self.requestHeader()

        logger.info(
            "Assign label -> {} to user -> {}; calling -> {}".format(
                label_name, user_email, request_url
            )
        )

        retries = 0
        while True:
            response = requests.post(
                request_url, headers=request_header, json=body, timeout=60
            )
            if response.ok:
                return self.parseRequestResponse(response)
            # Check if Session has expired - then re-authenticate and try once more
            elif response.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                request_header = self.requestHeader()
                retries += 1
            else:
                logger.error(
                    "Failed to assign label -> {} to user -> {}; status -> {}; error -> {}".format(
                        label_name, user_email, response.status_code, response.text
                    )
                )
                return None

    # end method definition
