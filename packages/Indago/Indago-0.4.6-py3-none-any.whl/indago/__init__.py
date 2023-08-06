# -*- coding: utf-8 -*-


__version__ = '0.4.6'

from indago._optimizer import Optimizer, CandidateState
from indago._utility import minimize, minimize_exhaustive, inspect, inspect_optimizers

from indago._pso import PSO
from indago._fwa import FWA
from indago._ssa import SSA
from indago._de import DE
from indago._ba import BA
from indago._efo import EFO
from indago._mrfo import MRFO
from indago._abc import ABC
from indago._direct_search import NelderMead, MSGS

optimizers = [PSO, FWA, SSA, DE, BA, EFO, MRFO, ABC, NelderMead, MSGS]
"""list of Optimizer : A list of all available Indago optimizer classes."""

optimizers_name_list = [o.__name__ for o in optimizers]
"""list of str : A list of all available Indago method names (abbreviations)."""

optimizers_dict = {o.__name__: o for o in optimizers}
"""dict : A dict of all available Indago optimizers, in the form of method
    name (abbreviation, type: str) as key, and optimizer class (type: Optimizer) as value."""

# Undocumented optimizers
from indago._mmo import MMO
from indago._sa import SA





