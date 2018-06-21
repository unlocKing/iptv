# Changelog

## [Unreleased]

### Added

- New .json format, one file for one channel instead of a big python file,
  the python format will be dropped in the future.
  The JSON must be valid.

### Changed

- Removed python2 support
- Allow the usage of dicts instead of tuples for streamlink data,
  the old method still works, but might be invalid at some point.

### Removed

- old python data example
