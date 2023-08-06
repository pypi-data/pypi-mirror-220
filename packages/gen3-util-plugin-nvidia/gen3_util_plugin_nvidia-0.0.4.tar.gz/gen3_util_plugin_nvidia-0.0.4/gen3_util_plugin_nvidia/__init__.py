import pathlib

from gen3_util.meta.importer import PathParser
from fhir.resources.identifier import Identifier

import logging
logger = logging.getLogger(__name__)

BLACKLIST = ['.DS_Store', 'HandE_annotations/HandE/tifs.tar.gz']
WHITELIST = ['2020_Immune', 'HandE_annotations']

WHITELIST_EXTENSIONS = ['.json', '.csv', '.tif']

class NVIDIAPathParser(PathParser):
    """A Class to extract Patient and Specimen from directory path.

    Must use PathParser as a base.

    Expected path format: 'RoundNumber5_MarkerName.MarkerName.MarkerName.MarkerName_TissueID_DateOfImaging__RandomFileSpecificNumber_ChannelID'
    """
    def extract_patient_identifier(self, path: str) -> Identifier:
        _ = parse_path(path)
        if _ and _['patient']:
            return Identifier.parse_obj({'system': 'http://ohsu.edu/nvidia-collaboration/patient', 'value': _['patient']})
        return None

    def extract_specimen_identifier(self, path: str) -> Identifier:
        _ = parse_path(path)
        if _ and _['tissue']:
            return Identifier.parse_obj({'system': 'http://ohsu.edu/nvidia-collaboration/specimen', 'value': _['tissue']})
        return None

def parse_path(line: str) -> dict:
    """Parse directory listing."""
    line
    failed_whitelist = True
    for _ in WHITELIST:
        if _ in line:
            failed_whitelist = False
    if failed_whitelist:
        raise ValueError(f"Do not include {line} (not in whitelist)")

    for _ in BLACKLIST:
        if _ in line:
            raise ValueError(f"Do not include {line} (blacklisted {_})")

    path = pathlib.Path(line)

    if path.suffix not in WHITELIST_EXTENSIONS:
        raise ValueError(f"Do not include {line} (not in whitelist extensions)")

    stem = path.stem
    if '__' in stem:
        parts = stem.split('__')
        assert len(parts) == 2, f"Expected 2 parts in {stem}"
        identifiers = parts[-1].split('_')
        assert len(parts) == 2, f"Expected 2 identifiers in {identifiers}"
        cell_line = identifiers[-1]
        tissue = identifiers[-1]
        # print("parsed from file name", line)
        return {
            # 'round': round_,  <<< SKIP
            # 'markers': markers,  <<< SKIP (for now)
            'tissue': tissue,
            # 'date_of_imaging': date_of_imaging,   <<< SKIP
            # 'random_file_number': random_file_number, <<< SKIP
            # 'channel_id': channel_id,  <<< SKIP
            'file_name': path.name,
            'patient': cell_line,
            'path': line
        }

    if 'RegisteredImages/' in line:
        # print(line)
        cell_line = path.name.split('-')[1].split('_')[-1]
        tissue = cell_line
        # print("parsed from RegisteredImages/ file name", line)
        return {
            'tissue': tissue,
            'file_name': path.name,
            'patient': cell_line,
            'path': line
        }

    # print(f"Could not parse {line}")

    return {
            'tissue': None,
            'file_name': path.name,
            'patient': None,
            'path': line
        }


