# Changelog

## [Unreleased]

### Added

- Python 3.6+ is required
- Added a lot of example files.
- New .json format, one file for one channel instead of a big python file,
  the python format will be dropped in the future.
  The JSON must be valid.
- Added better log messages

### Changed

- Removed Python 2.7, 3.4 and 3.5 support
- Allow the usage of dicts instead of tuples for streamlink data,
  the old method still works, but might be invalid at some point.

### Removed

- old Python data example

### Deprecated

- old data.py file, use the new method
- upload.py, it will be removed in favor of a curl script
