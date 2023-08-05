# (c) 2022 DTU Wind Energy
"""
Class and associated class methods to work with landcover tables.
"""

import copy
import inspect
import json
import logging

import numpy as np

from windkit.plot.color import Color

logger = logging.getLogger(__name__)


class LandCoverTable(dict):
    """Subclass of dictionary that provides a lookup table for landcover and roughness.

    levels: list of float, optional. Default: None
        List of values marking different color bins, both min and max level should be
        included. If levels is None, no color is added. If level is 'default', a
        default list of 15 levels from 0 to 1, plus a level of 100 is included.
    colors: list of colors (rgb-tuple or html-str), optional. Default: None
        If tuple, should have 3 values, if string should have leading '#'.  List should
        be one less than the number of levels. If None, no color is added to the
        table. If 'default', a default list of 15 colors that represent the levels
        as roughness lengths is provided.
    """

    def __init__(self, *args, levels=None, colors=None, **kwargs):
        super().__init__(*args, **kwargs)
        for value in self.values():
            if not all(key in value for key in ["z0", "d", "desc"]):
                raise KeyError(
                    inspect.cleandoc(
                        """The dictionary that defines the landcover table at least has to contain `z0`, `d`, and `desc`"""
                    )
                )
        if levels is not None and colors is not None:
            if levels == "default":
                levels = None
            if colors == "default":
                colors = None
            self.add_colors_to_table(levels, colors)

    def __str__(self):
        desc = "id = LandCoverID\nz0 = Roughness length (m)\nd = Displacement height (m)\ndesc = Description\n"
        desc += "id\tz0\td\tdesc\n"
        for key, value in self.items():
            desc += "{0}\t{1:.4f}\t{2:.1f}\t{3}\n".format(
                key, value["z0"], value["d"], value["desc"]
            )
        return desc

    def _to_matrix(self):
        """Convert to numpy matrix

        Returns
        -------
        arr : numpy
            Array of landcover values

        Notes
        -----
        The fortran needs a numpy matrix to be passed in, so we convert
        the class above.
        """
        arr = np.array(
            [
                list(self.keys()),
                [d["z0"] for d in self.values()],
                [d["d"] for d in self.values()],
            ],
            dtype="f",
            order="F",
        )
        return arr.transpose()

    @classmethod
    def _from_matrix(cls, arr):
        """Create from numpy matrix

        Returns
        -------
        LandCoverTable
            Landcover table with values from a numpy matrix

        Notes
        -----
        The fortran needs a numpy matrix to be passed in, so we convert
        the class above.
        """
        dic = {int(val[0]): {"z0": val[1], "d": val[2], "desc": ""} for val in arr}

        return cls(dic)

    @classmethod
    def from_dict_ora(cls, dic, z0frac=0.1, dfrac=2 / 3, makecopy=True):
        """Use ORA model to convert tree height to LandCoverTable.

        Use ORA model :cite:`Floors2018b` for describing
        roughness and displacement. Optionally one can specify
        a fraction for the roughness length z0frac and a
        fraction for the displacement dfrac in the
        dictionary. If these are not given they will be
        used from the function arguments.

        Required in the dictionary are
        * h: tree height [m]

        Parameters
        ----------
        dic: dict
            Dictionary with tree heights to be converted.

        Returns
        -------
        LandCoverTable
            LandCoverTable class with valid roughness and displacement.

        Raises
        ------
        KeyError
            For landcover classes that don't have the keys to run
            the ORA model (h) nor the WAsP required keys z0 and d.

            * h: tree height [m]
        """
        if makecopy:
            dic = copy.deepcopy(dic)

        for key, value in dic.items():
            if all(key in value for key in ["h"]):
                if all(key in value for key in ["z0frac", "dfrac"]):
                    z0, d = (value["h"] * value["z0frac"], value["h"] * value["dfrac"])
                else:
                    z0, d = (value["h"] * z0frac, value["h"] * dfrac)
                dic[key]["z0"] = z0
                dic[key]["d"] = d
                dic[key][
                    "desc"
                ] = """Result from ORA model, z0={0}*h, d={1}*h""".format(z0frac, dfrac)
            elif not all(key in value for key in ["z0", "d"]):
                raise KeyError(
                    inspect.cleandoc(
                        """Tree height (h) is required for this model. No values for z0 and d can be found or were specified."""
                    )
                )

        return cls(dic)

    @classmethod
    def read_json(cls, filename):
        """Create LandCoverTable from json file.

        Parameters
        ----------
        filename : str or Path
            Path to file with landcover descriptions.

        Returns
        -------
        LandCoverTable
            filled from JSON file.
        """
        with open(filename, "r") as f:
            dic = json.load(f)
        dic = {int(float(k)): v for k, v in dic.items()}
        for key, value in dic.items():
            if not all(key in value for key in ["z0", "desc"]):
                error = """A roughness length and a description are missing for LandCoverID {0}"""
                raise ValueError(error.format(key))
            if "d" not in value:
                dic[key]["d"] = 0.0
                logger.info(
                    "A displacement height of 0.0 m was assumed for LandCoverID %s", key
                )

        return cls(dic)

    @classmethod
    def _from_z0s(cls, z0s):
        """Create landcover table filled with 0 displacement and no description

        Parameters
        ----------
        z0s : array like
            1D List of unique roughness lengths
        """
        return cls(
            {(i + 1): {"z0": z0, "d": 0.0, "desc": ""} for i, z0 in enumerate(z0s)}
        )

    def to_json(self, filename):
        """Write landcover table to json.

        Parameters
        ----------
        filename : str
            Path to write landcover file to
        """
        with open(filename, "w") as f:
            json.dump(self, f, indent=4)

    def add_colors_to_table(
        self, levels=None, colors=None, html=False, ignore_collisions=True
    ):
        """
        Return the landover table with an additional / updated color column.

        Parameters
        ----------
        levels: list of float, optional. Default: None
            List of values marking different color bins, both min and max level should be
            included. If levels is None, a default list of 15 levels from 0 to 1, plus a
            level of 100 is included.
        colors: list of colors (rgb-tuple or html-str), optional. Default: None
            If tuple, should have 3 values, if string should have leading '#'.  List should
            be one less than the number of levels. If None, a default list of 15 colors that
            represent the levels as roughness lengths is provided.
        html: bool, optional. Default: False
            If True, the colors will be in html format.
        ignore_collisions: bool, optional. Default: True
            if True, will raise an error if several roughness map to the same
            color.
        """
        color_manager = Color(levels, colors)
        z0 = [d["z0"] for d in self.values()]
        index = np.searchsorted(color_manager._levels, z0, side="right") - 1
        colors = color_manager.get_color_list(html=html, index=index)
        for i, key in enumerate(self.keys()):
            self[key]["color"] = colors[i]

        if not ignore_collisions:
            color_manager._check_for_duplicates(index, z0, retrieve=True)
