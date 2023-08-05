## Version 1.18.4 (2023-07-18)
### 👷 Bug fixes

- python 3.11 compatibility: inspect.getargspec has been deprecated

## Version 1.18.3 (2023-07-04)
### 👷 Bug fixes

- psycopg2: escape mostly all easy functions to escape (#1)

## Version 1.18.2 (2023-02-23)
### 👷 Bug fixes

- use maintained yapps2-logilab
- uses psycopg2-binary for tests

### 🤖 Continuous integration

- add check-dependencies-resolution
- add twine-check job
- disable heavy consuming jobs since the CI is dying
- make py3-from-forge extends from .retry
- make py3-from-forge interruptible
- move the v2 of gitlab templates
- move to native heptapod rtfd integration
- use templates

## Version 1.18.1 (2021-08-06)

### 🤷 Various changes

- maintenance release to remove deprecation warnings

## Version 1.18.0 (2021-05-04)
### 🎉 New features

- order: add support for order by NULLS LAST and NULLS FIRST
- order: use specific postgres function to order by NULLS LAST and NULLS FIRST

### 🤷 Various changes

- bump version to 1.17.2
- Remove mysql compatibility since it's no more used.
- Remove sqlserver compatibility since it's no more used.
