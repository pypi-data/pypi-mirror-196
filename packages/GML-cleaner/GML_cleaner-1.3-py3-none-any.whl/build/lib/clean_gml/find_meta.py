import os
from pathlib import Path


def find_meta_file(gml_file: str = None) -> str | None:
    """
    Returns a meta_file file path for a given gml file. Usually a .xsd or .gfs file
    :param gml_file: file path for gml file
    :return: meta_file: file path to meta file or None if not found
    """

    dirname = Path(gml_file).parent

    suffixes = ['.xsd', '.XSD', '.gfs', '.GFS']
    for suffix in suffixes:
        meta_file = Path(dirname, Path(gml_file).stem).with_suffix(suffix)
        if meta_file.exists():
            return str(meta_file)

        continue

    return None

