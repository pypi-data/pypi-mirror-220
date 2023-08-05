"""Contains functions which provide mapping of PNU types."""
from collections import namedtuple
from importlib.resources import files
from functools import lru_cache
import csv
import logging


@lru_cache
def read_pnu_map_file(pnu_map_file: str = None) -> list:
    """Creates a list of PNU map items based on a provided PNU type map file

    Parameters:
        pnu_map_file (str): Optional file to use for mapping. 
                                If nothing provided try to load mapping shipped with package.
    Returns:
        list: Containing PNU map items with fieldnames created from the header pnu_map_file. 
    """
    if not pnu_map_file:
        pnu_map_file = files('edcon.edrive.data').joinpath('pnu_map.csv')
    with open(pnu_map_file, encoding='ascii') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # Define a namedtuple where the header row determines the field names
        pnu_map_item = namedtuple('pnu_map_item', next(reader, None))

        logging.info(f"Load PNU map file: {pnu_map_file}")
        return [pnu_map_item(*row) for row in reader]


@lru_cache
def create_pnu_map() -> dict:
    """Creates a dict based on a provided PNU map item list.
        It maps PNU ids to provided PNU map items

    Returns:
        dict: PNU ids (key) and PNU items (value)
    """
    pnu_list = read_pnu_map_file()
    logging.info("Create mapping from PNU ids to PNU items")
    return {int(item.pnu): item for item in pnu_list}


@lru_cache
def create_parameter_map() -> dict:
    """Creates a dict based on a provided PNU map item list.
        It maps parameter ids to provided PNU map items

    Returns:
        dict: parameter ids (key) and PNU items (value)
    """
    pnu_list = read_pnu_map_file()
    logging.info("Create mapping from parameter ids to PNU items")
    return {item.parameter_id: item for item in pnu_list}


class PnuMap:
    """Class that provides a mapping from PNU to pnu_map_item."""

    def __init__(self) -> None:
        self.mapping = create_pnu_map()

    def __getitem__(self, pnu: int):
        """Determines the corresponding pnu_map_item from a provided PNU number

        Parameters:
            pnu (int): PNU number.
        Returns:
            value: pnu_map_item
        """
        return self.mapping[pnu]

    def __len__(self):
        return len(self.mapping)


class ParameterMap:
    """Class that provides a mapping from parameter id to pnu_map_item."""

    def __init__(self) -> None:
        self.mapping = create_parameter_map()

    def __getitem__(self, parameter_id: str):
        """Determines the corresponding pnu_map_item from a provided parameter id

        Parameters:
            parameter_id (str): Parameter id of the PNU type to be determined.
        Returns:
            value: pnu_map_item
        """
        axis, parameter_id, instance, _ = parameter_id.strip('P').split('.')
        return self.mapping[f'{axis}.{parameter_id}.{instance}']

    def __len__(self):
        return len(self.mapping)
