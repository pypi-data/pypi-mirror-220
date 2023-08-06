import platform
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

from subprocess import getoutput
from pathlib import Path
from os import path


def setup_webdriver(num_sec_implicit_wait=3, gui=True, options=Options()):
    """Sets up a selenium webdriver, while taking care of dependencies.
        num_sec_implicit_wait:  How many seconds the selenium driver should wait before failing (See selenium docs.)
        gui: False tells selenium to run headless
        options: Gives the possibility to add additional parameters for the driver startup
    """

    _linux = "Linux"
    _windows = "Windows"
    win_default_firefox_install_path = Path("C:/Program Files/Mozilla Firefox/firefox.exe")

    active_system = platform.system()
    options.headless = not gui

    if active_system == _linux:
        snap_firefox_binary_location = getoutput("find /snap/firefox -name firefox")
        if "No such file or directory" in snap_firefox_binary_location:
            options.binary_location = "/usr/bin/firefox"  # non snap version
        else:
            options.binary_location = snap_firefox_binary_location.split("\n")[-1]  # snap installed firefox version

    elif active_system == _windows:

        default_firefox_install_location = str(win_default_firefox_install_path.resolve())

        if path.exists(default_firefox_install_location):
            options.binary_location = default_firefox_install_location
        else:
            #TODO does not work with microsoft store firefox yet
            options.binary_location = getoutput("where firefox")
    else:
        raise ValueError("You are running on a non-supported platform.")

    driver = webdriver.Firefox(options=options,  service=Service(GeckoDriverManager().install()))

    driver.implicitly_wait(num_sec_implicit_wait)

    return driver
