import ast

import numpy as np

import nfl_veripy.analyzers as analyzers
import nfl_veripy.constraints as constraints
import nfl_veripy.dynamics as dynamics
from nfl_veripy.utils.nn import load_controller


def main_forward(params: dict) -> Tuple[Dict, Dict]:
    """Runs a forward reachability analysis experiment according to params."""
    np.random.seed(seed=0)

    dyn = dynamics.get_dynamics_instance(
        params["system"]["type"], params["system"]["feedback"]
    )

    controller = load_controller(
        system=dyn.__class__.__name__,
        model_name=params["system"]["controller"],
    )

    # Set up analyzer (+ parititoner + propagator)
    analyzer = analyzers.ClosedLoopAnalyzer(controller, dyn)
    analyzer.partitioner = params["analysis"]["partitioner"]
    analyzer.propagator = params["analysis"]["propagator"]

    initial_state_range = np.array(
        ast.literal_eval(params["analysis"]["initial_state_range"])
    )
    initial_state_set = constraints.state_range_to_constraint(
        initial_state_range, params["analysis"]["propagator"]["boundary_type"]
    )

    reachable_sets, analyzer_info = analyzer.get_reachable_set(
        initial_state_set, t_max=params["analysis"]["t_max"]
    )
