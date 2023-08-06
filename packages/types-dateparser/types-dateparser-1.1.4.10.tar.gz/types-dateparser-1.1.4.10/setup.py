from setuptools import setup

name = "types-dateparser"
description = "Typing stubs for dateparser"
long_description = '''
## Typing stubs for dateparser

This is a PEP 561 type stub package for the `dateparser` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`dateparser`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/dateparser. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `afe18e95a9592434e93b648de5194cfe54443f84` and was tested
with mypy 1.4.1, pyright 1.1.318, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="1.1.4.10",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/dateparser.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dateparser-stubs', 'dateparser_data-stubs'],
      package_data={'dateparser-stubs': ['__init__.pyi', 'calendars/__init__.pyi', 'calendars/hijri.pyi', 'calendars/hijri_parser.pyi', 'calendars/jalali.pyi', 'calendars/jalali_parser.pyi', 'conf.pyi', 'custom_language_detection/__init__.pyi', 'custom_language_detection/fasttext.pyi', 'custom_language_detection/langdetect.pyi', 'custom_language_detection/language_mapping.pyi', 'data/__init__.pyi', 'data/languages_info.pyi', 'date.pyi', 'date_parser.pyi', 'freshness_date_parser.pyi', 'languages/__init__.pyi', 'languages/dictionary.pyi', 'languages/loader.pyi', 'languages/locale.pyi', 'languages/validation.pyi', 'parser.pyi', 'search/__init__.pyi', 'search/detection.pyi', 'search/search.pyi', 'search/text_detection.pyi', 'timezone_parser.pyi', 'timezones.pyi', 'utils/__init__.pyi', 'utils/strptime.pyi', 'METADATA.toml'], 'dateparser_data-stubs': ['__init__.pyi', 'settings.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
