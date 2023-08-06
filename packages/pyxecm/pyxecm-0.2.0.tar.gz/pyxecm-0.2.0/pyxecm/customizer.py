"""[Automate OpenText Directory Services (OTDS) and Extended ECM (OTCS) configurations]

Functions:

init_m365: initialize the Microsoft 365 object
init_otds: initialize the OTDS object
init_otds: initialize the OTAC object
init_otcs: initialize the OTCS (Extended ECM) object
init_otpd: initialize the PowerDocs object
init_otawp: initialize OTDS settings for AppWorks Platform

restart_otcs_service: restart the OTCS backend and frontend pods -
                      required to make certain configurations effective
restart_otac_service: restart spawner process in Archive Center
consolidate_otds: consolidate OTDS users / groups (to get to a fully synchronized state)
restart_otawp_pod: restart the AppWorks Platform Pod to make settings effective

import_powerdocs_configuration: import PowerDocs database

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime

import requests
# OpenText specific modules:
import yaml
from pyxecm.k8s import K8s
from pyxecm.m365 import M365
from pyxecm.otac import OTAC
from pyxecm.otcs import OTCS
from pyxecm.otds import OTDS
from pyxecm.otiv import OTIV
from pyxecm.otpd import OTPD

logger = logging.getLogger("customizer")


@dataclass
class CustomizerSettings:
    """Class to manage settings"""

    placeholder_values = {}
    stop_on_error = os.environ.get("LOGLEVEL", "INFO") == "DEBUG"
    cust_log_file = "/tmp/customizing.log"
    customizer_start_time = customizer_end_time = datetime.now()

    # The following CUST artifacts are created by the main.tf in the python module:
    cust_settings_dir = "/settings/"
    cust_payload_dir = "/payload/"
    cust_payload = cust_payload_dir + "payload.yaml"
    cust_payload_external = "/payload-external/"

    cust_target_folder_nickname = (
        "deployment"  # nickname of folder to upload payload and log files
    )
    # CUST_RM_SETTINGS_DIR = "/opt/opentext/cs/appData/supportasset/Settings/"
    cust_rm_settings_dir = cust_settings_dir


@dataclass
class CustomizerSettingsOTDS:
    """Class for OTDS related settings"""

    protocol = os.environ.get("OTDS_PROTOCOL", "http")
    public_protocol = os.environ.get("OTDS_PUBLIC_PROTOCOL", "https")
    hostname = os.environ.get("OTDS_HOSTNAME", "otds")
    port = os.environ.get("OTDS_SERVICE_PORT_OTDS", 80)
    admin = os.environ.get("OTDS_ADMIN", "admin")
    admin_partition = "otds.admin"
    public_url = os.environ.get("OTDS_PUBLIC_URL", "otds.xecm.dev")
    password = os.environ.get("OTDS_PASSWORD", "Opentext1!")


@dataclass
class CustomizerSettingsOTCS:
    """Class for OTCS related settings"""

    # Content Server Constants:
    protocol = os.environ.get("OTCS_PROTOCOL", "http")
    public_protocol = os.environ.get("OTCS_PUBLIC_PROTOCOL", "https")
    hostname = hostname_backend = os.environ.get("OTCS_HOSTNAME", "otcs-admin-0")
    hostname_frontend = os.environ.get("OTCS_HOSTNAME_FRONTEND", "otcs-frontend")
    public_url = os.environ.get("OTCS_PUBLIC_URL", "otcs.xecm.dev")
    port = port_backend = os.environ.get("OTCS_SERVICE_PORT_OTCS", 8080)
    port_frontend = 80
    admin = os.environ.get("OTCS_ADMIN", "admin")
    password = os.environ.get("OTCS_PASSWORD", "Opentext1!")
    partition = os.environ.get("OTCS_PARTITION", "Content Server Members")
    resource_name = "cs"
    k8s_statefulset_frontend = "otcs-frontend"
    k8s_statefulset_backend = "otcs-admin"
    k8s_ingress = "otxecm-ingress"
    maintenance_mode = os.environ.get("OTCS_MAINTENANCE_MODE", "true").lower() == "true"
    license_feature = "X3"

    # K8s service name for maintenance pod
    maintenance_service_name = "maintenance"
    mainteance_service_port = 80  # K8s service name for maintenance pod

    replicas_frontend = 0
    replicas_backend = 0


@dataclass
class CustomizerSettingsOTAC:
    """Class for OTAC related settings"""

    enabled = os.environ.get("OTAC_ENABLED", True)
    hostname = os.environ.get("OTAC_SERVICE_HOST", "otac-0")
    port = os.environ.get("OTAC_SERVICE_PORT", 8080)
    protocol = os.environ.get("OTAC_PROTOCOL", "http")
    public_url = os.environ.get("OTAC_PUBLIC_URL", "otcs.xecm.dev")
    admin = os.environ.get("OTAC_ADMIN", "dsadmin")
    password = os.environ.get("OTAC_PASSWORD", "")
    known_server = os.environ.get("OTAC_KNOWN_SERVER", "")
    k8s_pod_name = "otac-0"


@dataclass
class CustomizerSettingsOTPD:
    """Class for OTPD related settings"""

    enabled = os.environ.get("OTPD_ENABLED", False)
    hostname = os.environ.get("OTPD_SERVICE_HOST", "otpd")
    port = os.environ.get("OTPD_SERVICE_PORT", 8080)
    protocol = os.environ.get("OTPD_PROTOCOL", "http")
    db_importfile = os.environ.get(
        "OTPD_DBIMPORTFILE", "URL://url.download.location/file.zip"
    )
    tenant = os.environ.get("OTPD_TENANT", "Successfactors")
    user = os.environ.get("OTPD_USER", "powerdocsapiuser")
    password = os.environ.get("OTPD_PASSWORD", "Opentext1!")
    k8s_pod_name = "otpd-0"


@dataclass
class CustomizerSettingsOTIV:
    """Class for OTIV related settings"""

    enabled = os.environ.get("OTIV_ENABLED", False)
    license_file = "/payload/otiv-license.lic"
    license_feature = "FULLTIME_USERS_REGULAR"
    product_name = "Viewing"
    product_description = "OpenText Intelligent Viewing"
    resource_name = "iv"


@dataclass
class CustomizerSettingsOTAWP:
    """Class for OTAWP related settings"""

    enabled = os.environ.get("OTAWP_ENABLED", False)
    resource_name = "awp"
    access_role_name = "Access to " + resource_name
    admin = os.environ.get("OTAWP_ADMIN", "sysadmin")
    password = os.environ.get("OTAWP_PASSWORD", "Opentext1!")
    public_protocol = os.environ.get("OTAWP_PROTOCOL", "https")
    public_url = os.environ.get("OTAWP_PUBLIC_URL", "otawp.xecm.dev")
    k8s_statefulset = "appworks"
    k8s_configmap = "appworks-config-ymls"


@dataclass
class CustomizerSettingsO365:
    """Class for O365 related settings"""

    enabled = os.environ.get("O365_ENABLED", False)
    """Enable/Disable the O365 Customization"""
    tenant_id = os.environ.get("O365_TENANT_ID", "")
    client_id = os.environ.get("O365_CLIENT_ID", "")
    client_secret = os.environ.get("O365_CLIENT_SECRET", "")
    user = os.environ.get("O365_USER", "")
    password = os.environ.get("O365_PASSWORD", "")
    domain = os.environ.get("O365_DOMAIN", "")
    sku_id = os.environ.get("O365_SKU_ID", "c7df2760-2c81-4ef7-b578-5b5392b571df")
    """Office 365 E5, used as default SKU for users (c7df2760-2c81-4ef7-b578-5b5392b571df)"""
    teams_app_name = "OpenText Extended ECM"
    """Name of the Microsoft Teams App (OpenText Extended ECM)"""


class Customizer:
    """Customizer Class to control the cusomization automation

    Args: None
    """

    def __init__(self):
        self.settings = CustomizerSettings()

        # OTDS Constants:
        self.otds = CustomizerSettingsOTDS()

        # Content Server Constants:
        self.otcs = CustomizerSettingsOTCS()

        # Archive Center constants:
        self.otac = CustomizerSettingsOTAC()

        # PowerDocs constants:
        self.otpd = CustomizerSettingsOTPD()

        # Intelligent Viewing constants:
        self.otiv = CustomizerSettingsOTIV()

        # AppWorks Platform constants:
        self.otawp = CustomizerSettingsOTAWP()

        # K8s Mode
        self.k8s_enabled = os.environ.get("K8S_ENABLED", "true").lower() == "true"

        # Microsoft 365 Environment variables:
        self.o365 = CustomizerSettingsO365()

        # Initialize Objects for later assignment
        self.otds_object: OTDS
        self.otcs_object: OTCS
        self.otcs_backend_object: OTCS
        self.otcs_frontend_object: OTCS
        self.otpd_object: OTPD | None
        self.otac_object: OTAC | None
        self.otiv_object: OTIV | None
        self.k8s_object: K8s
        self.m365_object: M365 | None

    def init_m365(self) -> M365:
        """Initialize the M365 object we use to talk to the Microsoft Graph API.

        Args:
            None
        Returns:
            object: M365 object or None if the object couldn't be created or
                    the authentication fails.
        """

        logger.info("Microsoft 365 Tenant ID             = %s", self.o365.tenant_id)
        logger.info("Microsoft 365 Client ID             = %s", self.o365.client_id)
        logger.debug(
            "Microsoft 365 Client Secret         = %s", self.o365.client_secret
        )
        logger.info(
            "Microsoft 365 User                  = %s",
            (self.o365.user if self.o365.user != "" else "<not configured>"),
        )
        logger.debug(
            "Microsoft 365 Password              = %s",
            (self.o365.password if self.o365.password != "" else "<not configured>"),
        )
        logger.info("Microsoft 365 Domain                = %s", self.o365.domain)
        logger.info("Microsoft 365 Default License SKU   = %s", self.o365.sku_id)
        logger.info(
            "Microsoft 365 Teams App             = %s", self.o365.teams_app_name
        )

        m365_object = M365(
            self.o365.tenant_id,
            self.o365.client_id,
            self.o365.client_secret,
            self.o365.domain,
            self.o365.sku_id,
            self.o365.teams_app_name,
        )

        if m365_object and m365_object.authenticate():
            logger.info("Connected to Microsoft Graph API.")
            return m365_object
        else:
            logger.error("Failed to connect to Microsoft Graph API.")
            return m365_object

        # end function definition

    def init_k8s(self, in_cluster: bool = True) -> K8s:
        """Initialize the Kubernetes object we use to talk to the Kubernetes API.

        Args:
            inCluster (boolean): controls wether the code runs inside a pod (inCluster = True)
                                or locally (access via .kube / kubectl, inCluster = False)
        Return:
            K8s object
            The global variables otcs_replicas_frontend and otcs_replicas_backend are initialized
        """

        logger.info("Connect to Kubernetes, inCluster -> %s", in_cluster)

        k8s_object = K8s(in_cluster)
        if k8s_object:
            logger.info("Kubernetes API is ready now.")
        else:
            logger.error("Cannot establish connection to Kubernetes.")

        # Get number of replicas for frontend:
        otcs_frontend_scale = k8s_object.getStatefulSetScale(
            self.otcs.k8s_statefulset_frontend
        )
        if not otcs_frontend_scale:
            logger.error(
                "Cannot find Kubernetes Stateful Set for OTCS Frontends -> %s",
                self.otcs.k8s_statefulset_frontend,
            )
            sys.exit()

        self.otcs.replicas_frontend = otcs_frontend_scale.spec.replicas  # type: ignore
        logger.info(
            "Stateful Set -> %s has -> %s replicas",
            self.otcs.k8s_statefulset_frontend,
            self.otcs.replicas_frontend,
        )

        # Get number of replicas for backend:
        otcs_backend_scale = k8s_object.getStatefulSetScale(
            self.otcs.k8s_statefulset_backend
        )
        if not otcs_backend_scale:
            logger.error(
                "Cannot find Kubernetes Stateful Set for OTCS Backends -> %s",
                self.otcs.k8s_statefulset_backend,
            )
            sys.exit()

        self.otcs.replicas_backend = otcs_backend_scale.spec.replicas  # type: ignore
        logger.info(
            "Stateful Set -> %s has -> %s replicas",
            self.otcs.k8s_statefulset_backend,
            self.otcs.replicas_backend,
        )

        return k8s_object

        # end function definition

    def init_otds(self) -> OTDS:
        """Initialize the OTDS object and parameters and authenticate at OTDS once it is ready.

        Args:
            None
        Returns:
            object: OTDS object
        """

        logger.info("Connection parameters OTDS:")
        logger.info("OTDS Protocol          = %s", self.otds.protocol)
        logger.info("OTDS Public Protocol   = %s", self.otds.public_protocol)
        logger.info("OTDS Hostname          = %s", self.otds.hostname)
        logger.info("OTDS Public URL        = %s", self.otds.public_url)
        logger.info("OTDS Port              = %s", str(self.otds.port))
        logger.info("OTDS Admin User        = %s", self.otds.admin)
        logger.debug("OTDS Admin Password   = %s", self.otds.password)
        logger.info("OTDS Admin Partition   = %s", self.otds.admin_partition)

        otds_object = OTDS(
            self.otds.protocol,
            self.otds.hostname,
            int(self.otds.port),
            self.otds.admin,
            self.otds.password,
        )

        logger.info("Authenticating to OTDS...")
        otds_cookie = otds_object.authenticate()
        while otds_cookie is None:
            logger.warning("Waiting 30 seconds for OTDS to become ready...")
            time.sleep(30)
            otds_cookie = otds_object.authenticate()
        logger.info("OTDS is ready now.")

        logger.info("Enable OTDS audit...")
        otds_object.enableAudit()

        return otds_object

        # end function definition

    def init_otac(self) -> OTAC:
        """Initialize the OTAC object and parameters.
          Configure the Archive Server as a known server
          if environment variable OTAC_KNOWN_SERVER is set.

        Args: None
        Return:
            OTAC object
        """

        logger.info("Connection parameters OTAC:")
        logger.info("OTAC Protocol          = %s", self.otac.protocol)
        logger.info("OTAC Hostname          = %s", self.otac.hostname)
        logger.info("OTAC Public URL        = %s", self.otac.public_url)
        logger.info("OTAC Port              = %s", str(self.otac.port))
        logger.info("OTAC Admin User        = %s", self.otac.admin)
        logger.debug("OTAC Admin Password   = %s", self.otac.password)
        logger.info(
            "OTAC Known Server      = %s",
            (
                self.otac.known_server
                if self.otac.known_server != ""
                else "<not configured>"
            ),
        )

        otac_object = OTAC(
            self.otac.protocol,
            self.otac.hostname,
            int(self.otac.port),
            self.otac.admin,
            self.otac.password,
            self.otds.admin,
            self.otds.password,
        )

        # is there a known server configured for Archive Center (to sync content with)
        if otac_object and self.otac.known_server != "":
            # wait until the OTAC pod is in ready state
            logger.info("Waiting for Archive Center to become ready...")
            self.k8s_object.waitPodCondition(self.otac.k8s_pod_name, "Ready")

            logger.info("Configure known host for Archive Center...")
            response = otac_object.execCommand(
                f"cf_create_host {self.otac.known_server} 0 /archive 8080 8090"
            )
            if not response or not response.ok:
                logger.error("Failed to configure known host for Archive Center!")

            logger.info("Configure host alias for Archive Center...")
            response = otac_object.execCommand(
                f"cf_set_variable MY_HOST_ALIASES {self.otac.k8s_pod_name},{self.otac.public_url},otac DS"
            )
            if not response or not response.ok:
                logger.error("Failed to configure host alias for Archive Center!")

            # Restart the spawner in Archive Center:
            logger.info("Restart Archive Center Spawner...")
            self.restart_otac_service()
        else:
            logger.info(
                "Skip configuration of known host for Archive Center (OTAC_KNOWN_SERVER is not set)."
            )

        return otac_object

        # end function definition

    def init_otcs(
        self,
        hostname: str,
        port: int,
        partition_name: str,
        resource_name: str,
    ) -> OTCS:
        """Initialize the OTCS class and parameters and authenticate at OTCS once it is ready.

        Args:
            hostname (string): OTCS hostname
            port (integer): port number of OTCS
            partition_name: name of OTDS Partition for Extended ECM users
            resource_name: name of OTDS resource for Extended ECM
        Returns:
            object: OTCS object
        """

        logger.info("Connection parameters OTCS (Extended ECM):")
        logger.info("OTCS Protocol              = %s", self.otcs.protocol)
        logger.info("OTCS Public Protocol       = %s", self.otcs.public_protocol)
        logger.info("OTCS Hostname              = %s", hostname)
        logger.info("OTCS Public URL            = %s", self.otcs.public_url)
        logger.info("OTCS Port                  = %s", str(port))
        logger.info("OTCS Admin User            = %s", self.otcs.admin)
        logger.debug("OTCS Admin Password       = %s", self.otcs.password)
        logger.info("OTCS User Partition        = %s", partition_name)
        logger.info("OTCS Resource Name         = %s", resource_name)
        logger.info("OTCS User Default License  = %s", self.otcs.license_feature)
        logger.info(
            "OTCS K8s Frontend Pods     = %s", self.otcs.k8s_statefulset_frontend
        )
        logger.info(
            "OTCS K8s Backend Pods      = %s", self.otcs.k8s_statefulset_backend
        )

        otcs_object = OTCS(
            self.otcs.protocol,
            hostname,
            int(port),
            self.otcs.admin,
            self.otcs.password,
            partition_name,
            resource_name,
        )

        # It is important to wait for OTCS to be configured - otherwise we
        # may interfere with the OTCS container automation and run into errors
        logger.info("Wait for OTCS to be configured...")
        otcs_configured = otcs_object.isConfigured()
        while not otcs_configured:
            logger.warning("OTCS is not configured yet. Waiting 30 seconds...")
            time.sleep(30)
            otcs_configured = otcs_object.isConfigured()
        logger.info("OTCS is configured now.")

        logger.info("Authenticating to OTCS...")
        otcs_cookie = otcs_object.authenticate()
        while otcs_cookie is None:
            logger.warning("Waiting 30 seconds for OTCS to become ready...")
            time.sleep(30)
            otcs_cookie = otcs_object.authenticate()
        logger.info("OTCS is ready now.")

        # Set first name and last name of Admin user (ID = 1000):
        otcs_object.updateUser(1000, field="first_name", value="Terrarium")
        otcs_object.updateUser(1000, field="last_name", value="Admin")

        if "OTCS_RESSOURCE_ID" not in self.settings.placeholder_values:
            self.settings.placeholder_values[
                "OTCS_RESSOURCE_ID"
            ] = self.otds_object.getResource(self.otcs.resource_name)["resourceID"]
            logger.debug(
                "Placeholder values after OTCS init = %s",
                self.settings.placeholder_values,
            )

        if self.otawp.enabled == "true":
            otcs_resource = self.otds_object.getResource(self.otcs.resource_name)
            otcs_resource[
                "logoutURL"
            ] = f"{self.otawp.public_protocol}://{self.otawp.public_url}/home/system/wcp/sso/sso_logout.htm"
            otcs_resource["logoutMethod"] = "GET"

            self.otds_object.updateResource(name="cs", resource=otcs_resource)

        # Allow impersonation of the resource for all users:
        self.otds_object.impersonateResource(resource_name)

        return otcs_object

        # end function definition

    def init_otiv(self) -> OTIV:
        """Initialize the OTIV (Intelligent Viewing) object and its OTDS settings.

        Args:
        Returns:
            objects: OTIV object
        """

        logger.info("Parameters for OTIV (Intelligent Viewing):")
        logger.info("OTDS Resource Name       = %s", self.otiv.resource_name)
        logger.info("OTIV License File        = %s", self.otiv.license_file)
        logger.info("OTIV Product Name        = %s", self.otiv.product_name)
        logger.info("OTIV Product Description = %s", self.otiv.product_description)
        logger.info("OTIV License Feature     = %s", self.otiv.license_feature)

        otiv_object = OTIV(
            self.otiv.resource_name,
            self.otiv.product_name,
            self.otiv.product_description,
            self.otiv.license_file,
            self.otiv.license_feature,
        )

        otds_resource = self.otds_object.getResource(self.otiv.resource_name)
        if not otds_resource:
            logger.error(
                "OTDS Resource -> {} for Intelligent Viewing not found. OTIV may not be ready."
            )
            sys.exit()

        otiv_license = self.otds_object.addLicenseToResource(
            self.otiv.license_file,
            self.otiv.product_name,
            self.otiv.product_description,
            otds_resource["resourceID"],
        )
        if not otiv_license:
            logger.info(
                "Couldn't apply license -> %s for product -> %s. Intelligent Viewing may not be deployed!",
                self.otiv.license_file,
                self.otiv.product_name,
            )
            sys.exit()

        return otiv_object

        # end function definition

    def init_otpd(self) -> OTPD:
        """Initialize the OTPD (PowerDocs) object and parameters.

        Args:
            None
        Returns:
            object: OTPD (PowerDocs) object
        """

        logger.info("Connection parameters OTPD (PowerDocs):")
        logger.info("OTPD Protocol             = %s", self.otpd.protocol)
        logger.info("OTPD Hostname             = %s", self.otpd.hostname)
        logger.info("OTPD Port                 = %s", str(self.otpd.port))
        logger.info("OTPD API User             = %s", self.otpd.user)
        logger.info("OTPD Tenant               = %s", self.otpd.tenant)
        logger.info(
            "OTPD Database Import File = %s",
            (
                self.otpd.db_importfile
                if self.otpd.db_importfile != ""
                else "<not configured>"
            ),
        )
        logger.info("OTPD K8s Pod Name         = %s", self.otpd.k8s_pod_name)

        otpd_object = OTPD(
            self.otpd.protocol,
            self.otpd.hostname,
            int(self.otpd.port),
            self.otpd.user,
            self.otpd.password,
        )

        # wait until the OTPD pod is in ready state
        self.k8s_object.waitPodCondition(self.otpd.k8s_pod_name, "Ready")

        # Fix settings for local Kubernetes deployments.
        # Unclear why this is not the default.
        if otpd_object:
            otpd_object.applySetting("LocalOtdsUrl", "http://otds/otdsws")
            otpd_object.applySetting(
                "LocalApplicationServerUrlForContentManager",
                "http://localhost:8080/c4ApplicationServer",
                self.otpd.tenant,
            )

        return otpd_object

        # end function definition

    def init_otawp(self):
        """Initialize OTDS for Appworks Platform
        Args:
        Return: None
        """

        logger.info("Connection parameters OTAWP:")
        logger.info("OTAWP Enabled          = %s", self.otawp.enabled)
        logger.info("OTAWP Resource         = %s", self.otawp.resource_name)
        logger.info("OTAWP Access Role      = %s", self.otawp.access_role_name)
        logger.info("OTAWP Admin User       = %s", self.otawp.admin)
        logger.debug("OTAWP Password         = %s", self.otawp.password)
        logger.info("OTAWP K8s Stateful Set = %s", self.otawp.k8s_statefulset)
        logger.info("OTAWP K8s Config Map   = %s", self.otawp.k8s_configmap)

        logger.info(
            "Wait for OTCS to create its OTDS resource with name -> %s...",
            self.otcs.resource_name,
        )

        # Loop to wait for OTCS to create its OTDS resource
        # (we need it to update the AppWorks K8s Config Map):
        otcs_resource = self.otds_object.getResource(self.otcs.resource_name)
        while otcs_resource is None:
            logger.warning(
                "OTDS resource for Content Server with name -> %s does not exist yet. Waiting...",
                self.otcs.resource_name,
            )
            time.sleep(30)
            otcs_resource = self.otds_object.getResource(self.otcs.resource_name)

        otcs_resource_id = otcs_resource["resourceID"]

        logger.info("OTDS resource ID for Content Server -> %s", otcs_resource_id)

        # make sure code is idempotent and only try to add ressource if it doesn't exist already:
        awp_resource = self.otds_object.getResource(self.otawp.resource_name)
        if not awp_resource:
            logger.info(
                "OTDS resource -> %s for AppWorks Platform does not yet exist. Creating...",
                self.otawp.resource_name,
            )
            # Create a Python dict with the special payload we need for AppWorks:
            additional_payload = {}
            additional_payload["connectorid"] = "rest"
            additional_payload["resourceType"] = "rest"
            user_attribute_mapping = [
                {
                    "sourceAttr": ["oTExternalID1"],
                    "destAttr": "__NAME__",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["displayname"],
                    "destAttr": "DisplayName",
                    "mappingFormat": "%s",
                },
                {"sourceAttr": ["mail"], "destAttr": "Email", "mappingFormat": "%s"},
                {
                    "sourceAttr": ["oTTelephoneNumber"],
                    "destAttr": "Telephone",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTMobile"],
                    "destAttr": "Mobile",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTFacsimileTelephoneNumber"],
                    "destAttr": "Fax",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTStreetAddress,l,st,postalCode,c"],
                    "destAttr": "Address",
                    "mappingFormat": "%s%n%s %s %s%n%s",
                },
                {
                    "sourceAttr": ["oTCompany"],
                    "destAttr": "Company",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["ds-pwp-account-disabled"],
                    "destAttr": "AccountDisabled",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTExtraAttr9"],
                    "destAttr": "IsServiceAccount",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["custom:proxyConfiguration"],
                    "destAttr": "ProxyConfiguration",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["c"],
                    "destAttr": "Identity-CountryOrRegion",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["gender"],
                    "destAttr": "Identity-Gender",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["displayName"],
                    "destAttr": "Identity-DisplayName",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTStreetAddress"],
                    "destAttr": "Identity-Address",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["l"],
                    "destAttr": "Identity-City",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["mail"],
                    "destAttr": "Identity-Email",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["givenName"],
                    "destAttr": "Identity-FirstName",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["sn"],
                    "destAttr": "Identity-LastName",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["initials"],
                    "destAttr": "Identity-MiddleNames",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTMobile"],
                    "destAttr": "Identity-Mobile",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["postalCode"],
                    "destAttr": "Identity-PostalCode",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["st"],
                    "destAttr": "Identity-StateOrProvince",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["title"],
                    "destAttr": "Identity-title",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["physicalDeliveryOfficeName"],
                    "destAttr": "Identity-physicalDeliveryOfficeName",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTFacsimileTelephoneNumber"],
                    "destAttr": "Identity-oTFacsimileTelephoneNumber",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["notes"],
                    "destAttr": "Identity-notes",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTCompany"],
                    "destAttr": "Identity-oTCompany",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTDepartment"],
                    "destAttr": "Identity-oTDepartment",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["birthDate"],
                    "destAttr": "Identity-Birthday",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["cn"],
                    "destAttr": "Identity-UserName",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["Description"],
                    "destAttr": "Identity-UserDescription",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["oTTelephoneNumber"],
                    "destAttr": "Identity-Phone",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["displayName"],
                    "destAttr": "Identity-IdentityDisplayName",
                    "mappingFormat": "%s",
                },
            ]
            additional_payload["userAttributeMapping"] = user_attribute_mapping
            group_attribute_mapping = [
                {
                    "sourceAttr": ["cn"],
                    "destAttr": "__NAME__",
                    "mappingFormat": '%js:function format(name) { return name.replace(/&/g,"-and-"); }',
                },
                {
                    "sourceAttr": ["description"],
                    "destAttr": "Description",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["description"],
                    "destAttr": "Identity-Description",
                    "mappingFormat": "%s",
                },
                {
                    "sourceAttr": ["displayName"],
                    "destAttr": "Identity-DisplayName",
                    "mappingFormat": "%s",
                },
            ]
            additional_payload["groupAttributeMapping"] = group_attribute_mapping
            additional_payload["connectorName"] = "REST (Generic)"
            additional_payload["pcCreatePermissionAllowed"] = "true"
            additional_payload["pcModifyPermissionAllowed"] = "true"
            additional_payload["pcDeletePermissionAllowed"] = "false"
            additional_payload["connectionParamInfo"] = [
                {
                    "name": "fBaseURL",
                    "value": "http://appworks:8080/home/system/app/otdspush",
                },
                {"name": "fUsername", "value": self.otawp.admin},
                {"name": "fPassword", "value": self.otawp.password},
            ]

            awp_resource = self.otds_object.addResource(
                self.otawp.resource_name,
                "AppWorks Platform",
                "AppWorks Platform",
                additional_payload,
            )
        else:
            logger.info(
                "OTDS resource -> %s for AppWorks Platform does already exist.",
                self.otawp.resource_name,
            )

        awp_resource_id = awp_resource["resourceID"]

        logger.info("OTDS resource ID for AppWorks Platform -> %s", awp_resource_id)

        self.settings.placeholder_values["OTAWP_RESOURCE_ID"] = str(awp_resource_id)

        logger.debug(
            "Placeholder values after OTAWP init = %s", self.settings.placeholder_values
        )

        logger.info("Update AppWorks Kubernetes Config Map with OTDS resource IDs...")

        config_map = self.k8s_object.getConfigMap(self.otawp.k8s_configmap)
        if not config_map:
            logger.error(
                "Failed to retrieve AppWorks Kubernetes Config Map -> %s",
                self.otawp.k8s_configmap,
            )
        else:
            solution = yaml.safe_load(config_map.data["solution.yaml"])  # type: ignore

            # Change values as required
            solution["platform"]["organizations"]["system"]["otds"][
                "resourceId"
            ] = awp_resource_id
            solution["platform"]["content"]["ContentServer"][
                "contentServerUrl"
            ] = f"{self.otcs.public_protocol}://{self.otcs.public_url}/cs/cs"
            solution["platform"]["content"]["ContentServer"][
                "contentServerSupportDirectoryUrl"
            ] = f"{self.otcs.public_protocol}://{self.otcs.public_url}/cssupport"
            solution["platform"]["content"]["ContentServer"][
                "otdsResourceId"
            ] = otcs_resource_id
            solution["platform"]["authenticators"]["OTDS_auth"]["publicLoginUrl"] = (
                self.otds.public_protocol
                + "://"
                + self.otds.public_url
                + "/otdsws/login"
            )
            solution["platform"]["security"]["contentSecurityPolicy"] = (
                "frame-ancestors 'self' "
                + self.otcs.public_protocol
                + "://"
                + self.otcs.public_url
            )
            data = {"solution.yaml": yaml.dump(solution)}
            result = self.k8s_object.replaceConfigMap(self.otawp.k8s_configmap, data)
            if result:
                logger.info("Successfully updated AppWorks Solution YAML.")
            else:
                logger.error("Failed to update AppWorks Solution YAML.")
            logger.debug("Solution YAML for AppWorks -> %s", solution)

        logger.info("Scale AppWorks Kubernetes Stateful Set to 1...")
        self.k8s_object.scaleStatefulSet(sts_name=self.otawp.k8s_statefulset, scale=1)

        # Add the OTCS Admin user to the AppWorks Access Role in OTDS
        self.otds_object.addUserToAccessRole(
            "Access to " + self.otawp.resource_name, "otadmin@otds.admin"
        )

        # Loop to wait for OTCS to create its OTDS user partition:
        otcs_partition = self.otds_object.getPartition(self.otcs.partition)
        while otcs_partition is None:
            logger.warning(
                "OTDS user partition for Content Server with name -> %s does not exist yet. Waiting...",
                self.otcs.partition,
            )

            time.sleep(30)
            otcs_partition = self.otds_object.getPartition(self.otcs.partition)

        # Add the OTDS user partition for OTCS to the AppWorks Platform Access Role in OTDS.
        # This will effectvely sync all OTCS users with AppWorks Platform:
        self.otds_object.addPartitionToAccessRole(
            self.otawp.access_role_name, self.otcs.partition
        )

        # Add the OTDS admin partition to the AppWorks Platform Access Role in OTDS.
        self.otds_object.addPartitionToAccessRole(
            self.otawp.access_role_name, self.otds.admin_partition
        )

        # Set Group inclusion for Access Role for OTAWP to "True":
        self.otds_object.updateAccessRoleAttributes(
            self.otawp.access_role_name, [{"name": "pushAllGroups", "values": ["True"]}]
        )

        # Add ResourceID User to OTDSAdmin to allow push
        self.otds_object.addUserToGroup(
            user=str(awp_resource_id) + "@otds.admin", group="otdsadmins@otds.admin"
        )

        # Allow impersonation for all users:
        self.otds_object.impersonateResource(self.otawp.resource_name)

        # end function definition

    def restart_otcs_service(self, otcs_object: OTCS):
        """Restart the Content Server service in all OTCS pods

        Args:
            otcs_object: OTCS class instance (object)
        Returns:
            None
        """

        logger.info("Restart OTCS frontend and backend pods...")

        # Restart all frontends:
        for x in range(0, self.otcs.replicas_frontend):
            pod_name = self.otcs.k8s_statefulset_frontend + "-" + str(x)

            logger.info("Deactivate Liveness probe for pod -> %s", pod_name)
            self.k8s_object.execPodCommand(
                pod_name, ["/bin/sh", "-c", "touch /tmp/keepalive"]
            )
            logger.info("Restarting pod -> %s", pod_name)
            self.k8s_object.execPodCommand(
                pod_name, ["/bin/sh", "-c", "/opt/opentext/cs/stop_csserver"]
            )
            self.k8s_object.execPodCommand(
                pod_name, ["/bin/sh", "-c", "/opt/opentext/cs/start_csserver"]
            )

        # Restart all backends:
        for x in range(0, self.otcs.replicas_backend):
            pod_name = self.otcs.k8s_statefulset_backend + "-" + str(x)

            logger.info("Deactivate Liveness probe for pod -> %s", pod_name)
            self.k8s_object.execPodCommand(
                pod_name, ["/bin/sh", "-c", "touch /tmp/keepalive"]
            )
            logger.info("Restarting pod -> %s", pod_name)
            self.k8s_object.execPodCommand(
                pod_name, ["/bin/sh", "-c", "/opt/opentext/cs/stop_csserver"]
            )
            self.k8s_object.execPodCommand(
                pod_name, ["/bin/sh", "-c", "/opt/opentext/cs/start_csserver"]
            )

        logger.info("Re-Authenticating to OTCS after restart of pods...")
        otcs_cookie = otcs_object.authenticate(revalidate=True)
        while otcs_cookie is None:
            logger.warning("Waiting 30 seconds for OTCS to become ready...")
            time.sleep(30)
            otcs_cookie = otcs_object.authenticate(revalidate=True)
        logger.info("OTCS is ready again.")

        # Reactivate Liveness probes in all pods:
        for x in range(0, self.otcs.replicas_frontend):
            pod_name = self.otcs.k8s_statefulset_frontend + "-" + str(x)

            logger.info("Reactivate Liveness probe for pod -> %s", pod_name)
            self.k8s_object.execPodCommand(
                pod_name, ["/bin/sh", "-c", "rm /tmp/keepalive"]
            )

        for x in range(0, self.otcs.replicas_backend):
            pod_name = self.otcs.k8s_statefulset_backend + "-" + str(x)

            logger.info("Reactivate Liveness probe for pod -> %s", pod_name)
            self.k8s_object.execPodCommand(
                pod_name, ["/bin/sh", "-c", "rm /tmp/keepalive"]
            )

        logger.info("Restart OTCS frontend and backend pods has been completed.")

        # end function definition

    def restart_otac_service(self) -> bool:
        """Restart the Archive Center spawner service in OTAC pod

        Args:
        Returns:
            boolean: True if restart was done, False if error occured
        """

        if not self.otac.enabled:
            return False

        logger.info(
            "Restarting spawner service in Archive Center pod -> %s",
            self.otac.k8s_pod_name,
        )
        # The Archive Center Spawner needs to be run in "interactive" mode - otherwise the command will "hang":
        # The "-c" parameter is not required in this case
        # False is given as parameter as OTAC writes non-errors to stderr
        response = self.k8s_object.execPodCommandInteractive(
            self.otac.k8s_pod_name,
            ["/bin/sh", "/etc/init.d/spawner restart"],
            60,
            False,
        )

        if response:
            return True
        else:
            return False

        # end function definition

    def restart_otawp_pod(self):
        """Delete the AppWorks Platform Pod to make Kubernetes restart it.

        Args:
        Returns:
            None
        """

        self.k8s_object.deletePod(self.otawp.k8s_statefulset + "-0")

        # end function definition

    def consolidate_otds(self):
        """Consolidate OTDS resources
        Args:
        Return: None
        """

        self.otds_object.consolidate(self.otcs.resource_name)

        if self.otawp.enabled == "true":  # is AppWorks Platform deployed?
            self.otds_object.consolidate(self.otawp.resource_name)

        # end function definition

    def import_powerdocs_configuration(self, otpd_object: OTPD):
        """Import a database export (zip file) into the PowerDocs database

        Args:
            otpd_object (object): PowerDocs object
        """

        if self.otpd.db_importfile.startswith("http"):
            # Download file from remote location specified by the OTPD_DBIMPORTFILE
            # this must be a public place without authentication:
            logger.info(
                "Download PowerDocs database file from URL -> %s",
                self.otpd.db_importfile,
            )

            try:
                package = requests.get(self.otpd.db_importfile, timeout=60)
                package.raise_for_status()
                logger.info(
                    "Successfully downloaded PowerDocs database file -> %s; status code -> %s",
                    self.otpd.db_importfile,
                    package.status_code,
                )
                filename = "/tmp/otpd_db_import.zip"
                with open(filename, mode="wb") as localfile:
                    localfile.write(package.content)

                logger.info(
                    "Starting import on %s://%s:%s of %s",
                    self.otpd.protocol,
                    self.otpd.hostname,
                    self.otpd.port,
                    self.otpd.db_importfile,
                )
                response = otpd_object.importDatabase(filename=filename)
                logger.info("Response -> %s", response)

            except requests.exceptions.HTTPError as err:
                logger.error("Request error -> %s", err)

        # end function definition

    def set_maintenance_mode(self, enable: bool = True):
        """Enable or Disable Maintenance Mode

        Args:
            enable (bool, optional): _description_. Defaults to True.
        """
        if enable:
            logger.info("========== Enable Maintenance Mode ==========")
            logger.info(
                "Put OTCS frontends in Maitenance Mode by changing the Kubernetes Ingress backend service..."
            )
            self.k8s_object.updateIngressBackendServices(
                self.otcs.k8s_ingress,
                "otcs",
                self.otcs.maintenance_service_name,
                self.otcs.mainteance_service_port,
            )
            logger.info("OTCS frontend is now in Maintenance Mode!")

        else:
            # Changing the Ingress backend service to OTCS frontend service:
            logger.info(
                "Put OTCS frontend back in Production Mode by changing the Kubernetes Ingress backend service..."
            )
            self.k8s_object.updateIngressBackendServices(
                self.otcs.k8s_ingress,
                "otcs",
                self.otcs.hostname_frontend,
                self.otcs.port_frontend,
            )
            logger.info("OTCS frontend is now back in Production Mode!")

    def customization_run(self):
        """Central function to initiate the customization"""
        # Set Timer for duration calculation
        self.settings.customizer_start_time = (
            self.settings.customizer_end_time
        ) = datetime.now()

        # Initialize the OTDS, OTCS and OTPD objects and wait for the
        # pods to be ready. If any of this fails we bail out:

        logger.info("========== Initialize OTDS ==============")

        self.otds_object = self.init_otds()
        if not self.otds_object:
            logger.error("Failed to initialize OTDS - exiting...")
            sys.exit()

        # Establish in-cluster Kubernetes connection
        logger.info("========== Initialize Kubernetes ============")
        if self.k8s_enabled:
            self.k8s_object = self.init_k8s(in_cluster=True)

            if not self.k8s_object:
                logger.error("Failed to initialize Kubernetes - exiting...")
                sys.exit()

        # Put Frontend in Maintenance mode to make sure nobody interferes
        # during customization:
        if self.otcs.maintenance_mode:
            self.set_maintenance_mode(True)

        if self.otawp.enabled == "true":  # is AppWorks Platform deployed?
            logger.info("========== Initialize OTAWP =============")

            # Configure required OTDS resources as AppWorks doesn't do this on its own:
            self.init_otawp()
        else:
            self.settings.placeholder_values["OTAWP_RESOURCE_ID"] = ""

        logger.info("========== Initialize OTCS backend ======")
        self.otcs_backend_object = self.init_otcs(
            self.otcs.hostname_backend,
            int(self.otcs.port_backend),
            self.otcs.partition,
            self.otcs.resource_name,
        )
        if not self.otcs_backend_object:
            logger.error("Failed to initialize OTCS backend - exiting...")
            sys.exit()

        logger.info("========== Initialize OTCS frontend =====")
        self.otcs_frontend_object = self.init_otcs(
            self.otcs.hostname_frontend,
            int(self.otcs.port_frontend),
            self.otcs.partition,
            self.otcs.resource_name,
        )
        if not self.otcs_frontend_object:
            logger.error("Failed to initialize OTCS frontend - exiting...")
            sys.exit()

        if self.otac.enabled == "true":  # is Archive Center deployed?
            logger.info("========== Initialize OTAC ==============")

            self.otac_object = self.init_otac()
            if not self.otac_object:
                logger.error("Failed to initialize OTAC - exiting...")
                sys.exit()
        else:
            self.otac_object = None

        if self.otiv.enabled == "true":  # is PowerDocs deployed?
            logger.info("========== Initialize OTIV ==============")

            self.otiv_object = self.init_otiv()

        if self.otpd.enabled == "true":  # is PowerDocs deployed?
            logger.info("========== Initialize OTPD ==============")

            self.otpd_object = self.init_otpd()
            if not self.otpd_object:
                logger.error("Failed to initialize OTPD - exiting...")
                sys.exit()
        else:
            self.otpd_object = None

        if (
            self.o365.enabled == "true"
            and self.o365.user != ""
            and self.o365.password != ""
        ):  # is M365 enabled?
            logger.info("======== Initialize MS Graph API ========")

            # Initialize the M365 object and connection to M365 Graph API:
            self.m365_object = self.init_m365()

            logger.info("======== Upload MS Teams App ============")

            # Download MS Teams App from OTCS (this has with 23.2 a nasty side-effect
            # of unsetting 2 checkboxes on that config page - we reset these checkboxes
            # with the settings file "O365Settings.xml"):
            response = self.otcs_frontend_object.downloadConfigFile(
                "/cs/cs?func=officegroups.DownloadTeamsPackage",
                "/tmp/ot.xecm.teams.zip",
            )
            self.m365_object.authenticateUser(self.o365.user, self.o365.password)

            # Check if the app is already installed:
            response = self.m365_object.getTeamsApps(
                f"contains(displayName, '{self.o365.teams_app_name}')"
            )
            if self.m365_object.existResultItem(
                response, "displayName", self.o365.teams_app_name
            ):
                logger.info(
                    "Extended ECM Teams App is already in app catalog. Trying to install an update (may give a warning if it is not a new version)..."
                )
                app_id = self.m365_object.getResultValue(
                    response, "id", 0
                )  # 0 = Index = first item
                logger.info(
                    "Extended ECM Teams App is already in app catalog (app ID -> %s). Updating existing app...",
                    app_id,
                )
                response = self.m365_object.uploadTeamsApp(
                    "/tmp/ot.xecm.teams.zip", update_existing_app=True, app_id=app_id
                )
            else:
                # this upload will be done with the user credentials - this is required:
                logger.info(
                    "Extended Teams ECM App is not yet in app catalog. Installing as new app..."
                )
                response = self.m365_object.uploadTeamsApp("/tmp/ot.xecm.teams.zip")
        else:
            self.m365_object = None

        logger.info("========== Processing Payload ===========")

        cust_payload_list = [self.settings.cust_payload]

        # do we have additional payload as an external file?
        if os.path.exists(self.settings.cust_payload_external):
            for filename in os.scandir(self.settings.cust_payload_external):
                if filename.is_file() and os.path.getsize(filename) > 0:
                    logger.info("Found external payload file -> %s", filename.path)
                    cust_payload_list.append(filename.path)
        else:
            logger.info(
                "No external payload file -> %s", self.settings.cust_payload_external
            )

        for cust_payload in cust_payload_list:
            # Open the payload file. If this fails we bail out:
            logger.info("Starting processing of payload -> %s", cust_payload)

            # Set startTime for duration calculation
            start_time = datetime.now()

            payload_object = payload.Payload(
                payload_source=cust_payload,
                custom_settings_dir=self.settings.cust_settings_dir,
                k8s_object=self.k8s_object,
                otds_object=self.otds_object,
                otac_object=self.otac_object,
                otcs_backend_object=self.otcs_backend_object,
                otcs_frontend_object=self.otcs_frontend_object,
                otcs_restart_callback=self.restart_otcs_service,
                otiv_object=self.otiv_object,
                m365_object=self.m365_object,
                placeholder_values=self.settings.placeholder_values,  # this dict includes placeholder replacements for the Ressource IDs of OTAWP and OTCS
                stop_on_error=self.settings.stop_on_error,
            )
            # Load the payload file and initialize the payload sections:
            if not payload_object.initPayload():
                logger.error(
                    "Failed to initialize payload -> %s - skipping...", cust_payload
                )
                continue

            # Now process the payload in the defined ordering:
            payload_object.processPayload()

            logger.info("========== Consolidate OTDS Resources ==================")
            self.consolidate_otds()

            # Upload payload file for later review to Enterprise Workspace
            logger.info("========== Upload Payload file to Extended ECM =========")
            response = self.otcs_backend_object.getNodeFromNickname(
                self.settings.cust_target_folder_nickname
            )
            target_folder_id = self.otcs_backend_object.getResultValue(response, "id")
            if not target_folder_id:
                target_folder_id = 2000  # use Enterprise Workspace as fallback
            # Write YAML file with upadated payload (including IDs, etc.).
            # We need to write to /tmp as initial location is read-only:
            cust_payload = "/tmp/" + os.path.basename(cust_payload)
            with open(cust_payload, "w", encoding="utf-8") as file:
                yaml.dump(payload_object.getPayload(), file)

            # Check if the payload file has been uploaded before.
            # This can happen if we re-run the python container.
            # In this case we add a version to the existing document:
            response = self.otcs_backend_object.getNodeByParentAndName(
                int(target_folder_id), os.path.basename(cust_payload)
            )
            target_document_id = self.otcs_backend_object.getResultValue(response, "id")
            if target_document_id:
                response = self.otcs_backend_object.addDocumentVersion(
                    int(target_document_id),
                    cust_payload,
                    os.path.basename(cust_payload),
                    "text/plain",
                    "Updated payload file after re-run of customization",
                )
            else:
                response = self.otcs_backend_object.uploadFileToParent(
                    cust_payload,
                    os.path.basename(cust_payload),
                    "text/plain",
                    int(target_folder_id),
                )

            duration = datetime.now() - start_time
            logger.info(
                "========== Payload -> %s completed execution in %s ===",
                cust_payload,
                duration,
            )

        if self.otcs.maintenance_mode:
            self.set_maintenance_mode(False)

        # Restart AppWorksPlatform pod if it is deployed (to make settings effective):
        if self.otawp.enabled == "true":  # is AppWorks Platform deployed?
            otawp_resource = self.otds_object.getResource(self.otawp.resource_name)
            if (
                not "allowImpersonation" in otawp_resource
                or not otawp_resource["allowImpersonation"]
            ):
                # Allow impersonation for all users:
                logger.warning(
                    "OTAWP impersonation is not correct in OTDS before OTAWP pod restart!"
                )
            else:
                logger.info(
                    "OTAWP impersonation is correct in OTDS before OTAWP pod restart!"
                )
            logger.info("Restart OTAWP pod...")
            self.restart_otawp_pod()
            # For some reason we need to double-check that the impersonation for OTAWP has been set correctly
            # and if not set it again:
            otawp_resource = self.otds_object.getResource(self.otawp.resource_name)
            if (
                not "allowImpersonation" in otawp_resource
                or not otawp_resource["allowImpersonation"]
            ):
                # Allow impersonation for all users:
                logger.warning(
                    "OTAWP impersonation is not correct in OTDS - set it once more..."
                )
                self.otds_object.impersonateResource(self.otawp.resource_name)

        # Upload log file for later review to "Deployment" folder in "Administration" folder
        if os.path.exists(self.settings.cust_log_file):
            logger.info("========== Upload log file to Extended ECM =============")
            response = self.otcs_backend_object.getNodeFromNickname(
                self.settings.cust_target_folder_nickname
            )
            target_folder_id = self.otcs_backend_object.getResultValue(response, "id")
            if not target_folder_id:
                target_folder_id = 2000  # use Enterprise Workspace as fallback
            # Check if the log file has been uploaded before.
            # This can happen if we re-run the python container:
            # In this case we add a version to the existing document:
            response = self.otcs_backend_object.getNodeByParentAndName(
                int(target_folder_id), os.path.basename(self.settings.cust_log_file)
            )
            target_document_id = self.otcs_backend_object.getResultValue(response, "id")
            if target_document_id:
                response = self.otcs_backend_object.addDocumentVersion(
                    int(target_document_id),
                    self.settings.cust_log_file,
                    os.path.basename(self.settings.cust_log_file),
                    "text/plain",
                    "Updated Python Log after re-run of customization",
                )
            else:
                response = self.otcs_backend_object.uploadFileToParent(
                    self.settings.cust_log_file,
                    os.path.basename(self.settings.cust_log_file),
                    "text/plain",
                    int(target_folder_id),
                )

        self.settings.customizer_end_time = datetime.now()
        logger.info(
            "======= Script execution completed in %s ===",
            self.settings.customizer_end_time - self.settings.customizer_start_time,
        )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    my_customizer = Customizer()
    my_customizer.customization_run()
