from setuptools import setup

name = "types-s2clientprotocol"
description = "Typing stubs for s2clientprotocol"
long_description = '''
## Typing stubs for s2clientprotocol

This is a PEP 561 type stub package for the `s2clientprotocol` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`s2clientprotocol`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/s2clientprotocol. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `7d33060e6ae3ebe54462a891f0c566c97371915b` and was tested
with mypy 1.4.1, pyright 1.1.318, and
pytype 2023.7.21.
'''.lstrip()

setup(name=name,
      version="5.0.0.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/s2clientprotocol.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-protobuf'],
      packages=['s2clientprotocol-stubs'],
      package_data={'s2clientprotocol-stubs': ['build.pyi', 'common_pb2.pyi', 'data_pb2.pyi', 'debug_pb2.pyi', 'error_pb2.pyi', 'query_pb2.pyi', 'raw_pb2.pyi', 'sc2api_pb2.pyi', 'score_pb2.pyi', 'spatial_pb2.pyi', 'ui_pb2.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
