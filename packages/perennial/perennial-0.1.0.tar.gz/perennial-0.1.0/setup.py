import setuptools

from perennial.__version__ import __version__

with open("README.md", "r", encoding="utf-8") as fh:
   long_description = fh.read()

setuptools.setup(
   name="perennial",
   version=__version__,
   author="Madison Landry",
   author_email="mlandry@mit.edu",
   description="Journaling kit for long-term self-analysis.",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://almonds.dev/focus/perennial",
   license="MIT",
   packages=setuptools.find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3.9", # milestone in type checking
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3.11",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   extras_require = {
      "dev": [
         "twine", # for uploading to PyPI
         "wheel>=0.36.2", # for building wheels
         "check-manifest", # creating MANIFEST.in
         "Sphinx>=6.1.3", # for docs
         "sphinx-autodoc-typehints", # better sphinx parsing
         "sphinxcontrib-trio",
      ]
   },
   python_requires=">=3.9",
)
