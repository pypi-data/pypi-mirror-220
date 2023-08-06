from setuptools import setup

name = "types-DateTimeRange"
description = "Typing stubs for DateTimeRange"
long_description = '''
## Typing stubs for DateTimeRange

This is a PEP 561 type stub package for the `DateTimeRange` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`DateTimeRange`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/DateTimeRange. All fixes for
types and metadata should be contributed there.

*Note:* The `DateTimeRange` package includes type annotations or type stubs
since version 2.1.0. Please uninstall the `types-DateTimeRange`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `afe18e95a9592434e93b648de5194cfe54443f84` and was tested
with mypy 1.4.1, pyright 1.1.318, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="2.0.0.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/DateTimeRange.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-python-dateutil'],
      packages=['datetimerange-stubs'],
      package_data={'datetimerange-stubs': ['__init__.pyi', '__version__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
