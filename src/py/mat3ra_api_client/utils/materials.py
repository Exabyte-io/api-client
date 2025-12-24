import urllib.parse

from ..endpoints.enums import MATERIALSPROJECT_HOST, MATERIALSPROJECT_PORT, MATERIALSPROJECT_VERSION


def get_materialsproject_url(material_id):
    """
    Constructs the URL to access a material with given ID from materialsproject.

    Args:
        material_id (str): materialsproject ID.

    Returns:
        str
    """
    url = ":".join((MATERIALSPROJECT_HOST, str(MATERIALSPROJECT_PORT)))
    return urllib.parse.urljoin(url, "/".join(("rest", MATERIALSPROJECT_VERSION, "materials", material_id, "vasp")))


def flatten_material(material):
    """
    Flattens a given material.

    Args:
        material (dict): material config.

    Returns:
        list
    """
    lattice = material["lattice"]
    return [
        material["_id"],
        material["name"],
        ", ".join(material["tags"]),
        len(material["basis"]["coordinates"]),
        lattice["a"],
        lattice["b"],
        lattice["c"],
        lattice["alpha"],
        lattice["beta"],
        lattice["gamma"],
    ]
