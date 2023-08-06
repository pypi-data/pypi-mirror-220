"""
Main entry point for the project when run from the command line
i.e. via $ python -m w7x
"""
import sys
import argparse
import os
import numpy as np

import rna
import rna.plotting
import tfields
import w7x


def extend(args):
    from w7x.simulation.vmec import Wout
    from w7x.simulation.extender import Extender
    from w7x.simulation.flt import FieldLineTracer
    from w7x.plotting.extender import FieldFigure

    if args.vmec_id:
        wout = Wout(file_id=args.vmec_id)
        state = wout.to_state()
    else:
        raise NotImplementedError()

    extender = Extender()

    if args.realistic:
        path = f"extended_field_of_vmec_id_{args.vmec_id}.dill"
        if args.load and os.path.exists(path):
            state = w7x.State.load(path)
        else:
            # The full field takes much longer
            state = extender.field(
                state,
            )

            # Save the state for later working with it
            state.save(path)

    else:
        path = f"extended_field_of_vmec_id_{args.vmec_id}_short.dill"
        # You can change the resolution of the grid by passing the points explicitly:
        # Here we show with a dummy grid which has uselessly small resolution
        if args.load and os.path.exists(path):
            state = w7x.State.load(path)
        else:
            state = extender.field(
                state,
                points=tfields.TensorGrid.empty(
                    (4.05, 6.75, 10j),
                    (
                        0,
                        2 * np.pi / 10,
                        20j,
                    ),  # np.pi / 10 -> 5 field periods, 2 fold symmetry
                    (0, 0, 1j),
                    coord_sys=tfields.bases.CYLINDER,
                    iter_order=[1, 0, 2],
                ),
            )

    if args.export:
        # TODO-1(@dboe) make this a function
        path = path.rstrip(".dill") + ".datc"
        # state.equilibrium.export("field", path)
        state.equilibrium.field.save(path)
        file_ = w7x.model.MGrid(data=state.equilibrium.field, path=path)
        state.equilibrium.field = rna.pattern.link.Link(
            ref=file_, fget=w7x.model.MGrid.to_numpy
        )
        state.resources.add(file_)

    ##########################################
    # display the field with a poincare plot #
    ##########################################
    if args.poincare:
        flt = FieldLineTracer()
        phi = 0
        state = flt.trace_poincare(
            state,
            phi=phi,
            seeds=tfields.Points3D([[5.8, 0.0, 0.0], [6.0, 0.0, 0.0]]),
            n_points=100,
        )
        rna.plotting.set_style()
        poincare_figure = w7x.plotting.Poincare()
        poincare_figure.gca().grid(color="lightgrey")
        poincare_figure.plot(state, phi=phi)
        rna.plotting.show()

    ####################################
    # Inspect the computed equilibrium #
    ####################################
    field = state.equilibrium.field

    # plot the field in the z=0 plane
    plot_field = field
    # plot_field = plot_field[plot_field[:, 1] == 0]  # select phi = 0
    # plot_field = plot_field[plot_field[:, 2] == 0]  # select z = 0
    plot_field = plot_field[
        w7x.lib.tfields.where_phi_between(plot_field, 0, 2 * np.pi / 5)
    ]
    plot_field = plot_field[plot_field[:, 2] == np.abs(plot_field[:, 2]).min()]
    plot_field.transform_field(tfields.bases.NATURAL_CARTESIAN, field_index=0)
    plot_field.transform(tfields.bases.CARTESIAN)
    fig = FieldFigure(plot_field)
    fig.plot()
    fig.show()


def poincare(args):
    """poincare plot creation"""
    phiList = args.phi.values

    if args.phi.deg:
        phiList = [val / 180 * np.pi for val in phiList]

    if not args.assemblies.off:
        machine = w7x.flt.Machine.from_mm_ids(*args.assemblies.values)
    else:
        machine = w7x.flt.Machine()

    relativeCurrents = args.magnetic_config.relativeCurrents
    dat_path = args.magnetic_config.path
    if dat_path:
        dat_path = tfields.lib.in_out.resolve(dat_path)
        cyl = w7x.extender.getHybridFromDat(dat_path)
        grid = w7x.flt.Grid(cylinder=cyl)
        magnetic_config = w7x.flt.MagneticConfig.from_dat_file(dat_path, grid=grid)
    elif relativeCurrents:
        magnetic_config = w7x.flt.MagneticConfig.from_currents(
            relativeCurrents=relativeCurrents
        )
    else:
        magnetic_config = w7x.flt.MagneticConfig.from_currents()

    """ plotting """
    axis = rna.plotting.gca(2)
    for phi in phiList:
        axis.grid(color="lightgrey")
        machine.plot_poincare(phi, axis=axis)
        magnetic_config.plot_poincare(phi, axis=axis)
        rna.plotting.save(
            "~/tmp/poincare-{phi:.4f}".format(**locals()), "png", "pgf", "pdf"
        )
        axis.clear()


def parse_args(args_):
    """Parse args."""
    # create the top-level parser
    parser = argparse.ArgumentParser(prog="w7x app", parents=[rna.parsing.LogParser()])
    parser.add_argument(
        "--version",
        action="version",
        version="v" + w7x.__version__,
        help="Show program's version number and exit",
    )
    parser.add_argument(
        "--distribute", "-d", action="store_true", help="distribute the work load"
    )

    # subparsers
    subparsers = parser.add_subparsers(help="sub-command help")

    # create the parser for the "extend" command
    parser_extend = subparsers.add_parser("extend", help="extend help")
    parser_extend.add_argument("vmec_id", type=str, help="vmec_id to extend")
    parser_extend.add_argument("-n", type=int, default=4, help="number of cores")
    parser_extend.add_argument(
        "--realistic", "-r", action="store_true", help="Compute a high res field"
    )
    parser_extend.add_argument(
        "--load", action="store_true", help="Load the state from file"
    )
    parser_extend.add_argument(
        "--export",
        action="store_true",
        help="Export the field to .datc file. -> fast communication with the web service.",
    )
    parser_extend.add_argument(
        "--poincare", action="store_true", help="Plot the poincare cross section"
    )
    parser_extend.add_argument(
        "--vmec_id",
        type=str,
        default=w7x.config.vmec.test.example_vmec_id,
        help="vmec_id of the run",
    )
    parser_extend.set_defaults(func=extend)

    # create the parser for the "poincare" command
    parser_poincare = subparsers.add_parser("poincare", help="poincare help")
    parser_poincare.add_argument(
        "--baseDir",
        type=str,
        default="~/Data/Strikeline/",
        help="already extended vmec_id",
    )
    parser_poincare.add_argument(
        "--phi", dest="phi.values", nargs="*", type=float, default=[0.0]
    )
    parser_poincare.add_argument(
        "--phi.deg",
        dest="phi.deg",
        help="switch phi from radian to degree",
        action="store_true",
    )
    parser_poincare.add_argument(
        "--assemblies",
        dest="assemblies.values",
        nargs="+",
        type=str,
        default=None,
    )
    parser_poincare.add_argument("--assemblies.off", action="store_true")
    parser_poincare.add_argument(
        "--magnetic_config.relativeCurrents",
        help="relative currents in case of vacuum config",
    )
    parser_poincare.add_argument(
        "--magnetic_config.coilConfig",
        help="set the coil config for the relative currents",
    )
    parser_poincare.add_argument(
        "--magnetic_config.path",
        default=None,
        help="create config with magnetic field grid at path",
    )
    parser_poincare.set_defaults(func=poincare)

    # If no arguments were used, print base-level help with possible commands.
    if len(args_) == 0:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    args_ = parser.parse_args(args_)
    # let argparse do the job of calling the appropriate function after
    # argument parsing is complete
    return args_.func(args_)


if __name__ == "__main__":
    _ = parse_args(sys.argv[1:])
