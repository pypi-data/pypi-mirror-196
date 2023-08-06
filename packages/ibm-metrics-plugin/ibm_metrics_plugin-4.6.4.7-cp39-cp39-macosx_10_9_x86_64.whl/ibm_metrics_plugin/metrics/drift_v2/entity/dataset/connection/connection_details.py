# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2023
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import base64
import ssl
import tempfile
from typing import Dict
from urllib.parse import urlparse

import sqlalchemy

from ibm_metrics_plugin.common.utils.python_utils import get


class Connection:

    def __init__(self) -> None:
        self.username = None
        self.password = None
        self.jdbc_url = None
        self.parsed_url = None
        self.location_type = None
        self.use_ssl = False
        self.certificate = None

        self.certificate_file_prefix = "cert_prefix_"
        self.certificate_file_suffix = "_suffix.arm"
        self._dialect = None
        self._engine = None

    @property
    def dialect(self) -> str:
        if self._dialect is not None:
            return self._dialect

        if self.location_type == "db2":
            self._dialect = "ibm_db_sa"
        elif self.location_type == "postgresql":
            self._dialect = "postgresql"

        return self._dialect

    @property
    def connection_url(self) -> str:
        url = self.jdbc_url.split("://")[1]
        url = f"{self.dialect}://{self.username}:{self.password}@{self.parsed_url.hostname}"

        if self.parsed_url.port is not None:
            url = f"{url}:{self.parsed_url.port}"

        url = f"{url}{self.parsed_url.path}"
        return url

    @property
    def engine(self) -> sqlalchemy.engine.base.Engine:
        if self._engine is None:
            self._engine = sqlalchemy.create_engine(self.connection_url)

        return self._engine

    def create_certificate_file(self):
        certificate = None
        cert_file = None
        if self.certificate:
            # if certificate already set in the connection_details
            if "BEGIN CERTIFICATE" not in self.certificate:
                # If 'BEGIN CERTIFICATE' is not present, assuming that it will be a base64 encoded.
                certificate = base64.b64decode(
                    self.certificate.strip()).decode()
            else:
                certificate = self.certificate.strip()
        else:
            # else get it from the host
            certificate = ssl.get_server_certificate(
                (self.parsed_url.hostname, self.parsed_url.port))

        with tempfile.NamedTemporaryFile(mode="w", prefix=self.certificate_file_prefix, suffix=self.certificate_file_suffix, delete=False) as f:
            cert_file = f.name
            f.write(certificate)
        return cert_file

    @classmethod
    def from_dict(cls, dict_: Dict) -> "Connection":

        location_type = get(dict_, "storage_details.connection.location_type")
        if location_type not in ("db2", "postgresql"):
            raise ValueError(
                f"Unsupported connection type: {conn.type}. Supported types are: 'db2' and 'postgresql'")

        if location_type == "db2":
            conn = DB2Connection()
        else:
            conn = PostgresqlConnection()

        conn.jdbc_url = get(dict_, "storage_details.connection.jdbc_url")
        conn.parsed_url = urlparse(conn.jdbc_url.replace("jdbc:", ""))

        conn.use_ssl = (
            get(dict_, "storage_details.connection.use_ssl") in (True, "true", "True"))
        conn.certificate = get(dict_, "storage_details.connection.certificate")

        if location_type == "postgresql":
            conn.parse_sslmode(dict_=dict_)

        conn.username = get(dict_, "storage_details.credentials.username")
        conn.password = get(dict_, "storage_details.credentials.password")

        return conn


class DB2Connection(Connection):

    def __init__(self) -> None:
        super().__init__()
        self.location_type = "db2"
        self.certificate_file_prefix = "db2_ssl_"
        self.certificate_file_suffix = ".arm"

    @property
    def connection_url(self) -> str:
        url = super().connection_url

        if self.use_ssl:
            url += ";SECURITY=SSL;"
            cert_file = self.create_certificate_file()
            url += f"SSLServerCertificate={cert_file};"

        return url


class PostgresqlConnection(Connection):

    ALLOWED_SSL_MODES = ["disable", "allow", "prefer",
                         "require", "verify-ca", "verify-full"]

    def __init__(self) -> None:
        super().__init__()
        self.location_type = "postgresql"
        self.certificate_file_prefix = "postgresql_ssl_"
        self.certificate_file_suffix = ".crt"
        self.sslmode = None

    @property
    def connection_url(self) -> str:
        url = super().connection_url

        if self.use_ssl and self.certificate is not None:
            cert_file = self.create_certificate_file()
            url += f"?sslmode={self.sslmode}&sslrootcert={cert_file}"

        return url

    def parse_sslmode(self, dict_: Dict):
        sslmode = get(dict_, "storage_details.connection.sslmode")

        if sslmode and sslmode not in PostgresqlConnection.ALLOWED_SSL_MODES:
            raise ValueError(
                f"The sslmode '{sslmode}' is not valid. Allowed modes are {PostgresqlConnection.ALLOWED_SSL_MODES}")

        if self.use_ssl:
            if not sslmode:
                raise ValueError(f"The sslmode parameter is not specified.")

            if sslmode == "disable":
                raise ValueError(
                    f"The 'use_ssl' parameter is true but 'sslmode' is 'disable'")

        self.sslmode = sslmode
