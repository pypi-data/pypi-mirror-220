import os

from hyfi import HyFI, about

from ._version import __version__

# Read the package name from the current directory
__package_name__ = os.path.basename(os.path.dirname(__file__))

# Set package information in about
about.__package_name__ = __package_name__
about.__version__ = __version__

# Initialize the logger
HyFI.setLogger()


def get_version() -> str:
    """Get the package version."""
    return __version__
