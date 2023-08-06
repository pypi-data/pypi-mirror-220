"""
Payload Module to implement functions to process Terrarium payload

This code processes a YAML payload file that includes various settings:
* WebHooks (URLs) to call (e.g. to start-up external services or applications)
* OTDS partitions and OAuth clients
* OTDS trusted sites and system attributes
* OTDS licenses
* Extended ECM users and groups
* Extended ECM Admin Settings (LLConfig)
* Extended ECM External System Connections (SAP, SuccessFactors, ...)
* Extended ECM Transport Packages (scenarios and demo content)
* Extended ECM CS Applications (typically based on Web Reports)
* Extended ECM Web Reports to run
* Extended ECM Workspaces to create (incl. members, workspace relationships)
* Extended ECM user photos, user favorites and user settings
* Extended ECM items to create and permissions to apply
* Extended ECM items to rename
* Extended ECM assignments (used e.g. for Government scenario)
* Extended ECM Records Management settings, Security Clearance, Supplemental Markings, and Holds
* SAP RFCs (Remote Function Calls)
* Commands to execute in Kubernetes Pods

This code typically runs in a container as part of the cloud automation.

Class: Payload
Methods:

__init__ : class initializer
replacePlaceholders: replace placeholder in admin config files
initPayload: load and initialize the YAML payload
getPayloadSection: delivers a section of the payload as a list of settings
getAllGroupNames: construct a list of all group name
checkStatusFile: check if the payload section has been processed before
writeStatusFile: Write a status file into the Admin Personal Workspace in Extended ECM
                 to indicate that the payload section has been deployed successfully
determineGroupID: determine the id of a group - either from payload or from OTCS
determineUserID: determine the id of a user - either from payload or from OTCS
determineWorkspaceID: determine the nodeID of a workspace - either from payload or from OTCS

processPayload: process payload (main method)
processWebHooks: process list of web hooks
processPartitions: process the OTDS partitions
processPartitionLicenses: process the licenses that should be assigned to OTDS partitions (this includes existing partitions)
processOAuthClients: process the OTDS OAuth clients
processTrustedSites: process the OTDS trusted sites
processSystemAttributes: process the OTDS system attributes
processGroups: process Extended ECM user groups
processGroupsM365: process M365 user groups
processUsers: process Extended ECM users
processUsersM365: process M365 users
processAdminSettings: process Extended ECM administration settings (LLConfig)
processExternalSystems: process Extended ECM external systems
processTransportPackages: process Extended ECM transport packages
processUserPhotos: process Extended ECM user photos (user profile)
processUserPhotosM365: process user photos in payload and assign them to Microsoft 365 users.
processWorkspaceTypes: process Extended ECM workspace types (needs to run after processTransportPackages)
processWorkspaces: process Extended ECM workspace instances
processWorkspaceRelationships: process Extended ECM workspace relationships
processWorkspaceMembers: process Extended ECM workspace members (users and groups)
processWebReports: process Extended ECM Web Reports (starts them with parameters)
processCSApplications: process Extended ECM CS Applications
processUserSettings: Process user settings in payload and apply themin OTDS.
processUserFavoritesAndProfile: Process user favorites in payload and create them in Extended ECM
processSecurityClearances: process Security Clearance for users
processSupplementalMarkings: process Supplemental Markings for users
processUserSecurity: process Security Clearance and Supplemental Markings for users
processRecordsManagementSettings: process Records Management settings by applying settings files
processHolds: process Records Management Holds
processAdditionalGroupMembers: process additional OTDS group memberships
processAdditionalAccessRoleMembers: process additional OTDS group memberships
processRenamings: process Extended ECM node renamings
processItems: process Extended ECM items (nodes) to create
processPermissions: process permission changes for alist of Extended ECM items or volumes
processAssignments: process assignments of workspaces / documents to users / groups
processUserLicenses: process and apply licenses to all Extended ECM users (used for OTIV)
processExecPodCommands: process Kubernetes pod commands
initSAP: initalize SAP object for RFC communication
processSAPRFCs: process SAP Remote Function Calls (RFC) to trigger automation in SAP S/4HANA
processDocumentGenerators: Generate documents for a defined workspace type based on template

getPayload: return the payload data structure
getUsers: return list of users
getGroups: return list of groups
getWorkspaces: return list of workspaces
getOTCSFrontend: return OTCS object for OTCS frontend
getOTCSBackend: return OTCS object for OTCS backend
getOTDS: return OTDS object
getK8S: return the Kubernetes object

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
import time
from typing import Callable
from urllib.parse import urlparse

import yaml
import hcl2.api

# OpenText specific modules:
from pyxecm.k8s import K8s
from pyxecm.m365 import M365
from pyxecm.otac import OTAC
from pyxecm.otcs import OTCS
from pyxecm.otds import OTDS
from pyxecm.sap import SAP
from pyxecm.otiv import OTIV
from pyxecm.otpd import OTPD
from pyxecm.helper.web import HTTP as web

logger = logging.getLogger("customizer.payload")


class Payload:
    """Used to process Terrarium payload."""

    # _debug controls whether or not transport processing is
    # stopped if one transport fails:
    _debug: bool = False
    _otcs: OTCS
    _otcs_backend: OTCS
    _otcs_frontend: OTCS
    _otac: OTAC | None
    _otds: OTDS
    _otiv = OTIV | None
    _k8s = K8s | None
    _web = web
    _m365 = M365 | None
    _custom_settings_dir = ""

    # _payload_source (string): This is either path + filename of the yaml payload
    # or an path + filename of the Terraform HCL payload
    _payload_source = ""
    # _payload is a dict of the complete payload file.
    # It is initialized by the initPayload() method:
    _payload = {}
    # _payload_sections is a list of dicts:
    _payload_sections = []

    # Initialize payload section variables. They are all liust of dicts:
    _webhooks = []
    _webhooks_post = []
    _partitions = []
    _oauth_clients = []
    _trusted_sites = []
    _system_attributes = []
    _groups = []
    # users: List of users. List items are dicts with "id", "name" (= login),
    # "password", "firstname", "lastname", and "email"
    _users = []
    _admin_settings = []
    # exec_pod_commands: list of commands to be executed in the pods
    # list elements need to be dicts with pod name, command, etc.
    _exec_pod_commands = []
    # external_systems (list): List of external systems. Each list element is a dict with
    # "description", "external_system_name", "connection_type",
    # "as_url", "base_url", "username", and "password". Depending
    # on the connection type there may be additional dict values.
    _external_systems = []
    # transport_packages (list): List of transport packages systems. Each list element is a
    # dict with "url", "name", and "description" keys.
    _transport_packages = []
    _content_transport_packages = []
    _transport_packages_post = []
    _workspace_types = []
    _workspaces = []
    _sap_rfcs = []
    _web_reports = []
    _web_reports_post = []
    _cs_applications = []
    _admin_settings_post = []
    # additional_group_members: List of memberships to establish. Each element
    # is a dict with these keys:
    # - parent_group (string)
    # - user_name (string)
    # - group_name (string)
    _additional_group_members = []
    # additional_access_role_members: List of memberships to establish. Each element
    # is a dict with these keys:
    # - access_role (string)
    # - user_name (string)
    # - group_name (string)
    # - partition_name (string)
    _additional_access_role_members = []
    _renamings = []
    _items = []
    _items_post = []
    _permissions = []
    _permissions_post = []
    # assignments: List of assignments. Each element is a dict with these keys:
    # - subject (string)
    # - instruction (string)
    # - workspace (string)
    # - nickname (string)
    # - groups (list)
    # - users (list)
    _assignments = []
    _workspace_template_registrations = []
    _security_clearances = []
    _supplemental_markings = []
    _records_management_settings = []
    _holds = []
    _doc_generators = []

    _placeholder_values = {}

    _otcs_restart_callback: Callable

    def __init__(
        self,
        payload_source: str,
        custom_settings_dir: str,
        k8s_object: K8s | None,
        otds_object: OTDS,
        otac_object: OTAC | None,
        otcs_backend_object: OTCS,
        otcs_frontend_object: OTCS,
        otcs_restart_callback,
        otiv_object: OTIV | None,
        m365_object: M365 | None,
        placeholder_values: dict,
        stop_on_error: bool = False,
    ):
        """Initialize the Payload object

        Args:
            payload_source (string): path or URL to payload source file
            k8s_object (object): Kubernetes object
            otds_object (OTDS): OTDS object
            otac_object (OTAC): OTAC object
            otcs_backend_object (OTCS): OTCS backend object
            otcs_frontend_object (OTCS): OTCS frontend object
            otcs_restart_callback (callable): function to call if OTCS service needs a restart
            otiv_object (object): OTIV object
            m365_object (object): M365 object to talk to Microsoft Graph API
            placeholder_values (dict): dictionary of placeholder values to be replaced in admin settings
            stop_on_error (bool): controls if transport deployment should stop if one transport fails
        """

        self._stop_on_error = stop_on_error
        self._payload_source = payload_source
        self._k8s = k8s_object
        self._otds = otds_object
        self._otac = otac_object
        self._otcs = otcs_backend_object
        self._otcs_backend = otcs_backend_object
        self._otcs_frontend = otcs_frontend_object
        self._otiv = otiv_object
        self._m365 = m365_object
        self._custom_settings_dir = custom_settings_dir
        self._placeholder_values = placeholder_values
        self._otcs_restart_callback = otcs_restart_callback

        self._http_object = HTTP()

    # end method definition

    def replacePlaceholders(self, content: str):
        """Function to replace placeholders in file"""
        # https://stackoverflow.com/questions/63502218/replacing-placeholders-in-a-text-file-with-python
        return re.sub(
            r"%%(\w+?)%%",
            lambda match: self._placeholder_values[match.group(1)],
            content,
        )

        # end method definition

    def initPayload(self):
        """Read the YAML or Terraform HCL payload file.

        Args: None
        Return:
            payload as a Python dict. Elements are the different payload sections.
            None in case the file couldn't be found or read.
        """

        if not os.path.exists(self._payload_source):
            logger.error("Cannot access payload file -> %s", self._payload_source)
            return None

        # Is it a YAML file?
        if self._payload_source.endswith(".yaml"):
            logger.info("Open payload from YAML file -> %s", self._payload_source)
            try:
                with open(self._payload_source, "r", encoding="utf-8") as stream:
                    payload_data = stream.read()
                self._payload = yaml.safe_load(payload_data)
            except yaml.YAMLError as exc:
                logger.error(
                    "Error while reading YAML payload file -> %s; error -> %s",
                    self._payload_source,
                    exc,
                )
                self._payload = {}
        # Or is it a Terraform HCL file?
        elif self._payload_source.endswith(".tf"):
            logger.info(
                "Open payload from Terraform HCL file -> %s", self._payload_source
            )
            try:
                with open(self._payload_source, "r", encoding="utf-8") as stream:
                    self._payload = hcl2.api.load(stream)
                # If payload is wrapped into "external_payload" we unwrap it:
                if self._payload.get("external_payload"):
                    self._payload = self._payload["external_payload"]
            except FileNotFoundError as exc:
                logger.error(
                    "Error while reading Terraform HCL payload file -> %s; error -> %s",
                    self._payload_source,
                    exc,
                )
                self._payload = {}

        # If not, it is an unsupported type:
        else:
            logger.error(
                "File -> %s has unsupported file type",
                self._payload_source,
            )
            self._payload = {}

        if self._payload is not None:
            self._payload_sections = self._payload["payloadSections"]

            if not self._payload_sections:
                logger.error(
                    "Sections for payload -> %s are undefined - skipping...",
                    self._payload_source,
                )
                return None

        # Retrieve all the payload sections and store them in lists:
        self._webhooks = self.getPayloadSection("webHooks")
        self._webhooks_post = self.getPayloadSection("webHooksPost")
        self._partitions = self.getPayloadSection("partitions")
        self._oauth_clients = self.getPayloadSection("oauthClients")
        self._trusted_sites = self.getPayloadSection("trustedSites")
        self._system_attributes = self.getPayloadSection("systemAttributes")
        self._groups = self.getPayloadSection("groups")
        self._users = self.getPayloadSection("users")
        self._admin_settings = self.getPayloadSection("adminSettings")
        self._exec_pod_commands = self.getPayloadSection("execPodCommands")
        self._external_systems = self.getPayloadSection("externalSystems")
        self._transport_packages = self.getPayloadSection("transportPackages")
        self._content_transport_packages = self.getPayloadSection(
            "contentTransportPackages"
        )
        self._transport_packages_post = self.getPayloadSection("transportPackagesPost")
        self._workspaces = self.getPayloadSection("workspaces")
        self._sap_rfcs = self.getPayloadSection("sapRFCs")
        self._web_reports = self.getPayloadSection("webReports")
        self._web_reports_post = self.getPayloadSection("webReportsPost")
        self._cs_applications = self.getPayloadSection("csApplications")
        self._admin_settings_post = self.getPayloadSection("adminSettingsPost")
        self._additional_group_members = self.getPayloadSection(
            "additionalGroupMemberships"
        )
        self._additional_access_role_members = self.getPayloadSection(
            "additionalAccessRoleMemberships"
        )
        self._renamings = self.getPayloadSection("renamings")
        self._items = self.getPayloadSection("items")
        self._items_post = self.getPayloadSection("itemsPost")
        self._permissions = self.getPayloadSection("permissions")
        self._permissions_post = self.getPayloadSection("permissionsPost")
        self._assignments = self.getPayloadSection("assignments")
        self._security_clearances = self.getPayloadSection("securityClearances")
        self._supplemental_markings = self.getPayloadSection("supplementalMarkings")
        self._records_management_settings = self.getPayloadSection(
            "recordsManagementSettings"
        )
        self._holds = self.getPayloadSection("holds")
        self._doc_generators = self.getPayloadSection("documentGenerators")

        return self._payload
        # end method definition

    def getPayloadSection(self, payload_section_name: str) -> list:
        """Get a defined section of the payload. The section is delivered as a list of settings.
        It deliveres an empty list if this payload section is disabled by the corresponding
        payload switch (this is read from the payloadSections dictionary of the payload)

        Args:
            payload_section_name (string): name of the dict element in the payload structure
        Returns:
            list: section of the payload as a Python list. Empty list if section does not exist
            or section is disabled by the corresponding payload switch.
        """

        if not isinstance(self._payload, dict):
            return []

        # if the secton is not in the payload we return an empty list:
        if not self._payload.get(payload_section_name):
            return []

        # Check if the payload section is either enabled
        # or the struct for payloadSection enabling is not in the payload:
        sections = self._payload.get("payloadSections")
        if sections:
            section = next(
                (item for item in sections if item["name"] == payload_section_name),
                None,
            )
            if not section or not section["enabled"]:
                return []

        return self._payload[payload_section_name]

        # end method definition

    def getAllGroupNames(self) -> list:
        """Construct a list of all group name

        Returns:
            list: list of all group names
        """
        return [group.get("name") for group in self._groups]

        # end method definition

    def checkStatusFile(
        self, payload_section_name: str, payload_specific: bool = True
    ) -> bool:
        """Check if the payload section has been processed before. This is
           done by checking the existance of a text file in the Admin Personal
           workspace in Extended ECM with the name of the payload section.

        Args:
            payload_section_name (str): name of the payload section. This
                                        is used to construct the file name
            payload_specific (bool): whether or not the success should be specific for
                                     each payload file or if success is "global" - like for the deletion
                                     of the existing M365 teams (which we don't want to execute per
                                     payload file)
        Returns:
            bool: True if the payload has been processed successfully before, False otherwise
        """

        logger.info(
            "Check if payload section -> %s has been processed successfully before...",
            payload_section_name,
        )

        response = self._otcs.getNodeByVolumeAndPath(
            142
        )  # write to Personal Workspace of Admin
        target_folder_id = self._otcs.getResultValue(response, "id")
        if not target_folder_id:
            target_folder_id = 2004  # use Personal Workspace of Admin as fallback

        # Some sections are actually not payload specific like teamsM365Cleanup
        # we don't want external payload runs to re-apply this processing:
        if payload_specific:
            file_name = os.path.basename(self._payload_source)  # remove directories
            file_name = os.path.splitext(file_name)[0]  # remove file suffix
            file_name = "success_" + file_name + "_" + payload_section_name + ".txt"
        else:
            file_name = "success_" + payload_section_name + ".txt"

        status_document = self._otcs.getNodeByParentAndName(
            parent_id=int(target_folder_id), name=file_name, show_error=False
        )
        if status_document and status_document["results"]:
            name = self._otcs.getResultValue(status_document, "name")
            if name == file_name:
                logger.info(
                    "Payload section -> %s has been processed successfully before. Skipping...",
                    payload_section_name,
                )
                return True
        logger.info(
            "Payload section -> %s has not been processed successfully before. Processing...",
            payload_section_name,
        )
        return False

        # end method definition

    def writeStatusFile(
        self,
        payload_section_name: str,
        payload_section: list,
        payload_specific: bool = True,
    ) -> bool:
        """Write a status file into the Admin Personal Workspace in Extended ECM
           to indicate that the payload section has been deployed successfully.
           This speeds up the customizing process in case the customizer pod
           is restarted.

        Args:
            payload_section_name (str): name of the payload section
            payload_section (list): payload section content - this is written as JSon into the file
            payload_specific (bool): whether or not the success should be specific for
                                     each payload file or if success is "global" - like for the deletion
                                     of the existing M365 teams (which we don't want to execute per
                                     payload file)
        Returns:
            bool: True if the status file as been upladed to Extended ECM successfully, False otherwise
        """

        response = self._otcs.getNodeByVolumeAndPath(
            142
        )  # write to Personal Workspace of Admin (with Volume Type ID = 142)
        target_folder_id = self._otcs.getResultValue(response, "id")
        if not target_folder_id:
            target_folder_id = 2004  # use Personal Workspace of Admin as fallback

        # Some sections are actually not payload specific like teamsM365Cleanup
        # we don't want external payload runs to re-apply this processing:
        if payload_specific:
            file_name = os.path.basename(self._payload_source)  # remove directories
            file_name = os.path.splitext(file_name)[0]  # remove file suffix
            file_name = "success_" + file_name + "_" + payload_section_name + ".txt"
        else:
            file_name = "success_" + payload_section_name + ".txt"
        full_path = "/tmp/" + file_name

        with open(full_path, mode="w", encoding="utf-8") as localfile:
            localfile.write(json.dumps(payload_section, indent=2))

        response = self._otcs.uploadFileToParent(
            file_url=full_path,
            file_name=file_name,
            mime_type="text/plain",
            parent_id=int(target_folder_id),
        )

        if response:
            logger.info(
                "Payload section -> %s has been completed successfully!",
                payload_section_name,
            )
            return True

        return False

        # end method definition

    def determineGroupID(self, group: dict) -> int:
        """Determine the id of a group - either from payload or from OTCS.
           If the group is found in OTCS write back the ID into the payload.

        Args:
            group (dict): group payload element

        Returns:
            int: group ID
        Side Effects:
            the group items are modified by adding an "id" dict element that
            includes the technical ID of the group in Extended ECM
        """

        if "id" in group:
            return group["id"]

        if not "name" in group:
            logger.error("Group needs a name to lookup the ID.")
            return 0
        group_name = group["name"]

        existing_groups = self._otcs.getGroup(name=group_name)
        if not existing_groups or not existing_groups["data"]:
            logger.info("Cannot find an existing group with name -> %s", group_name)
            return 0

        # Get list of all matching groups:
        existing_groups_list = existing_groups["data"]
        # Find the group with the exact match of the name:
        existing_group = next(
            (item for item in existing_groups_list if item["name"] == group_name),
            None,
        )
        # Have we found an exact match?
        if existing_group:
            group["id"] = existing_group["id"]
            return group["id"]
        else:
            logger.info("Did not find an existing group with name -> %s", group_name)
            return 0

        # end method definition

    def determineUserID(self, user: dict):
        """Determine the id of a group - either from payload or from OTCS
           If the user is found in OTCS write back the ID into the payload.

        Args:
            user (dict): user payload element

        Returns:
            int: user ID
        Side Effects:
            the user items are modified by adding an "id" dict element that
            includes the technical ID of the user in Extended ECM
        """

        if "id" in user:
            return user["id"]

        if not "name" in user:
            logger.error("User needs a login name to lookup the ID.")
            return 0
        user_name = user["name"]

        existing_users = self._otcs.getUser(name=user_name)
        if not existing_users or not existing_users["data"]:
            logger.info("Cannot find an existing user with name -> %s", user_name)
            return 0

        # Get list of all matching users:
        existing_users_list = existing_users["data"]
        # Find the group with the exact match of the name:
        existing_user = next(
            (item for item in existing_users_list if item["name"] == user_name),
            None,
        )
        # Have we found an exact match?
        if existing_user:
            user["id"] = existing_user["id"]
            return user["id"]
        else:
            logger.info("Did not find an existing user with name -> %s", user_name)
            return 0

        # end method definition

    def determineWorkspaceID(self, workspace: dict):
        """Determine the nodeID of a workspace - either from payload or from OTCS

        Args:
            workspace (dict): workspace payload element

        Returns:
            int: workspace Node ID
        Side Effects:
            the workspace items are modified by adding an "nodeId" dict element that
            includes the node ID of the workspace in Extended ECM
        """

        if "nodeId" in workspace:
            return workspace["nodeId"]

        response = self._otcs.getWorkspaceByTypeAndName(
            workspace["type_name"], workspace["name"]
        )
        workspace_id = self._otcs.getResultValue(response, "id")
        if workspace_id:
            workspace["nodeId"] = workspace_id
            return workspace_id
        else:
            logger.info(
                "Workspace of type -> %s and name -> %s does not yet exist.",
                workspace["type_name"],
                workspace["name"],
            )
            return 0

        # end method definition

    def processPayload(self):
        """Main method to process a payload file.

        Args:
            None
        Returns:
            None
        """

        if not self._payload_sections:
            return None

        for payload_section in self._payload_sections:
            match payload_section["name"]:
                case "webHooks":
                    logger.info(
                        "========== Process Web Hooks ==========================="
                    )
                    self.processWebHooks(self._webhooks)
                case "webHooksPost":
                    logger.info(
                        "========== Process Web Hooks (post) ===================="
                    )
                    self.processWebHooks(self._webhooks_post, "webHooksPost")
                case "partitions":
                    logger.info(
                        "========== Process OTDS Partitions ====================="
                    )
                    self.processPartitions()
                    logger.info(
                        "========== Assign OTCS Licenses to Partitions =========="
                    )
                    self.processPartitionLicenses()
                case "oauthClients":
                    logger.info(
                        "========== Process OTDS OAuth Clients =================="
                    )
                    self.processOAuthClients()
                case "trustedSites":
                    logger.info(
                        "========== Process OTDS Trusted Sites =================="
                    )
                    self.processTrustedSites()
                case "systemAttributes":
                    logger.info(
                        "========== Process OTDS System Attributes =============="
                    )
                    self.processSystemAttributes()
                case "groups":
                    logger.info(
                        "========== Process OTCS Groups ========================="
                    )
                    self.processGroups()
                    # Add all groups with ID the a lookup dict for placeholder replacements
                    # in adminSetting. This also updates the payload with group IDs from OTCS
                    # if the group already exists in Extended ECM. This is important especially
                    # if the customizer pod is restarted / run multiple times:
                    self.processGroupPlaceholders()
                    if self._m365 and isinstance(self._m365, M365):
                        logger.info(
                            "========== Cleanup existing MS Teams ==================="
                        )
                        self.cleanupAllTeamsM365()
                        logger.info(
                            "========== Process M365 Groups ========================="
                        )
                        self.processGroupsM365()
                case "users":
                    logger.info(
                        "========== Process OTCS Users =========================="
                    )
                    self.processUsers()
                    # Add all users with ID the a lookup dict for placeholder replacements
                    # in adminSetting. This also updates the payload with user IDs from OTCS
                    # if the user already exists in Extended ECM. This is important especially
                    # if the cutomizer pod is restarted / run multiple times:
                    self.processUserPlaceholders()
                    logger.info(
                        "========== Assign OTCS Licenses to Users ==============="
                    )
                    self.processUserLicenses(
                        self._otcs.config()["resource"],
                        self._otcs.config()["license"],
                        "EXTENDED_ECM",
                        user_specific_payload_field="licenses",
                    )
                    logger.info(
                        "========== Assign OTIV Licenses to Users ==============="
                    )

                    if (
                        isinstance(self._otiv, OTIV)
                        and self._otiv.config()
                        and self._otiv.config()["resource"]
                        and self._otiv.config()["license"]
                    ):
                        self.processUserLicenses(
                            self._otiv.config()["resource"],
                            self._otiv.config()["license"],
                            "INTELLIGENT_VIEWING",
                            user_specific_payload_field="",
                        )
                    else:
                        logger.error(
                            "Cannot assign OTIV licenses as OTIV seems to not be ready yet."
                        )
                    logger.info(
                        "========== Process User Settings ======================="
                    )
                    self.processUserSettings()
                    if self._m365 and isinstance(self._m365, M365):
                        logger.info(
                            "========== Process M365 Users =========================="
                        )
                        self.processUsersM365()
                        # We need to do the MS Teams creation after the creation of
                        # the M365 users as we require Group Owners to create teams
                        logger.info(
                            "========== Process M365 Teams =========================="
                        )
                        self.processTeamsM365()
                case "adminSettings":
                    logger.info(
                        "========== Process Administration Settings (1) ========="
                    )
                    self.processAdminSettings(self._admin_settings)
                case "adminSettingsPost":
                    logger.info(
                        "========== Process Administration Settings (2) ========="
                    )
                    self.processAdminSettings(
                        self._admin_settings_post, "adminSettingsPost"
                    )
                case "execPodCommands":
                    logger.info(
                        "========== Process Pod Commands ========================"
                    )
                    self.processExecPodCommands()
                case "csApplications":
                    logger.info(
                        "========== Process CS Apps (backend) ==================="
                    )
                    self.processCSApplications(
                        self._otcs_backend, section_name="csApplicationsBackend"
                    )
                    logger.info(
                        "========== Process CS Apps (frontend) =================="
                    )
                    self.processCSApplications(
                        self._otcs_frontend, section_name="csApplicationsFrontend"
                    )
                case "externalSystems":
                    logger.info(
                        "========== Process External System Connections ========="
                    )
                    self.processExternalSystems()
                case "transportPackages":
                    logger.info(
                        "========== Process Transport Packages =================="
                    )
                    self.processTransportPackages(self._transport_packages)
                    # right after the transport that create the workspace types
                    # we extract them and put them in a generated payload list:
                    logger.info(
                        "========== Process Workspace Types ====================="
                    )
                    self.processWorkspaceTypes()
                case "contentTransportPackages":
                    logger.info(
                        "========== Process Content Transport Packages =========="
                    )
                    self.processTransportPackages(
                        self._content_transport_packages, "contentTransportPackages"
                    )
                case "transportPackagesPost":
                    logger.info(
                        "========== Process Transport Packages (post) ==========="
                    )
                    self.processTransportPackages(
                        self._transport_packages_post, "transportPackagesPost"
                    )
                case "workspaces":
                    logger.info(
                        "========== Process Workspaces =========================="
                    )
                    self.processWorkspaces()
                    logger.info(
                        "========== Process Workspace Relationships ============="
                    )
                    self.processWorkspaceRelationships()
                    logger.info(
                        "========== Process Workspace Memberships ==============="
                    )
                    self.processWorkspaceMembers()
                case "sapRFCs":
                    logger.info(
                        "========== Process SAP RFCs ============================"
                    )

                    sap_external_system = {}
                    if self._external_systems:
                        sap_external_system = next(
                            (
                                item
                                for item in self._external_systems
                                if item.get("external_system_type")
                                and item["external_system_type"] == "SAP"
                            ),
                            {},
                        )
                    if not sap_external_system:
                        logger.warning(
                            "SAP RFC in payload but SAP external system is configured. RFCs will not be processed."
                        )
                    elif not sap_external_system.get("enabled"):
                        logger.warning(
                            "SAP RFC in payload but SAP external system is disabled. RFCs will not be processed."
                        )
                    elif not sap_external_system.get("reachable"):
                        logger.warning(
                            "SAP RFC in payload but SAP external system is not reachable. RFCs will not be processed."
                        )
                    else:
                        sap = self.initSAP(sap_external_system)
                        if sap:
                            self.processSAPRFCs(sap)
                case "webReports":
                    logger.info(
                        "========== Process Web Reports ========================="
                    )
                    self.processWebReports(self._web_reports)
                case "webReportsPost":
                    logger.info(
                        "========== Process Web Reports (post) =================="
                    )
                    self.processWebReports(self._web_reports_post, "webReportsPost")
                case "additionalGroupMemberships":
                    logger.info(
                        "========== Process additional group members for OTDS ==="
                    )
                    self.processAdditionalGroupMembers()
                case "additionalAccessRoleMemberships":
                    logger.info(
                        "==== Process additional access role members for OTDS ==="
                    )
                    self.processAdditionalAccessRoleMembers()
                case "renamings":
                    logger.info(
                        "========== Process Custom Node Renamings ==============="
                    )
                    self.processRenamings()
                case "items":
                    logger.info(
                        "========== Process Items ==============================="
                    )
                    self.processItems(self._items)
                case "itemsPost":
                    logger.info(
                        "========== Process Items (post) ========================"
                    )
                    self.processItems(self._items_post, "itemsPost")
                case "permissions":
                    logger.info(
                        "========== Process Permissions ========================="
                    )
                    self.processPermissions(self._permissions)
                case "permissionsPost":
                    logger.info(
                        "========== Process Permissions (post) =================="
                    )
                    self.processPermissions(self._permissions_post)
                case "assignments":
                    logger.info(
                        "========== Process Assignments ========================="
                    )
                    self.processAssignments()
                case "securityClearances":
                    logger.info(
                        "========== Process Security Clearances ================="
                    )
                    self.processSecurityClearances()
                case "supplementalMarkings":
                    logger.info(
                        "========== Process Supplemental Markings ==============="
                    )
                    self.processSupplementalMarkings()
                case "recordsManagementSettings":
                    logger.info(
                        "========== Process Records Management Settings ========="
                    )
                    self.processRecordsManagementSettings()
                case "holds":
                    logger.info(
                        "========== Process Records Management Holds ============"
                    )
                    self.processHolds()
                case "documentGenerators":
                    logger.info(
                        "========== Process Document Generators ================="
                    )
                    self.processDocumentGenerators()
                case _:
                    logger.error(
                        "Illegal payload section name -> %s in payloadSections!",
                        payload_section["name"],
                    )
            payload_section_restart = payload_section.get("restart", False)
            if payload_section_restart:
                logger.info(
                    "Payload section -> %s requests a restart of OTCS services...",
                    payload_section["name"],
                )
                # Restart OTCS frontend and backend pods:
                self._otcs_restart_callback(self._otcs_backend)
                # give some additional time to make sure service is responsive
                time.sleep(30)
            else:
                logger.info(
                    "Payload section -> %s does not require a restart of OTCS services",
                    payload_section["name"],
                )

        if self._users:
            logger.info("========== Process User Profile Photos =================")
            self.processUserPhotos()
            if self._m365 and isinstance(self._m365, M365):
                logger.info("========== Process M365 User Profile Photos ============")
                self.processUserPhotosM365()
            logger.info("========== Process User Favorites and Profiles =========")
            self.processUserFavoritesAndProfiles()
            logger.info("========== Process User Security =======================")
            self.processUserSecurity()

        # end method definition

    def processWebHooks(self, webhooks: list, section_name: str = "webHooks") -> bool:
        """Process Web Hooks in payload and do HTTP requests.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not webhooks:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more

        # WE LET THIS RUN EACH TIME!
        #        if self.checkStatusFile(section_name):
        #            return True

        success: bool = True

        for webhook in webhooks:
            url = webhook.get("url")
            if not url:
                logger.info("Web Hook does not have a url - skipping...")
                success = False
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in webhook and not webhook["enabled"]:
                logger.info("Payload for Web Hook -> %s is disabled. Skipping...", url)
                continue

            description = webhook.get("description")

            method = webhook.get("method", "POST")

            payload = webhook.get("payload", {})

            headers = webhook.get("headers", {})

            if description:
                logger.info("Calling Web Hook -> %s: %s (%s)", method, url, description)
            else:
                logger.info("Calling Web Hook -> %s: %s", method, url)

            self._http_object.httpRequest(url, method, payload, headers)

        #        if success:
        #            self.writeStatusFile(section_name, webhooks)

        return success

        # end method definition

    def processPartitions(self, section_name: str = "partitions") -> bool:
        """Process OTDS partitions in payload and create them in OTDS.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._partitions:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for partition in self._partitions:
            partition_name = partition.get("name")
            if not partition_name:
                logger.error("Partition does not have a name - skipping...")
                success = False
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in partition and not partition["enabled"]:
                logger.info(
                    "Payload for Partition -> %s is disabled. Skipping...",
                    partition_name,
                )
                continue

            partition_description = partition.get("description")

            # Check if Partition does already exist
            # (in an attempt to make the code idem-potent)
            logger.info(
                "Check if OTDS partition -> %s does already exist...", partition_name
            )
            response = self._otds.getPartition(partition_name, show_error=False)
            if response:
                logger.info(
                    "Partition -> %s does already exist. Skipping...", partition_name
                )
                continue

            # Only continue if Partition does not exist already
            logger.info("Partition -> %s does not exist. Creating...", partition_name)

            response = self._otds.addPartition(partition_name, partition_description)
            if response:
                logger.info("Added OTDS partition -> %s", partition_name)
            else:
                logger.error("Failed to add OTDS partition -> %s", partition_name)
                success = False
                continue

            access_role = partition.get("access_role")
            if access_role:
                response = self._otds.addPartitionToAccessRole(
                    access_role, partition_name
                )
                if response:
                    logger.info(
                        "Added OTDS partition -> %s to access role -> %s",
                        partition_name,
                        access_role,
                    )
                else:
                    logger.error(
                        "Failed to add OTDS partition -> %s to access role -> %s",
                        partition_name,
                        access_role,
                    )
                    success = False
                    continue

            # Partions may have an optional list of licenses in
            # the payload. Assign the partition to all these licenses:
            partition_specific_licenses = partition.get("licenses")
            if partition_specific_licenses:
                # We assume these licenses are Extended ECM licenses!
                otcs_resource_name = self._otcs.config()["resource"]
                otcs_resource = self._otds.getResource(otcs_resource_name)
                if not otcs_resource:
                    logger.error("Cannot find OTCS resource -> %s", otcs_resource_name)
                    success = False
                    continue
                otcs_resource_id = otcs_resource["resourceID"]
                license_name = "EXTENDED_ECM"
                for license_feature in partition_specific_licenses:
                    assigned_license = self._otds.assignPartitionToLicense(
                        partition_name,
                        otcs_resource_id,
                        license_feature,
                        license_name,
                    )

                    if not assigned_license:
                        logger.error(
                            "Failed to assign partition -> %s to license feature -> %s of license -> %s!",
                            partition_name,
                            license_feature,
                            license_name,
                        )
                        success = False
                    else:
                        logger.info(
                            "Successfully assigned partition -> %s to license feature -> %s of license -> %s",
                            partition_name,
                            license_feature,
                            license_name,
                        )

        if success:
            self.writeStatusFile(section_name, self._partitions)

        return success

        # end method definition

    def processPartitionLicenses(self, section_name: str = "partitionLicenses") -> bool:
        """Process the licenses that should be assigned to OTDS partitions
           (this includes existing partitions).

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._partitions:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for partition in self._partitions:
            partition_name = partition.get("name")
            if not partition_name:
                logger.error("Partition does not have a name - skipping...")
                success = False
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in partition and not partition["enabled"]:
                logger.info(
                    "Payload for Partition -> %s is disabled. Skipping...",
                    partition_name,
                )
                continue

            response = self._otds.getPartition(partition_name, show_error=True)
            if not response:
                logger.error(
                    "Partition -> %s does not exist. Skipping...", partition_name
                )
                success = False
                continue

            # Partions may have an optional list of licenses in
            # the payload. Assign the partition to all these licenses:
            partition_specific_licenses = partition.get("licenses")
            if partition_specific_licenses:
                # We assume these licenses are Extended ECM licenses!
                otcs_resource_name = self._otcs.config()["resource"]
                otcs_resource = self._otds.getResource(otcs_resource_name)
                if not otcs_resource:
                    logger.error("Cannot find OTCS resource -> %s", otcs_resource_name)
                    success = False
                    continue
                otcs_resource_id = otcs_resource["resourceID"]
                license_name = "EXTENDED_ECM"
                for license_feature in partition_specific_licenses:
                    if self._otds.isPartitionLicensed(
                        partition_name=partition_name,
                        resource_id=otcs_resource_id,
                        license_feature=license_feature,
                        license_name=license_name,
                    ):
                        logger.info(
                            "Partition -> %s is already licensed for -> %s (%s)",
                            partition_name,
                            license_name,
                            license_feature,
                        )
                        continue
                    assigned_license = self._otds.assignPartitionToLicense(
                        partition_name,
                        otcs_resource_id,
                        license_feature,
                        license_name,
                    )

                    if not assigned_license:
                        logger.error(
                            "Failed to assign partition -> %s to license feature -> %s of license -> %s!",
                            partition_name,
                            license_feature,
                            license_name,
                        )
                        success = False
                    else:
                        logger.info(
                            "Successfully assigned partition -> %s to license feature -> %s of license -> %s",
                            partition_name,
                            license_feature,
                            license_name,
                        )

        if success:
            self.writeStatusFile(section_name, self._partitions)

        return success

        # end method definition

    def processOAuthClients(self, section_name: str = "oauthClients") -> bool:
        """Process OTDS OAuth clients in payload and create them in OTDS.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._oauth_clients:
            logger.info("Payload section -> % is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for oauth_client in self._oauth_clients:
            client_name = oauth_client.get("name")
            if not client_name:
                logger.error("OAuth client does not have a name - skipping...")
                success = False
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in oauth_client and not oauth_client["enabled"]:
                logger.info(
                    "Payload for OAuthClient -> %s is disabled. Skipping...",
                    client_name,
                )
                continue

            client_description = oauth_client.get("description")
            client_confidential = oauth_client.get("confidential")
            client_partition = oauth_client.get("partition")
            if client_partition == "Global":
                client_partition = []
            client_redirect_urls = oauth_client.get("redirect_urls")
            client_permission_scopes = oauth_client.get("permission_scopes")
            client_default_scopes = oauth_client.get("default_scopes")
            client_allow_impersonation = oauth_client.get("allow_impersonation")

            # Check if OAuth client does already exist
            # (in an attempt to make the code idem-potent)
            logger.info(
                "Check if OTDS OAuth Client -> %s does already exist...", client_name
            )
            response = self._otds.getOauthClient(client_name, show_error=False)
            if response:
                logger.info(
                    "OAuth Client -> %s does already exist. Skipping...", client_name
                )
                continue
            else:
                logger.info(
                    "OAuth Client -> %s does not exist. Creating...", client_name
                )

            response = self._otds.addOauthClient(
                client_id=client_name,
                description=client_description,
                redirect_urls=client_redirect_urls,
                allow_impersonation=client_allow_impersonation,
                confidential=client_confidential,
                auth_scopes=client_partition,
                allowed_scopes=client_permission_scopes,
                default_scopes=client_default_scopes,
            )
            if response:
                logger.info("Added OTDS OAuth client -> %s", client_name)
            else:
                logger.error("Failed to add OTDS OAuth client -> %s", client_name)
                success = False
                continue

            client_secret = response.get("secret")
            if not client_secret:
                logger.error("OAuth client -> %s does not have a secret!", client_name)
                continue

            client_description += " Client Secret Key: " + str(client_secret)
            response = self._otds.updateOauthClient(
                client_name, {"description": client_description}
            )

        if success:
            self.writeStatusFile(section_name, self._oauth_clients)

        return success

    #        self._otds.addOauthClientsToAccessRole()

    # end method definition

    def processTrustedSites(self, section_name: str = "trustedSites") -> bool:
        """Process OTDS trusted sites in payload and create them in OTDS.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._trusted_sites:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for trusted_site in self._trusted_sites:
            response = self._otds.addTrustedSite(trusted_site)
            if response:
                logger.info("Added OTDS trusted site -> %s", trusted_site)
            else:
                logger.error("Failed to add trusted site -> %s", trusted_site)
                success = False

        if success:
            self.writeStatusFile(section_name, self._trusted_sites)

        return success

        # end method definition

    def processSystemAttributes(self, section_name: str = "systemAttributes") -> bool:
        """Process OTDS system attributes in payload and create them in OTDS.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._system_attributes:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for system_attribute in self._system_attributes:
            # Check if there's a matching formal parameter defined on the Web Report node:
            if not system_attribute.get("name"):
                logger.error("OTDS System Attribute needs a name. Skipping...")
                success = False
                continue
            attribute_name = system_attribute["name"]

            if "enabled" in system_attribute and not system_attribute["enabled"]:
                logger.info(
                    "Payload for OTDS System Attribute -> %s is disabled. Skipping...",
                    attribute_name,
                )
                continue

            if not system_attribute.get("value"):
                logger.error("OTDS System Attribute needs a value. Skipping...")
                continue

            attribute_value = system_attribute["value"]
            attribute_description = system_attribute.get("description")
            response = self._otds.addSystemAttribute(
                attribute_name, attribute_value, attribute_description
            )
            if response:
                logger.info(
                    "Added OTDS system attribute -> %s with value -> %s",
                    attribute_name,
                    attribute_value,
                )
            else:
                logger.error(
                    "Failed to add OTDS system attribute -> %s with value -> %s",
                    attribute_name,
                    attribute_value,
                )
                success = False

        if success:
            self.writeStatusFile(section_name, self._system_attributes)

        return success

        # end method definition

    def processGroupPlaceholders(self):
        """For some adminSettings we may need to replace a placeholder (sourrounded by %%...%%)
        with the actual ID of the Extended ECM group. For this we prepare a lookup dict.
        The dict self._placeholder_values already includes lookups for the OTCS and OTAWP
        OTDS resource IDs (see main.py)
        """

        for group in self._groups:
            if not "name" in group:
                logger.error(
                    "Group needs a name for placeholder definition. Skipping..."
                )
                continue
            group_name = group["name"]
            # Check if group has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in group and not group["enabled"]:
                logger.info(
                    "Payload for Group -> %s is disabled. Skipping...", group_name
                )
                continue

            # Now we determine the ID. Either it is in the payload section from
            # the current customizer run or we try to look it up in the system.
            # The latter case may happen if the custiomuer pod got restarted.
            group_id = self.determineGroupID(group)
            if not group_id:
                logger.warning(
                    "Group needs an ID for placeholder definition. Skipping..."
                )
                continue

            # Add Group with its ID to the dict self._placeholder_values:
            self._placeholder_values[
                "OTCS_GROUP_ID_"
                + group_name.upper().replace(" & ", "_").replace(" ", "_")
            ] = str(group_id)

        logger.debug(
            "Placeholder values after group processing = %s", self._placeholder_values
        )

    def processUserPlaceholders(self):
        """For some adminSettings we may need to replace a placeholder (sourrounded by %%...%%)
        with the actual ID of the Extended ECM user. For this we prepare a lookup dict.
        The dict self._placeholder_values already includes lookups for the OTCS and OTAWP
        OTDS resource IDs (see main.py)
        """

        for user in self._users:
            if not "name" in user:
                logger.error(
                    "User needs a name for placeholder definition. Skipping..."
                )
                continue
            user_name = user["name"]
            # Check if group has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> %s is disabled. Skipping...", user_name
                )
                continue

            # Now we determine the ID. Either it is in the payload section from
            # the current customizer run or we try to look it up in the system.
            # The latter case may happen if the custiomuer pod got restarted.
            user_id = self.determineUserID(user)
            if not user_id:
                logger.warning(
                    "User needs an ID for placeholder definition. Skipping..."
                )
                continue

            # Add Group with its ID to the dict self._placeholder_values:
            self._placeholder_values["OTCS_USER_ID_%s", user_name.upper()] = str(
                user_id
            )

        logger.debug(
            "Placeholder values after user processing = %s", self._placeholder_values
        )

    def processGroups(self, section_name: str = "groups") -> bool:
        """Process groups in payload and create them in Extended ECM.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        Side Effects:
            the group items are modified by adding an "id" dict element that
            includes the technical ID of the group in Extended ECM
        """

        if not self._groups:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        # First run through groups: create all groups in payload
        # and store the IDs of the created groups:
        for group in self._groups:
            if not "name" in group:
                logger.error("Group needs a name. Skipping...")
                success = False
                continue
            group_name = group["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in group and not group["enabled"]:
                logger.info(
                    "Payload for Group -> %s is disabled. Skipping...", group_name
                )
                continue

            # Check if the group does already exist (e.g. if job is restarted)
            # as this is a pattern search it could return multiple groups:
            group_id = self.determineGroupID(group)
            if group_id:
                logger.info(
                    "Found existing group -> %s (%s) - skipping to next group...",
                    group_name,
                    group_id,
                )
                continue

            logger.info("Did not find an existing group - creating a new group...")

            # Now we know it is a new group...
            new_group = self._otcs.addGroup(group_name)
            if new_group is not None:
                logger.debug("New group -> %s", new_group)
                group["id"] = new_group["id"]
            else:
                logger.error("Failed to create group -> %s", new_group)
                success = False
                continue

        logger.debug("Groups = %s", self._groups)

        # Second run through groups: create all group memberships
        # (nested groups) based on the IDs created in first run:
        for group in self._groups:
            if not "id" in group:
                logger.error("Group -> %s does not have an ID.", group["name"])
                success = False
                continue
            parent_group_names = group["parent_groups"]
            for parent_group_name in parent_group_names:
                # First, try to find parent group in payload by parent group name:
                parent_group = next(
                    (
                        item
                        for item in self._groups
                        if item["name"] == parent_group_name
                    ),
                    None,
                )
                if parent_group is None:
                    # If this didn't work, try to get the parent group from OTCS. This covers
                    # cases where the parent group is system generated or part
                    # of a former payload processing:
                    parent_group = self._otcs.getGroup(parent_group_name)
                    if not parent_group:
                        logger.error(
                            "Parent Group -> %s not found. Skipping...",
                            parent_group_name,
                        )
                        success = False
                        continue
                    parent_group = parent_group["data"][0]
                elif not "id" in parent_group:
                    logger.error(
                        "Parent Group -> %s does not have an ID. Skipping...",
                        parent_group["name"],
                    )
                    success = False
                    continue

                # retrieve all members of the parent group (1 = get only groups)
                members = self._otcs.getGroupMembers(parent_group["id"], 1)
                if self._otcs.existResultItem(members, "id", group["id"]):
                    #                if existing_member:
                    logger.info(
                        "Group -> %s (%s) is already a member of parent group -> %s (%s) - skipping to next parent group...",
                        group["name"],
                        group["id"],
                        parent_group["name"],
                        parent_group["id"],
                    )
                else:
                    logger.info(
                        "Add group -> %s (%s) to parent group -> %s (%s)",
                        group["name"],
                        group["id"],
                        parent_group["name"],
                        parent_group["id"],
                    )
                    self._otcs.addGroupMember(group["id"], parent_group["id"])

        if success:
            self.writeStatusFile(section_name, self._groups)

        return success

        # end method definition

    def processGroupsM365(self, section_name: str = "groupsM365") -> bool:
        """Process groups in payload and create them in Microsoft 365.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """
        if not isinstance(self._m365, M365):
            logger.error(
                "Office 365 connection not setup properly -> Skipping %s...",
                section_name,
            )
            return False

        if not self._groups:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        # First run through groups: create all groups in payload
        # and store the IDs of the created groups:
        for group in self._groups:
            if not "name" in group:
                logger.error("Group needs a name. Skipping...")
                success = False
                continue
            group_name = group["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in group and not group["enabled"]:
                logger.info(
                    "Payload for Group -> %s is disabled. Skipping...", group_name
                )
                continue
            if not "enable_o365" in group or not group["enable_o365"]:
                logger.info(
                    "Office 365 is not enabled in payload for Group -> %s. Skipping...",
                    group_name,
                )
                continue

            # Check if the group does already exist (e.g. if job is restarted)
            # as this is a pattern search it could return multiple groups:
            existing_groups = self._m365.getGroup(group_name)

            if existing_groups and existing_groups["value"]:
                logger.debug(
                    "Found existing Microsoft 365 groups -> %s",
                    existing_groups["value"],
                )
                # Get list of all matching groups:
                existing_groups_list = existing_groups["value"]
                # Find the group with the exact match of the name:
                existing_group = next(
                    (
                        item
                        for item in existing_groups_list
                        if item["displayName"] == group_name
                    ),
                    None,
                )
                # Have we found an exact match?
                if existing_group is not None:
                    logger.info(
                        "Found existing Microsoft 365 group -> %s (%s) - skip creation of group...",
                        existing_group["displayName"],
                        existing_group["id"],
                    )
                    group["m365_id"] = existing_group["id"]
                    continue
                logger.info(
                    "Did not find an exact match for the group - creating a new Microsoft 365 group..."
                )
            else:
                logger.info(
                    "Did not find any matching group - creating a new Microsoft 365 group..."
                )

            # Now we know it is a new group...
            new_group = self._m365.addGroup(group_name)
            if new_group is not None:
                # Store the Microsoft 365 group ID in payload:
                group["m365_id"] = new_group["id"]
                logger.info(
                    "New Microsoft 365 group -> %s with ID -> %s has been created",
                    group_name,
                    group["m365_id"],
                )
            else:
                success = False

        if success:
            self.writeStatusFile(section_name, self._groups)

        return success

        # end method definition

    def processUsers(self, section_name: str = "users") -> bool:
        """Process users in payload and create them in Extended ECM.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        Side Effects:
            the user items are modified by adding an "id" dict element that
            includes the technical ID of the user in Extended ECM
        """

        if not self._users:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        # Add all users in payload and establish membership in
        # specified groups:
        for user in self._users:
            # Sanity checks:
            if not "name" in user:
                logger.error("User is missing a login - skipping to next user...")
                success = False
                continue
            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> %s is disabled. Skipping...", user_name
                )
                continue

            # Sanity checks:
            if not "password" in user:
                logger.error(
                    "User -> %s is missing a password - skipping to next user...",
                    user_name,
                )
                success = False
                continue

            # Sanity checks:
            if not "base_group" in user:
                logger.warning(
                    "User -> %s is missing a base group - setting to default group",
                    user_name,
                )
                user["base_group"] = "DefaultGroup"

            # Check if the user does already exist (e.g. if job is restarted)
            # determineUserID() also writes back the user ID into the payload
            # if it has gathered it from OTCS.
            user_id = self.determineUserID(user)
            if user_id:
                logger.info(
                    "Found existing user -> %s (%s) - skipping to next user...",
                    user_name,
                    user_id,
                )
                continue
            logger.info("Did not find an existing user - creating a new user...")

            # Find the base group of the user. Assume 'Default Group' (= 1001) if not found:
            base_group = next(
                (
                    item["id"]
                    for item in self._groups
                    if item["name"] == user["base_group"] and item.get("id")
                ),
                1001,
            )

            # Now we know it is a new user...
            new_user = self._otcs.addUser(
                name=user_name,
                password=user["password"],
                # be careful - can be empty
                first_name=user.get("firstname", ""),
                # be careful - can be empty
                last_name=user.get("lastname", ""),
                email=user.get("email", ""),  # be careful - can be empty
                base_group=base_group,
                privileges=user.get("privileges", ["Login", "Public Access"]),
            )

            # Process group memberships of new user:
            if new_user is not None:
                logger.info(
                    "New user -> %s with ID -> %s has been created",
                    user_name,
                    new_user["id"],
                )
                user["id"] = new_user["id"]
                group_names = user["groups"]
                for group_name in group_names:
                    # Find the group dictionary item to the parent group name:
                    group = next(
                        (item for item in self._groups if item["name"] == group_name),
                        None,
                    )
                    if group is None:
                        # if group is not in payload try to find group in OTCS
                        # in case it is a pre-existing group:
                        group = self._otcs.getGroup(group_name)
                        if group is None:
                            logger.error(
                                "Group -> %s not found. Skipping...", group_name
                            )
                            success = False
                            continue
                        group = group["data"][0]

                    if group["id"] is None:
                        logger.error(
                            "Group -> %s does not have an ID. Skipping...",
                            group["name"],
                        )
                        success = False
                        continue

                    logger.info(
                        "Add user -> %s (%s) to group -> %s (%s)",
                        user["name"],
                        user["id"],
                        group["name"],
                        group["id"],
                    )
                    response = self._otcs.addGroupMember(user["id"], group["id"])
                    if not response:
                        success = False
                # for some unclear reason the user is not added to its base group in OTDS
                # so we do this explicitly:
                response = self._otds.addUserToGroup(user["name"], user["base_group"])
                if not response:
                    success = False

                # Extra OTDS attributes for the user can be provided in "extra_attributes"
                # as part of the user payload.
                if "extra_attributes" in user:
                    extra_attributes = user["extra_attributes"]
                    for extra_attribute in extra_attributes:
                        attribute_name = extra_attribute.get("name")
                        attribute_value = extra_attribute.get("value")
                        if not attribute_name or not attribute_value:
                            logger.error(
                                "User attribute is missing a name or value. Skipping..."
                            )
                            success = False
                            continue
                        logger.info(
                            "Set user attribute -> %s to -> %s",
                            attribute_name,
                            attribute_value,
                        )
                        user_partition = self._otcs.config()["partition"]
                        if not user_partition:
                            logger.error("User partition not found!")
                            success = False
                            continue
                        self._otds.updateUser(
                            user_partition,
                            user["name"],
                            attribute_name,
                            attribute_value,
                        )

        if success:
            self.writeStatusFile(section_name, self._users)

        return success

        # end method definition

    def processUsersM365(self, section_name: str = "usersM365") -> bool:
        """Process users in payload and create them in Microsoft 365 via MS Graph API.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not isinstance(self._m365, M365):
            logger.error(
                "Office 365 connection not setup properly -> Skipping %s...",
                section_name,
            )
            return False

        if not self._users:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        # Add all users in payload and establish membership in
        # specified groups:
        for user in self._users:
            # Sanity checks:
            if not "name" in user:
                logger.error("User is missing a login - skipping to next user...")
                success = False
                continue
            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> %s is disabled. Skipping...", user_name
                )
                continue
            if not "enable_o365" in user or not user["enable_o365"]:
                logger.info(
                    "Office 365 is not enabled in payload for User -> %s. Skipping...",
                    user_name,
                )
                continue

            # Sanity checks:
            if not "password" in user:
                logger.error(
                    "User -> %s is missing a password - skipping to next user...",
                    user_name,
                )
                success = False
                continue
            user_password = user["password"]
            # be careful with the following fields - they could be empty
            user_department = user.get("base_group", "")
            user_first_name = user.get("firstname", "")
            user_last_name = user.get("lastname", "")
            user_location = user.get("location", "US")

            # Check if the user does already exist (e.g. if job is restarted)
            # As this is a pattern search it could return multiple users:
            user_name = user_name + "@" + self._m365.config()["domain"]
            existing_user = self._m365.getUser(user_name)
            if existing_user:
                logger.info(
                    "Found existing Microsoft 365 user -> %s (%s) with ID -> %s",
                    existing_user["displayName"],
                    existing_user["userPrincipalName"],
                    existing_user["id"],
                )
                user["m365_id"] = existing_user["id"]
            else:
                logger.info(
                    "Did not find existing user - creating a new Microsoft 365 user..."
                )

                # Now we know it is a new user...
                new_user = self._m365.addUser(
                    email=user_name,
                    password=user_password,
                    first_name=user_first_name,
                    last_name=user_last_name,
                    location=user_location,
                    department=user_department,
                )
                if new_user is not None:
                    # Store the Microsoft 365 user ID in payload:
                    user["m365_id"] = new_user["id"]
                    logger.info(
                        "New Microsoft 365 user -> %s with ID -> %s has been created",
                        user_name,
                        user["m365_id"],
                    )
                else:
                    logger.error(
                        "Failed to create new Microsoft 365 user -> %s. Skipping.",
                        user_name,
                    )
                    success = False
                    continue

            # Now we assign a license to the new M365 user.
            # First we see if there's a M365 SKU list in user
            # payload - if not we wrap the default SKU configured
            # for the m365 object into a single item list:
            existing_user_licenses = self._m365.getUserLicenses(user["m365_id"])
            sku_list = user.get("m365_skus", [self._m365.config()["skuId"]])
            for sku_id in sku_list:
                # Check if the M365 user already has this license:
                if not self._m365.existResultItem(
                    existing_user_licenses, "skuId", sku_id
                ):
                    response = self._m365.assignLicenseToUser(user["m365_id"], sku_id)
                    if not response:
                        logger.error(
                            "Failed to assign license -> %s to Microsoft 365 user -> %s",
                            sku_id,
                            user_name,
                        )
                        success = False
                    else:
                        if (
                            not "m365_skus" in user
                        ):  # this is only True if the default license from the m365 object is taken
                            user["m365_skus"] = [sku_id]
                        logger.info(
                            "License -> %s has been assigned to Microsoft 365 user -> %s",
                            sku_id,
                            user_name,
                        )
                else:
                    logger.info(
                        "Microsoft 365 user -> %s already has the license -> %s",
                        user_name,
                        sku_id,
                    )

            # Now we assign the Extended ECM Teams App to the new M365 user.
            # First we check if the app is already assigned to the user.
            # If not we install / assign the app. If the user already has
            # the Extended ECM app we try to uprade it:
            app_name = self._m365.config()["teamsAppName"]
            response = self._m365.getTeamsAppsOfUser(
                user["m365_id"],
                f"contains(teamsAppDefinition/displayName, '{app_name}')",
            )
            if self._m365.existResultItem(
                response, "displayName", app_name, sub_dict_name="teamsAppDefinition"
            ):
                logger.info(
                    "Upgrade MS Teams app -> %s for user -> %s", app_name, user_name
                )
                response = self._m365.upgradeTeamsAppOfUser(user["m365_id"], app_name)
            else:
                logger.info(
                    "Install MS Teams app -> %s for user -> %s", app_name, user_name
                )
                response = self._m365.assignTeamsAppToUser(user["m365_id"], app_name)

            # Process Microsoft 365 group memberships of new user:
            if "m365_id" in user:
                user_id = user["m365_id"]
                # don't forget the base group (department) !
                group_names = user["groups"]
                if user_department:
                    group_names.append(user_department)
                logger.info(
                    "User -> %s has these groups in payload -> %s (including base group -> %s). Checking if they are Microsoft 365 Groups...",
                    user_name,
                    group_names,
                    user_department,
                )
                # Go through all group names:
                for group_name in group_names:
                    # Find the group payload item to the parent group name:
                    group = next(
                        (item for item in self._groups if item["name"] == group_name),
                        None,
                    )
                    if not group:
                        # if group is not in payload then this membership
                        # is not relevant for Microsoft 365. This could be system generated
                        # groups like "PageEdit" or "Business Administrators".
                        # In this case we do "continue" as we can't process parent groups
                        # either:
                        logger.info(
                            "No payload found for Group -> %s. Skipping...", group_name
                        )
                        continue
                    elif not "enable_o365" in group or not group["enable_o365"]:
                        # If Microsoft 365 is not enabled for this group in
                        # the payload we don't create a M365 but we do NOT continue
                        # as there may still be parent groups that are M365 enabled
                        # we want to put the user in (see below):
                        logger.info(
                            "Payload Group -> %s is not enabled for M365.", group_name
                        )
                    else:
                        response = self._m365.getGroup(group_name)
                        if (
                            response is None
                            or not "value" in response
                            or not response["value"]
                        ):
                            logger.error(
                                "Microsoft 365 Group -> %s not found. Skipping...",
                                group_name,
                            )
                            success = False
                        else:
                            group_id = response["value"][0]["id"]

                            # Check if user is already a member. We don't want
                            # to throw an error if the user is not found as a member:
                            if self._m365.isMember(group_id, user_id, show_error=False):
                                logger.info(
                                    "Microsoft 365 user -> %s (%s) is already in Microsoft 365 group -> %s (%s)",
                                    user["name"],
                                    user_id,
                                    group_name,
                                    group_id,
                                )
                            else:
                                logger.info(
                                    "Add Microsoft 365 user -> %s (%s) to Microsoft 365 group -> %s (%s)",
                                    user["name"],
                                    user_id,
                                    group_name,
                                    group_id,
                                )
                                self._m365.addGroupMember(group_id, user_id)
                                # As each group should have at least one owner in M365
                                # we set all users also as owners for now. Later we
                                # may want to configure this via payload:
                                logger.info(
                                    "Make Microsoft 365 user -> %s (%s) owner of Microsoft 365 group -> %s (%s)",
                                    user["name"],
                                    user_id,
                                    group_name,
                                    group_id,
                                )
                                self._m365.addGroupOwner(group_id, user_id)

                    # As M365 groups are flat (not nested) we also add the
                    # user as member to the parent groups of the current group
                    # if the parent group is enabled for M365:
                    parent_group_names = group.get("parent_groups")
                    logger.info(
                        "Group -> %s has the following parent groups -> %s",
                        group_name,
                        parent_group_names,
                    )
                    for parent_group_name in parent_group_names:
                        # Find the group dictionary item to the parent group name:
                        parent_group = next(
                            (
                                item
                                for item in self._groups
                                if item["name"] == parent_group_name
                            ),
                            None,
                        )
                        if (
                            parent_group is None
                            or not "enable_o365" in parent_group
                            or not parent_group["enable_o365"]
                        ):
                            # if parent group is not in payload then this membership
                            # is not relevant for Microsoft 365.
                            # If Office 365 is not enabled for this parent group in
                            # the payload we can also skip:
                            logger.info(
                                "Parent Group -> %s is not enabled for M365. Skipping...",
                                group_name,
                            )
                            continue

                        response = self._m365.getGroup(parent_group_name)
                        if (
                            response is None
                            or not "value" in response
                            or not response["value"]
                        ):
                            logger.error(
                                "Microsoft 365 Group -> %s not found. Skipping...",
                                group_name,
                            )
                            success = False
                            continue
                        parent_group_id = response["value"][0]["id"]

                        # Check if user is already a member. We don't want
                        # to throw an error if the user is not found as a member:
                        if self._m365.isMember(
                            parent_group_id, user_id, show_error=False
                        ):
                            logger.info(
                                "Microsoft 365 user -> %s (%s) is already in Microsoft 365 group -> %s (%s)",
                                user["name"],
                                user_id,
                                parent_group_name,
                                parent_group_id,
                            )
                            continue

                        logger.info(
                            "Add Microsoft 365 user -> %s (%s) to Microsoft 365 group -> %s (%s)",
                            user["name"],
                            user_id,
                            parent_group_name,
                            parent_group_id,
                        )
                        self._m365.addGroupMember(parent_group_id, user_id)

        if success:
            self.writeStatusFile(section_name, self._users)

        return success

        # end method definition

    def processTeamsM365(self, section_name: str = "teamsM365") -> bool:
        """Process groups in payload and create matching Teams in Microsoft 365.
           We need to do this after the creation of the M365 users as wie require
           Group Owners to create teams.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not isinstance(self._m365, M365):
            logger.error(
                "Office 365 connection not setup properly -> Skipping %s...",
                section_name,
            )
            return False

        if not self._groups:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for group in self._groups:
            if not "name" in group:
                logger.error("Team needs a name. Skipping...")
                success = False
                continue
            group_name = group["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in group and not group["enabled"]:
                logger.info(
                    "Payload for Group -> %s is disabled. Skipping...", group_name
                )
                continue
            if not "enable_o365" in group or not group["enable_o365"]:
                logger.info(
                    "Office 365 is not enabled in payload for Group -> %s. Skipping...",
                    group_name,
                )
                continue

            # Check if the M365 group does not exist (this should actually never happen at this point)
            if not "m365_id" in group:
                # The "m365_id" value is set by the method processGroupsM365()
                logger.error(
                    "No M365 Group exist for group -> %s (M365 Group creation may have failed). Skipping...",
                    group_name,
                )
                success = False
                continue

            if not self._m365.hasTeam(group_name):
                logger.info(
                    "Create M365 Team -> %s for existing M365 Group -> %s...",
                    group_name,
                    group_name,
                )
                # Now "upgrading" this group to a MS Team:
                new_team = self._m365.addTeam(group_name)
                if not new_team:
                    success = False
            else:
                logger.info(
                    "M365 group -> %s already has an MS Team connected. Skipping...",
                    group_name,
                )

        if success:
            self.writeStatusFile(section_name, self._groups)

        return success

        # end method definition

    def cleanupStaleTeamsM365(self, workspace_types: list):
        """Delete Microsoft Teams that are left-overs from former deployments.
           This method is currently not used.

        Args:
            workspace_types (list): list of all workspace types
        """

        if not isinstance(self._m365, M365):
            logger.error(
                "Office 365 connection not setup properly -> Skipping %s...",
                workspace_types,
            )
            return False

        if workspace_types == []:
            logger.error("Empty workspace type list!")
            return

        for workspace_type in workspace_types:
            if not "name" in workspace_type:
                logger.error(
                    "Workspace type -> %s does not have a name. Skipping...",
                    workspace_type,
                )
                continue
            response = self._otcs.getWorkspaceInstances(workspace_type["name"])
            workspace_instances = response["results"]
            if not workspace_instances:
                logger.info(
                    "Workspace type -> %s does not have any instances!",
                    workspace_type["name"],
                )
                continue
            for workspace_instance in workspace_instances:
                workspace_name = workspace_instance["data"]["properties"]["name"]
                logger.info(
                    "Check if stale Microsoft 365 Teams with name -> %s exist...",
                    workspace_name,
                )
                response = self._m365.deleteTeams(workspace_name)

        # end method definition

    def cleanupAllTeamsM365(self, section_name: str = "teamsM365Cleanup") -> bool:
        """Delete Microsoft Teams that are left-overs from former deployments

        Args:
            None
        Returns:
            bool: True if teams have been deleted, False otherwise
        """

        if not isinstance(self._m365, M365):
            logger.error(
                "Office 365 connection not setup properly -> Skipping %s...",
                section_name,
            )
            return False

        # We want this cleanup to only run once even if we have
        # multiple payload files - so we pass payload_specific=False here:
        if self.checkStatusFile(
            payload_section_name=section_name, payload_specific=False
        ):
            logger.info(
                "Payload section -> %s has been processed successfully before. Skip cleanup of M365 teams...",
                section_name,
            )
            return True

        logger.info("Processing payload section -> %s...", section_name)

        # We don't want to delete MS Teams that are matching the regular OTCS Group Names (like "Sales")
        exception_list = self.getAllGroupNames()

        # These are the patterns that each MS Teams needs to match at least one of to be deleted
        # Pattern 1: all MS teams with a name that has a number in brackets, line "(1234)"
        # Pattern 2: all MS Teams with a name that starts with a number followed by a space,
        #            followed by a "- and followed by another space
        # Pattern 3: all MS Teams with a name that starts with "WS" and a 1-4 digit number
        #            (these are the workspaces for Purchase Contracts generated for Intelligent Filing)
        # Pattern 4: all MS Teams with a name that ends with a 1-2 character + a number in brackets, like (US-1000)
        #            this is a specialization of pattern 1
        pattern_list = [
            r"\(\d+\)",
            r"\d+\s-\s",
            r"^WS\d{1,4}$",
            r"^.+?\s\(.{1,2}-\d+\)$",
        ]

        result = self._m365.deleteAllTeams(exception_list, pattern_list)

        # We want this cleanup to only run once even if we have
        # multiple payload files - so we pass payload_specific=False here:
        self.writeStatusFile(
            payload_section_name=section_name,
            payload_section=exception_list + pattern_list,
            payload_specific=False,
        )

        return result

        # end method definition

    def processAdminSettings(
        self, admin_settings: list, section_name: str = "adminSettings"
    ) -> bool:
        """Process admin settings in payload and import them to Extended ECM.

        Args:
            admin_settings (list): list of admin settings. We need this parameter
                                   as we process two different lists.
        Returns:
            bool: True if a restart of the OTCS pods is required. False otherwise.
        """

        if not admin_settings:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        restart_required: bool = False
        success: bool = True

        for admin_setting in admin_settings:
            # Sanity checks:
            if not "filename" in admin_setting:
                logger.error("Filename is missing - skipping to next admin setting...")
                continue
            filename = admin_setting["filename"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in admin_setting and not admin_setting["enabled"]:
                logger.info(
                    "Payload for setting file -> %s is disabled. Skipping...", filename
                )
                continue

            settings_file = self._custom_settings_dir + filename
            if os.path.exists(settings_file):
                description = admin_setting.get("description")
                if description:
                    logger.info(description)

                # Read the config file:
                with open(settings_file, "r", encoding="utf-8") as file:
                    file_content = file.read()

                logger.debug(
                    "Replace Placeholder -> %s in file -> %s",
                    self._placeholder_values,
                    file_content,
                )

                file_content = self.replacePlaceholders(file_content)

                # Write the updated config file:
                tmpfile = "/tmp/" + os.path.basename(settings_file)
                with open(tmpfile, "w", encoding="utf-8") as file:
                    file.write(file_content)

                response = self._otcs.applyConfig(tmpfile)
                if response and response["results"]["data"]["restart"]:
                    logger.info("A restart of Extended ECM service is required.")
                    restart_required = True
            else:
                logger.error("Admin settings file -> %s not found.", settings_file)
                success = False

        if success:
            self.writeStatusFile(section_name, admin_settings)

        return restart_required

        # end method definition

    def processExternalSystems(self, section_name: str = "externalSystems") -> bool:
        """Process external systems in payload and create them in Extended ECM.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        Side Effects:
            - based on system_type different other settings in the dict are set
            - reachability is tested and a flag is set in the dict are set
        """

        if not self._external_systems:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for external_system in self._external_systems:
            #
            # 1: Do sanity checks for the payload:
            #
            if not "external_system_name" in external_system:
                logger.error(
                    "External System connection needs a logical system name! Skipping to next external system..."
                )
                success = False
                continue
            system_name = external_system["external_system_name"]

            if not "external_system_type" in external_system:
                logger.error(
                    "External System connection -> %s needs a type (SAP, Salesfoce, SuccessFactors, AppWorks Platform)! Skipping to next external system...",
                    system_name,
                )
                success = False
                continue
            system_type = external_system["external_system_type"]

            if "enabled" in external_system and not external_system["enabled"]:
                logger.info(
                    "Payload for External System -> %s (%s) is disabled. Skipping...",
                    system_name,
                    system_type,
                )
                continue

            description = (
                external_system["description"]
                if external_system.get("description")
                else ""
            )

            # Possible Connection Types for external systems:
            # "Business Scenario Sample" (Business Scenarios Sample Adapter)
            # "ot.sap.c4c.SpiAdapter" (SAP C4C SPI Adapter)
            # "ot.sap.c4c.SpiAdapterV2" (C4C SPI Adapter V2)
            # "HTTP" (Default WebService Adapter)
            # "ot.sap.S4HANAAdapter" (S/4HANA SPI Adapter)
            # "SF" (SalesForce Adapter)
            # "SFInstance" (SFWebService)

            # Set the default settings for the different system types:
            match system_type:
                # Check if we have a SuccessFactors system:
                case "SuccessFactors":
                    connection_type = "SFInstance"
                    auth_method = "OAUTH"
                    provider_name = system_type
                    username = None
                    password = None
                case "SAP":
                    connection_type = "HTTP"
                    auth_method = "BASIC"
                    provider_name = ""
                    oauth_client_id = None
                    oauth_client_secret = None
                case "Salesforce":
                    connection_type = "SF"
                    auth_method = "OAUTH"
                    provider_name = system_type
                    username = None
                    password = None
                case "AppWorks Platform":
                    connection_type = "HTTP"
                    auth_method = "BASIC"
                    provider_name = ""
                    oauth_client_id = None
                    oauth_client_secret = None
                case _:
                    logger.error("Unsupported system_type defined -> %s", system_type)
                    return False

            if not "base_url" in external_system:
                base_url = ""  # baseUrl is optional
            else:
                base_url = external_system["base_url"]

            if not "as_url" in external_system:
                logger.warning(
                    "External System connection -> %s needs an Application Server URL! Skipping to next external system...",
                    system_name,
                )
                success = False
                continue
            as_url = external_system["as_url"]

            # Extract the hostname:
            external_system_hostname = urlparse(as_url).hostname
            # Write this information back into the data structure:
            external_system["external_system_hostname"] = external_system_hostname
            # Extract the port:
            external_system_port = (
                urlparse(as_url).port if urlparse(as_url).port else 80
            )
            # Write this information back into the data structure:
            external_system["external_system_port"] = external_system_port

            if self._http_object.checkHostReachable(
                external_system_hostname, external_system_port
            ):
                logger.info(
                    "Mark external system -> %s as reachable for later workspace creation...",
                    system_name,
                )
                external_system["reachable"] = True
            else:
                external_system["reachable"] = False

            # Read either username/password (BASIC) or client ID / secret (OAuth)
            match auth_method:
                case "BASIC":
                    if not "username" in external_system:
                        logger.warning(
                            "External System connection -> %s needs a user name for BASIC authentication! Skipping to next external system...",
                            system_name,
                        )
                        continue
                    if not "password" in external_system:
                        logger.warning(
                            "External System connection -> %s needs a password for BASIC authentication! Skipping to next external system...",
                            system_name,
                        )
                        continue
                    username = external_system["username"]
                    password = external_system["password"]
                    oauth_client_id = ""
                    oauth_client_secret = ""

                case "OAUTH":
                    if not "oauth_client_id" in external_system:
                        logger.error(
                            "External System connection -> %s is missing OAuth client ID! Skipping to next external system...",
                            system_name,
                        )
                        success = False
                        continue
                    if not "oauth_client_secret" in external_system:
                        logger.error(
                            "External System connection -> %s is missing OAuth client secret! Skipping to next external system...",
                            system_name,
                        )
                        success = False
                        continue
                    oauth_client_id = external_system["oauth_client_id"]
                    oauth_client_secret = external_system["oauth_client_secret"]
                    # For backward compatibility we also read username/password
                    # with OAuth settings:
                    username = (
                        external_system["username"]
                        if external_system.get("username")
                        else None
                    )
                    password = (
                        external_system["password"]
                        if external_system.get("password")
                        else None
                    )
                case _:
                    logger.error(
                        "Unsupported authmethod specified (%s) , Skipping ... ",
                        auth_method,
                    )
                    return False

            # We do this existance test late in this function to make sure the payload
            # datastructure is properly updated for debugging purposes.
            logger.info(
                "Test if external system -> %s does already exist...", system_name
            )
            if self._otcs.getExternalSystemConnection(system_name):
                logger.info(
                    "External System connection -> %s already exists! Skipping to next external system...",
                    system_name,
                )
                continue

            #
            # 2: Create External System:
            #
            logger.info(
                "Create external system -> %s; type -> %s", system_name, connection_type
            )
            response = self._otcs.addExternalSystemConnection(
                system_name,
                connection_type,
                as_url,
                base_url,
                str(username),
                str(password),
                auth_method,
                oauth_client_id,
                oauth_client_secret,
            )
            if response is None:
                logger.error(
                    "Failed to create external system -> %s; type -> %s",
                    system_name,
                    connection_type,
                )
                success = False
            else:
                logger.info("Successfully created external system -> %s", system_name)

            #
            # 3: Create Authentication Handler for external system:
            #

            match system_type:
                case "SuccessFactors":
                    # Configure a SAML authentication handler:
                    if not "saml_url" in external_system:
                        logger.error(
                            "SuccessFactors system -> %s (%s) is missing the SAML URL!",
                            system_name,
                            connection_type,
                        )
                        success = False
                        continue
                    saml_url = external_system["saml_url"]
                    if not "otds_sp_endpoint" in external_system:
                        logger.error(
                            "SuccessFactors system -> %s (%s) is missing the OTDS endpoint!",
                            system_name,
                            connection_type,
                        )
                        success = False
                        continue
                    otds_sp_endpoint = external_system["otds_sp_endpoint"]

                    response = self._otds.addAuthHandlerSAML(
                        name=system_name,
                        description=description,
                        provider_name=provider_name,
                        saml_url=saml_url,
                        otds_url=otds_sp_endpoint,
                    )
                    if response:
                        logger.info("Successfully added SAML authentication handler.")
                    else:
                        logger.error("Failed to add SAML authentication handler.")
                        success = False
                case "SAP":
                    # Configure a certificate-based SAP authentication handler:
                    if not "certificate_file" in external_system:
                        logger.error(
                            "External system -> %s; type -> %s; is missing the certificate file!",
                            system_name,
                            system_type,
                        )
                        continue
                    if not "certificate_password" in external_system:
                        logger.error(
                            "External system -> %s; type -> %s; has a certificate file -> %s but it is missing the certificate password!",
                            system_name,
                            connection_type,
                            external_system["certificate_file"],
                        )
                        success = False
                        continue
                    certificate_file = external_system["certificate_file"]
                    certificate_password = external_system["certificate_password"]
                    certificate_description = external_system["description"]
                    response = self._otds.addAuthHandlerSAP(
                        name=system_name,
                        description=certificate_description,
                        certificate_file=certificate_file,
                        certificate_password=certificate_password,
                    )
                    if response:
                        logger.info("Successfully added SAP authentication handler.")
                    else:
                        logger.error("Failed to add SAP authentication handler.")
                        success = False
                    # Upload and enable certificate file for Archive Center that is required for SAP scenarios
                    # we only do this if the necessary information is in payload and if OTAC is enabled:
                    if (
                        "archive_logical_name" in external_system
                        and "archive_certificate_file" in external_system
                        and self._otac
                    ):
                        logger.info(
                            "Put certificate file -> %s for logical archive -> %s into Archive Center",
                            external_system["archive_certificate_file"],
                            external_system["archive_logical_name"],
                        )
                        response = self._otac.putCert(
                            external_system["external_system_name"],
                            external_system["archive_logical_name"],
                            external_system["archive_certificate_file"],
                        )
                        logger.info(
                            "Enable certificate file -> %s for logical archive -> %s",
                            external_system["archive_certificate_file"],
                            external_system["archive_logical_name"],
                        )
                        response = self._otac.enableCert(
                            external_system["external_system_name"],
                            external_system["archive_logical_name"],
                            True,
                        )
                case "Salesforce":
                    # Configure an OAuth-based authentication handler:
                    if not "authorization_endpoint" in external_system:
                        logger.error(
                            "Salesforce system -> %s (%s) is missing the authorization endpoint!",
                            system_name,
                            connection_type,
                        )
                        success = False
                        continue
                    authorization_endpoint = external_system["authorization_endpoint"]
                    if not "token_endpoint" in external_system:
                        logger.error(
                            "Salesforce system -> %s (%s) is missing the token endpoint!",
                            system_name,
                            connection_type,
                        )
                        success = False
                        continue
                    token_endpoint = external_system["token_endpoint"]
                    response = self._otds.addAuthHandlerOAuth(
                        name=system_name,
                        description=description,
                        provider_name=provider_name,
                        client_id=oauth_client_id,
                        client_secret=oauth_client_secret,
                        active_by_default=False,
                        authorization_endpoint=authorization_endpoint,
                        token_endpoint=token_endpoint,
                        scope_string="id",
                    )
                    if response:
                        logger.info("Successfully added OAuth authentication handler.")
                    else:
                        success = False
                        logger.error("Failed to add OAuth authentication handler.")

        if success:
            self.writeStatusFile(section_name, self._external_systems)

        return success

        # end method definition

    def processTransportPackages(
        self, transport_packages: list, section_name: str = "transportPackages"
    ) -> bool:
        """Process transport packages in payload and import them to Extended ECM.

        Args:
            transport_packages (list): list of transport packages. As we
                                       have three different lists (transport,
                                       content_transport, transport_post) so
                                       we need a parameter
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not transport_packages:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for transport_package in transport_packages:
            if not "name" in transport_package:
                logger.error(
                    "Transport Package needs a name! Skipping to next transport..."
                )
                success = False
                continue
            name = transport_package["name"]

            if "enabled" in transport_package and not transport_package["enabled"]:
                logger.info(
                    "Payload for Transport Package -> %s is disabled. Skipping...", name
                )
                continue

            if not "url" in transport_package:
                logger.error(
                    "Transport Package -> %s needs a URL! Skipping to next transport...",
                    name,
                )
                success = False
                continue
            if not "description" in transport_package:
                logger.warning("Transport Package -> %s is missing a description", name)
            url = transport_package["url"]
            description = transport_package["description"]

            # For some transports there can be string replacements
            # configured:
            if "replacements" in transport_package:
                replacements = transport_package["replacements"]
                logger.info(
                    "Deploy transport -> %s with replacements -> %s; URL -> %s",
                    description,
                    url,
                    replacements,
                )
                response = self._otcs.deployTransport(
                    url, name, description, replacements
                )
            else:
                logger.info("Deploy transport -> %s; URL -> %s", description, url)
                response = self._otcs.deployTransport(url, name, description)
            if response is None:
                logger.error("Failed to deploy transport -> %s; URL -> %s", name, url)
                success = False
                if self._stop_on_error:
                    break
            else:
                logger.info("Successfully deployed transport -> %s", name)

        if success:
            self.writeStatusFile(section_name, transport_packages)

        return success

        # end method definition

    def processUserPhotos(self, section_name: str = "userPhotos") -> bool:
        """Process user photos in payload and assign them to Extended ECM users.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._users:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        # we assume the nickname of the photo item equals the login name of the user
        # we also assume that the photos have been uploaded / transported into the target system
        for user in self._users:
            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> %s is disabled. Skipping...", user_name
                )
                continue

            if not "id" in user:
                logger.error(
                    "User -> %s does not have an ID. The user creation may have failed before. Skipping...",
                    user_name,
                )
                success = False
                continue

            user_id = user["id"]

            response = self._otcs.getNodeFromNickname(user_name)
            if response is None:
                logger.warning(
                    "Missing photo for user -> %s - nickname not found. Skipping...",
                    user_name,
                )
                continue
            photo_id = self._otcs.getResultValue(response, "id")
            response = self._otcs.updateUserPhoto(user_id, photo_id)
            if not response:
                logger.error("Failed to add photo for user -> %s", user_name)
                success = False
            else:
                logger.info("Successfully added photo for user -> %s", user_name)

        # Check if Admin has a photo as well (nickname needs to be "admin"):
        response = self._otcs.getNodeFromNickname("admin")
        if response is None:
            logger.warning("Missing photo for admin - nickname not found. Skipping...")
        else:
            photo_id = self._otcs.getResultValue(response, "id")
            response = self._otcs.updateUserPhoto(1000, photo_id)
            if response is None:
                logger.warning("Failed to add photo for admin")
            else:
                logger.info("Successfully added photo for admin")

        if success:
            self.writeStatusFile(section_name, self._users)

        return success

        # end method definition

    def processUserPhotosM365(self, section_name: str = "userPhotosM365") -> bool:
        """Process user photos in payload and assign them to Microsoft 365 users.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not isinstance(self._m365, M365):
            logger.error(
                "Office 365 connection not setup properly -> Skipping %s...",
                section_name,
            )
            return False

        if not self._users:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        # we assume the nickname of the photo item equals the login name of the user
        # we also assume that the photos have been uploaded / transported into the target system
        for user in self._users:
            user_name = user["name"]
            if not "id" in user:
                logger.error(
                    "User -> %s does not have an ID. The user creation may have failed before. Skipping...",
                    user_name,
                )
                success = False
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> %s is disabled. Skipping...", user_name
                )
                continue
            if not "enable_o365" in user or not user["enable_o365"]:
                logger.info(
                    "Office 365 is not enabled in payload for User -> %s. Skipping...",
                    user_name,
                )
                continue
            if not "m365_id" in user:
                logger.error(
                    "Office 365 user -> %s has not been created. Skipping...", user_name
                )
                success = False
                continue

            user_m365_id = user["m365_id"]

            if self._m365.getUserPhoto(user_m365_id, show_error=False):
                logger.info(
                    "User -> %s (%s) has already a photo in Microsoft 365. Skipping...",
                    user_name,
                    user_m365_id,
                )
                continue
            else:
                logger.info(
                    "User -> %s (%s) has not yet a photo in Microsoft 365. Uploading...",
                    user_name,
                    user_m365_id,
                )

            response = self._otcs.getNodeFromNickname(user_name)
            if response is None:
                logger.warning(
                    "Missing photo for user -> %s - nickname not found. Skipping...",
                    user_name,
                )
                continue
            photo_id = self._otcs.getResultValue(response, "id")
            photo_name = self._otcs.getResultValue(response, "name")
            photo_path = "/tmp/" + str(photo_name)
            response = self._otcs.downloadDocument(photo_id, photo_path)
            if response is None:
                logger.warning(
                    "Failed to download photo for user -> %s from Extended ECM",
                    user_name,
                )
                success = False
            else:
                logger.info(
                    "Successfully downloaded photo for user -> %s from Extended ECM to file -> %s",
                    user_name,
                    photo_path,
                )

            # Upload photo to M365:
            response = self._m365.updateUserPhoto(user_m365_id, photo_path)
            if response is None:
                logger.error(
                    "Failed to upload photo for user -> %s to Microsoft 365", user_name
                )
                success = False
            else:
                logger.info(
                    "Successfully uploaded photo for user -> %s to Microsoft 365",
                    user_name,
                )

        if success:
            self.writeStatusFile(section_name, self._users)

        return success

        # end method definition

    def processWorkspaceTypes(self, section_name: str = "workspaceTypes") -> list:
        """Create a data structure for all workspace types in the Extended ECM system.

        Args:
            None
        Returns:
            list: list of workspace types. Each list element is a dict with these values:
                - id (string)
                - name (string)
                - templates (list)
                    + name
                    + id
        """

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return []

        # get all workspace types (these have been created by the transports and are not in the payload!):
        response = self._otcs.getWorkspaceTypes()
        if response is None:
            logger.error("No workspace types found!")
            self._workspace_types = []
        else:
            self._workspace_types = response["results"]

        # now we enrich the workspace_type list elments (which are dicts)
        # with additional dict elements for further processing:
        for workspace_type in self._workspace_types:
            workspace_type_id = workspace_type["data"]["properties"]["wksp_type_id"]
            logger.info("Workspace Types ID -> %s", workspace_type_id)
            workspace_type["id"] = workspace_type_id
            workspace_type_name = workspace_type["data"]["properties"]["wksp_type_name"]
            logger.info("Workspace Types Name -> %s", workspace_type_name)
            workspace_type["name"] = workspace_type_name
            workspace_templates = workspace_type["data"]["properties"]["templates"]
            # Create empty lists of dicts with template names and node IDs:
            workspace_type["templates"] = []
            if workspace_templates:
                # Determine available templates per workspace type (there can be multiple!)
                for workspace_template in workspace_templates:
                    workspace_template_id = workspace_template["id"]
                    workspace_template_name = workspace_template["name"]
                    logger.info(
                        "Found template with name -> %s and ID -> %s",
                        workspace_template_name,
                        workspace_template_id,
                    )
                    template = {
                        "name": workspace_template_name,
                        "id": workspace_template_id,
                    }
                    workspace_type["templates"].append(template)

                    # Workaround for problem with workspace role inheritance
                    # which may be related to Transport or REST API: to work-around this we
                    # push down the workspace roles to the workspace folders explicitly:
                    response = self._otcs.getWorkspaceRoles(workspace_template_id)

                    for roles in response["results"]:
                        role_name = roles["data"]["properties"]["name"]
                        role_id = roles["data"]["properties"]["id"]
                        permissions = roles["data"]["properties"]["perms"]
                        # as getWorkspaceRoles() delivers permissions as a value (bit encoded)
                        # we need to convert it to a permissions string list:
                        permission_string_list = (
                            self._otcs.convertPermissionValueToPermissionString(
                                permissions
                            )
                        )

                        logger.info(
                            "Inherit permissions of workspace template -> %s and role -> %s to workspace folders...",
                            workspace_template_name,
                            role_name,
                        )

                        # Inherit permissions to folders of workspace template:
                        response = self._otcs.assignWorkspacePermissions(
                            workspace_template_id,
                            role_id,
                            permission_string_list,
                            1,  # Only sub items - workspace node itself is OK
                        )

            else:
                logger.warning(
                    "Workspace Types Name -> %s has no templates!", workspace_type_name
                )
                continue

        self.writeStatusFile(section_name, self._workspace_types)

        return self._workspace_types

        # end method definition

    def processWorkspaces(self, section_name: str = "workspaces") -> bool:
        """Process workspaces in payload and create them in Extended ECM.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise

        Side Effects:
            Set workspace["nodeId] to the node ID of the created workspace
        """

        if not self._workspaces:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for workspace in self._workspaces:
            # Read name from payload:
            if not "name" in workspace:
                logger.error("Workspace needs a name! Skipping to next workspace...")
                continue
            name = workspace["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in workspace and not workspace["enabled"]:
                logger.info(
                    "Payload for Workspace -> %s is disabled. Skipping...", name
                )
                continue

            # Read Type Name from payload:
            if not "type_name" in workspace:
                logger.error(
                    "Workspace -> %s needs a type name! Skipping to next workspace...",
                    name,
                )
                continue
            type_name = workspace["type_name"]

            # check if the workspace has been created before (effort to make the customizing code idem-potent)
            logger.info(
                "Check if workspace -> %s of type -> %s does already exist...",
                name,
                type_name,
            )
            workspace_id = int(self.determineWorkspaceID(workspace))
            if workspace_id:
                # we still want to set the nodeId as other parts of the payload depend on it:
                # workspace["nodeId"] = workspace_id
                logger.info(
                    "Workspace -> %s of type -> %s does already exist and has ID -> %s! Skipping to next workspace...",
                    name,
                    type_name,
                    workspace_id,
                )
                continue

            logger.info(
                "Creating new Workspace -> %s; Workspace Type -> %s...", name, type_name
            )

            # Read optional description from payload:
            if not "description" in workspace:
                description = ""
            else:
                description = workspace["description"]

            # Parent ID is optional and only required if workspace type does not specify a create location.
            # This is typically the case if it is a nested workspace or workspaces of the same type can be created
            # in different locations in the Enterprise Workspace:
            parent_id = workspace["parent_id"] if workspace.get("parent_id") else None

            if parent_id is not None:
                parent_workspace = next(
                    (item for item in self._workspaces if item["id"] == parent_id), None
                )
                if parent_workspace is None:
                    logger.error(
                        "Parent Workspace with logical ID -> %s not found.", parent_id
                    )
                    continue

                parent_workspace_node_id = self.determineWorkspaceID(parent_workspace)
                if not parent_workspace_node_id:
                    logger.warning(
                        "Parent Workspace without node ID (parent workspace creation may have failed) - skipping to next workspace..."
                    )
                    continue

                logger.info(
                    "Parent Workspace with logical ID -> %s has node ID -> %s",
                    parent_id,
                    parent_workspace_node_id,
                )
            else:
                # if no parent_id is specified the workspace location is determined by the workspace type definition
                # and we pass None as parent ID to the getWorkspaceCreateForm and createWorkspace methods below:
                parent_workspace_node_id = None

            # Find the workspace type with the name given in the payload:
            workspace_type = next(
                (item for item in self._workspace_types if item["name"] == type_name),
                None,
            )
            if workspace_type is None:
                logger.error(
                    "Workspace Type -> %s not found. Skipping to next workspace.",
                    type_name,
                )
                continue
            if workspace_type["templates"] == []:
                logger.error(
                    "Workspace Type -> %s does not have templates. Skipping to next workspace.",
                    type_name,
                )
                continue

            # check if the template to be used is specified in the payload:
            if "template_name" in workspace:
                template_name = workspace["template_name"]
                workspace_template = next(
                    (
                        item
                        for item in workspace_type["templates"]
                        if item["name"] == template_name
                    ),
                    None,
                )
                if workspace_template:  # does this template exist?
                    logger.info(
                        "Workspace Template -> %s has been specified in payload and it does exist.",
                        template_name,
                    )
                else:
                    logger.error(
                        "Workspace Template -> %s has been specified in payload but it doesn't exist!",
                        template_name,
                    )
                    logger.error(
                        "Workspace Type -> %s has only these templates -> %s",
                        type_name,
                        workspace_type["templates"],
                    )
                    continue
            # template to be used is NOT specified in the payload - then we just take the first one:
            else:
                workspace_template = workspace_type["templates"][0]
                logger.info(
                    "Workspace Template has not been specified in payload - we just take the first one (%s)",
                    workspace_template,
                )

            template_id = workspace_template["id"]
            template_name = workspace_template["name"]
            workspace_type_id = workspace_type["id"]

            logger.info(
                "Create Workspace -> %s (type -> %s) from workspace template -> %s (ID -> %s)",
                name,
                type_name,
                template_name,
                template_id,
            )

            # Read business object data from workspace payload:
            ext_system_id = None
            bo_type = None
            bo_id = None
            # Check if business objects are in workspace payload and list is not empty:
            if "business_objects" in workspace and workspace["business_objects"]:
                # Currently we can only process one business object (workspaces connected to multiple leading systems are not support yet)
                business_object_data = workspace["business_objects"][0]
                # business_object_data is a dict with 3 elements:
                if "external_system" in business_object_data:
                    ext_system_id = business_object_data["external_system"]
                if "bo_type" in business_object_data:
                    bo_type = business_object_data["bo_type"]
                if "bo_id" in business_object_data:
                    bo_id = business_object_data["bo_id"]
                logger.info(
                    "Workspace -> %s has business object information -> (%s, %s, %s)",
                    name,
                    ext_system_id,
                    bo_type,
                    bo_id,
                )

                # Check if external system has been declared in payload:
                external_system = next(
                    (
                        item
                        for item in self._external_systems
                        if (item["external_system_name"] == ext_system_id)
                    ),
                    None,
                )
                if not external_system:
                    logger.warning(
                        "External System -> %s does not exist. Cannot connect workspace -> %s to -> %s. Create workspace without connection.",
                        ext_system_id,
                        name,
                        ext_system_id,
                    )
                    # we remove the Business Object information to avoid communication
                    # errors during workspace create form and workspace creation
                    ext_system_id = None
                    bo_type = None
                    bo_id = None
                elif not external_system.get("reachable"):
                    logger.warning(
                        "External System -> %s is not reachable. Cannot connect workspace -> %s to -> %s. Create workspace without connection.",
                        ext_system_id,
                        name,
                        ext_system_id,
                    )
                    # we remove the Business Object information to avoid communication
                    # errors during workspace create form and workspace creation
                    ext_system_id = None
                    bo_type = None
                    bo_id = None
                else:
                    logger.info(
                        "Workspace -> %s will be connected with external system -> %s (%s, %s)",
                        name,
                        ext_system_id,
                        bo_type,
                        bo_id,
                    )

            # Read categories from payload:
            if not "categories" in workspace:
                logger.info(
                    "Workspace payload has no category data! Will leave category attributes empty..."
                )
                category_create_data = {}
            else:
                categories = workspace["categories"]
                category_create_data = {"categories": {}}

                response = self._otcs.getWorkspaceCreateForm(
                    template_id, ext_system_id, bo_type, bo_id, parent_workspace_node_id
                )
                if response is None:
                    logger.error(
                        "Failed to retrieve create information for template -> %s",
                        template_id,
                    )
                    continue

                logger.info(
                    "Successfully retrieved create information for template -> %s",
                    template_id,
                )

                # Process category information
                forms = response["forms"]

                categories_form = {}

                # Typically the the create workspace form delivers 3 forms:
                # 1. Form for System Attributes (has no role name)
                # 2. Form for Category Data (role name = "categories")
                # 3. Form for Classifications (role name = "classifications")
                # First we extract these 3 forms:
                for form in forms:
                    if "role_name" in form and form["role_name"] == "categories":
                        categories_form = form
                        logger.debug("Found Categories form -> %s", form)
                        continue
                    if "role_name" in form and form["role_name"] == "classifications":
                        logger.debug("Found Classification form -> %s", form)
                        continue
                    # the remaining option is that this form is the system attributes form:
                    logger.debug("Found System Attributes form -> %s", form)

                # We are just interested in the single category data set (role_name = "categories"):
                data = categories_form["data"]
                logger.debug("Categories data found -> %s", data)
                schema = categories_form["schema"]["properties"]
                logger.debug("Categories schema found -> %s", schema)
                # parallel loop over category data and schema
                for cat_data, cat_schema in zip(data, schema):
                    logger.info("Category ID -> %s", cat_data)
                    data_attributes = data[cat_data]
                    logger.debug("Data Attributes -> %s", data_attributes)
                    schema_attributes = schema[cat_schema]["properties"]
                    logger.debug("Schema Attributes -> %s", schema_attributes)
                    cat_name = schema[cat_schema]["title"]
                    logger.info("Category name -> %s", cat_name)
                    # parallel loop over attribute data and schema
                    # Sets with one (fixed) row have type = object
                    # Multi-value Sets with (multiple) rows have type = array and "properties" in "items" schema
                    # Multi-value attributes have also type = array but NO "properties" in "items" schema
                    for attr_data, attr_schema in zip(
                        data_attributes, schema_attributes
                    ):
                        logger.debug("Attribute ID -> %s", attr_data)
                        logger.debug("Attribute Data -> %s", data_attributes[attr_data])
                        logger.debug(
                            "Attribute Schema -> %s", schema_attributes[attr_schema]
                        )
                        attr_type = schema_attributes[attr_schema]["type"]
                        logger.debug("Attribute Type -> %s", attr_type)
                        if not "title" in schema_attributes[attr_schema]:
                            logger.debug("Attribute has no title - skipping")
                            continue
                        # Check if it is an multi-line set:
                        if attr_type == "array" and (
                            "properties" in schema_attributes[attr_schema]["items"]
                        ):
                            set_name = schema_attributes[attr_schema]["title"]
                            logger.info("Multi-line Set -> %s", set_name)
                            set_data_attributes = data_attributes[
                                attr_data
                            ]  # this is a list []
                            logger.debug(
                                "Set Data Attributes -> %s", set_data_attributes
                            )
                            set_schema_attributes = schema_attributes[attr_schema][
                                "items"
                            ]["properties"]
                            logger.debug(
                                "Set Schema Attributes -> %s", set_schema_attributes
                            )
                            set_schema_max_rows = schema_attributes[attr_schema][
                                "items"
                            ]["maxItems"]
                            logger.debug(
                                "Set Schema Max Rows -> %s", set_schema_max_rows
                            )
                            set_data_max_rows = len(set_data_attributes)
                            logger.debug("Set Data Max Rows -> %s", set_data_max_rows)
                            row = 1
                            # it can happen that the payload contains more rows than the
                            # initial rows in the set data structure. In this case we use
                            # a copy of the data structure from row 0 as template...
                            first_row = dict(set_data_attributes[0])
                            # We don't know upfront how many rows of data we will find in payload
                            # but we at max process the maxItems specified in the schema:
                            while row <= set_schema_max_rows:
                                # Test if we have any payload for this row:
                                attribute = next(
                                    (
                                        item
                                        for item in categories
                                        if (
                                            item["name"] == cat_name
                                            and item["set"] == set_name
                                            and "row" in item
                                            and item["row"] == row
                                        )
                                    ),
                                    None,
                                )
                                # stop if there's no payload for the row:
                                if attribute is None:
                                    logger.info(
                                        "No payload found for set -> %s, row -> %s",
                                        set_name,
                                        row,
                                    )
                                    # we assume that if there's no payload for row n there will be no payload for rows > n
                                    # and break the while loop:
                                    break
                                # do we need to create a new row in the data set?
                                elif row > set_data_max_rows:
                                    # use the row we stored above to create a new empty row:
                                    logger.info(
                                        "Found payload for row -> %s, we need a new data row for it",
                                        row,
                                    )
                                    logger.info(
                                        "Adding an additional row -> %s to set data -> %s",
                                        row,
                                        set_name,
                                    )
                                    # add the empty dict to the list:
                                    set_data_attributes.append(dict(first_row))
                                    set_data_max_rows += 1
                                else:
                                    logger.info(
                                        "Found payload for row -> %s %s we can store in existing data row",
                                        row,
                                        set_name,
                                    )
                                # traverse all attributes in a single row:
                                for set_attr_schema in set_schema_attributes:
                                    logger.debug(
                                        "Set Attribute ID -> %s (row -> %s)",
                                        set_attr_schema,
                                        row,
                                    )
                                    logger.debug(
                                        "Set Attribute Schema -> %s (row -> %s)",
                                        set_schema_attributes[set_attr_schema],
                                        row,
                                    )
                                    set_attr_type = set_schema_attributes[
                                        set_attr_schema
                                    ]["type"]
                                    logger.debug(
                                        "Set Attribute Type -> %s (row -> %s)",
                                        set_attr_type,
                                        row,
                                    )
                                    set_attr_name = set_schema_attributes[
                                        set_attr_schema
                                    ]["title"]
                                    logger.debug(
                                        "Set Attribute Name -> %s (row -> %s)",
                                        set_attr_name,
                                        row,
                                    )
                                    # Lookup the attribute with the right category, set, attribute name, and row number in payload:
                                    attribute = next(
                                        (
                                            item
                                            for item in categories
                                            if (
                                                item["name"] == cat_name
                                                and item["set"] == set_name
                                                and item["attribute"] == set_attr_name
                                                and "row" in item
                                                and item["row"] == row
                                            )
                                        ),
                                        None,
                                    )
                                    if attribute is None:
                                        logger.warning(
                                            "Set -> %s, Attribute -> %s, Row -> %s not found in payload.",
                                            set_name,
                                            set_attr_name,
                                            row,
                                        )

                                        # need to use row - 1 as index starts with 0 but payload rows start with 1
                                        set_data_attributes[row - 1][
                                            set_attr_schema
                                        ] = ""
                                    else:
                                        logger.info(
                                            "Set -> %s, Attribute -> %s, Row -> %s found in payload, value -> %s",
                                            set_name,
                                            set_attr_name,
                                            row,
                                            attribute["value"],
                                        )
                                        # Put the value from the payload into data structure
                                        # need to use row - 1 as index starts with 0 but payload rows start with 1
                                        set_data_attributes[row - 1][
                                            set_attr_schema
                                        ] = attribute["value"]
                                row += 1  # continue the while loop with the next row
                        # Check if it is single-line set:
                        elif attr_type == "object":
                            set_name = schema_attributes[attr_schema]["title"]
                            logger.info("Single-line Set -> %s", set_name)
                            set_data_attributes = data_attributes[attr_data]
                            logger.debug(
                                "Set Data Attributes -> %s", set_data_attributes
                            )

                            set_schema_attributes = schema_attributes[attr_schema][
                                "properties"
                            ]
                            logger.debug(
                                "Set Schema Attributes -> %s", set_schema_attributes
                            )
                            for set_attr_data, set_attr_schema in zip(
                                set_data_attributes, set_schema_attributes
                            ):
                                logger.debug("Set Attribute ID -> %s", set_attr_data)
                                logger.debug(
                                    "Set Attribute Data -> %s",
                                    set_data_attributes[set_attr_data],
                                )
                                logger.debug(
                                    "Set Attribute Schema -> %s",
                                    set_schema_attributes[set_attr_schema],
                                )
                                set_attr_type = set_schema_attributes[set_attr_schema][
                                    "type"
                                ]
                                logger.debug("Set Attribute Type -> %s", set_attr_type)
                                set_attr_name = set_schema_attributes[set_attr_schema][
                                    "title"
                                ]
                                logger.debug("Set Attribute Name -> %s", set_attr_name)
                                # Lookup the attribute with the right category, set and attribute name in payload:
                                attribute = next(
                                    (
                                        item
                                        for item in categories
                                        if (
                                            item["name"] == cat_name
                                            and item["set"] == set_name
                                            and item["attribute"] == set_attr_name
                                        )
                                    ),
                                    None,
                                )
                                if attribute is None:
                                    logger.warning(
                                        "Set -> %s, Attribute -> %s not found in payload.",
                                        set_name,
                                        set_attr_name,
                                    )
                                    set_data_attributes[set_attr_data] = ""
                                else:
                                    logger.info(
                                        "Set -> %s, Attribute -> %s found in payload, value -> %s",
                                        set_name,
                                        set_attr_name,
                                        attribute["value"],
                                    )
                                    # Put the value from the payload into data structure
                                    set_data_attributes[set_attr_data] = attribute[
                                        "value"
                                    ]
                        # It is a plain attribute (not inside a set) or it is a multi-value attribute (not inside a set):
                        else:
                            attr_name = schema_attributes[attr_schema]["title"]
                            logger.debug("Attribute Name -> %s", attr_name)
                            # Lookup the attribute with the right category and attribute name in payload:
                            attribute = next(
                                (
                                    item
                                    for item in categories
                                    if (
                                        item["name"] == cat_name
                                        and item["attribute"] == attr_name
                                    )
                                ),
                                None,
                            )
                            if attribute is None:
                                logger.warning(
                                    "Attribute -> %s not found in payload.", attr_name
                                )
                                data_attributes[attr_data] = ""
                            else:
                                logger.info(
                                    "Attribute -> %s found in payload, value -> %s",
                                    attr_name,
                                    attribute["value"],
                                )
                                # We need to handle a very special case here for Extended ECM for Government
                                # which has an attribute type "Organizational Unit" (OU). This is referring to a group ID
                                # which is not stable across deployments. So we need to lookup the Group ID and add it
                                # to the data structure. This expects that the payload has the Group Name and not the Group ID
                                if attr_type == str(11480):
                                    logger.info(
                                        "Attribute -> %s is is of type -> Organizational Unit (%s). Looking up group ID for group name -> %s",
                                        attr_name,
                                        attr_type,
                                        attribute["value"],
                                    )
                                    response = self._otcs.getGroup(attribute["value"])
                                    # retrieve the list of matching group names - should just be 1
                                    group_list = response["data"]
                                    # Make sure we have an exact match:
                                    group = next(
                                        (
                                            item
                                            for item in group_list
                                            if item["name"] == attribute["value"]
                                        ),
                                        None,
                                    )
                                    if group:
                                        # Group has been found - determine ID:
                                        group_id = group["id"]
                                        logger.info(
                                            "Group for Organizational Unit -> %s has ID -> %s",
                                            attribute["value"],
                                            group_id,
                                        )
                                        # Put the group ID into data structure
                                        data_attributes[attr_data] = str(group_id)
                                    else:
                                        logger.error(
                                            "Group for Organizational Unit -> %s does not exist!",
                                            attribute["value"],
                                        )
                                        # Clear the value to avoid workspace create failure
                                        data_attributes[attr_data] = ""
                                # handle special case where attribute type is a user picker.
                                # we expect that the payload includes the login name for this
                                # (as user IDs are not stable across systems) but then we need
                                # to lookup the real user ID here:
                                elif attr_type == "otcs_user_picker":
                                    logger.info(
                                        "Attribute -> %s is is of type -> User Picker (%s). Looking up user ID for user login name -> %s",
                                        attr_name,
                                        attr_type,
                                        attribute["value"],
                                    )
                                    response = self._otcs.getUser(attribute["value"])
                                    # retrieve the list of matching group names - should just be 1
                                    user_list = response["data"]
                                    # Make sure we have an exact match:
                                    user = next(
                                        (
                                            item
                                            for item in user_list
                                            if item["name"] == attribute["value"]
                                        ),
                                        None,
                                    )
                                    if user:
                                        # User has been found - determine ID:
                                        user_id = user["id"]
                                        logger.info(
                                            "User -> %s has ID -> %s",
                                            attribute["value"],
                                            user_id,
                                        )
                                        # Put the user ID into data structure
                                        data_attributes[attr_data] = str(user_id)
                                    else:
                                        logger.error(
                                            "User with login name -> %s does not exist!",
                                            attribute["value"],
                                        )
                                        # Clear the value to avoid workspace create failure
                                        data_attributes[attr_data] = ""

                                else:
                                    # Put the value from the payload into data structure
                                    data_attributes[attr_data] = attribute["value"]
                    category_create_data["categories"][cat_data] = data_attributes

            logger.debug("Category Create Data -> %s", category_create_data)

            # Create the workspace with all provided information:
            response = self._otcs.createWorkspace(
                template_id,
                name,
                description,
                workspace_type_id,
                category_create_data,
                ext_system_id,
                bo_type,
                bo_id,
                parent_workspace_node_id,
            )
            if response is None:
                logger.error("Failed to create workspace -> %s", name)
                continue

            # Now we add the node ID of the new workspace to the payload data structure
            # This will be reused when creating the workspace relationships!
            workspace["nodeId"] = self._otcs.getResultValue(response, "id")

            # We also get the name the workspace was finally created with.
            # This can be different form the name in the payload as additional
            # naming conventions from the Workspace Type definitions may apply.
            # This is important to make the python container idem-potent.
            response = self._otcs.getWorkspace(workspace["nodeId"])
            workspace["name"] = self._otcs.getResultValue(response, "name")

            logger.info(
                "Successfully created workspace with final name -> %s and node ID -> %s",
                workspace["name"],
                workspace["nodeId"],
            )

            # Check if an RM classification is specified for the workspace:
            # RM Classification is specified as list of path elements (top-down)
            if (
                "rm_classification_path" in workspace
                and workspace["rm_classification_path"] != []
            ):
                rm_class_node = self._otcs.getNodeByVolumeAndPath(
                    198, workspace["rm_classification_path"]
                )
                rm_class_node_id = self._otcs.getResultValue(rm_class_node, "id")
                if rm_class_node_id:
                    response = self._otcs.assignRMClassification(
                        workspace["nodeId"], rm_class_node_id, False
                    )
                    if response is None:
                        logger.error(
                            "Failed to assign RM classification -> %s (%s) to workspace -> %s",
                            workspace["rm_classification_path"][-1],
                            rm_class_node_id,
                            name,
                        )
                    else:
                        logger.info(
                            "Assigned RM Classification -> %s to workspace -> %s",
                            workspace["rm_classification_path"][-1],
                            name,
                        )
            # Check if one or multiple classifications are specified for the workspace
            # Classifications are specified as list of path elements (top-down)
            if (
                "classification_pathes" in workspace
                and workspace["classification_pathes"] != []
            ):
                for classification_path in workspace["classification_pathes"]:
                    class_node = self._otcs.getNodeByVolumeAndPath(
                        198, classification_path
                    )
                    class_node_id = self._otcs.getResultValue(class_node, "id")
                    if class_node_id:
                        response = self._otcs.assignClassification(
                            workspace["nodeId"], [class_node_id], False
                        )
                        if response is None:
                            logger.error(
                                "Failed to assign classification -> %s to workspace -> %s",
                                class_node_id,
                                name,
                            )
                        else:
                            logger.info(
                                "Assigned Classification -> %s to workspace -> %s",
                                classification_path[-1],
                                name,
                            )

        if success:
            self.writeStatusFile(section_name, self._workspaces)

        return success

        # end method definition

    def processWorkspaceRelationships(
        self, section_name: str = "workspaceRelationships"
    ) -> bool:
        """Process workspaces relationships in payload and create them in Extended ECM.

        Relationships can only be created if all workspaces have been created before.
        Once a workspace got created, the node ID of that workspaces has been added
        to the payload["workspaces"] data structure (see processWorkspaces())
        Relationships are created between the node IDs of two business workspaces
        (and not the logical IDs in the inital payload specification)

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._workspaces:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for workspace in self._workspaces:
            # Read name from payload:
            if not "name" in workspace:
                continue
            name = workspace["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in workspace and not workspace["enabled"]:
                logger.info(
                    "Payload for Workspace -> %s is disabled. Skipping...", name
                )
                continue

            # Read relationships from payload:
            if not "relationships" in workspace:
                logger.info(
                    "Workspace -> %s has no relationships - skipping to next workspace...",
                    name,
                )
                continue

            # Check that workspaces actually have a logical ID -
            # otherwise we cannot establish the relationship:
            if not "id" in workspace:
                logger.warning(
                    "Workspace without ID cannot have a relationship - skipping to next workspace..."
                )
                continue

            workspace_id = workspace["id"]
            logger.info("Workspace -> %s has relationships - creating...", name)

            workspace_node_id = self.determineWorkspaceID(workspace)
            if not workspace_node_id:
                logger.warning(
                    "Workspace without node ID cannot have a relationship (workspace creation may have failed) - skipping to next workspace..."
                )
                continue
            # now determine the actual node IDs of the workspaces (have been created above):
            logger.info(
                "Workspace with logical ID -> %s has node ID -> %s",
                workspace_id,
                workspace_node_id,
            )

            for related_workspace_id in workspace["relationships"]:
                # Find the workspace type with the name given in the payload:
                related_workspace = next(
                    (
                        item
                        for item in self._workspaces
                        if item["id"] == related_workspace_id
                    ),
                    None,
                )
                if related_workspace is None:
                    logger.error(
                        "Related Workspace with logical ID -> %s not found.",
                        related_workspace_id,
                    )
                    success = False
                    continue

                if "enabled" in related_workspace and not related_workspace["enabled"]:
                    logger.info(
                        "Payload for Related Workspace -> %s is disabled. Skipping...",
                        related_workspace["name"],
                    )
                    continue

                related_workspace_node_id = self.determineWorkspaceID(related_workspace)
                if not related_workspace_node_id:
                    logger.warning(
                        "Related Workspace without node ID (workspaces creation may have failed) - skipping to next workspace..."
                    )
                    continue

                logger.info(
                    "Related Workspace with logical ID -> %s has node ID -> %s",
                    related_workspace_id,
                    related_workspace_node_id,
                )

                logger.info(
                    "Create Workspace Relationship between workspace node ID -> %s and workspace node ID -> %s",
                    workspace_node_id,
                    related_workspace_node_id,
                )

                # Check if relationship does already exists:
                response = self._otcs.getWorkspaceRelationships(workspace_node_id)

                existing_workspace_relationship = self._otcs.existResultItem(
                    response, "id", related_workspace_node_id
                )
                if existing_workspace_relationship:
                    logger.info(
                        "Workspace relationship between workspace ID -> %s and related workspace ID -> %s does already exist. Skipping...",
                        workspace_node_id,
                        related_workspace_node_id,
                    )
                    continue

                response = self._otcs.createWorkspaceRelationship(
                    workspace_node_id, related_workspace_node_id
                )
                if not response:
                    logger.error("Failed to create workspace relationship.")
                    success = False
                else:
                    logger.info("Successfully created workspace relationship.")

        if success:
            self.writeStatusFile(section_name, self._workspaces)

        return success

        # end method definition

    def processWorkspaceMembers(self, section_name: str = "workspaceMembers") -> bool:
        """Process workspaces members in payload and create them in Extended ECM.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._workspaces:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for workspace in self._workspaces:
            # Read name from payload (just for logging):
            if not "name" in workspace:
                continue
            workspace_name = workspace["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in workspace and not workspace["enabled"]:
                logger.info(
                    "Payload for Workspace -> %s is disabled. Skipping...",
                    workspace_name,
                )
                continue

            # Read members from payload:
            if not "members" in workspace:
                logger.info(
                    "Workspace -> %s has no members in payload - skipping to next workspace...",
                    workspace_name,
                )
                continue
            members = workspace["members"]

            workspace_id = workspace["id"]
            logger.info(
                "Workspace -> %s has memberships in payload - establishing...",
                workspace_name,
            )

            workspace_node_id = int(self.determineWorkspaceID(workspace))
            if not workspace_node_id:
                logger.warning(
                    "Workspace without node ID cannot have a members (workspaces creation may have failed) - skipping to next workspace..."
                )
                continue

            # now determine the actual node IDs of the workspaces (have been created by processWorkspaces()):
            workspace_node = self._otcs.getNode(workspace_node_id)
            workspace_owner_id = self._otcs.getResultValue(
                workspace_node, "owner_user_id"
            )
            workspace_owner_name = self._otcs.getResultValue(workspace_node, "owner")

            workspace_roles = self._otcs.getWorkspaceRoles(workspace_node_id)
            if workspace_roles is None:
                logger.info(
                    "Workspace with ID -> %s and node Id -> %s has no roles - skipping to next workspace...",
                    workspace_id,
                    workspace_node_id,
                )
                continue

            # We don't want the workspace creator to be in the leader role
            # of automatically created workspaces - this can happen because the
            # creator gets added to the leader role automatically:
            leader_role_id = int(
                self._otcs.lookupResultValue(workspace_roles, "leader", "True", "id")
            )

            if leader_role_id:
                leader_role_name = self._otcs.lookupResultValue(
                    workspace_roles, "leader", str(True), "name"
                )
                response = self._otcs.removeMemberFromWorkspace(
                    workspace_node_id, leader_role_id, workspace_owner_id, False
                )
                if response:
                    logger.info(
                        "Removed creator user -> %s (%s) from leader role -> {%s (%s) of workspace -> %s",
                        workspace_owner_name,
                        workspace_owner_id,
                        leader_role_name,
                        leader_role_id,
                        workspace_name,
                    )

            logger.info(
                "Adding members to workspace with ID -> %s and node ID -> %s defined in payload...",
                workspace_id,
                workspace_node_id,
            )

            for member in members:
                # read user list and role name from payload:
                member_users = (
                    member["users"] if member.get("users") else []
                )  # be careful to avoid key errors as users are optional
                member_groups = (
                    member["groups"] if member.get("groups") else []
                )  # be careful to avoid key errors as groups are optional
                member_role_name = member["role"]

                if member_role_name == "":  # role name is required
                    logger.error(
                        "Members of workspace -> %s is missing the role name.",
                        workspace_name,
                    )
                    success = False
                    continue
                if (
                    member_users == [] and member_groups == []
                ):  # we either need users or groups (or both)
                    logger.warning(
                        "Role -> %s of workspace -> %s does not have any members (no users nor groups).",
                        member_role_name,
                        workspace_name,
                    )
                    continue

                role_id = self._otcs.lookupResultValue(
                    workspace_roles, "name", member_role_name, "id"
                )
                if role_id is None:
                    #    if member_role is None:
                    logger.error(
                        "Workspace -> %s does not have a role with name -> %s",
                        workspace_name,
                        member_role_name,
                    )
                    success = False
                    continue
                logger.info("Role -> %s has ID -> %s", member_role_name, role_id)

                # Process users as workspaces members:
                for member_user in member_users:
                    # find member user in current payload:
                    member_user_id = next(
                        (item for item in self._users if item["name"] == member_user),
                        {},
                    )
                    if member_user_id:
                        user_id = member_user_id["id"]
                    else:
                        # If this didn't work, try to get the member user from OTCS. This covers
                        # cases where the user is system generated or part
                        # of a former payload processing (thus not in the current payload):
                        logger.info(
                            "Member -> %s not found in current payload - check if it exists in OTCS already...",
                            member_user,
                        )
                        existing_user = self._otcs.getUser(member_user)
                        if (
                            not existing_user or not existing_user["data"]
                        ):  # we cannot use getResultValue() here - not a V2 call
                            logger.error(
                                "Cannot find member user with login -> %s. Skipping...",
                                member_user,
                            )
                            continue
                        user_id = existing_user["data"][0][
                            "id"
                        ]  # we cannot use getResultValue()here!

                    # Add member if it does not yet exists - suppress warning
                    # message if user is already in role:
                    response = self._otcs.addMemberToWorkspace(
                        workspace_node_id, int(role_id), user_id, False
                    )
                    if response is None:
                        logger.error(
                            "Failed to add user -> %s (%s) to role -> %s of workspace -> %s",
                            member_user_id["name"],
                            user_id,
                            member_role_name,
                            workspace_name,
                        )
                        success = False
                    else:
                        logger.info(
                            "Successfully added user -> %s (%s) to role -> %s of workspace -> %s",
                            member_user_id["name"],
                            user_id,
                            member_role_name,
                            workspace_name,
                        )

                # Process groups as workspaces members:
                for member_group in member_groups:
                    member_group_id = next(
                        (item for item in self._groups if item["name"] == member_group),
                        None,
                    )
                    if member_group_id is None:
                        logger.error("Cannot find group with name -> %s", member_group)
                        success = False
                        continue
                    group_id = member_group_id["id"]

                    response = self._otcs.addMemberToWorkspace(
                        workspace_node_id, int(role_id), group_id
                    )
                    if response is None:
                        logger.error(
                            "Failed to add group -> %s (%s) to role -> %s of workspace -> %s",
                            member_group_id["name"],
                            group_id,
                            member_role_name,
                            workspace_name,
                        )
                        success = False
                    else:
                        logger.info(
                            "Successfully added group -> %s (%s) to role -> %s of workspace -> %s",
                            member_group_id["name"],
                            group_id,
                            member_role_name,
                            workspace_name,
                        )

        if success:
            self.writeStatusFile(section_name, self._workspaces)

        return success

        # end method definition

    def processWebReports(
        self, web_reports: list, section_name: str = "webReports"
    ) -> bool:
        """Process web reports in payload and run them in Extended ECM.

        Args:
            web_reports (list): list of web reports. As we have two different list (pre and post)
                                we need to pass the actual list as parameter.
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not web_reports:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for web_report in web_reports:
            nick_name = web_report["nickname"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in web_report and not web_report["enabled"]:
                logger.info(
                    "Payload for Web Report -> %s is disabled. Skipping...", nick_name
                )
                continue

            description = web_report["description"]

            if not self._otcs.getNodeFromNickname(nick_name):
                logger.error(
                    "Web Report with nickname -> %s does not exist! Skipping...",
                    nick_name,
                )
                success = False
                continue

            # be careful to avoid key errors as Web Report parameters are optional:
            actual_params = (
                web_report["parameters"] if web_report.get("parameters") else {}
            )
            formal_params = self._otcs.getWebReportParameters(nick_name)
            if actual_params:
                logger.info(
                    "Running Web Report -> %s (%s) with parameters -> %s ...",
                    nick_name,
                    description,
                    actual_params,
                )
                # Do some sanity checks to see if the formal and actual parameters are matching...
                # Check 1: are there formal parameters at all?
                if not formal_params:
                    logger.error(
                        "Web Report -> %s is called with actual parameters but it does not expect parameters! Skipping...",
                        nick_name,
                    )
                    success = False
                    continue
                lets_continue = False
                # Check 2: Iterate through the actual parameters given in the payload
                # and see if there's a matching formal parameter expected by the Web Report:
                for key, value in actual_params.items():
                    # Check if there's a matching formal parameter defined on the Web Report node:
                    formal_param = next(
                        (item for item in formal_params if item["parm_name"] == key),
                        None,
                    )
                    if formal_param is None:
                        logger.error(
                            "Web Report -> %s is called with parameter -> %s that is not expected! Value: %s) Skipping...",
                            nick_name,
                            key,
                            value,
                        )
                        success = False
                        lets_continue = True  # we cannot do a "continue" here directly as we are in an inner loop
                # Check 3: Iterate through the formal parameters and validate there's a matching
                # actual parameter defined in the payload for each mandatory formal parameter
                # that does not have a default value:
                for formal_param in formal_params:
                    if (
                        (formal_param["mandatory"] is True)
                        and (formal_param["default_value"] is None)
                        and not actual_params.get(formal_param["parm_name"])
                    ):
                        logger.error(
                            "Web Report -> %s is called without mandatory parameter -> %s! Skipping...",
                            nick_name,
                            formal_param["parm_name"],
                        )
                        success = False
                        lets_continue = True  # we cannot do a "continue" here directly as we are in an inner loop
                # Did any of the checks fail?
                if lets_continue:
                    continue
                # Actual parameters are validated, we can run the Web Report:
                response = self._otcs.runWebReport(nick_name, actual_params)
            else:
                logger.info(
                    "Running Web Report -> %s (%s) without parameters...",
                    nick_name,
                    description,
                )
                # Check if there's a formal parameter that is mandatory but
                # does not have a default value:
                if formal_params:
                    required_param = next(
                        (
                            item
                            for item in formal_params
                            if (item["mandatory"] is True)
                            and (not item["default_value"])
                        ),
                        None,
                    )
                    if required_param:
                        logger.error(
                            "Web Report -> %s is called without parameters but has a mandatory parameter -> %s without a default value! Skipping...",
                            nick_name,
                            required_param["parm_name"],
                        )
                        success = False
                        continue
                    else:  # we are good to proceed!
                        logger.debug(
                            "Web Report -> %s does not have a mandatory parameter without a default value!",
                            nick_name,
                        )
                response = self._otcs.runWebReport(nick_name)
            if response is None:
                logger.error("Failed to run web report -> %s", nick_name)
                success = False

        if success:
            self.writeStatusFile(section_name, web_reports)

        return success

        # end method definition

    def processCSApplications(
        self, otcs_object: OTCS, section_name: str = "csApplications"
    ) -> bool:
        """Process CS applications in payload and install them in Extended ECM.
        The CS Applications need to be installed in all frontend and backends.

        Args:
            otcs_object (object): this can either be the OTCS frontend or OTCS backend. If None
                                  then the otcs_backend is used.
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._cs_applications:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        # OTCS backend is the default:
        if not otcs_object:
            otcs_object = self._otcs_backend

        for cs_application in self._cs_applications:
            application_name = cs_application["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in cs_application and not cs_application["enabled"]:
                logger.info(
                    "Payload for CS Application -> %s is disabled. Skipping...",
                    application_name,
                )
                continue

            application_description = cs_application["description"]

            logger.info(
                "Install CS Application -> %s (%s)...",
                application_name,
                application_description,
            )
            response = otcs_object.installCSApplication(application_name)
            if response is None:
                logger.error(
                    "Failed to install CS Application -> %s!", application_name
                )
                success = False

        if success:
            self.writeStatusFile(section_name, self._cs_applications)

        return success

        # end method definition

    def processUserSettings(self, section_name: str = "userSettings") -> bool:
        """Process user settings in payload and apply themin OTDS.
           This includes password settings and user display settings.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._users:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for user in self._users:
            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> %s is disabled. Skipping...", user_name
                )
                continue

            user_partition = self._otcs.config()["partition"]
            if not user_partition:
                logger.error("User partition not found!")
                success = False
                continue

            # Set the OTDS display name. Extended ECM does not use this but
            # it makes AppWorks display users correctly (and it doesn't hurt)
            # We only set this if firstname _and_ last name are in the payload:
            if "firstname" in user and "lastname" in user:
                user_display_name = user["firstname"] + " " + user["lastname"]
                response = self._otds.updateUser(
                    user_partition, user_name, "displayName", user_display_name
                )
                if response:
                    logger.info(
                        "Display name for user -> %s has been updated to -> %s",
                        user_name,
                        user_display_name,
                    )
                else:
                    logger.error(
                        "Display name for user -> %s could not be updated to -> %s",
                        user_name,
                        user_display_name,
                    )
                    success = False

            # Don't enforce the user to reset password at first login (settings in OTDS):
            logger.info("Don't enforce password change for user -> %s...", user_name)
            response = self._otds.updateUser(
                user_partition, user_name, "UserMustChangePasswordAtNextSignIn", "False"
            )
            if not response:
                success = False

        if success:
            self.writeStatusFile(section_name, self._users)

        return success

        # end method definition

    def processUserFavoritesAndProfiles(
        self, section_name: str = "userFavoritesAndProfiles"
    ) -> bool:
        """Process user favorites in payload and create them in Extended ECM.
           This method also simulates browsing the favorites to populate the
           widgets on the landing pages and sets personal preferences.

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._users:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        # We can only set favorites if we impersonate / authenticate as the user.
        # The following code (for loop) will change the authenticated user - we need to
        # switch it back to admin user later so we safe the admin credentials for this:

        if self._users:
            # save admin credentials for later switch back to admin user:
            admin_credentials = self._otcs.credentials()
        else:
            admin_credentials = {}

        for user in self._users:
            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> %s is disabled. Skipping...", user_name
                )
                continue

            user_password = user["password"]

            # we change the otcs credentials to the user:
            self._otcs.setCredentials(user_name, user_password)

            # we re-authenticate as the user:
            logger.info("Authenticate user -> %s...", user_name)
            # True = force new login with new user
            cookie = self._otcs.authenticate(True)
            if not cookie:
                logger.error("Couldn't authenticate user -> %s", user_name)
                success = False
                continue

            # we update the user profile to activate navigation tree:
            response = self._otcs.updateUserProfile("conwsNavigationTreeView", True)
            if response is None:
                logger.warning("Profile for user -> %s couldn't be updated!", user_name)
            else:
                logger.info(
                    "Profile for user -> %s has been updated to enable Workspace Navigation Tree.",
                    user_name,
                )

            # we work through the list of favorites defined for the user:
            favorites = user["favorites"]
            for favorite in favorites:
                # check if favorite is a logical workspace name
                favorite_item = next(
                    (item for item in self._workspaces if item["id"] == favorite), None
                )
                is_workspace = False
                if favorite_item:
                    logger.info(
                        "Found favorite item (workspace) in payload -> %s",
                        favorite_item["name"],
                    )
                    favorite_id = self.determineWorkspaceID(favorite_item)
                    if not favorite_id:
                        logger.warning(
                            "Workspace of type -> %s and name -> %s does not exist. Cannot create favorite. Skipping...",
                            favorite_item["type_name"],
                            favorite_item["name"],
                        )
                        continue

                    is_workspace = True
                else:
                    # alternatively try to find the item as a nickname:
                    favorite_item = self._otcs.getNodeFromNickname(favorite)
                    favorite_id = self._otcs.getResultValue(favorite_item, "id")
                    #                    if favorite_item is None:
                    if favorite_id is None:
                        logger.warning(
                            "Favorite -> %s neither found as workspace ID nor as nickname - skipping to next favorite...",
                            favorite,
                        )
                        continue

                response = self._otcs.addFavorite(favorite_id)
                if response is None:
                    logger.warning(
                        "Favorite ID -> %s couldn't be added for user -> %s!",
                        favorite_id,
                        user_name,
                    )
                else:
                    logger.info(
                        "Added favorite for user -> %s, node ID -> %s.",
                        user_name,
                        favorite_id,
                    )
                    logger.info(
                        "Simulate user -> %s browsing node ID -> %s.",
                        user_name,
                        favorite_id,
                    )
                    # simulate a browse by the user to populate recently accessed items
                    if is_workspace:
                        response = self._otcs.getWorkspace(favorite_id)
                    else:
                        response = self._otcs.getNode(favorite_id)

            # we work through the list of proxies defined for the user
            # (we need to consider that not all users have the proxies element):
            proxies = user["proxies"] if user.get("proxies") else []

            for proxy in proxies:
                proxy_user = next(
                    (item for item in self._users if item["name"] == proxy),
                    None,
                )
                if not proxy_user or not "id" in proxy_user:
                    logger.error(
                        "The proxy -> %s for user -> %s does not exist! Skipping proxy...",
                        proxy,
                        user_name,
                    )
                    success = False
                    continue
                proxy_user_id = proxy_user["id"]

                # Check if the proxy is already set:
                if not self._otcs.isProxy(proxy):
                    logger.info(
                        "Set user -> %s (%s) as proxy for user -> %s.",
                        proxy,
                        proxy_user_id,
                        user_name,
                    )
                    # set the user proxy - currently we don't support time based proxies in payload.
                    # The called method is ready to support this.
                    response = self._otcs.updateUserProxy(proxy_user_id)
                else:
                    logger.info(
                        "User -> %s (%s) is already proxy for user -> %s. Skipping...",
                        proxy,
                        proxy_user_id,
                        user_name,
                    )
        if self._users:
            # Set back admin credentials:
            self._otcs.setCredentials(
                admin_credentials["username"], admin_credentials["password"]
            )

            # we re-authenticate as the admin user:
            logger.info(
                "Authenticate as admin user -> %s...", admin_credentials["username"]
            )
            # True = force new login with new user
            cookie = self._otcs.authenticate(True)

        if success:
            self.writeStatusFile(section_name, self._users)

        return success

        # end method definition

    def processSecurityClearances(
        self, section_name: str = "securityClearances"
    ) -> bool:
        """Process Security Clearances for Extended ECM.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._security_clearances:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for security_clearance in self._security_clearances:
            clearance_level = security_clearance.get("level")
            clearance_name = security_clearance.get("name")

            if "enabled" in security_clearance and not security_clearance["enabled"]:
                logger.info(
                    "Payload for Security Clearance -> %s is disabled. Skipping...",
                    clearance_name,
                )
                continue

            clearance_description = security_clearance.get("description")
            if not clearance_description:
                clearance_description = ""
            if clearance_level and clearance_name:
                logger.info(
                    "Creating Security Clearance -> %s : %s",
                    clearance_level,
                    clearance_name,
                )
                self._otcs.runWebReport(
                    "web_report_security_clearance", security_clearance
                )
            else:
                logger.error(
                    "Cannot create Security Clearance - either level or name is missing!"
                )
                success = False

        if success:
            self.writeStatusFile(section_name, self._security_clearances)

        return success

        # end method definition

    def processSupplementalMarkings(
        self, section_name: str = "supplementalMarkings"
    ) -> bool:
        """Process Supplemental Markings for Extended ECM.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._supplemental_markings:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for supplemental_marking in self._supplemental_markings:
            code = supplemental_marking.get("code")

            if (
                "enabled" in supplemental_marking
                and not supplemental_marking["enabled"]
            ):
                logger.info(
                    "Payload for Supplemental Marking -> %s is disabled. Skipping...",
                    code,
                )
                continue

            description = supplemental_marking.get("description")
            if not description:
                description = ""
            if code:
                logger.info(
                    "Creating Supplemental Marking -> %s : %s", code, description
                )
                self._otcs.runWebReport(
                    "web_report_supplemental_marking", supplemental_marking
                )
            else:
                logger.error(
                    "Cannot create Supplemental Marking - either code or description is missing!"
                )
                success = False

        if success:
            self.writeStatusFile(section_name, self._supplemental_markings)

        return success

        # end method definition

    def processUserSecurity(self, section_name: str = "userSecurity"):
        """Process Security Clearance and Supplemental Markings for Extended ECM users.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._users:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for user in self._users:
            user_id = user.get("id")
            user_name = user.get("name")

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> %s is disabled. Skipping...", user_name
                )
                continue

            # Read security clearance from user payload (it is optional!)
            user_security_clearance = user.get("security_clearance")
            if user_id and user_security_clearance:
                self._otcs.assignUserSecurityClearance(user_id, user_security_clearance)

            # Read supplemental markings from user payload (it is optional!)
            user_supplemental_markings = user.get("supplemental_markings")
            if user_id and user_supplemental_markings:
                self._otcs.assignUserSupplementalMarkings(
                    user_id, user_supplemental_markings
                )

        if success:
            self.writeStatusFile(section_name, self._users)

        return success

        # end method definition

    def processRecordsManagementSettings(
        self, section_name: str = "recordsManagementSettings"
    ):
        """Process Records Management Settings for Extended ECM.
        The setting files need to be placed in the OTCS file system file via
        a transport into the Support Asset Volume.

        Args: None
        Return: None
        """

        if not self._records_management_settings:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        if (
            "records_management_system_settings" in self._records_management_settings
            and self._records_management_settings["records_management_system_settings"]
            != ""
        ):
            filename = (
                self._custom_settings_dir
                + self._records_management_settings[
                    "records_management_system_settings"
                ]
            )
            response = self._otcs.importRecordsManagementSettings(filename)
            if not response:
                success = False

        if (
            "records_management_codes" in self._records_management_settings
            and self._records_management_settings["records_management_codes"] != ""
        ):
            filename = (
                self._custom_settings_dir
                + self._records_management_settings["records_management_codes"]
            )
            response = self._otcs.importRecordsManagementCodes(filename)
            if not response:
                success = False

        if (
            "records_management_rsis" in self._records_management_settings
            and self._records_management_settings["records_management_rsis"] != ""
        ):
            filename = (
                self._custom_settings_dir
                + self._records_management_settings["records_management_rsis"]
            )
            response = self._otcs.importRecordsManagementRSIs(filename)
            if not response:
                success = False

        if (
            "physical_objects_system_settings" in self._records_management_settings
            and self._records_management_settings["physical_objects_system_settings"]
            != ""
        ):
            filename = (
                self._custom_settings_dir
                + self._records_management_settings["physical_objects_system_settings"]
            )
            response = self._otcs.importPhysicalObjectsSettings(filename)
            if not response:
                success = False

        if (
            "physical_objects_codes" in self._records_management_settings
            and self._records_management_settings["physical_objects_codes"] != ""
        ):
            filename = (
                self._custom_settings_dir
                + self._records_management_settings["physical_objects_codes"]
            )
            response = self._otcs.importPhysicalObjectsCodes(filename)
            if not response:
                success = False

        if (
            "physical_objects_locators" in self._records_management_settings
            and self._records_management_settings["physical_objects_locators"] != ""
        ):
            filename = (
                self._custom_settings_dir
                + self._records_management_settings["physical_objects_locators"]
            )
            response = self._otcs.importPhysicalObjectsLocators(filename)
            if not response:
                success = False

        if (
            "security_clearance_codes" in self._records_management_settings
            and self._records_management_settings["security_clearance_codes"] != ""
        ):
            filename = (
                self._custom_settings_dir
                + self._records_management_settings["security_clearance_codes"]
            )
            response = self._otcs.importSecurityClearanceCodes(filename)
            if not response:
                success = False

        if success:
            self.writeStatusFile(section_name, self._records_management_settings)

        return success

        # end method definition

    def processHolds(self, section_name: str = "holds") -> bool:
        """Process Records Management Holds for Extended ECM users.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._holds:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for hold in self._holds:
            if not "name" in hold:
                logger.error("Cannot create Hold without a name! Skipping...")
                continue
            hold_name = hold["name"]

            if not "type" in hold:
                logger.error(
                    "Cannot create Hold -> %s without a type! Skipping...", hold_name
                )
                success = False
                continue
            hold_type = hold["type"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in hold and not hold["enabled"]:
                logger.info(
                    "Payload for Hold -> %s is disabled. Skipping...", hold_name
                )
                continue

            hold_group = hold.get("group")
            hold_comment = hold.get("comment")
            hold_alternate_id = hold.get("alternate_id")
            hold_date_applied = hold.get("date_applied")
            hold_date_suspend = hold.get("date_to_remove")

            if hold_group:
                # Check if the Hold Group (folder) does already exist.
                # 2122 is the ID of the "Hold Maintenance" top level
                # folder in Records Management area that (we hope) will remain
                # stable:
                response = self._otcs.getNodeByParentAndName(2122, hold_group)
                parent_id = self._otcs.getResultValue(response, "id")
                if not parent_id:
                    response = self._otcs.createItem(2122, "833", hold_group)
                    parent_id = self._otcs.getResultValue(response, "id")
            else:
                parent_id = 2122

            # Holds are special - they ahve folders that cannot be traversed
            # in the normal way - we need to get the whole list of holds and use
            # specialparameters for the existResultItems() method as the REST
            # API calls delivers a results->data->holds structure (not properties)
            response = self._otcs.getRecordsManagementHolds()
            if self._otcs.existResultItem(
                response, "HoldName", hold_name, property_name="holds"
            ):
                logger.info("Hold -> %s does already exist. Skipping...", hold_name)
                continue

            hold = self._otcs.createRecordsManagementHold(
                hold_type,
                hold_name,
                hold_comment,
                hold_alternate_id,
                int(parent_id),
                hold_date_applied,
                hold_date_suspend,
            )

            if hold and hold["holdID"]:
                logger.info(
                    "Successfully created hold -> %s with ID -> %s",
                    hold_name,
                    hold["holdID"],
                )
            else:
                success = False

        if success:
            self.writeStatusFile(section_name, self._holds)

        return success

        # end method definition

    def processAdditionalGroupMembers(
        self, section_name: str = "additionalGroupMemberships"
    ) -> bool:
        """Process additional groups memberships we want to have in OTDS.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._additional_group_members:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for additional_group_member in self._additional_group_members:
            if not "parent_group" in additional_group_member:
                logger.error("Missing parent_group! Skipping...")
                continue
            parent_group = additional_group_member["parent_group"]

            if (
                "enabled" in additional_group_member
                and not additional_group_member["enabled"]
            ):
                logger.info(
                    "Payload for Additional Group Member with Parent Group -> %s is disabled. Skipping...",
                    parent_group,
                )
                continue

            if (not "user_name" in additional_group_member) and (
                not "group_name" in additional_group_member
            ):
                logger.error(
                    "Either group_name or user_name need to be specified! Skipping..."
                )
                success = False
                continue
            if "group_name" in additional_group_member:
                group_name = additional_group_member["group_name"]
                logger.info(
                    "Adding group -> %s to parent group -> %s in OTDS.",
                    group_name,
                    parent_group,
                )
                response = self._otds.addGroupToParentGroup(group_name, parent_group)
                if not response:
                    logger.error(
                        "Failed to add group -> %s to parent group -> %s in OTDS.",
                        group_name,
                        parent_group,
                    )
                    success = False
            elif "user_name" in additional_group_member:
                user_name = additional_group_member["user_name"]
                logger.info(
                    "Adding user -> %s to group -> %s in OTDS.", user_name, parent_group
                )
                response = self._otds.addUserToGroup(user_name, parent_group)
                if not response:
                    logger.error(
                        "Failed to add user -> %s to group -> %s in OTDS.",
                        user_name,
                        parent_group,
                    )
                    success = False

        if success:
            self.writeStatusFile(section_name, self._additional_group_members)

        return success

        # end method definition

    def processAdditionalAccessRoleMembers(
        self, section_name: str = "additionalAccessRoleMemberships"
    ) -> bool:
        """Process additional access role memberships we want to have in OTDS.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._additional_access_role_members:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for additional_access_role_member in self._additional_access_role_members:
            if not "access_role" in additional_access_role_member:
                logger.error("Missing access_role! Skipping...")
                continue
            access_role = additional_access_role_member["access_role"]

            if (
                "enabled" in additional_access_role_member
                and not additional_access_role_member["enabled"]
            ):
                logger.info(
                    "Payload for Additional Member for AccessRole -> %s is disabled. Skipping...",
                    access_role,
                )
                continue

            if (
                (not "user_name" in additional_access_role_member)
                and (not "group_name" in additional_access_role_member)
                and (not "partition_name" in additional_access_role_member)
            ):
                logger.error(
                    "Either group_name or user_name need to be specified! Skipping..."
                )
                success = False
                continue
            if "group_name" in additional_access_role_member:
                group_name = additional_access_role_member["group_name"]
                logger.info(
                    "Adding group -> %s to access role -> %s in OTDS.",
                    group_name,
                    access_role,
                )
                response = self._otds.addGroupToAccessRole(access_role, group_name)
                if not response:
                    logger.error(
                        "Failed to add group -> %s to access role -> %s in OTDS.",
                        group_name,
                        access_role,
                    )
                    success = False
            elif "user_name" in additional_access_role_member:
                user_name = additional_access_role_member["user_name"]
                logger.info(
                    "Adding user -> %s to access role -> %s in OTDS.",
                    user_name,
                    access_role,
                )
                response = self._otds.addUserToAccessRole(access_role, user_name)
                if not response:
                    logger.error(
                        "Failed to add user -> %s to access role -> %s in OTDS.",
                        user_name,
                        access_role,
                    )
                    success = False
            elif "partition_name" in additional_access_role_member:
                partition_name = additional_access_role_member["partition_name"]
                logger.info(
                    "Adding partition -> %s to access role -> %s in OTDS.",
                    partition_name,
                    access_role,
                )
                response = self._otds.addPartitionToAccessRole(
                    access_role, partition_name
                )
                if not response:
                    logger.error(
                        "Failed to add partition -> %s to access role -> %s in OTDS.",
                        partition_name,
                        access_role,
                    )
                    success = False

        if success:
            self.writeStatusFile(section_name, self._additional_access_role_members)

        return success

        # end method definition

    def processRenamings(self, section_name: str = "renamings") -> bool:
        """Process renamings specified in payload and rename existing Extended ECM items.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._renamings:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for renaming in self._renamings:
            if not "nodeid" in renaming:
                if not "volume" in renaming:
                    logger.error(
                        "Renamings require either a node ID or a volume! Skipping to next renaming..."
                    )
                    continue
                # Determine object ID of volume:
                volume = self._otcs.getVolume(renaming["volume"])
                node_id = self._otcs.getResultValue(volume, "id")
            else:
                node_id = renaming["nodeid"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in renaming and not renaming["enabled"]:
                logger.info("Payload for Renaming is disabled. Skipping...")
                continue

            response = self._otcs.renameNode(
                int(node_id), renaming["name"], renaming["description"]
            )
            if not response:
                logger.error(
                    "Failed to rename node ID -> %s to new name -> %s.",
                    node_id,
                    renaming["name"],
                )
                success = False

        if success:
            self.writeStatusFile(section_name, self._renamings)

        return success

        # end method definition

    def processItems(self, items: list, section_name: str = "items") -> bool:
        """Process items specified in payload and create them in Extended ECM.

        Args:
            items: list of items to create (need this as parameter as we
                   have multiple lists)
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not items:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)

            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for item in items:
            if not "name" in item:
                logger.error("Item needs a name. Skipping...")
                continue
            item_name = item["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in item and not item["enabled"]:
                logger.info(
                    "Payload for Item -> %s is disabled. Skipping...", item_name
                )
                continue

            if not "description" in item:
                item_description = ""
            else:
                item_description = item["description"]

            parent_nickname = item.get("parent_nickname")
            parent_path = item.get("parent_path")

            if parent_nickname:
                parent_node = self._otcs.getNodeFromNickname(parent_nickname)
                parent_id = self._otcs.getResultValue(parent_node, "id")
                # if not parent_node:
                if not parent_id:
                    logger.error(
                        "Item -> %s has a parent nickname -> %s that does not exist. Skipping...",
                        item_name,
                        parent_nickname,
                    )
                    success = False
                    continue
            else:  # use parent_path and Enterprise Volume
                parent_node = self._otcs.getNodeByVolumeAndPath(141, parent_path)
                parent_id = self._otcs.getResultValue(parent_node, "id")
                if not parent_id:
                    # if not parent_node:
                    logger.error(
                        "Item -> %s has a parent path that does not exist. Skipping...",
                        item_name,
                    )
                    success = False
                    continue

            original_nickname = item.get("original_nickname")
            original_path = item.get("original_path")

            if original_nickname:
                original_node = self._otcs.getNodeFromNickname(original_nickname)
                original_id = self._otcs.getResultValue(original_node, "id")
                if not original_id:
                    # if not original_node:
                    logger.error(
                        "Item -> %s has a original nickname -> %s that does not exist. Skipping...",
                        item_name,
                        original_nickname,
                    )
                    success = False
                    continue
            elif original_path:
                original_node = self._otcs.getNodeByVolumeAndPath(141, original_path)
                original_id = self._otcs.getResultValue(original_node, "id")
                if not original_id:
                    # if not original_node:
                    logger.error(
                        "Item -> %s has a original path that does not exist. Skipping...",
                        item_name,
                    )
                    success = False
                    continue
            else:
                original_id = 0

            if not "type" in item:
                logger.error("Item -> %s needs a type. Skipping...", item_name)
                success = False
                continue

            item_type = item.get("type")
            item_url = item.get("url")

            # check that we have the required information
            # for the given item type:
            match item_type:
                case 140:  # URL
                    if item_url == "":
                        logger.error(
                            "Item -> %s has type URL but the URL is not in the payload. Skipping...",
                            item_name,
                        )
                        success = False
                        continue
                case 1:  # Shortcut
                    if original_id == 0:
                        logger.error(
                            "Item -> %s has type Shortcut but the original item is not in the payload. Skipping...",
                            item_name,
                        )
                        success = False
                        continue

            # Check if an item with the same name does already exist.
            # This can also be the case if the python container runs a 2nd time.
            # For this reason we are also not issuing an error but just an info (False):
            response = self._otcs.getNodeByParentAndName(
                int(parent_id), item_name, show_error=False
            )
            if self._otcs.getResultValue(response, "name") == item_name:
                logger.info(
                    "Item with name -> %s does already exist in parent folder with ID -> %s",
                    item_name,
                    parent_id,
                )
                continue
            response = self._otcs.createItem(
                int(parent_id),
                str(item_type),
                item_name,
                item_description,
                item_url,
                int(original_id),
            )
            if not response:
                logger.error("Failed to create item -> %s.", item_name)
                success = False

        if success:
            self.writeStatusFile(section_name, items)

        return success

        # end method definition

    def processPermissions(
        self, permissions: list, section_name: str = "permissions"
    ) -> bool:
        """Process items specified in payload and upadate permissions.

        Args:
            permissions: list of items to apply permissions to.
                         Each list item in the payload is a dict with this structure:
                            {
                                nodeid = "..."
                                volume = "..."
                                nickname = "..."
                                public_access_permissions = ["see", "see_content", ...]
                                owner_permissions = []
                                owner_group_permissions = []
                                groups = [
                                {
                                    name = "..."
                                    permissions = []
                                }
                                ]
                                users = [
                                {
                                    name = "..."
                                    permissions = []
                                }
                                ]
                                apply_to = 2
                            }

        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not permissions:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for permission in permissions:
            if (
                not "path" in permission
                and not "volume" in permission
                and not "nickname" in permission
            ):
                logger.error("Item to change permission is not specified. Skipping...")
                success = False
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in permission and not permission["enabled"]:
                logger.info("Payload for Permission is disabled. Skipping...")
                continue

            node_id = 0

            # Check if "volume" is in payload and not empty string:
            if "volume" in permission and permission["volume"]:
                volume_type = permission["volume"]
                logger.info(
                    "Found volume type -> %s in permission definition. Determine volume ID...",
                    volume_type,
                )
                volume = self._otcs.getVolume(volume_type)
                node_id = self._otcs.getResultValue(volume, "id")
                if not node_id:
                    logger.error(
                        "Illegal volume -> %s in permission specification. Skipping...",
                        volume_type,
                    )
                    success = False
                    continue
            else:
                continue

            # Check if "path" is in payload and not empty list
            # (path can be combined with volume so we need to take volume into account):
            if "path" in permission and permission["path"]:
                path = permission["path"]
                logger.info(
                    "Found path -> %s in permission definition. Determine node ID...",
                    path,
                )
                node = self._otcs.getNodeByVolumeAndPath(volume_type, path)
                node_id = self._otcs.getResultValue(node, "id")
                if not node_id:
                    logger.error("Path -> %s does not exist. Skipping...", path)
                    success = False
                    continue

            # Check if "nickname" is in payload and not empty string:
            if "nickname" in permission and permission["nickname"]:
                nickname = permission["nickname"]
                logger.info(
                    "Found nickname -> %s in permission definition. Determine node ID...",
                    nickname,
                )
                node = self._otcs.getNodeFromNickname(nickname)
                node_id = self._otcs.getResultValue(node, "id")
                if not node_id:
                    logger.error("Nickname -> {} does not exist. Skipping...")
                    success = False
                    continue
            else:
                continue

            # Now we should have a value for node_id:
            if not node_id:
                logger.error("No node ID found! Skipping permission...")
                success = False
                continue

            node_name = self._otcs.getResultValue(node, "name")
            logger.info(
                "Found node -> %s with ID -> %s to apply permission to.",
                node_name,
                node_id,
            )

            if "apply_to" in permission:
                apply_to = permission["apply_to"]
            else:
                apply_to = 2  # make item + sub-items the default

            # 1. Process Owner Permissions (list canbe empty!)
            if "owner_permissions" in permission:
                permissions = permission["owner_permissions"]
                logger.info(
                    "Update owner permissions for item -> %s to -> %s",
                    node_id,
                    permissions,
                )
                response = self._otcs.assignPermission(
                    int(node_id), "owner", 0, permissions, apply_to
                )
                if not response:
                    logger.error(
                        "Failed to update owner permissions for item -> %s.", node_id
                    )
                    success = False

            # 2. Process Owner Group Permissions
            if "owner_group_permissions" in permission:
                permissions = permission["owner_group_permissions"]
                logger.info(
                    "Update owner group permissions for item -> %s to -> %s",
                    node_id,
                    permissions,
                )
                response = self._otcs.assignPermission(
                    int(node_id), "group", 0, permissions, apply_to
                )
                if not response:
                    logger.error(
                        "Failed to update group permissions for item -> %s.", node_id
                    )
                    success = False

            # 3. Process Public Permissions
            if "public_permissions" in permission:
                permissions = permission["public_permissions"]
                logger.info(
                    "Update public permissions for item -> %s to -> %s",
                    node_id,
                    permissions,
                )
                response = self._otcs.assignPermission(
                    int(node_id), "public", 0, permissions, apply_to
                )
                if not response:
                    logger.error(
                        "Failed to update public permissions for item -> %s.", node_id
                    )
                    success = False
                    continue

            # 3. Process Assigned User Permissions (if specified and not empty)
            if "users" in permission and permission["users"]:
                users = permission["users"]
                for user in users:
                    if not "name" in user or not "permissions" in user:
                        logger.error(
                            "Missing user name or permissions in user permission specificiation. Cannot set user permissions. Skipping..."
                        )
                        success = False
                        continue
                    user_name = user["name"]
                    permissions = user["permissions"]
                    otcs_user = self._otcs.getUser(user_name, True)
                    if not otcs_user or not otcs_user["data"]:
                        logger.error(
                            "Cannot find user with name -> %s; cannot set user permissions. Skipping user...",
                            user_name,
                        )
                        success = False
                        continue
                    user_id = otcs_user["data"][0]["id"]
                    logger.info(
                        "Update user -> %s permissions for item -> %s to -> %s",
                        user_name,
                        node_id,
                        permissions,
                    )
                    response = self._otcs.assignPermission(
                        int(node_id), "custom", user_id, permissions, apply_to
                    )
                    if not response:
                        logger.error(
                            "Failed to update assigned user permissions for item -> %s.",
                            node_id,
                        )
                        success = False

            # 4. Process Assigned Group Permissions (if specified and not empty)
            if "groups" in permission and permission["groups"]:
                groups = permission["groups"]
                for group in groups:
                    if not "name" in group or not "permissions" in group:
                        logger.error(
                            "Missing group name or permissions in group permission specificiation. Cannot set group permissions. Skipping..."
                        )
                        continue
                    group_name = group["name"]
                    permissions = group["permissions"]
                    logger.info(
                        "Update group -> %s permissions for item -> %s to -> %s",
                        group_name,
                        node_id,
                        permissions,
                    )
                    otcs_group = self._otcs.getGroup(group_name, True)
                    if not otcs_group or not otcs_group["data"]:
                        logger.error(
                            "Cannot find group with name -> %s; cannot set group permissions. Skipping group...",
                            group_name,
                        )
                        success = False
                        continue
                    group_id = otcs_group["data"][0]["id"]
                    response = self._otcs.assignPermission(
                        int(node_id), "custom", group_id, permissions, apply_to
                    )
                    if not response:
                        logger.error(
                            "Failed to update assigned group permissions for item -> %s.",
                            node_id,
                        )
                        success = False

        if success:
            self.writeStatusFile(section_name, permissions)

        return success

        # end method definition

    def processAssignments(self, section_name: str = "assignments") -> bool:
        """Process assignments specified in payload and assign items (such as workspaces and
        items withnicknames) to users or groups.

        Args:
            None
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._assignments:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for assignment in self._assignments:
            # Sanity check: we need a subject - it's mandatory:
            if not "subject" in assignment:
                logger.error("Assignment needs a subject! Skipping assignment...")
                success = False
                continue
            subject = assignment["subject"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in assignment and not assignment["enabled"]:
                logger.info(
                    "Payload for Assignment -> %s is disabled. Skipping...", subject
                )
                continue

            # instruction is optional but we give a warning if they are missing:
            if not "instruction" in assignment:
                logger.warning("Assignment -> %s should have an instruction!", subject)
                instruction = ""
            else:
                instruction = assignment["instruction"]
            # Sanity check: we either need users or groups (or both):
            if not "groups" in assignment and not "users" in assignment:
                logger.error(
                    "Assignment -> %s needs groups or users! Skipping assignment...",
                    subject,
                )
                success = False
                continue
            # Check if a workspace is specified for the assignment and check it does exist:
            if "workspace" in assignment and assignment["workspace"]:
                workspace = next(
                    (
                        item
                        for item in self._workspaces
                        if item["id"] == assignment["workspace"]
                    ),
                    None,
                )
                if not workspace:
                    logger.error(
                        "Assignment -> %s has specified a not existing workspace -> %s! Skipping assignment...",
                        subject,
                        assignment["workspace"],
                    )
                    success = False
                    continue
                node_id = self.determineWorkspaceID(workspace)
                if not node_id:
                    logger.error(
                        "Assignment -> %s has specified a not existing workspace -> %s! Skipping assignment...",
                        subject,
                        assignment["workspace"],
                    )
                    success = False
                    continue
            # If we don't have a workspace then check if a nickname is specified for the assignment:
            elif "nickname" in assignment:
                response = self._otcs.getNodeFromNickname(assignment["nickname"])
                node_id = self._otcs.getResultValue(response, "id")
                if not node_id:
                    # if response == None:
                    logger.error(
                        "Assignment item with nickname -> %s not found",
                        assignment["nickname"],
                    )
                    success = False
                    continue
            else:
                logger.error(
                    "Assignment -> %s needs a workspace or nickname! Skipping assignment...",
                    subject,
                )
                success = False
                continue

            assignees = []

            if "groups" in assignment:
                group_assignees = assignment["groups"]
                for group_assignee in group_assignees:
                    # find the group in the group list
                    group = next(
                        (
                            item
                            for item in self._groups
                            if item["name"] == group_assignee
                        ),
                        None,
                    )
                    if not group:
                        logger.error(
                            "Assignment group -> %s does not exist! Skipping group...",
                            group_assignee,
                        )
                        success = False
                        continue
                    if not "id" in group:
                        logger.error(
                            "Assignment group -> %s does not have an ID. Skipping group...",
                            group_assignee,
                        )
                        success = False
                        continue
                    group_id = group["id"]
                    # add the group ID to the assignee list:
                    assignees.append(group_id)

            if "users" in assignment:
                user_assignees = assignment["users"]
                for user_assignee in user_assignees:
                    # find the user in the user list
                    user = next(
                        (item for item in self._users if item["name"] == user_assignee),
                        None,
                    )
                    if not user:
                        logger.error(
                            "Assignment user -> %s does not exist! Skipping user...",
                            user_assignee,
                        )
                        success = False
                        continue
                    if not "id" in user:
                        logger.error(
                            "Assignment user -> %s does not have an ID. Skipping user...",
                            user_assignee,
                        )
                        success = False
                        continue
                    user_id = user["id"]
                    # add the group ID to the assignee list:
                    assignees.append(user_id)

            if not assignees:
                logger.error(
                    "Cannot add assignment -> %s for node ID -> %s because no assignee was found.",
                    subject,
                    node_id,
                )
                success = False
                continue

            response = self._otcs.assignItemToUserGroup(
                int(node_id), subject, instruction, assignees
            )
            if not response:
                logger.error(
                    "Failed to add assignment -> %s for node ID -> %s with assignees -> %s.",
                    subject,
                    node_id,
                    assignees,
                )
                success = False

        if success:
            self.writeStatusFile(section_name, self._assignments)

        return success

        # end method definition

    def processUserLicenses(
        self,
        resource_name: str,
        license_feature: str,
        license_name: str,
        user_specific_payload_field: str = "licenses",
        section_name: str = "userLicenses",
    ) -> bool:
        """Assign a specific OTDS license feature to all Extended ECM users.
           This method is used for OTIV and Extended ECM licenses.

        Args:
            resource_name: name of the OTDS resource
            license_feature: license feature to assign to the user (product specific)
            license_name: Name of the license Key (e.g. "EXTENDED_ECM" or "INTELLIGENT_VIEWING")
            user_specific_payload_field: name of the user specific field in payload
                                         (if empty it will be ignored)
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._users:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        otds_resource = self._otds.getResource(resource_name)
        if not otds_resource:
            logger.error(
                "OTDS Resource -> {} not found. Cannot assign licenses to users."
            )
            return False

        user_partition = self._otcs.config()["partition"]
        if not user_partition:
            logger.error("OTCS user partition not found in OTDS!")
            return False

        for user in self._users:
            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> %s is disabled. Skipping...", user_name
                )
                continue

            if user_specific_payload_field and user_specific_payload_field in user:
                logger.info(
                    "Found specific license feature -> %s for User -> %s. Overwriting default license feature -> %s",
                    user[user_specific_payload_field],
                    user_name,
                    license_feature,
                )
                user_license_feature = user[user_specific_payload_field]
            else:  # use the default feature from the actual parameter
                user_license_feature = [license_feature]

            for license_feature in user_license_feature:
                if self._otds.isUserLicensed(
                    user_name=user_name,
                    resource_id=otds_resource["resourceID"],
                    license_feature=license_feature,
                    license_name=license_name,
                ):
                    logger.info(
                        "User -> %s is already licensed for -> %s (%s)",
                        user_name,
                        license_name,
                        license_feature,
                    )
                    continue
                assigned_license = self._otds.assignUserToLicense(
                    user_partition,
                    user_name,  # we want the plain login name here
                    otds_resource["resourceID"],
                    license_feature,
                    license_name,
                )

                if not assigned_license:
                    logger.error(
                        "Failed to assign license feature -> %s to user -> %s!",
                        license_feature,
                        user_name,
                    )
                    success = False

        if success:
            self.writeStatusFile(section_name, self._users)

        return success

        # end method definition

    def processExecPodCommands(self, section_name: str = "execPodCommands") -> bool:
        """Process commands that should be executed in the Kubernetes pods.

        Args:
            None
        Return:
            None
        """

        if not isinstance(self._k8s, K8s):
            logger.error("K8s not setup properly -> Skipping %s...", section_name)
            return False

        if not self._exec_pod_commands:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for exec_pod_command in self._exec_pod_commands:
            if not "pod_name" in exec_pod_command:
                logger.error(
                    "To execute a command in a pod the pod name needs to be specified in the payload! Skipping to next pod command..."
                )
                success = False
                continue
            pod_name = exec_pod_command["pod_name"]

            if not "command" in exec_pod_command or not exec_pod_command.get("command"):
                logger.error(
                    "Pod command is not specified for pod -> %s! It needs to be a non-empty list! Skipping to next pod command...",
                    pod_name,
                )
                success = False
                continue
            command = exec_pod_command["command"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in exec_pod_command and not exec_pod_command["enabled"]:
                logger.info(
                    "Payload for Exec Pod Command in pod -> %s is disabled. Skipping...",
                    pod_name,
                )
                continue

            if not "description" in exec_pod_command:
                logger.info("Executing command -> %s in pod -> %s", command, pod_name)

            else:
                description = exec_pod_command["description"]
                logger.info(
                    "Executing command -> %s in pod -> %s (%s)",
                    command,
                    pod_name,
                    description,
                )

            if (
                not "interactive" in exec_pod_command
                or exec_pod_command["interactive"] is False
            ):
                result = self._k8s.execPodCommand(pod_name, command)
            else:
                if not "timeout" in exec_pod_command:
                    result = self._k8s.execPodCommandInteractive(pod_name, command)
                else:
                    timeout = exec_pod_command["timeout"]
                    result = self._k8s.execPodCommandInteractive(
                        pod_name, command, timeout
                    )

            if result:
                logger.info(
                    "Execution of command -> %s in pod -> %s returned result -> %s",
                    command,
                    pod_name,
                    result,
                )
            else:
                # It is not an error if no result is returned. It depends on the nature of the command
                # if a result is written to stdout or stderr.
                logger.info(
                    "Execution of command -> %s in pod -> %s did not return a result (%s)",
                    command,
                    pod_name,
                    result,
                )

        if success:
            self.writeStatusFile(section_name, self._exec_pod_commands)

        return success

        # end method definition

    def processDocumentGenerators(
        self, section_name: str = "documentGenerators"
    ) -> bool:
        """Generate documents for a defined workspace type based on template

        Args:
            None
        Returns:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._doc_generators:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        # save admin credentials for later switch back to admin user:
        admin_credentials = self._otcs.credentials()
        authenticated_user = "admin"

        for doc_generator in self._doc_generators:
            if not "workspace_type" in doc_generator:
                logger.error(
                    "To generate documents for workspaces the workspace type needs to be specified in the payload! Skipping to next document generator..."
                )
                success = False
                continue
            workspace_type = doc_generator["workspace_type"]

            if not "template_path" in doc_generator:
                logger.error(
                    "To generate documents for workspaces of type -> %s the path to the document template needs to be specified in the payload! Skipping to next document generator...",
                    workspace_type,
                )
                success = False
                continue
            template_path = doc_generator["template_path"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in doc_generator and not doc_generator["enabled"]:
                logger.info(
                    "Payload for document generator of workspace type -> %s and template path -> %s is disabled. Skipping...",
                    workspace_type,
                    template_path,
                )
                continue

            if not "classification_path" in doc_generator:
                logger.error(
                    "To generate documents for workspaces of type -> %s the path to the document classification needs to be specified in the payload! Skipping to next document generator...",
                    workspace_type,
                )
                success = False
                continue
            classification_path = doc_generator["classification_path"]

            if not "category_name" in doc_generator:
                logger.error(
                    "To generate documents for workspaces of type -> %s the category name needs to be specified in the payload! Skipping to next document generator...",
                    workspace_type,
                )
                success = False
                continue
            category_name = doc_generator["category_name"]

            if not "attributes" in doc_generator:
                logger.error(
                    "To generate documents for workspaces of type -> %s the attributes needs to be specified in the payload! Skipping to next document generator...",
                    workspace_type,
                )
                success = False
                continue
            attributes = doc_generator["attributes"]

            if not "workspace_folder_path" in doc_generator:
                logger.info(
                    "No workspace folder path defined for workspaces of type -> %s. Documents will be stored in workspace root.",
                    workspace_type,
                )
                workspace_folder_path = []
            else:
                workspace_folder_path = doc_generator["workspace_folder_path"]

            if "exec_as_user" in doc_generator:
                exec_as_user = doc_generator["exec_as_user"]

                # Find the user in the users payload:
                exec_user = next(
                    (item for item in self._users if item["name"] == exec_as_user),
                    None,
                )
                # Have we found the user in the payload?
                if exec_user is not None:
                    logger.info(
                        "Executing document generator with user -> %s", exec_as_user
                    )
                    # we change the otcs credentials to the user:
                    self._otcs.setCredentials(exec_user["name"], exec_user["password"])

                    # we re-authenticate as the user:
                    logger.info("Authenticate user -> %s...", exec_as_user)
                    # True = force new login with new user
                    cookie = self._otcs.authenticate(True)
                    if not cookie:
                        logger.error("Couldn't authenticate user -> %s", exec_as_user)
                        continue
                    admin_context = False
                    authenticated_user = exec_as_user
                else:
                    logger.error(
                        "Cannot find user with login name -> %s for executing. Executing as admin...",
                        exec_as_user,
                    )
                    admin_context = True
                    success = False
            else:
                admin_context = True

            if admin_context and authenticated_user != "admin":
                # Set back admin credentials:
                self._otcs.setCredentials(
                    admin_credentials["username"], admin_credentials["password"]
                )

                # we re-authenticate as the admin user:
                logger.info(
                    "Authenticate as admin user -> %s...", admin_credentials["username"]
                )
                # True = force new login with new user
                cookie = self._otcs.authenticate(True)
                authenticated_user = "admin"

            template = self._otcs.getNodeByVolumeAndPath(20541, template_path)
            template_id = self._otcs.getResultValue(template, "id")
            template_name = self._otcs.getResultValue(template, "name")
            classification = self._otcs.getNodeByVolumeAndPath(198, classification_path)
            classification_id = self._otcs.getResultValue(classification, "id")

            category_id, attribute_definitions = self._otcs.getNodeCategoryDefinition(
                template_id, category_name
            )
            logger.info(
                "Category ID -> %s, Attribute definitions -> %s",
                category_id,
                attribute_definitions,
            )

            category_data = {str(category_id): {}}

            for attribute in attributes:
                attribute_name = attribute["name"]
                attribute_value = attribute["value"]
                attribute_type = attribute_definitions[attribute_name]["type"]
                attribute_id = attribute_definitions[attribute_name]["id"]

                # Special treatment for type user: determine the ID for the login name.
                # the ID is the actual value we have to put in the attribute:
                if attribute_type == "user":
                    user = self._otcs.getUser(attribute_value, show_error=True)

                    if not user or not user["data"]:
                        logger.error(
                            "Cannot find user with login name -> %s. Skipping...",
                            attribute_value,
                        )
                        success = False
                        continue
                    attribute_value = user["data"][0]["id"]

                category_data[str(category_id)][attribute_id] = attribute_value

            logger.info(
                "Generate documents for workspace type -> %s based on template -> %s with metadata -> %s...",
                workspace_type,
                template_name,
                category_data,
            )

            workspace_instances = self._otcs.getWorkspaceInstances(workspace_type)
            for workspace_instance in workspace_instances["results"]:
                workspace_id = workspace_instance["data"]["properties"]["id"]
                workspace_name = workspace_instance["data"]["properties"]["name"]
                if workspace_folder_path:
                    workspace_folder = self._otcs.getNodeByWorkspaceAndPath(
                        workspace_id, workspace_folder_path
                    )
                    if workspace_folder:
                        workspace_folder_id = self._otcs.getResultValue(
                            workspace_folder, "id"
                        )
                    else:
                        # If the workspace template is not matching
                        # the path we may have an error here. Then
                        # we fall back to workspace root level.
                        logger.info(
                            "Folder path does not exist in workspace -> %s. Using workspace root level instead...",
                            workspace_name,
                        )
                        workspace_folder_id = workspace_id
                else:
                    workspace_folder_id = workspace_id

                document_name = workspace_name + " - " + template_name

                response = self._otcs.checkNodeName(
                    int(workspace_folder_id), document_name
                )
                if response["results"]:
                    logger.warning(
                        "Node with name -> %s does already exist in workspace folder with ID -> %s",
                        document_name,
                        workspace_folder_id,
                    )
                    continue
                response = self._otcs.createDocumentFromTemplate(
                    int(template_id),
                    int(workspace_folder_id),
                    int(classification_id),
                    category_data,
                    document_name,
                    "This document has been auto-generated by Terrarium",
                )
                if not response:
                    logger.error(
                        "Failed to generate document -> %s in workspace -> %s",
                        document_name,
                        workspace_name,
                    )
                    success = False
                else:
                    logger.info(
                        "Successfully generated document -> %s in workspace -> %s",
                        document_name,
                        workspace_name,
                    )

        if authenticated_user != "admin":
            # Set back admin credentials:
            self._otcs.setCredentials(
                admin_credentials["username"], admin_credentials["password"]
            )

            # we authenticate back as the admin user:
            logger.info(
                "Authenticate as admin user -> %s...", admin_credentials["username"]
            )
            # True = force new login with new user
            cookie = self._otcs.authenticate(True)

        if success:
            self.writeStatusFile(section_name, self._doc_generators)

        return success

        # end method definition

    def initSAP(
        self, sap_external_system: dict, direct_application_server_login: bool = True
    ) -> SAP | None:
        """Initialize SAP object for RFC communication with SAP S/4HANA.

        Args:
            sap_external_system (dictionary): SAP external system created before
            direct_application_server_login (boolean): flag to control wether we comminicate directly with
                                                       SAP application server or via a load balancer
        Return: sap_object
        """

        if not sap_external_system:
            return None

        username = sap_external_system["username"]
        password = sap_external_system["password"]
        # "external_system_hostname" is extracted from as_url in processExternalSystems()
        host = sap_external_system["external_system_hostname"]
        client = sap_external_system.get("client", "100")
        system_number = sap_external_system.get("external_system_number", "00")
        system_id = sap_external_system["external_system_name"]
        group = sap_external_system.get("group", "PUBLIC")
        destination = sap_external_system.get("destination", "")

        logger.info("Connection parameters SAP:")
        logger.info("SAP Hostname             = %s", host)
        logger.info("SAP Client               = %s", client)
        logger.info("SAP System Number        = %s", system_number)
        logger.info("SAP System ID            = %s", system_id)
        logger.info("SAP User Name            = %s", username)
        if not direct_application_server_login:
            logger.info("SAP Group Name (for RFC) = %s", group)
        if destination:
            logger.info("SAP Destination          = %s", destination)

        if direct_application_server_login:
            logger.info("SAP Login                = Direct Application Server (ashost)")
            sap_object = SAP(
                username=username,
                password=password,
                ashost=host,
                client=client,
                system_number=system_number,
                system_id=system_id,
                destination=destination,
            )
        else:
            logger.info("SAP Login                = Logon with load balancing (mshost)")
            sap_object = SAP(
                username=username,
                password=password,
                mshost=host,
                group=group,
                client=client,
                system_number=system_number,
                system_id=system_id,
                destination=destination,
            )

        return sap_object

        # end method definition

    def processSAPRFCs(self, sap_object: SAP, section_name: str = "sapRFCs") -> bool:
        """Process SAP RFCs in payload and run them in SAP S/4HANA.

        Args:
            sap_object: SAP object
        Return:
            bool: True if payload has been processed without errors, False otherwise
        """

        if not self._doc_generators:
            logger.info("Payload section -> %s is empty. Skipping...", section_name)
            return True

        # if this payload section has been processed successfully before we can return True
        # and skip processing once more
        if self.checkStatusFile(section_name):
            return True

        success: bool = True

        for sap_rfc in self._sap_rfcs:
            rfc_name = sap_rfc["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in sap_rfc and not sap_rfc["enabled"]:
                logger.info(
                    "Payload for SAP RFC -> %s is disabled. Skipping...", rfc_name
                )
                continue

            rfc_description = (
                sap_rfc["description"] if sap_rfc.get("description") else ""
            )

            # be careful to avoid key errors as SAP RFC parameters are optional:
            rfc_params = sap_rfc["parameters"] if sap_rfc.get("parameters") else {}
            if rfc_params:
                logger.info(
                    "Calling SAP RFC -> %s (%s) with parameters -> %s ...",
                    rfc_name,
                    rfc_description,
                    rfc_params,
                )
            else:
                logger.info(
                    "Calling SAP RFC -> %s (%s) without parameters...",
                    rfc_name,
                    rfc_description,
                )

            # be careful to avoid key errors as SAP RFC parameters are optional:
            rfc_call_options = (
                sap_rfc["call_options"] if sap_rfc.get("call_options") else {}
            )
            if rfc_call_options:
                logger.debug("Using call options -> %s ...", rfc_call_options)

            result = sap_object.call(rfc_name, rfc_call_options, rfc_params)
            if result is None:
                logger.error("Failed to call SAP RFC -> %s", rfc_name)
                success = False
            else:
                logger.info(
                    "Successfully called RFC -> %s. Result -> %s", rfc_name, result
                )

        if success:
            self.writeStatusFile(section_name, self._sap_rfcs)

        return success

        # end method definition

    def getPayload(self) -> dict:
        """Get the Payload"""
        return self._payload

    def getUsers(self) -> list:
        """Get all useres"""
        return self._users

    def getGroups(self) -> list:
        """Get all groups"""
        return self._groups

    def getWorkspaces(self) -> list:
        """Get all workspaces"""
        return self._workspaces

    def getOTCSFrontend(self) -> object:
        """Get OTCS Frontend oject"""
        return self._otcs_frontend

    def getOTCSBackend(self) -> object:
        """Get OTCS Backend object"""
        return self._otcs_backend

    def getOTDS(self) -> object:
        """Get OTDS object"""
        return self._otds

    def getK8S(self) -> object:
        """Get K8s object"""
        return self._k8s

    def getM365(self) -> object:
        """Get M365 object"""
        return self._m365
