#! /usr/bin/env python3

import os

try:
    from setuptools import find_packages, setup
except AttributeError:
    from setuptools import find_packages, setup

NAME = 'OASYS1-HALF-SRW'
VERSION = '0.0.1'
ISRELEASED = True

DESCRIPTION = 'OASYS1-HALF-SRW: for attempt only in oasys'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'LYJ'
AUTHOR_EMAIL = 'luyujie_nsrl@mail.ustc.edu.cn'

LICENSE = 'GPLv3'

KEYWORDS = (
    'X-ray wavefront',
    'HALF',
    'simulator',
    'oasys1',
)

CLASSIFIERS = (
    'Development Status :: 5 - Production/Stable',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Science/Research',
)

SETUP_REQUIRES = (
    'setuptools',
)

INSTALL_REQUIRES = (
    'oasys1>=1.2.62',
    'wofrysrw>=1.1.22',
    'scikit-image',
)

PACKAGES = find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests'))

PACKAGE_DATA = {
    "orangecontrib.halfsrw.widgets.sources":["icons/*.png", "icons/*.jpg"],
    "orangecontrib.halfsrw.widgets.optical_elements":["icons/*.png", "icons/*.jpg", "misc/*.*"],
}

NAMESPACE_PACAKGES = ["orangecontrib", "orangecontrib.halfsrw", "orangecontrib.halfsrw.widgets"]

ENTRY_POINTS = {
    'oasys.addons' : ("HALF-SRW = orangecontrib.halfsrw", ),
    'oasys.widgets' : (
        "HALF-SRW Sources = orangecontrib.halfsrw.widgets.sources",
        "HALF-SRW Optical Elements = orangecontrib.halfsrw.widgets.optical_elements",
    ),
    'oasys.menus' : ("halfsrwmenu = orangecontrib.halfsrw.menu",)
}

if __name__ == '__main__':
    is_beta = False

    try:
        import PyMca5, PyQt5

        is_beta = True
    except:
        setup(
              name = NAME,
              version = VERSION,
              description = DESCRIPTION,
              long_description = LONG_DESCRIPTION,
              author = AUTHOR,
              author_email = AUTHOR_EMAIL,
              #url = URL,
              #download_url = DOWNLOAD_URL,
              license = LICENSE,
              keywords = KEYWORDS,
              classifiers = CLASSIFIERS,
              packages = PACKAGES,
              package_data = PACKAGE_DATA,
              #py_modules = PY_MODULES,
              setup_requires = SETUP_REQUIRES,
              install_requires = INSTALL_REQUIRES,
              #extras_require = EXTRAS_REQUIRE,
              #dependency_links = DEPENDENCY_LINKS,
              entry_points = ENTRY_POINTS,
              namespace_packages=NAMESPACE_PACAKGES,
              include_package_data = True,
              zip_safe = False,
              )

        if is_beta: raise NotImplementedError("This version of HALF-SRW doesn't work with Oasys1 beta.\nPlease install OASYS1 final release.")
