from setuptools import setup

name = "types-editdistance"
description = "Typing stubs for editdistance"
long_description = '''
## Typing stubs for editdistance

This is a PEP 561 type stub package for the `editdistance` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`editdistance`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/editdistance. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `754473a30d50b918ac6f1a824f41600806defa94` and was tested
with mypy 1.4.1, pyright 1.1.318, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="0.6.3.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/editdistance.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['editdistance-stubs'],
      package_data={'editdistance-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
