import subprocess
import os
import w7x
from w7x.lib.webdav import download_webdav


def install():
    # import w7x just here because it is not working until libs are installed

    # Assuming vmecnn installed via pip extras (vmec_nn)
    # We could install vmecnn via poetry with the following in pyproject (and add vmecnn to extra)
    #    -> vmecnn = { git = "https://gitlab.mpcdf.mpg.de/amerlo/vmecnn.git", optional = true }
    # but pypi does not allow publishing then :/
    repo_url = "https://gitlab.mpcdf.mpg.de/amerlo/vmecnn.git"
    subprocess.run(["pip", "install", f"git+{repo_url}"])

    # Now
    paths_present = [
        os.path.exists(w7x.config.vmec.nn.checkpoint),
        os.path.exists(w7x.config.vmec.nn.metadata),
    ]

    if all(paths_present):
        pass
    elif not all(paths_present) and any(paths_present):
        raise ValueError("Partially existent vmecnn data")
    elif not any(paths_present):
        download_webdav(
            w7x.config.vmec.nn.model_url,
            w7x.config.vmec.nn.checkpoint_relative_path,
            w7x.config.vmec.nn.cache,
            is_dir=True,
        )
        download_webdav(
            w7x.config.vmec.nn.model_url,
            w7x.config.vmec.nn.metadata_relative_path,
            w7x.config.vmec.nn.cache,
            is_dir=True,
        )
