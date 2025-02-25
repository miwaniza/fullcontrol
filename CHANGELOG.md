# Changelog

All notable changes to FullControl will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added retraction attribute to base Extruder class to control retraction distance when turning extrusion off
- Added retraction handling in gcode generation when extruder is turned off

### Changed
- Fixed circular import between common.py and extrusion_classes.py
- Improved printer name validation in GcodeControls using Pydantic validator
- Updated GcodeControls to validate printer names during initialization
- Improved tips system to show specific messages for missing extrusion width/height parameters
- Fixed State initialization test to properly check for input steps in state.steps sequence