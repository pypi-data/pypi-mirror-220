import json
import pathlib
import ssl
from urllib import error, request

from . import exceptions


def api_client(endpoint: str, remote_data, headers: dict):
    """
    Yields the result from `simple_api_client`. Wraps errors into a
    `~.exceptions.CommandFail` exception.

    :param dict[str, str, bool] remote_data:
        A dict containing ``"url"``, ``"token"`` and ``"insecure"``.

    :returns: A generator

    """
    try:
        yield from simple_api_client(endpoint, remote_data, headers)
    except exceptions.Fail as err:
        raise exceptions.CommandFail(err)
    except error.HTTPError as err:
        raise exceptions.CommandFail(
            f"{err}: {endpoint}: {err.read().decode(errors='ignore')}"
        )
    except error.URLError as err:
        raise exceptions.CommandFail(f"{remote_data['url']}: {err}")
    except Exception as err:
        raise exceptions.CommandFail(f"{endpoint}: {repr(err)}")


def simple_api_client(endpoint: str, remote_data, headers: dict):
    """
    Send a GET request to ``<remote_data:url>/<endpoint>``.

        Yield protocol:

        - If type is `str`: log message
        - If type is `dict`: result

    .. code-block:: pycon

        >>> def gen():
        ...   yield from simple_api_client(endpoint, remote_data, headers)

        >>> for res in gen()
        ...     print(res)

    :param dict[str, str, bool] remote_data:
        A dict containing ``"url"``, ``"token"`` and ``"insecure"``.

    :returns: A generator
    """

    prefix = remote_data.get("url")
    token = remote_data.get("token")
    insecure = remote_data.get("insecure", False)
    headers["Token"] = token
    req = request.Request(url=f"{prefix}/{endpoint}", headers=headers)

    context = ssl.create_default_context()
    if insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    yield f"query {endpoint}"
    res = request.urlopen(req, context=context)

    buffer = " "
    payload = ""
    yield f"response from {prefix}"
    while buffer:
        buffer = res.readline(1024).decode(errors="ignore")
        if buffer.startswith("//"):
            yield f"      {buffer[2:].strip()}"
        else:
            payload += buffer

    result = json.loads(payload)
    if "result_code" in result and not result["result_code"] == 0:
        raise exceptions.CommandFail(f"request failed: {payload}")

    yield result
