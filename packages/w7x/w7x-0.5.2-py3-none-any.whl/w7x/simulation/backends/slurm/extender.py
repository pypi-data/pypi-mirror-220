#  import numpy as np
#  from past.builtins import basestring
#
#  import transcoding as tc
#  import w7x
#
#
#  class mgrid_file:
#      """A set of routines to read/write mgrid files for VMEC/EXTENDER"""
#
#      def __init__(self, parameter):
#          if isinstance(parameter, basestring):
#              self.read(parameter)
#          else:
#              self.fromWebserviceConfig(parameter)
#
#      def flt_magnetic_config(self):
#          """
#          Store the mgrid file contents in an equivalent field line tracer
#          compatible magnetic conf datatype.
#          """
#          tracer = w7x.config.flt.web_service.server
#
#          # Figure out the coil groups (same coilgroup and current)
#          coils = []
#          currents = []
#          for coil in self.coils:
#              # Prepare the vertices
#              pf1 = tracer.types.PolygonFilament()
#              pf1.vertices = tracer.types.Points3D()
#              pf1.name = coil["name"]
#              pf1.vertices.x1 = coil["x"].tolist()
#              pf1.vertices.x2 = coil["y"].tolist()
#              pf1.vertices.x3 = coil["z"].tolist()
#
#              coils.append(pf1)
#              currents.append(coil["I"][0])
#
#          config = tracer.types.MagneticConfig()
#          config.coils = coils
#          config.coilsCurrents = currents
#
#          if self.filename is None:
#              config.name = "Config from mgrid_coilfile.py"
#          else:
#              config.name = self.filename
#
#          # Add a grid for caching the Biot-Savart law stage.
#          gridSymmetry = 5
#          grid = tracer.types.Grid()
#          grid.fieldSymmetry = gridSymmetry
#
#          cyl = tracer.types.CylindricalGrid()
#          cyl.numR, cyl.numZ, cyl.numPhi = 181, 181, 481
#          cyl.RMin, cyl.RMax, cyl.ZMin, cyl.ZMax = 4.05, 6.75, -1.35, 1.35
#
#          grid.cylindrical = cyl
#          config.grid = grid
#
#          return config
#
#      def fromWebserviceConfig(self, config):
#          coils = []
#          # for coilgroup in range(0,len(config))
#          for coilgroup, circuit in enumerate(config.circuit):
#              if np.abs(circuit.current) == 0.0:
#                  print(
#                      "No current in circuit/coilgroup {}/{} => "
#                      "skipping.".format(coilgroup, coilgroup + 1)
#                  )
#                  continue
#              for coil in circuit.currentCarrier:
#                  name = coil.name
#                  nWinds = coil.numWindings
#                  direction = coil.windingDirection
#                  x = np.array(coil.currentCarrierPrimitive[0].vertices.x1).T
#                  y = np.array(coil.currentCarrierPrimitive[0].vertices.x2).T
#                  z = np.array(coil.currentCarrierPrimitive[0].vertices.x3).T
#                  I = circuit.current * direction * nWinds * np.ones_like(x)  # noqa
#                  I[-1] = 0.0
#                  coils.append(
#                      {
#                          "x": x,
#                          "y": y,
#                          "z": z,
#                          "I": I,
#                          "coilgroup": coilgroup + 1,
#                          "name": name,
#                      }
#                  )
#          self.coils = coils
#          self.filename = None
#          self.nPeriods = 5
#
#      def save(self, filename):
#          with open(filename, "w") as f:
#              # Header
#              f.write("periods {}\n".format(self.nPeriods))
#              f.write("begin filament\n")
#              f.write("mirror NULL")  # The new line comes from next print
#
#              # Each coil
#              for c in self.coils:
#                  for i in range(0, len(c["x"])):
#                      f.write(
#                          "\n{: 12.8f} {: 12.8f} {: 12.8f} {: 15.8e}".format(
#                              c["x"][i], c["y"][i], c["z"][i], c["I"][i]
#                          )
#                      )
#                  f.write(" {} {}".format(c["coilgroup"], c["name"]))
#              f.write("\nend\n")
#
#      def load(self, filename):
#          import numpy as np
#
#          with open(filename, "r") as f:
#
#              # Read number of periods.
#              str = f.readline()
#              if str[0:8] != "periods ":
#                  raise ValueError('Missing "periods " in the beginning of file.')
#              nPeriods = int(str[8:])
#
#              # Read begin filament
#              str = f.readline()
#              if str[0:14] != "begin filament":
#                  raise ValueError('Missing "begin filament" in the beginning of file.')
#
#              # Read/skip "mirror NULL"
#              f.readline()
#
#              # Read coils
#              coils = []
#              while True:
#                  # Read segments
#                  x = np.array([], float)
#                  y = np.array([], float)
#                  z = np.array([], float)
#                  I = np.array([], float)  # noqa
#                  while True:
#                      strs = f.readline().split()
#                      v = [float(strs[i]) for i in range(0, 4)]
#                      x = np.append(x, v[0])
#                      y = np.append(y, v[1])
#                      z = np.append(z, v[2])
#                      I = np.append(I, v[3])  # noqa
#
#                      # Each coil is marked to end with a 0 Amps segment
#                      if v[3] == 0.0:
#                          coilgroup = int(strs[4])
#                          name = strs[5:]
#                          coils.append(
#                              {
#                                  "x": x,
#                                  "y": y,
#                                  "z": z,
#                                  "I": I,
#                                  "coilgroup": coilgroup,
#                                  "name": name,
#                              }
#                          )
#                          break
#                  # Check if we are at the end of file
#                  last_pos = f.tell()
#                  str = f.readline()
#                  if str[0:3].lower() == "end":
#                      break
#                  f.seek(last_pos)  # Go back where we were.
#          self.filename = filename
#          self.coils = coils
#          self.nPeriods = nPeriods
#
#      def scaleCurrents(self, scale):
#          for i in range(0, len(self.coils)):
#              self.coils[i]["I"] = scale * self.coils[i]["I"]
#          if not hasattr(self, "currentScalingHistory"):
#              self.currentScalingHistory = []
#          self.currentScalingHistory.append(scale)
#
#
#  def write_control_file(control_file="grid_in"):
#      gridFile = (
#          "nr 173   # number of radial grid points\n"
#          "nz 170   # number of vertical grid points\n"
#          "nphi 141  # number of toroidal cut planes, never be fooled to believe"
#          " you can save too much on nphi\n"
#          "rmin 3.810000 # optional param., can be computed autom. from"
#          " boundary\n"
#          "rmax 6.870000 # optional parameter\n"
#          "zmax 1.450000 # optional parameter\n"
#      )
#
#      with open(control_file, "w") as f:
#          f.write(gridFile)
#
#
#  def write_parameters_file(
#      vmec_calc_url, vmec_id, param_file="parameters.txt", net_cdf_file="wout.nc"
#  ):
#      with open(param_file, "w") as f:
#          f.write(vmec_calc_url + "\n")
#          f.write(vmec_id + "\n")
#          f.write(net_cdf_file + "\n")
#
#
#  def read_cylindrical(hybrid_path):
#      hybridFileBox = tc.Block(
#          "{header}",
#          "cyl.RMin, cyl.RMax = {RMin:f}, {RMax:f}",
#          "cyl.ZMin, cyl.ZMax = {ZMin:f}, {ZMax:f}",
#          "cyl.numR, cyl.numZ, cyl.numPhi = {numR:d}, {numZ:d}, {numPhi:d}",
#      )
#      transc = tc.Transcoding(hybridFileBox)
#      hybridPars = transc.read(hybrid_path)
#      hybridPars.pop("header")
#      cyl = w7x.flt.CylindricalGrid()
#      cyl.__dict__.update(hybridPars)
#      return cyl
#
#
#  # def write_run_command(
#  #     vmec_id,
#  #     vmec_calc_url,
#  #     net_cdf_file="wout.nc",
#  #     script_file="runExtender.cmd",
#  #     n_proc=32,
#  #     control_file="grid_in",
#  #     coil_file="w7x.coil",
#  # ):
#  #     script = (
#  #         "#!/bin/tcsh\n"
#  #         "\n"
#  #         "# Stdout and Sterr redirection\n"
#  #         "#SBATCH -o ./{vmec_id}.o%j\n"
#  #         "#SBATCH -e ./{vmec_id}.e%j\n"
#  #         "# Initial working directory:\n"
#  #         "#SBATCH -D ./\n"
#  #         "# Job Name :\n"
#  #         "#SBATCH -J extender-{vmec_id}\n"
#  #         "# Queue (Partition):\n"
#  #         "#SBATCH --partition=express\n"
#  #         "# Number of nodes and MPI tasks per node:\n"
#  #         "#SBATCH --nodes=20\n"
#  #         "#SBATCH --ntasks-per-node=64\n"
#  #         "# Enable Hyperthreading:\n"
#  #         "#SBATCH --ntasks-per-core=2\n"
#  #         "#\n"
#  #         "# Request 504 GB of main Memory per node in Units of MB:\n"
#  #         "#-- BATCH --mem=512000\n"
#  #         "#\n"
#  #         "#SBATCH --mail-type=all\n"
#  #         "#SBATCH --mail-user=dboe@rzg.mpg.de\n"
#  #         "# Wall clock limit:\n"
#  #         "#SBATCH --time=0:30:00\n"
#  #         "\n"
#  #         "echo Start...\n"
#  #         "\n"
#  #         "# Run the program:\n"
#  #         "\n"
#  #         "set BIN=/u/mad/bin/EXTENDER_P\n"
#  #         "\n"
#  #         "set RUN={vmec_id}\n"
#  #         "\n"
#  #         "echo Downloading netcdf.\n"
#  #         "wget {netCDFurl}\n"
#  #         "\n"
#  #         "set NETCDFfile={net_cdf_file}\n"
#  #         "set COILfile={coil_file}\n"
#  #         "set OUTPUT_SUFFIX=$RUN\n"
#  #         "set CONTROL_FILE={control_file}\n"
#  #         "\n"
#  #         "set OTHER_OPTS=-full\n"
#  #         "\n"
#  #         "\n"
#  #         "module load intel/16.0\n"
#  #         "module load mkl/11.3\n"
#  #         "module load impi/5.1.3\n"
#  #         "module load ddt/7.0\n"
#  #         "module load nag_flib/intel/mk24\n"
#  #         "module load hdf5-serial/1.8.18\n"
#  #         "module load netcdf-serial/4.4.1.1\n"
#  #         "module load anaconda/2/4.4.0\n"
#  #         "\n"
#  #         "echo Starting extender with srun\n"
#  #         "date\n"
#  #         "\n"
#  #         "echo srun $BIN -vmec_nyquist $NETCDFfile -i $CONTROL_FILE -c $COILfile"
#  #         " -s $OUTPUT_SUFFIX $OTHER_OPTS\n"
#  #         "srun $BIN -vmec_nyquist $NETCDFfile -i $CONTROL_FILE -c $COILfile -s"
#  #         " $OUTPUT_SUFFIX $OTHER_OPTS > extender.out\n"
#  #         "\n"
#  #         "date\n"
#  #         "\n"
#  #         "echo Extender finished\n"
#  #         "\n"
#  #         "echo 'Starting conversion to ASCOT format'\n"
#  #         "../to_ascoth5_onHGW.py > toascot.out\n"
#  #         "\n"
#  #         "echo 'Starting conversion to field line tracer format'\n"
#  #         "../ascoth5_to_fieldLineTracer.py $RUN.h5 $RUN.dat > totracer.out\n"
#  #         "\n".format(jobname=vmec_id, netCDFurl=vmec_calc_url, **locals())
#  #     )
#  #
#  #     with open(script_file, "w") as f:
#  #         f.write(script)
#
#
#  # def writeCoils(vmec_id, coil_file="wout.coil"):
#  #     w7x_config = Run(vmec_id).get_coils()
#  #     G = mgrid_file(w7x_config)
#  #     # invert currents
#  #     print("Scaling the coil currents by -1")
#  #     G.scaleCurrents(-1.0)
#  #     G.write(coil_file)
#
#
#  def extend(args):
#      import subprocess
#
#      vmec_calc_url = (
#          "http://svvmec1.ipp-hgw.mpg.de:8080/vmecrest/v1/run/"
#          + args.vmec_id
#          + "/wout.nc"
#      )
#      coil_file = args.vmec_id + ".coil"
#      net_cdf_file = "wout.nc"
#      script_file = "runExtender.cmd"
#
#      work_dir = "~/Ascott/{args.vmec_id}".format(**locals())
#      rna.path.mkdir(work_dir, is_dir=True)
#      with rna.path.cd_tmp(work_dir):
#          logging.info("Writing '{script_file}'.".format(**locals()))
#          write_run_command(
#              args.vmec_id,
#              vmec_calc_url,
#              net_cdf_file=net_cdf_file,
#              script_file=script_file,
#              n_proc=32,
#              coil_file=coil_file,
#          )
#
#          logging.info("Making the coil file '{coil_file}'.".format(**locals()))
#          writeCoils(args.vmec_id, coil_file=coil_file)
#
#          logging.info("Making the grid/control file.")
#          write_control_file()
#
#          logging.info("Making the parameter file")
#          write_parameters_file(vmec_calc_url, args.vmec_id, net_cdf_file=net_cdf_file)
#
#          logging.info("Submitting it...")
#          subprocess.call("sbatch " + script_file, shell=True)
#          logging.info("  and now we wait...")
#
