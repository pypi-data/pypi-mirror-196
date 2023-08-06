import logging
import os
from dataclasses import dataclass
from enum import Enum, auto

LOG_LEVEL = logging.DEBUG


class Logger:
    """
    Implementation based on https://dotnettutorials.net/lesson/customized-logging-in-python/
    """

    def __init__(self, name, level=LOG_LEVEL):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S%p",
        )
        self.consoleHandler.setFormatter(formatter)
        self.logger.addHandler(self.consoleHandler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def set_level(self, level):
        self.consoleHandler.addFilter(LogFilter(level))


class LogFilter:
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        if self.__level == logging.INFO:
            return logRecord.levelno in [logging.INFO, logging.WARNING, logging.ERROR]
        else:
            return logRecord.levelno >= self.__level


class FileTypes(Enum):
    pdb_file = auto()
    glb_file = auto()
    ply_file = auto()
    ascii_file = auto()
    rgb_file = auto()
    xyz_low_file = auto()
    xyz_high_file = auto()
    thumbnail_file = auto()


@dataclass
class ProteinStructure:
    uniprot_id: str
    file_name: str = ""
    pdb_file: str = ""
    glb_file: str = ""
    ply_file: str = ""
    ascii_file: str = ""
    rgb_file: str = ""
    xyz_low_file: str = ""
    xyz_high_file: str = ""
    thumbnail_file: str = ""
    existing_files: dict = None
    scale: float = 1.0

    def __post_init__(self):
        self.update_existence()

    def update_existence(self):
        """Checks whether a fail is already existance in the corresponding directory, if so they will be skipped in some steps of the process."""
        if self.existing_files is None:
            self.existing_files = {}
        files = [
            self.__dict__[file] for file in self.__dict__.keys() if "_file" in file
        ]
        for file, file_type in zip(files, FileTypes.__members__):
            exists = False
            if os.path.exists(file):
                exists = True
            self.existing_files[FileTypes.__members__[file_type]] = exists

    def update_file_existence(self, file_type):
        if isinstance(file_type, list):
            for f_type in file_type:
                self.update_file_existence(f_type)
            return
        path = {
            FileTypes.pdb_file: self.pdb_file,
            FileTypes.glb_file: self.glb_file,
            FileTypes.ply_file: self.ply_file,
            FileTypes.ascii_file: self.ascii_file,
            FileTypes.rgb_file: self.rgb_file,
            FileTypes.xyz_low_file: self.xyz_low_file,
            FileTypes.xyz_high_file: self.xyz_high_file,
            FileTypes.thumbnail_file: self.thumbnail_file,
        }
        if os.path.exists(path[file_type]):
            self.existing_files[file_type] = True
        else:
            self.existing_files[file_type] = False


class ColoringModes(Enum):
    cartoons_ss_coloring = "cartoons_ss_coloring"
    cartoons_rainbow_coloring = "cartoons_rainbow_coloring"
    cartoons_heteroatom_coloring = "cartoons_heteroatom_coloring"
    cartoons_polymer_coloring = "cartoons_polymer_coloring"
    cartoons_chain_coloring = "cartoons_chain_coloring"
    cartoons_bFactor_coloring = "cartoons_bFactor_coloring"
    cartoons_nucleotide_coloring = "cartoons_nucleotide_coloring"
    surface_ss_coloring = "surface_ss_coloring"
    surface_rainbow_coloring = "surface_rainbow_coloring"
    surface_heteroatom_coloring = "surface_heteroatom_coloring"
    surface_polymer_coloring = "surface_polymer_coloring"
    surface_chain_coloring = "surface_chain_coloring"
    surface_electrostatic_coloring = "surface_electrostatic_coloring"
    surface_hydrophobic_coloring = "surface_hydrophobic_coloring"
    surface_bFactor_coloring = "surface_bFactor_coloring"
    surface_nucleotide_coloring = "surface_nucleotide_coloring"
    # surface_mfpl_coloring = "surface_mfpl_coloring"
    stick_ss_coloring = "stick_ss_coloring"
    stick_rainbow_coloring = "stick_rainbow_coloring"
    stick_heteroatom_coloring = "stick_heteroatom_coloring"
    stick_polymer_coloring = "stick_polymer_coloring"
    stick_chain_coloring = "stick_chain_coloring"
    stick_bFactor_coloring = "stick_bFactor_coloring"
    stick_nucleotide_coloring = "stick_nucleotide_coloring"
    ball_ss_coloring = "ball_ss_coloring"
    ball_rainbow_coloring = "ball_rainbow_coloring"
    ball_heteroatom_coloring = "ball_heteroatom_coloring"
    ball_polymer_coloring = "ball_polymer_coloring"
    ball_chain_coloring = "ball_chain_coloring"
    ball_bFactor_coloring = "ball_bFactor_coloring"
    ball_nucleotide_coloring = "ball_nucleotide_coloring"
    sphere_ss_coloring = "sphere_ss_coloring"
    sphere_rainbow_coloring = "sphere_rainbow_coloring"
    sphere_heteroatom_coloring = "sphere_heteroatom_coloring"
    sphere_polymer_coloring = "sphere_polymer_coloring"
    sphere_chain_coloring = "sphere_chain_coloring"
    sphere_bFactor_coloring = "sphere_bFactor_coloring"
    sphere_nucleotide_coloring = "sphere_nucleotide_coloring"

    @staticmethod
    def list_of_modes():
        return [mode.value for mode in ColoringModes]


class AlphaFoldVersion(Enum):
    v1 = "v1"
    v2 = "v2"
    v3 = "v3"
    v4 = "v4"

    @staticmethod
    def list_of_versions():
        return [ver.value for ver in AlphaFoldVersion]


class Database(Enum):
    AlphaFold = "alphafold"
    RCSB = "rcsb"
