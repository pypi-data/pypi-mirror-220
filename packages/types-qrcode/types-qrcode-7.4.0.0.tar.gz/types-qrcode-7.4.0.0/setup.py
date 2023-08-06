from setuptools import setup

name = "types-qrcode"
description = "Typing stubs for qrcode"
long_description = '''
## Typing stubs for qrcode

This is a PEP 561 type stub package for the `qrcode` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`qrcode`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/qrcode. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `afe18e95a9592434e93b648de5194cfe54443f84` and was tested
with mypy 1.4.1, pyright 1.1.318, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="7.4.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/qrcode.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['qrcode-stubs'],
      package_data={'qrcode-stubs': ['LUT.pyi', '__init__.pyi', 'base.pyi', 'console_scripts.pyi', 'constants.pyi', 'exceptions.pyi', 'image/__init__.pyi', 'image/base.pyi', 'image/pil.pyi', 'image/pure.pyi', 'image/styledpil.pyi', 'image/styles/__init__.pyi', 'image/styles/colormasks.pyi', 'image/styles/moduledrawers/__init__.pyi', 'image/styles/moduledrawers/base.pyi', 'image/styles/moduledrawers/pil.pyi', 'image/styles/moduledrawers/svg.pyi', 'image/svg.pyi', 'main.pyi', 'release.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
