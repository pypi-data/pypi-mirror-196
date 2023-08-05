from setuptools import setup
import versioneer
import re
# remove commit hash from version
setup(version = versioneer.get_version(),
      cmdclass = versioneer.get_cmdclass(),
        )
