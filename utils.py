import os
import requests
import subprocess


def find_nested_element(element, *keys):
    """
    Find *keys (nested) in `element` (dict).
    """
    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return None
    return _element


def get_nested_element_from_json_response(response: requests.Response, *keys):
    """
    Given a response returned by requests, parse it as JSON and searches for an element located at response[key1]...[keyn]
    Throws an exception if the response is not parsable as JSON or if the element is not found

    :param response:: A Requests response
    :param keys: A list of keys, in order, which forms the path to the desired element
    :return: The requested element from the JSON response
    """
    try:
        json_data = response.json()
    except ValueError:
        raise RuntimeError("Invalid JSON")

    element = find_nested_element(json_data, *keys)
    if not element:
        raise RuntimeError("Unexpected JSON format")
    return element


def is_executable(fpath):
    """
    Tells whether a file pointed by fpath is executable or not

    :param fpath: Path to the executable
    :return: Whether the given file is executable or not
    """
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def find_program_exe(program):
    """
    Searches PATH and tries to find the given program

    :param program: The name of the program to run
    :return: The absolute path to a runnable executable, or None if not found
    """
    fpath, fname = os.path.split(program)
    if fpath:
        if is_executable(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            exe_file_windows = exe_file + ".exe"
            if is_executable(exe_file):
                return exe_file
            elif is_executable(exe_file_windows):
                return exe_file_windows

    return None


def find_vlc():
    """
    Tries to find a path to an VLC executable. If not found, will try to find VLC in common Windows directories

    :return: The absolute path to a VLC executable, or None if not found
    """
    common_vlc_paths = ["C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe", "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
                        "D:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe", "D:\\Program Files\\VideoLAN\\VLC\\vlc.exe"]

    vlc_path = find_program_exe("vlc")
    if vlc_path:
        return vlc_path
    for common_vlc_path in common_vlc_paths:
        vlc_path = find_program_exe(common_vlc_path)
        if vlc_path:
            return vlc_path
    return None


def start_vlc(link):
    """
    Starts a VLC process (only if VLC is found by find_vlc) with a given stream
    """
    vlc_path = find_vlc()
    if not vlc_path:
        return
    subprocess.Popen([vlc_path, link])
