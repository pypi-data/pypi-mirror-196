"""
small code snippet that opens a gui window with a animated color

Author: Niels Maeder
"""
import pkg_resources

from colorbymood.window import Window  # type:ignore pylint:disable=E0611

__version__ = pkg_resources.get_distribution("colorbymood").version
