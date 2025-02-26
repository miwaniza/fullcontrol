# Changelog

All notable changes to FullControl will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added retraction attribute to base Extruder class to control retraction distance when turning extrusion off
- Added retraction handling in gcode generation when extruder is turned off
- Added comprehensive Vector class with support for basic vector operations, dot product, cross product, normalization and more
- Added support for None value handling in vector and rotation operations
- Added extensive test coverage for geometry operations including vector math, rotations, and interpolation
- Added proper configuration inheritance and overrides in GcodeControls
- Added improved path segmentation with equal distance points for curves and shapes
- Added manual G-code handling capabilities
- Added vector rotation functionality
- Added enhanced test execution scripts for better debugging

### Changed
- Fixed circular import between common.py and extrusion_classes.py
- Updated GcodeControls to use Pydantic V2 style field_validator instead of deprecated validator
- Improved printer name validation in GcodeControls using Pydantic validator
- Updated GcodeControls to validate printer names during initialization
- Improved tips system to show specific messages for missing extrusion width/height parameters
- Fixed State initialization test to properly check for input steps in state.steps sequence
- Enhanced geometry operations to handle None values consistently across all functions
- Improved interpolation operations to handle mixed None/value coordinates correctly
- Improved wave generation (square, triangle, sine) to maintain consistent spacing and shapes
- Enhanced shape generation with better handling of clockwise/counterclockwise options
- Updated angle measurement to properly handle angle ranges and normalization
- Improved printer error handling for more robust operation
- Enhanced test infrastructure for more reliable test execution
- Bumped version to 1.1.0 with increased stability and functionality

### Fixed
- Fixed handling of None values in vector operations and rotations
- Fixed interpolation behavior with mixed None/value coordinates
- Fixed segmented path generation to ensure equal distances between points
- Fixed reflection calculations about arbitrary lines and points
- Fixed square wave point spacing and segment calculation
- Fixed triangle wave geometry and point generation
- Fixed sine wave phase shift and amplitude calculations
- Fixed polar angle calculations in reflection operations
- Fixed G-code configuration inheritance and parameter overrides
- Fixed start/end G-code handling in printer configurations
- Fixed printer speed settings and handling
- Fixed tip display and message formatting
- Fixed path segmentation algorithm for consistent results
- Fixed reflection algorithm for correct geometry transformations
- Fixed wave generation functions for proper spacing and shapes
- Fixed test compatibility issues across different environments