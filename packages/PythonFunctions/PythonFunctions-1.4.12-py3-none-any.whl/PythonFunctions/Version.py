# Module update checker, based off the github file
import os
from packaging import version

GlobalRead = True
try:
    import requests
except ModuleNotFoundError:
    print(
        "Requests is not installed. Can not check for a new PythonFunction update!"
    )
    GlobalRead = False


def CanReadGlobal():
    """Get if requests is installed

    Returns:
        bool: Requests is installed
    """
    return GlobalRead


def ReadLocal():
    """Get the module version

    Returns:
        str: Module version
    """
    return "1.4.12"


url = "https://raw.githubusercontent.com/FunAndHelpfulDragon/python-Functions/main/Version.txt"


def ReadGlobal():
    """Get the version on the server"""
    if GlobalRead:
        try:
            r = requests.get(url, timeout=10)
            return r.text
        except (
            requests.exceptions.TooManyRedirects,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout,
        ):
            print("Failed to read the latest version!")

    return None


def Compare():
    current = ReadLocal()
    server = ReadGlobal()

    if server is None:
        # break eariler if no response, we have already mentioned about it.
        return

    if version.parse(server) > version.parse(current):
        print("*" * os.get_terminal_size().columns)
        print(
            f"""Notice: A newer version of PythonFunctions is alvalible.
Current Version: {current}. New version: {server}"""
        )
        print("*" * os.get_terminal_size().columns)


if __name__ == "__main__":
    if GlobalRead:
        ReadGlobal()
