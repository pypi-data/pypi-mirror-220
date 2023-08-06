import subprocess
import requests
import os
import w7x


def download_webdav(
    url: str, relative_path: str, output: str, password: str = "", is_dir=False
):
    """
    Download a file (folder not possible) via webdav protocol given a public share url

    Args:
        url (str): Url to public data share repo
        relative_path (str): Relative path to file within repo
        output (str): Path to the output. If output.endswith("/") or is_dir relative_path is joined
        password (str, optional): Password of the share if set. Defaults to ''.
        is_dir (bool, optional): Flag to mark if output is a directory or file. Defaults to False.
    """
    # Assuming url is a public webdav link (e.g. nextCloud)
    domain, token = url.split("/s/")
    webdav_url = os.path.join(domain, "public.php/webdav/" + relative_path)
    if output.endswith("/") or is_dir:
        # this is understood to be the base path. Prepend the relative_path then.
        # Otherwise take it as full path
        output = os.path.join(output, relative_path)
    username = token

    # TODO-2: In case you have to add the certificate... Dont think it is a problem though
    # good read: openssl x509 -in server.cer -inform DER -outform PEM  >> consolidate.pem
    # host = webdav_url.lstrip('https://')
    # port = 443
    # cert_path = os.path.join("/tmp", host + ".pem")
    # # Create a socket and connect to the server
    # sock = socket.create_connection((host, port))
    # # Wrap the socket with an SSL context
    # context = ssl.create_default_context()
    # with context.wrap_socket(sock, server_hostname=host) as ssock:
    #     # Get the server's SSL certificate
    #     cert_bytes = ssock.getpeercert(binary_form=True)

    # pem_cert = ssl.DER_cert_to_PEM_cert(cert_bytes)
    # # Save the certificate to a file
    # with open(cert_path, 'w') as f:
    #     f.write(pem_cert)
    # verify = cert_path
    verify = False

    # Perform the HTTPS request and provide the certificate
    response = requests.get(webdav_url, auth=(username, password), verify=verify)

    if response.status_code == 200:
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, "wb") as f:
            f.write(response.content)
            print(f"Downloaded file {output}")
    else:
        print(f"Request failed with response {response}")


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
