import subprocess


def install():
    """
    install and enable jupyter nbextension, i.e. call

    .. code-block:: bash
        conda install -c conda-forge pdf2svg
        jupyter contrib nbextension install --user
        jupyter nbextension enable splitcell/splitcell
    """
    subprocess.check_call(["conda", "install", "-c", "conda-forge", "pdf2svg"])
    subprocess.check_call(["jupyter", "contrib", "nbextension", "install", "--user"])
    subprocess.check_call(["jupyter", "nbextension", "enable", "splitcell/splitcell"])
