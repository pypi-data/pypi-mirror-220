import pathlib

from gen3_util.meta.importer import PathParser
from fhir.resources.identifier import Identifier

import logging
logger = logging.getLogger(__name__)

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

    if line == '':
        return None
    if line.startswith('/'):
        line = line[1:]

    if '/' not in line:
        logger.debug(f"Start cell-line: {line}")
        return None

    try:
        cell_line, file_name = line.split('/')
    except ValueError:
        logger.warning(f"Un-parsable: {line}")
        return None

    if not all([cell_line, file_name]):
        logger.warning(f"Un-parsable: {line}")
        return None

    file_name = file_name.replace('__', '_')

    try:
        round_, markers, tissue, year, month, day, random_file_number, channel_id, u_ = file_name.split('_')
        markers = markers.split('.')
        date_of_imaging = f"{year}-{month}-{day}T00:00:00"

        return {
            'round': round_,
            'markers': markers,
            'tissue': tissue,
            'date_of_imaging': date_of_imaging,
            'random_file_number': random_file_number,
            'channel_id': channel_id,
            'file_name': file_name,
            'patient': cell_line,
            'path': line
        }

    except ValueError as e:
        logger.debug(f"Could not parse: {line} {e}")
        return {
            'round': None,
            'markers': None,
            'tissue': None,
            'date_of_imaging': None,
            'random_file_number': None,
            'channel_id': None,
            'file_name': file_name,
            'patient': cell_line,
            'path': line
        }
