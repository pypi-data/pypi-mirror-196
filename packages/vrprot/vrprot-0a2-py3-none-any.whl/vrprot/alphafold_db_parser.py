#! python3
import gzip
import os
import shutil
import tarfile
import traceback
from argparse import Namespace
from dataclasses import dataclass, field

from . import classes, exceptions
from . import overview_util as ov_util
from . import util
from .classes import AlphaFoldVersion, ColoringModes
from .classes import FileTypes as FT
from .classes import Logger, ProteinStructure
from .overview_util import DEFAULT_OVERVIEW_FILE
from . import pointcloud2map_8bit as pcd2map
from . import sample_pointcloud as spc
from . import util
import multiprocessing as mp
from logging import _nameToLevel, INFO
import time
import threading


@dataclass
class AlphafoldDBParser:
    """Class to parse PDB files and convert them to ply.

    Raises:
        exceptions.ChimeraXException: If ChimeraX is not installed or cannot be found this Exception is raised.
    Args:
        WD (str): Working directory to store processing files and output files. Defaults to "./" .
        chimerax (str): Path to ChimeraX executable. Defaults to "chimerax"
        alphafold_ver (str): Defines the version of the AlphaFoldDB to be used. Options are "v1,v2,v3,v4".
        batch_size (int): Defines the size of each batch which is to be processed.
        processing (str): Defines the processing mode which is used to color the protein structures in ChimeraX. Defaults to "cartoons_ss_coloring".
        overview_file (str): Path to where to store the overview file in which the scale of each protein strucure and the color mode is stored. Defaults to "./static/csv/overview.csv".
        structures (dict[str,ProteinStructure]): Dictionary that maps strings of structures to the ProteinStructure object. Defaults to {}.
        not_fetched set[str]: Set of protein structures which could no be fetched. Deafults to [].
        keep_tmp dict[FT, bool]: Configuration to keep or remove processing files like PDB or GLB files after each processing step. Defaults to:
            {
                FT.pdb_file: True,
                FT.glb_file: False,
                FT.ply_file: False,
                FT.ascii_file: False,
            }
        log: logging.logger: Log with a specific name. Defaults to Logger("AlphafoldDBParser")
    """

    WD: str = util.WD
    chimerax: str = "chimerax"
    alphafold_ver: str = AlphaFoldVersion.v1.value
    batch_size: int = 50
    processing: str = ColoringModes.cartoons_ss_coloring.value
    overview_file: str = DEFAULT_OVERVIEW_FILE
    structures: dict[str, ProteinStructure] = field(default_factory=lambda: {})
    not_fetched: list[str] = field(default_factory=lambda: set())
    already_processed: list[str] = field(default_factory=lambda: set())
    keep_tmp: dict[FT, bool] = field(
        default_factory=lambda: {
            FT.pdb_file: True,
            FT.glb_file: False,
            FT.ply_file: False,
            FT.ascii_file: False,
        }
    )
    log: Logger = Logger("AlphafoldDBParser")
    img_size: int = 256
    db: str = classes.Database.AlphaFold.value
    overwrite: bool = False
    images: bool = False
    num_cached: int = None
    force_refetch: bool = False
    colors: list[str] = field(default_factory=lambda: ["red", "green", "blue"])
    gui: bool = False
    only_images: bool = False
    pcc_preview: bool = False
    multi_fraction = []
    parallel: bool = False
    pool_initialized: bool = False

    def update_output_dir(self, output_dir):
        """Updates the output directory of resulting images.

        Args:
            output_dir (_type_): _description_
        """

        self.OUTPUT_DIR = output_dir
        self.init_dirs()

    def update_existence(self, protein):
        """Updates the existence of the files for each protein structure."""
        if protein in self.structures:
            self.structures[protein].update_existence()

    def __post_init__(self) -> None:
        self.PDB_DIR = os.path.join(self.WD, "processing_files", "pdbs")
        self.PLY_DIR = os.path.join(self.WD, "processing_files", "plys")
        self.GLB_DIR = os.path.join(self.WD, "processing_files", "glbs")
        self.ASCII_DIR = os.path.join(self.WD, "processing_files", "ASCII_clouds")
        self.OUTPUT_DIR = os.path.join(self.WD, "processing_files", "MAPS")
        self.IMAGES_DIR = os.path.join(self.WD, "thumbnails")
        self.combine_thread = None

    def init_dirs(self, subs=True) -> None:
        """
        Initialize the directories.
        """
        self.OUTPUT_RGB_DIR = os.path.join(self.OUTPUT_DIR, "rgb")
        self.OUTPUT_XYZ_LOW_DIR = os.path.join(
            self.OUTPUT_DIR, os.path.join("xyz", "low")
        )
        self.OUTPUT_XYZ_HIGH_DIR = os.path.join(
            self.OUTPUT_DIR, os.path.join("xyz", "high")
        )
        self.IMAGES_DIR = os.path.join(self.OUTPUT_DIR, "thumbnails")
        directories = [var for var in self.__dict__.keys() if "_DIR" in var]
        if not subs:
            for var in directories:
                if "RGB" in var or "XYZ" in var:
                    directories.remove(var)

        for _dir in directories:
            path = self.__dict__[str(_dir)]
            os.makedirs(path, exist_ok=True)
        self.DIRS = {
            FT.pdb_file: self.PDB_DIR,
            FT.ply_file: self.PLY_DIR,
            FT.glb_file: self.GLB_DIR,
            FT.ascii_file: self.ASCII_DIR,
            "output": self.OUTPUT_DIR,
            FT.rgb_file: self.OUTPUT_RGB_DIR,
            FT.xyz_low_file: self.OUTPUT_XYZ_LOW_DIR,
            FT.xyz_high_file: self.OUTPUT_XYZ_HIGH_DIR,
            FT.thumbnail_file: self.IMAGES_DIR,
        }
        proteins = set(self.structures.keys())
        self.init_structures_dict(proteins)

    def get_filename(self, protein: str) -> str:
        """
        Get the filename of the protein.
        """
        return f"AF-{protein}-F1-model_{self.alphafold_ver}"

    def init_structures_dict(self, proteins: set[str]) -> dict[dict[str or dict[str]]]:
        for protein in proteins:
            # Catch cases in which the filename is already given
            file_name = self.get_filename(protein)
            pdb_file = os.path.join(self.PDB_DIR, file_name + ".pdb")
            glb_file = os.path.join(self.GLB_DIR, file_name + ".glb")
            ply_file = os.path.join(self.PLY_DIR, file_name + ".ply")
            ASCII_file = os.path.join(self.ASCII_DIR, file_name + ".xyzrgb")
            output_rgb = os.path.join(self.OUTPUT_RGB_DIR, file_name + ".png")
            output_xyz = file_name + ".bmp"
            output_xyz_low = os.path.join(self.OUTPUT_XYZ_LOW_DIR, output_xyz)
            output_xyz_high = os.path.join(self.OUTPUT_XYZ_HIGH_DIR, output_xyz)
            output_thumbnail = os.path.join(self.IMAGES_DIR, file_name + ".png")
            files = (
                pdb_file,
                glb_file,
                ply_file,
                ASCII_file,
                output_rgb,
                output_xyz_low,
                output_xyz_high,
                output_thumbnail,
            )
            structure = ProteinStructure(protein, file_name, *files)
            self.structures[protein] = structure
        return self.structures

    def fetch_pdb(self, proteins: list[str], on_demand: bool = True) -> None:
        """
        Fetches .pdb File from the AlphaFold Server. This function uses the request module from python standard library to directly download pdb files from the AlphaFold server. PDB files which are already stored locally wont be downloaded again. To enforce refetching of the PDB files, the self.force_fetch flag can be set to True.

        Args:
            proteins (list[str]): List of proteins to fetch.
            on_demand (bool): If True, the function will check if there is enough space on the disk to store the files. If not, it will delete the oldest files.

        Returns:
            None
        """
        if isinstance(proteins, str):
            proteins = set([proteins])
        if isinstance(proteins, list):
            proteins = set(proteins)
        self.init_structures_dict(proteins)
        # Check whether the result of the pipeline does already exist and if so, skip the download for these structures.
        proteins = self.filter_already_processed(proteins)
        if len(proteins) == 0:
            self.log.info(
                f"All structures of this batch: {proteins} are already fetched. wont download them again."
            )
            return

        # Check if there is enough space on the disk and collect all file that are not needed anymore until enough space is available
        if on_demand:
            tmp = util.free_space(
                self.DIRS,
                len(proteins),
                self.num_cached,
                proteins=proteins,
                version=self.alphafold_ver,
            )

        # Check which pdb files have to be fetched and which are already fetched.
        self.not_fetched = set()
        for protein in proteins:
            structure = self.structures[protein]
            self.log.debug(f"Checking if {protein} is already processed.")
            if not structure.existing_files[FT.pdb_file] or self.force_refetch:
                self.log.debug(f"Fetching {protein} from {self.db}.")
                if self.db == classes.Database.AlphaFold.value:
                    if util.fetch_pdb_from_alphafold(
                        protein,
                        self.PDB_DIR,
                        self.alphafold_ver,
                    ):
                        structure.existing_files[FT.pdb_file] = True
                    else:
                        self.not_fetched.add(protein)
                elif self.db == classes.Database.RCSB.value:
                    if util.fetch_pdb_from_rcsb(protein, self.PDB_DIR):
                        structure.existing_files[FT.pdb_file] = True
                    else:
                        self.not_fetched.add(protein)
            else:
                self.log.debug(
                    f"Structure {protein} is already processed and refetch is not allowed."
                )

        # Remove the collected files
        if on_demand:
            util.remove_cached_files(
                tmp, self.num_cached, len(proteins) - len(self.not_fetched)
            )

    def chimerax_process(self, proteins: list[str], processing: str or None) -> None:
        """
        Processes the .pdb files using ChimeraX and the bundle chimerax_bundle.py. Default processing mode is ColoringModes.cartoons_sscoloring
        As default, the source pdb file is NOT removed.
        To change this set self.keep_tmp[FT.pdb_file] = False.
        """
        colors = None
        import timeit

        self.chimerax = util.search_for_chimerax()
        if processing is None:
            processing = ColoringModes.cartoons_ss_coloring.value
        if processing.find("ss") != -1:
            colors = self.colors

        to_process = set()
        tmp_structs = []
        for protein in proteins:
            structure = self.structures[protein]
            if (
                (
                    not structure.existing_files[
                        FT.glb_file
                    ]  # Skip if GLB file is present
                    and not structure.existing_files[
                        FT.ply_file
                    ]  # Skip if PLY file is present
                    and not structure.existing_files[FT.ascii_file]
                    # Skip if ASCII file is present
                )
                and structure.existing_files[FT.pdb_file]  # check if source is there
                or (self.overwrite and structure.existing_files[FT.pdb_file])
            ):
                to_process.add(structure.pdb_file.split("/")[-1])
                tmp_structs.append(structure)
        # Process all Structures
        if len(to_process) > 0:
            self.log.info(f"Processing Structures:{to_process}")
            util.run_chimerax_coloring_script(
                self.chimerax,
                self.PDB_DIR,
                to_process,
                self.GLB_DIR,
                processing,
                colors,
                self.IMAGES_DIR,
                self.images,
                self.gui,
                self.only_images,
            )
            for structure in tmp_structs:
                structure.update_file_existence(
                    [FT.glb_file, FT.ply_file, FT.ascii_file]
                )
                if (
                    not self.keep_tmp[FT.pdb_file]
                    and structure.existing_files[FT.pdb_file]
                ):
                    os.remove(structure.pdb_file)
                self.structures[structure.uniprot_id] = structure

    def convert_glbs(self, proteins: list[str]) -> None:
        """
        Converts the .glb files to .ply files.
        As default, the source glb file is removed afterwards.
        To change this set self.keep_tmp[FT.glb_file] = True.
        """
        for protein in proteins:
            structure = self.structures[protein]
            structure.update_file_existence([FT.glb_file, FT.ply_file, FT.ascii_file])
            if (
                (
                    not structure.existing_files[FT.ply_file]
                    # Skip if PLY file is present
                    and not structure.existing_files[
                        FT.ascii_file
                    ]  # Skip if ASCII file is present
                )
                and structure.existing_files[FT.glb_file]
            ) or (self.overwrite and structure.existing_files[FT.glb_file]):
                if util.convert_glb_to_ply(
                    structure.glb_file, structure.ply_file, self.pcc_preview
                ):
                    self.log.debug(
                        f"Converted {structure.glb_file} to {structure.ply_file}"
                    )
                    if not self.keep_tmp[FT.glb_file]:
                        os.remove(structure.glb_file)  # remove source file
                    structure.update_file_existence([FT.ply_file, FT.glb_file])
                    self.structures[protein] = structure
                else:
                    self.log.warning(
                        f"Could not convert {structure.glb_file} to {structure.ply_file}"
                    )
            else:
                self.log.debug(
                    f"Structure {protein} is already processed and overwrite is not allowed."
                )

    def sample_pcd(self, proteins: list[str], async_call=False) -> None:
        """
        Samples the point cloud form the ply files.
        As default, the source ply file is removed afterwards.
        To change this set self.keep_tmp[FT.ply_file] = True.
        """
        for protein in proteins:
            structure = self.structures[protein]
            structure.update_file_existence([FT.ply_file, FT.ascii_file])
            if (
                not structure.existing_files[FT.ascii_file]
                and structure.existing_files[FT.ply_file]
            ) or (self.overwrite and structure.existing_files[FT.ply_file]):
                scale = spc.sample_pcd(
                    structure.ply_file,
                    structure.ascii_file,
                    self.img_size * self.img_size,
                    debug=self.pcc_preview,
                )
                structure.update_file_existence(FT.ascii_file)
                if structure.existing_files[FT.ascii_file]:
                    if not self.keep_tmp[FT.ply_file]:
                        os.remove(structure.ply_file)
                    structure.update_file_existence(FT.ply_file)
                    self.structures[protein] = structure
                    if not async_call:
                        self.write_scale(protein)
                        self.log.debug(
                            f"Sampled pcd to {structure.ascii_file} and wrote scale of {scale} to file {self.overview_file}"
                        )
                else:
                    self.log.warning(
                        f"Could not sample {structure.ply_file} to {structure.ascii_file}"
                    )

            else:
                self.log.warning(
                    f"PLY file for {protein} does not exist. Skipping sampling."
                )

    def gen_maps(self, proteins: list[str]) -> None:
        """
        Generates the maps from the point cloud files.
        If all of the output files already exists, this protein is skipped.
        As default, the source ascii point cloud is removed afterwards.
        To change this set self.keep_tmp[FT.ascii_file] = True.
        """
        for protein in proteins:
            structure = self.structures[protein]
            structure.update_file_existence(
                [
                    FT.ascii_file,
                    FT.rgb_file,
                    FT.xyz_low_file,
                    FT.xyz_high_file,
                ]
            )
            if (
                not (
                    structure.existing_files[FT.rgb_file]
                    and structure.existing_files[FT.xyz_low_file]
                    and structure.existing_files[FT.xyz_high_file]
                )
                and structure.existing_files[FT.ascii_file]
                or (self.overwrite and structure.existing_files[FT.ascii_file])
            ):
                pcd2map.pcd_to_png(
                    structure.ascii_file,
                    structure.rgb_file,
                    structure.xyz_low_file,
                    structure.xyz_high_file,
                    self.img_size,
                )
                self.log.debug(
                    f"Generated color maps {structure.rgb_file}, {structure.xyz_low_file} and {structure.xyz_high_file} with a size of {self.img_size}x{self.img_size} from {structure.ascii_file}"
                )
                if not self.keep_tmp[FT.ascii_file]:
                    os.remove(structure.ascii_file)
                self.structures[protein].update_file_existence(
                    [FT.rgb_file, FT.xyz_low_file, FT.xyz_high_file, FT.ascii_file]
                )

    def write_scale(self, protein) -> None:
        """
        Writes the scale of the protein to the overview file. This file is used to keep track of the scale of each protein structure.
        """
        # Write the scales you received all at once when parallelized
        structure = self.structures[protein]
        ov_util.write_scale(
            structure.uniprot_id,
            structure.scale,
            structure.pdb_file,
            self.processing,
            self.overview_file,
        )

    def set_version_from_filenames(self) -> None:
        """Iterates over all Directories and searches for files, which have Alphafold version number. If one is found, set the Parser to this version. All files are treated with this version."""
        for dir in self.DIRS.values():
            for file in os.listdir(dir):
                for version in list(AlphaFoldVersion):
                    if file.find(version.value) >= 0:
                        self.alphafold_ver = version.value
                        return

    def proteins_from_list(self, proteins: list[str]) -> None:
        """Add all uniprot_ids from the list to the set of proteins."""
        self.set_version_from_filenames()
        # self.init_structures_dict(proteins)
        self.batch(
            [self.fetch_pdb, self.pdb_pipeline],
            proteins,
            self.batch_size,
            on_demand=False,
        )

    def proteins_from_dir(self, source: str) -> None:
        """
        Processes proteins from a directory. In the source directory, the program will search for each of the available file types. Based on this, the class directories are initialized. The program will then start at the corresponding step for each structure.
        """

        self.multi_fraction.append(util.find_fractions(source))
        self.combine_thread = threading.Thread(
            util.combine_fractions(
                self.PDB_DIR, self.GLB_DIR, self.processing, gui=self.gui
            )
        )
        self.combine_thread.start()

        file_list = os.listdir(source)
        files = []
        for file in file_list:
            self.check_dirs(file, source)
            if file.endswith((".pdb", ".glb", ".ply", ".xyzrgb", ".png", ".bmp")):
                files.append(file)
        del file_list
        self.alphafold_ver = (
            files[0].split("/")[-1].split("_")[1]
        )  # extract the Alphafold version from the first file
        self.alphafold_ver = self.alphafold_ver[: self.alphafold_ver.find(".")]
        proteins = set()
        for file in files:
            file_name = file.split("/")[-1]
            proteins.add(file_name.split("-")[1])

        self.init_structures_dict(proteins)
        self.batch([self.pdb_pipeline], proteins, self.batch_size, on_demand=False)

    def pdb_pipeline(self, proteins: list[str], **kwargs) -> None:
        """
        Default pipeline which is used in all program modes.
        For each structure, the PDB file we be processed in chimerax and exported as GLB file. This GLB file will be converted into a PLY file.
        The PLY file is used to sample the point cloud which will be saved as an ASCII point cloud. This ASCII point cloud will then be used to generate the color maps (rgb, xyz_low and xyz_high).
        """
        tmp = ", ".join(proteins)
        proteins = self.filter_already_processed(proteins)
        proteins = [
            p for p in proteins if p not in self.not_fetched
        ]  # If they are not fetched, You wont be able to process them
        not_multi_fraction = [
            proteins for proteins in proteins if proteins not in self.multi_fraction
        ]

        if len(not_multi_fraction) == 0:
            self.log.info(
                f"All structures of this batch: {tmp} are already processed. Skipping this batch."
            )
            return
        # clean up exiting glb files
        if self.overwrite:
            for protein in not_multi_fraction:
                structure = self.structures[protein]
                if structure.existing_files[FT.glb_file]:
                    os.remove(structure.glb_file)
                    structure.update_file_existence([FT.glb_file])
                    self.structures[protein] = structure

        try:
            chimeraX_thread = threading.Thread(
                target=self.chimerax_process,
                args=(
                    not_multi_fraction,
                    self.processing,
                ),
            )
            chimeraX_thread.start()
        except Exception as e:
            traceback.print_exc(e)
            raise exceptions.ChimeraXException

        if self.only_images:
            chimeraX_thread.join()
            if self.combine_thread:
                self.combine_thread.join()
            return

        if self.parallel and len(proteins) > 1 and os.cpu_count() > 2:
            self.fill_queue(proteins)
            if chimeraX_thread.is_alive():
                chimeraX_thread.join()
            if self.combine_thread:
                self.combine_thread.join()
            return

        chimeraX_thread.join()
        if self.combine_thread:
            self.combine_thread.join()
        for protein in proteins:
            self.structures[protein].update_file_existence([FT.glb_file])
        # If the program is not parallelized, run the pipeline sequentially
        self.log.debug("Converting GLBs to PLYs...")
        self.convert_glbs(proteins)
        self.log.debug("Sampling PointClouds...")
        self.sample_pcd(proteins)
        self.log.debug("Generating Color Maps...")
        self.gen_maps(proteins)

    def fetch_pipeline(self, proteins: set[str], **kwargs) -> None:
        """
        Fetch of the structure from the alphafold db.
        """
        if isinstance(proteins, str):
            proteins = set([proteins])
        if isinstance(proteins, list):
            proteins = set(proteins)
        self.init_structures_dict(proteins)
        self.log.debug("Structure Dict initialized.")
        proteins = self.filter_already_processed(proteins)
        if len(proteins) == 0:
            self.log.info("All structures are already processed. Skipping this batch.")
            return
        self.batch(
            [self.fetch_pdb, self.pdb_pipeline], proteins, self.batch_size, **kwargs
        )
        self.log.info(f"Missing Structures:{self.not_fetched}")

    def filter_already_processed(self, proteins: list[str]) -> list[str]:
        """
        Filter out the proteins that have already been processed.
        """
        to_process = []
        for protein in proteins:
            if not self.output_exists(self.structures[protein]):
                to_process.append(protein)
            else:
                self.already_processed.add(protein)
        return to_process

    def output_exists(self, structures: ProteinStructure) -> bool:
        """
        Checks if the output files already exist in the  output directory.
        """
        if self.overwrite:
            return False
        for file in [
            structures.rgb_file,
            structures.xyz_low_file,
            structures.xyz_high_file,
        ]:
            if not os.path.isfile(file):
                return False
        return True

    def check_dirs(self, file: str, source: str) -> None:
        """
        Check wether a source file is in different directory than the default directory. If so set the corresponding directory to the source.
        """
        # TODO reduce to do this only once for each file type.
        if self.PDB_DIR != source:
            if file.endswith(".pdb"):
                self.PDB_DIR = source
        if self.GLB_DIR != source:
            if file.endswith(".glb"):
                self.GLB_DIR = source
        if self.PLY_DIR != source:
            if file.endswith(".ply"):
                self.PLY_DIR = source
        if self.ASCII_DIR != source:
            if file.endswith(".xyzrgb"):
                self.ASCII_DIR = source
        if self.OUTPUT_DIR != source:
            if file.endswith((".png", ".bmp")):
                self.OUTPUT_DIR = source

    def set_dirs(self, args: Namespace) -> None:
        """Uses arguments from the argument parser Namespace and sets the directories to the corresponding values."""
        # Set the directories for the files to be saved
        if args.pdb_file is not None:
            self.PDB_DIR = args.pdb_file
        if args.glb_file is not None:
            self.GLB_DIR = args.glb_file
        if args.ply_file is not None:
            self.PLY_DIR = args.ply_file
        if args.cloud is not None:
            self.ASCII_DIR = args.cloud
        if args.map is not None:
            self.OUTPUT_DIR = args.map
        self.init_dirs()

    def set_keep_tmp(self, args: Namespace) -> None:
        """Uses arguments from the argument parser Namespace and sets the switch to keep or to remove the corresponding file types after a processing step is completed."""
        if args.keep_pdb is not None:
            self.keep_tmp[FT.pdb_file] = args.keep_pdb
        if args.keep_glb is not None:
            self.keep_tmp[FT.glb_file] = args.keep_glb
        if args.keep_ply is not None:
            self.keep_tmp[FT.ply_file] = args.keep_ply
        if args.keep_ascii is not None:
            self.keep_tmp[FT.ascii_file] = args.keep_ascii

    def set_batch_size(self, args: Namespace) -> None:
        """Parsers arguments from the argument parser Namespace and sets the batch size to the corresponding value."""
        if args.batch_size is not None:
            self.batch_size = args.batch_size

    def set_alphafold_version(self, args: Namespace) -> None:
        """Parsers arguments from the argument parser Namespace and sets the alphafold version to the corresponding value."""
        if args.alphafold_version is not None:
            for value in AlphaFoldVersion.__members__.keys():
                if value == args.alphafold_version:
                    self.alphafold_ver = value
                    break

    def set_coloring_mode(self, args: Namespace) -> None:
        if args.color_mode is not None:
            self.processing = args.color_mode

    def set_img_size(self, args: Namespace) -> None:
        if args.img_size is not None:
            self.img_size = args.img_size

    def set_database(self, args: Namespace) -> None:
        if args.database is not None:
            self.db = args.database

    def execute_fetch(self, proteins: str) -> None:
        """Uses a list of proteins to fetch the PDB files from the alphafold db. This PDB files will then be used to generated the color maps."""
        proteins = proteins.split(",")
        self.log.debug(f"Proteins to fetch from Alphafold:{proteins}")
        self.fetch_pipeline(proteins)

    def execute_from_object(self, proteins: list[str]) -> None:
        """Uses a list of proteins which are extracted from a Python object. This assumes that the PDB files of these structures already exist in the PDB directory."""
        self.proteins_from_list(proteins)

    def execute_local(self, source: str) -> None:
        """Will extract all Uniprot IDs from a local directory. Assumes that the file names have a the following format:
        AF-<Uniprot ID>-F1-model-<v1/v2>.[pdb/glb/ply/xyzrgb]"""
        self.proteins_from_dir(source)

    def execute_from_bulk(self, source: str):
        """Will extract all PDB files from a tar archive downloaded from AlphafoldDB to Process all structures within it with the desired processing mode. Furthermore, multi fraction structures are combined to one large structure. These structures are not handled with the desired processing mode."""
        self.extract_archive(source)
        self.proteins_from_dir(self.PDB_DIR)

    def extract_archive(self, source: str) -> None:
        """Extracts a tar archive to the PDB directory."""
        tar = tarfile.open(source)
        ext = ".pdb.gz"
        for member in tar.getmembers():
            if member.name.endswith(ext):
                tar.extract(member, self.PDB_DIR)
        tar.close()

        for file in os.listdir(self.PDB_DIR):
            if file.endswith(ext):
                in_file = os.path.join(self.PDB_DIR, file)
                out_file = os.path.join(self.PDB_DIR, file.replace(".gz", ""))
                with gzip.open(in_file, "rb") as f_in:
                    with open(out_file, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(in_file)

    def clear_default_dirs(self) -> None:
        """Clears the default directories."""
        processing_files = os.path.join(
            self.WD,
            "processing_files",
        )
        util.remove_dirs(processing_files)

    def set_chimerax(self, args: Namespace):
        if args.chimerax is not None:
            self.chimerax = args.chimerax

    def set_thumbnails(self, args: Namespace):
        if args.thumbnails is not None:
            self.images = args.thumbnails

    def set_gui(self, args: Namespace):
        if args.with_gui is not None:
            self.gui = args.with_gui

    def set_only_images(self, args: Namespace):
        if args.only_images is not None:
            self.only_images = args.only_images

    def set_pcc_preview(self, args: Namespace):
        if args.pcc_preview is not None:
            self.pcc_preview = args.pcc_preview

    def set_overwrite(self, args: Namespace):
        if args.overwrite is not None:
            self.overwrite = args.overwrite

    def set_console_log_level(self, args: Namespace):
        if isinstance(args, str):
            level = _nameToLevel[args]
            self.log.set_level(level)
            util.log.set_level(level)
            spc.log.set_level(level)
            pcd2map.log.set_level(level)
        elif args.log_level is not None:
            level = _nameToLevel[args.log_level]
            self.log.set_level(level)
            util.log.set_level(level)
            spc.log.set_level(level)
            pcd2map.log.set_level(level)

    def set_parallel(self, args: Namespace):
        if args.parallel is not None:
            self.parallel = args.parallel

    def set_all_arguments(self, args: Namespace):
        for func in [
            self.set_batch_size,
            self.set_dirs,
            self.set_alphafold_version,
            self.set_coloring_mode,
            self.set_chimerax,
            self.set_img_size,
            self.set_database,
            self.set_keep_tmp,
            self.set_only_images,
            self.set_thumbnails,
            self.set_gui,
            self.set_pcc_preview,
            self.set_overwrite,
            self.set_console_log_level,
            self.set_parallel,
        ]:
            func(args)

    def batch(
        self, funcs: list[object], proteins: list[str], batch_size: int = 50, **kwargs
    ) -> None:
        """Will run the functions listed in funcs in a batched process."""
        start = 0
        end = batch_size
        que = list(proteins).copy()
        if len(proteins) <= batch_size:
            self.parallel = False
        if self.parallel and os.cpu_count() > 2:
            np = os.cpu_count() - 1
            self.pool_initialized = True
            self.mp_manager = mp.Manager()
            self.mp_queue = self.mp_manager.Queue()
            self.to_process = set()
            self.result_dict = mp.Manager().dict()
            self.mp_structure_dict = mp.Manager().dict()
            self.all_done = mp.Manager().Event()
            self.pool = mp.Pool(np)
            for protein in proteins:
                self.mp_structure_dict[protein] = self.structures[protein]
            args = [
                self.mp_queue,
                self.result_dict,
                self.all_done,
                self.mp_structure_dict,
                self.overwrite,
                self.img_size,
                self.keep_tmp,
            ]
            [self.pool.apply_async(worker_setup, args) for _ in range(np)]
            self.log.info(f"Runs in parallel with {np} processes.")

        while len(que) > 0:
            self.log.debug(f"Starting Batch form: {start} to {end}")
            batch_proteins = que[:batch_size]
            for func in funcs:
                func(batch_proteins, **kwargs)
            start = end
            end += batch_size
            del que[:batch_size]

        if self.parallel and self.pool_initialized:
            self.all_done.set()
            np = os.cpu_count() - 1
            [self.mp_queue.put(None) for _ in range(np)]

            self.mp_queue.join()
            self.pool.terminate()
            self.pool.join()
            for protein, structure in self.result_dict.items():
                self.to_process.remove(protein)
                self.structures[protein] = structure
                self.write_scale(protein)
        self.log.info("=" * 30)
        self.log.info("All Batches, done!")

    def fill_queue(self, proteins: list[str]):
        while len(proteins) > 0:
            tmp = []
            for p in proteins:
                if p in self.to_process:
                    continue
                structure = self.structures[p]
                self.structures[p].update_file_existence(FT.glb_file)
                if structure.existing_files[FT.glb_file]:
                    self.mp_queue.put(p)
                    self.to_process.add(p)
                    continue
                tmp.append(p)
            proteins = tmp


class AlphafoldDBParser_Worker:
    def __init__(
        self,
        queue,
        result_dict,
        all_done,
        structure_dict,
        overwrite,
        img_size,
        keep_tmp,
    ):
        self.parser = AlphafoldDBParser(
            overwrite=overwrite, img_size=img_size, keep_tmp=keep_tmp
        )
        self.queue = queue
        self.all_done = all_done
        self.result_dict = result_dict
        self.structure_dict = structure_dict
        self.log = self.parser.log
        self.parser.structures = self.structure_dict

    def run(self):
        class Args:
            log_level = "INFO"

        self.parser.set_console_log_level(Args())
        while True:
            protein = self.queue.get()
            if protein is None:
                self.queue.task_done()
                break
            proteins = [protein]
            structure = self.parser.structures[protein]

            while not self.parser.structures[protein].existing_files[FT.glb_file]:
                self.log.debug(f"Waiting for GLB files of: {protein}")
                structure.update_file_existence(FT.glb_file)
                self.parser.structures[protein] = structure
            self.log.debug(f"Converting GLBs to PLYs for: {protein}")
            self.parser.convert_glbs(proteins)

            # while not self.parser.structures[protein].existing_files[FT.ply_file]:
            #     self.log.debug("Waiting for PLY files...")
            #     structure.update_file_existence(FT.ply_file)
            #     self.parser.structures[protein] = structure

            self.log.debug(f"Sampling PointClouds for: {protein}")
            self.parser.sample_pcd(proteins, async_call=True)

            # while not self.parser.structures[protein].existing_files[FT.ascii_file]:
            #     self.log.debug("Waiting for ASCII files...")
            #     structure.update_file_existence(FT.ascii_file)
            #     self.parser.structures[protein] = structure

            self.log.debug(f"Generating Color Maps for: {protein}")
            self.parser.gen_maps(proteins)

            self.result_dict[protein] = self.parser.structures[protein]
            self.queue.task_done()


def worker_setup(
    queue, result_dict, all_done, structures, overwrite, img_size, keep_tmp
):
    worker = AlphafoldDBParser_Worker(
        queue=queue,
        result_dict=result_dict,
        all_done=all_done,
        structure_dict=structures,
        overwrite=overwrite,
        img_size=img_size,
        keep_tmp=keep_tmp,
    )
    worker.run()
