from setuptools import setup

name = "types-pyvmomi"
description = "Typing stubs for pyvmomi"
long_description = '''
## Typing stubs for pyvmomi

This is a PEP 561 type stub package for the `pyvmomi` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pyvmomi`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pyvmomi. All fixes for
types and metadata should be contributed there.

*Note:* The `pyvmomi` package includes type annotations or type stubs
since version 8.0.1.0.1. Please uninstall the `types-pyvmomi`
package if you use this or a newer version.


This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `afe18e95a9592434e93b648de5194cfe54443f84` and was tested
with mypy 1.4.1, pyright 1.1.318, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="8.0.0.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyvmomi.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pyVmomi-stubs'],
      package_data={'pyVmomi-stubs': ['__init__.pyi', 'vim/__init__.pyi', 'vim/event.pyi', 'vim/fault.pyi', 'vim/option.pyi', 'vim/view.pyi', 'vmodl/__init__.pyi', 'vmodl/fault.pyi', 'vmodl/query.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
