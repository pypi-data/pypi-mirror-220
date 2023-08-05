"""Post process Gromacs simulation outputs."""
import glob
import os
import MDAnalysis as mda
import nglview as nv

from inductiva.types import Path
from inductiva.utils.templates import (TEMPLATES_PATH)

SCENARIO_TEMPLATE_DIR = os.path.join(TEMPLATES_PATH, "protein_visualization")
GROMACS_TEMPLATE_INPUT_DIR = "gromacs"


class GROMACSSimulationOutput:
    """Post process a GROMACS simulation outputs."""

    def __init__(self, sim_output_path: Path = None):
        """Initializes a `SimulationOutput` object.

        Given a simulation output directory that contains the standard files
        generated by a GROMACS simulation run, this class provides methods to
        visualize the simulation outputs in a notebook.

        Args:
            sim_output_path: Path to the simulation output directory."""

        self.sim_output_dir = sim_output_path

    def render(self,
               pdb_file_name: str = None,
               trajectory_file_name: str = "trajectory.xtc"):
        """Visualize the simulation outputs in a notebook using NGLView.

        Args:
            pdb_file: Path to the PDB file to be visualized.
            trajectory_name: Name of the trajectory file to be visualized."""

        if pdb_file_name is None:
            pdb_pattern = os.path.join(self.sim_output_dir, "*.pdb")
            pdb_file_name = glob.glob(pdb_pattern)

            if pdb_file_name is None:
                raise ValueError("No PDB file found in the output directory.")

            if len(pdb_file_name) != 1:
                raise ValueError(
                    "Please specify the .pdb file to be visualized.")

        protein_file = os.path.join(self.sim_output_dir, pdb_file_name)
        trajectory = os.path.join(self.sim_output_dir, trajectory_file_name)
        system = mda.Universe(protein_file, trajectory)

        view = nv.show_mdanalysis(system)
        view.add_ball_and_stick(
            "all")  # Render the molecules as ball-and-stick models
        view.center()  # Center the view
        view.parameters = {
            "backgroundColor": "white"
        }  # Set the background color

        return view
