import os
import subprocess
import w7x


def install():
    # TODO set machine variable
    # gxx_linux-64 in conda env
    # TODO-TODO conda install -c conda-forge gfortran
    # TODO set binary path of vmec in default for this lib

    base_dir = w7x.config.general.cache
    stellopt_dir = os.path.join(base_dir, "STELLOPT")

    if not os.path.exists(stellopt_dir):
        # clone the repository using SSH
        ssh_url = "git@github.com:PrincetonUniversity/STELLOPT.git"
        https_url = "https://github.com/PrincetonUniversity/STELLOPT.git"
        os.makedirs(base_dir, exist_ok=True)

        try:
            subprocess.check_call(["git", "clone", ssh_url], cwd=base_dir)
        except subprocess.CalledProcessError:
            subprocess.check_call(["git", "clone", https_url], cwd=base_dir)
    else:
        # pull the repository
        subprocess.check_call(["git", "pull"], cwd=stellopt_dir)

    os.environ["STELLOPT_PATH"] = os.path.abspath(stellopt_dir)
    os.environ["MACHINE"] = "ubuntu"

    # compile the code
    command = ["./build_all", "-o", "release", "VMEC2000"]
    subprocess.call(command, cwd=stellopt_dir, env=os.environ.copy())
