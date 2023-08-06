from setuptools import setup

name = "types-Pygments"
description = "Typing stubs for Pygments"
long_description = '''
## Typing stubs for Pygments

This is a PEP 561 type stub package for the `Pygments` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`Pygments`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/Pygments. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `afe18e95a9592434e93b648de5194cfe54443f84` and was tested
with mypy 1.4.1, pyright 1.1.318, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="2.15.0.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Pygments.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-docutils', 'types-setuptools'],
      packages=['pygments-stubs'],
      package_data={'pygments-stubs': ['__init__.pyi', 'cmdline.pyi', 'console.pyi', 'filter.pyi', 'filters/__init__.pyi', 'formatter.pyi', 'formatters/__init__.pyi', 'formatters/_mapping.pyi', 'formatters/bbcode.pyi', 'formatters/html.pyi', 'formatters/img.pyi', 'formatters/irc.pyi', 'formatters/latex.pyi', 'formatters/other.pyi', 'formatters/pangomarkup.pyi', 'formatters/rtf.pyi', 'formatters/svg.pyi', 'formatters/terminal.pyi', 'formatters/terminal256.pyi', 'lexer.pyi', 'lexers/__init__.pyi', 'modeline.pyi', 'plugin.pyi', 'regexopt.pyi', 'scanner.pyi', 'sphinxext.pyi', 'style.pyi', 'styles/__init__.pyi', 'token.pyi', 'unistring.pyi', 'util.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
