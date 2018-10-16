import json
import urlparse

from lib.http_base import BaseConnection
from endpoints.entity import EntityEndpoint
from endpoints.enums import DEFAULT_API_VERSION, SECURE
from endpoints.mixins.set import EntitySetEndpointsMixin
from endpoints.mixins.default import DefaultableEntityEndpointsMixin
from endpoints.enums import MATERIALSPROJECT_HOST, MATERIALSPROJECT_PORT, MATERIALSPROJECT_VERSION


class MaterialEndpoints(EntitySetEndpointsMixin, DefaultableEntityEndpointsMixin, EntityEndpoint):
    """
    Material endpoints.

    Args:
        host (str): Exabyte API hostname.
        port (int): Exabyte API port number.
        account_id (str): account ID.
        auth_token (str): authentication token.
        version (str): Exabyte API version.
        secure (bool): whether to use secure http protocol (https vs http).
        kwargs (dict): a dictionary of HTTP session options.
            timeout (int): session timeout in seconds.

    Attributes:
        name (str): endpoint name.
    """

    def __init__(self, host, port, account_id, auth_token, version=DEFAULT_API_VERSION, secure=SECURE, **kwargs):
        super(MaterialEndpoints, self).__init__(host, port, account_id, auth_token, version, secure, **kwargs)
        self.name = 'materials'

    def import_from_file(self, name, content, format="poscar", tags=()):
        """
        Imports a material from the given file.

        Args:
            name (str): material name.
            content (str): material as string.
            format (str): material format, either cif or poscar.
            tags (tuple[str]) a list of tags that should be assigned to the material.

        Returns:
            dict
        """
        data = {"name": name, "content": content, "format": format, "tags": tags}
        return self.request('POST', "/".join((self.name, "import")), headers=self.headers, data=json.dumps(data))

    def _get_materialsproject_url(self, material_id):
        """
        Constructs the URL to access a material with given ID from materialsproject.

        Args:
            material_id (str): materialsproject ID.

        Returns:
            str
        """
        url = ":".join((MATERIALSPROJECT_HOST, str(MATERIALSPROJECT_PORT)))
        return urlparse.urljoin(url, "/".join(("rest", MATERIALSPROJECT_VERSION, "materials", material_id, "vasp")))

    def import_from_materialsproject(self, api_key, material_ids, tags=()):
        materials = []
        conn = BaseConnection()
        with conn:
            for material_id in material_ids:
                conn.request("GET", self._get_materialsproject_url(material_id), params={"API_KEY": api_key})
                material = conn.json()["response"][0]
                tags.extend(material.get("tags", []))
                materials.append(self.import_from_file(material["material_id"], material["cif"], "cif", tags))
        return materials
