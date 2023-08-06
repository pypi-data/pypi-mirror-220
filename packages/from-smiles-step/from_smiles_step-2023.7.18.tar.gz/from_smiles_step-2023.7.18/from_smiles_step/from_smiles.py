# -*- coding: utf-8 -*-

"""a node to create a structure from a SMILES string"""

import logging
from pathlib import Path
import shutil
import string
import subprocess
import traceback

import from_smiles_step
import seamm
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("from_smiles")


class FromSMILES(seamm.Node):
    def __init__(self, flowchart=None, extension=None):
        """Initialize a specialized start node, which is the
        anchor for the graph.

        Keyword arguments:
        """
        logger.debug("Creating FromSMILESNode {}".format(self))

        super().__init__(
            flowchart=flowchart, title="from SMILES", extension=extension, logger=logger
        )

        self.parameters = from_smiles_step.FromSMILESParameters()

    @property
    def version(self):
        """The semantic version of this module."""
        return from_smiles_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return from_smiles_step.__git_revision__

    def description_text(self, P=None):
        """Return a short description of this step.

        Return a nicely formatted string describing what this step will
        do.

        Keyword arguments:
            P: a dictionary of parameter values, which may be variables
                or final values. If None, then the parameters values will
                be used as is.
        """

        if not P:
            P = self.parameters.values_to_dict()

        if P["notation"] == "perceive":
            if P["smiles string"][0] == "$":
                text = (
                    "Perceive the line notation (SMILES, InChI,...) and create the "
                    "structure from the string in the variable '{smiles string}', "
                )
            else:
                text = (
                    "Perceive the line notation (SMILES, InChI,...) and create the "
                    "structure from the string '{smiles string}', "
                )
        else:
            if P["smiles string"][0] == "$":
                text = (
                    "Create the structure from the {notation} in the variable"
                    " '{smiles string}', "
                )
            else:
                text = "Create the structure from the {notation} '{smiles string}', "

        handling = P["structure handling"]
        if handling == "Overwrite the current configuration":
            text += "overwriting the current configuration."
        elif handling == "Create a new configuration":
            text += "creating a new configuration for it."
        elif handling == "Create a new system and configuration":
            text += "creating a new system and configuration for it."
        else:
            raise ValueError(
                f"Do not understand how to handle the structure: '{handling}'"
            )

        sysname = P["system name"]
        if sysname == "use SMILES string":
            text += " The name of the system will be the SMILES string given."
        elif sysname == "use Canonical SMILES string":
            text += (
                " The name of the system will be the canonical SMILES of the"
                " structure."
            )
        else:
            text += f" The name of the system will be {sysname}."

        confname = P["configuration name"]
        if confname == "use SMILES string":
            text += " The name of the configuration will be the SMILES string given."
        elif confname == "use Canonical SMILES string":
            text += (
                " The name of the configuration will be the canonical SMILES of the"
                " structure."
            )
        else:
            text += f" The name of the configuration will be {confname}."

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def run(self):
        """Create 3-D structure from a SMILES string"""
        self.logger.debug("Entering from_smiles:run")

        next_node = super().run(printer)

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Print what we are doing
        printer.important(self.description_text(P))

        if P["smiles string"] is None or P["smiles string"] == "":
            return None

        notation = P["notation"]

        # Get the system
        system_db = self.get_variable("_system_db")

        handling = P["structure handling"]
        if handling == "Overwrite the current configuration":
            system = system_db.system
            if system is None:
                system = system_db.create_system()
            configuration = system.configuration
            if configuration is None:
                configuration = system.create_configuration()
            configuration.clear()
        elif handling == "Create a new configuration":
            system = system_db.system
            if system is None:
                system = system_db.create_system()
            configuration = system.create_configuration()
        elif handling == "Create a new system and configuration":
            system = system_db.create_system()
            configuration = system.create_configuration()
        else:
            raise ValueError(
                f"Do not understand how to handle the structure: '{handling}'"
            )

        # Create the structure in the given configuration
        text = P["smiles string"]
        if notation == "perceive":
            if len(text) == 27:
                tmp = text.split("-")
                if (
                    len(tmp) == 3
                    and len(tmp[0]) == 14
                    and len(tmp[1]) == 10
                    and len(tmp[2]) == 1
                ):
                    notation = "InChIKey"
        if notation == "perceive":
            if text[0:7] == "InChI=":
                notation = "InChI"
            else:
                notation = "SMILES"

        if notation == "SMILES":
            configuration.from_smiles(text)
        elif notation == "InChI":
            configuration.from_inchi(text)
        elif notation == "InChIKey":
            configuration.from_inchikey(text)
        else:
            raise RuntimeError(f"Can not handle line notation '{text}'")

        # Now set the names of the system and configuration, as appropriate.
        name = P["system name"]
        canonical_smiles = None
        if name != "keep current name":
            if name == "use SMILES string":
                name = configuration.smiles
            elif name == "use Canonical SMILES string":
                name = configuration.canonical_smiles
                canonical_smiles = name
            elif name == "use InChI":
                name = configuration.inchi
            elif name == "use InChIKey":
                name = configuration.inchikey
            system.name = name

        name = P["configuration name"]
        if name != "keep current name":
            if name == "use SMILES string":
                name = P["smiles string"]
            elif name == "use Canonical SMILES string":
                if canonical_smiles is None:
                    name = configuration.canonical_smiles
                else:
                    name = canonical_smiles
            elif name == "use InChI":
                name = configuration.inchi
            elif name == "use InChIKey":
                name = configuration.inchikey
            configuration.name = name

        # Finish the output
        printer.important(
            __(
                f"\n    Created a molecular structure with {configuration.n_atoms} "
                "atoms."
                f"\n           System name = {system.name}"
                f"\n    Configuration name = {configuration.name}",
                indent=4 * " ",
            )
        )
        printer.important("")

        # Add the citations for Open Babel
        self.references.cite(
            raw=self._bibliography["openbabel"],
            alias="openbabel_jcinf",
            module="from_smiles_step",
            level=1,
            note="The principle Open Babel citation.",
        )

        # See if we can get the version of obabel
        path = shutil.which("obabel")
        if path is not None:
            path = Path(path).expanduser().resolve()
            try:
                result = subprocess.run(
                    [str(path), "--version"],
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                    text=True,
                )
            except Exception:
                version = "unknown"
            else:
                version = "unknown"
                lines = result.stdout.splitlines()
                for line in lines:
                    line = line.strip()
                    tmp = line.split()
                    if len(tmp) == 9 and tmp[0] == "Open":
                        version = tmp[2]
                        month = tmp[4]
                        year = tmp[6]
                        break

            if version != "unknown":
                try:
                    template = string.Template(self._bibliography["obabel"])

                    citation = template.substitute(
                        month=month, version=version, year=year
                    )

                    self.references.cite(
                        raw=citation,
                        alias="obabel-exe",
                        module="from_smiles_step",
                        level=1,
                        note="The principle citation for the Open Babel executables.",
                    )

                except Exception as e:
                    printer.important(f"Exception in citation {type(e)}: {e}")
                    printer.important(traceback.format_exc())

        return next_node
