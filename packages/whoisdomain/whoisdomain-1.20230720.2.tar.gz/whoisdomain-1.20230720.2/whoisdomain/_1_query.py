import subprocess
import time
import sys
import os
import platform
import json
import shutil
from .exceptions import WhoisCommandFailed, WhoisCommandTimeout

from typing import Dict, List, Optional, Tuple


# PYTHON_VERSION = sys.version_info[0]
CACHE: Dict[str, Tuple[int, str]] = {}
CACHE_MAX_AGE = 60 * 60 * 48  # 48h

IS_WINDOWS = platform.system() == "Windows"

if not IS_WINDOWS and shutil.which("stdbuf"):
    STDBUF_OFF_CMD = ["stdbuf", "-o0"]
else:
    STDBUF_OFF_CMD = []


def _cache_load(cf: str) -> None:
    if not os.path.isfile(cf):
        return

    global CACHE
    f = open(cf, "r")

    try:
        CACHE = json.load(f)
    except Exception as e:
        print(f"ignore lson load err: {e}", file=sys.stderr)

    f.close()


def _cache_save(cf: str) -> None:
    global CACHE

    f = open(cf, "w")
    json.dump(CACHE, f)
    f.close()


def _testWhoisPythonFromStaticTestData(
    dl: List[str],
    ignore_returncode: bool,
    server: Optional[str] = None,
    verbose: bool = False,
) -> str:
    domain = ".".join(dl)
    testDir = os.getenv("TEST_WHOIS_PYTHON")
    pathToTestFile = f"{testDir}/{domain}/input"
    if os.path.exists(pathToTestFile):
        with open(pathToTestFile, mode="rb") as f:  # switch to binary mode as that is what Popen uses
            # make sure the data is treated exactly the same as the output of Popen
            return f.read().decode(errors="ignore")

    raise WhoisCommandFailed("")


def _tryInstallMissingWhoisOnWindows(
    verbose: bool = False,
) -> None:
    """
    Windows 'whois' command wrapper
    https://docs.microsoft.com/en-us/sysinternals/downloads/whois
    """
    folder = os.getcwd()
    copy_command = r"copy \\live.sysinternals.com\tools\whois.exe " + folder
    if verbose:
        print("downloading dependencies", file=sys.stderr)
        print(copy_command, file=sys.stderr)

    subprocess.call(
        copy_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )


def _makeWhoisCommandToRun(
    dl: List[str],
    server: Optional[str] = None,
    verbose: bool = False,
    wh: str = "whois",
) -> List[str]:
    domain = ".".join(dl)

    if " " in wh:
        whList = wh.split(" ")
    else:
        whList = [wh]

    if IS_WINDOWS:
        if wh == "whois":  # only if the use did not specify what whois to use
            if os.path.exists("whois.exe"):
                wh = r".\whois.exe"
            else:
                find = False
                paths = os.environ["path"].split(";")
                for path in paths:
                    wpath = os.path.join(path, "whois.exe")
                    if os.path.exists(wpath):
                        wh = wpath
                        find = True
                        break

                if not find:
                    _tryInstallMissingWhoisOnWindows(verbose)
        whList = [wh]

        if server:
            return whList + ["-v", "-nobanner", domain, server]
        return whList + ["-v", "-nobanner", domain]

    # not windows
    if server:
        return whList + [domain, "-h", server]
    return whList + [domain]


def _do_whois_query(
    dl: List[str],
    ignore_returncode: bool,
    server: Optional[str] = None,
    verbose: bool = False,
    timeout: Optional[float] = None,
    parse_partial_response: bool = False,
    wh: str = "whois",
    simplistic: bool = False,
) -> str:
    # if getenv[TEST_WHOIS_PYTON] fake whois by reading static data from a file
    # this wasy we can actually implemnt a test run with known data in and expected data out
    if os.getenv("TEST_WHOIS_PYTHON"):
        return _testWhoisPythonFromStaticTestData(dl, ignore_returncode, server, verbose)

    cmd = _makeWhoisCommandToRun(
        dl=dl,
        server=server,
        verbose=verbose,
        wh=wh,
    )
    if verbose:
        print(cmd, wh, file=sys.stderr)

    # LANG=en is added to make the ".jp" output consist across all environments
    p = subprocess.Popen(
        # STDBUF_OFF_CMD needed to not lose data on kill
        STDBUF_OFF_CMD + cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={"LANG": "en"} if dl[-1] in ".jp" else None,
    )

    try:
        r = p.communicate(timeout=timeout)[0].decode(errors="ignore")
    except subprocess.TimeoutExpired:
        # Kill the child process & flush any output buffers
        p.kill()
        r = p.communicate()[0].decode(errors="ignore")
        # In most cases whois servers returns partial domain data really fast
        # after that delay occurs (probably intentional) before returning contact data.
        # Add this option to cover those cases
        if not parse_partial_response or not r:
            raise WhoisCommandTimeout(f"timeout: query took more then {timeout} seconds")

    if verbose:
        print(r, file=sys.stderr)

    if ignore_returncode is False and p.returncode not in [0, 1]:
        # network error, "fgets: Connection reset by peer" fix, ignore
        if "fgets: Connection reset by peer" in r:
            return r.replace("fgets: Connection reset by peer", "")
        # connect: Connection refused
        elif "connect: Connection refused" in r:
            return r.replace("connect: Connection refused", "")

        if simplistic:
            return r

        raise WhoisCommandFailed(r)

    return r


# PUBLIC


def do_query(
    dl: List[str],
    force: bool = False,
    cache_file: Optional[str] = None,
    cache_age: int = CACHE_MAX_AGE,
    slow_down: int = 0,
    ignore_returncode: bool = False,
    server: Optional[str] = None,
    verbose: bool = False,
    timeout: Optional[float] = None,
    parse_partial_response: bool = False,
    wh: str = "whois",
    simplistic: bool = False,
) -> str:
    k = ".".join(dl)

    if cache_file:
        if verbose:
            print(f"using cache file: {cache_file}", file=sys.stderr)
        _cache_load(cache_file)

    # actually also whois uses cache, so if you really dont want to use cache
    # you should also pass the --force-lookup flag (on linux)
    if force or k not in CACHE or CACHE[k][0] < time.time() - cache_age:
        if verbose:
            print(f"force = {force}", file=sys.stderr)

        # slow down before so we can force individual domains at a slower tempo
        if slow_down:
            time.sleep(slow_down)

        # populate a fresh cache entry
        CACHE[k] = (
            int(time.time()),
            _do_whois_query(
                dl=dl,
                ignore_returncode=ignore_returncode,
                server=server,
                verbose=verbose,
                timeout=timeout,
                parse_partial_response=parse_partial_response,
                wh=wh,
                simplistic=simplistic,
            ),
        )

        if cache_file:
            _cache_save(cache_file)

    return CACHE[k][1]
