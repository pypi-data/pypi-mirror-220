# import tfields
#
# import w7x.simulation.extender
# from  w7x.simulation.backends.runner.base import Local, Job
#
#
# runner = Local()
#
#
# def control_file():
#     gridFile = (
#         "nr 173   # number of radial grid points\n"
#         "nz 170   # number of vertical grid points\n"
#         "nphi 141  # number of toroidal cut planes, never be fooled to believe"
#         " you can save too much on nphi\n"
#         "rmin 3.810000 # optional param., can be computed autom. from"
#         " boundary\n"
#         "rmax 6.870000 # optional parameter\n"
#         "zmax 1.450000 # optional parameter\n"
#     )
#     return gridFile
#
#
# class ExtenderWebServiceBackend(w7x.simulation.extender.ExtenderBackend):
#     @staticmethod
#     def _field(state, **kwargs) -> tfields.TensorFields:
#         """
#         The returned field can directly be used as a magnetic config grid with the
#         field line tracer
#         """
#         id_ = gen_run_id(obj, code="extender", unique=True)
#         points = kwargs.pop("points")
#         runner = 'local'
#         exe = rna.path.resolve(w7x.config."extender.{runner}.exe path=True))
#         options = ("-vmec_nyquist $NETCDFfile -i $CONTROL_FILE -c $COILfile -s"
#                    " $OUTPUT_SUFFIX $OTHER_OPTS > extender.out\n"
#         job = Job(
#             name=id_,
#             cwd=get(f"extender.{runner}", "folder", path=True),
#             shebang: "#!/bin/tcsh",
#             nodes: int=20,
#             tasks: int=64,
#             files=[(vmec_input.to_string(), get_indata_file_name(vmec_id))],
#             modules=[
#                 "intel/16.0",
#                 "mkl/11.3",
#                 "impi/5.1.3",
#                 "ddt/7.0",
#                 "nag_flib/intel/mk24",
#                 "hdf5-serial/1.8.18",
#                 "netcdf-serial/4.4.1.1",
#                 "anaconda/2/4.4.0",
#             ],
#             cmd=f"{exe} {options}",
#         )
#
#         field = None
#         return tfields.TensorFields(points, field)
#
#     @staticmethod
#     def _plasma_field(state, **kwargs) -> tfields.TensorFields:
#         raise NotImplementedError()
#
#
# def extend(args):
#     import subprocess
#
#     vmec_calc_url = (
#         "http://svvmec1.ipp-hgw.mpg.de:8080/vmecrest/v1/run/"
#         + args.vmec_id
#         + "/wout.nc"
#     )
#     coil_file = args.vmec_id + ".coil"
#     net_cdf_file = "wout.nc"
#     script_file = "runExtender.cmd"
#
#     work_dir = "~/Ascott/{args.vmec_id}".format(**locals())
#     rna.path.mkdir(work_dir, is_dir=True)
#     with rna.path.cd_tmp(work_dir):
#         logging.info("Writing '{script_file}'.".format(**locals()))
#         write_run_command(
#             args.vmec_id,
#             vmec_calc_url,
#             net_cdf_file=net_cdf_file,
#             script_file=script_file,
#             n_proc=32,
#             coil_file=coil_file,
#         )
#
#         logging.info("Making the coil file '{coil_file}'.".format(**locals()))
#         writeCoils(args.vmec_id, coil_file=coil_file)
#
#         logging.info("Making the grid/control file.")
#         write_control_file()
#
#         logging.info("Making the parameter file")
#         write_parameters_file(vmec_calc_url, args.vmec_id, net_cdf_file=net_cdf_file)
#
#         logging.info("Submitting it...")
#         subprocess.call("sbatch " + script_file, shell=True)
#         logging.info("  and now we wait...")
