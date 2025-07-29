# Changelog

## v1.6
- Initial public release of the Goon Squad bots.
- Added installer with token prompts and diagnostics script.

## v1.7
- Improved error handling and startup diagnostics.
- Added health command and runtime checks for missing tokens.
- Updated installer with color-coded prompts.

## v1.8
- Added colorized console logging via `src/logger.py`.

## v1.9
- Bots send messages using color-coded embeds.
- Bloom delivers scheduled compliments twice a day.

## v2.0.0
- Official release with a complete command reference.
- All code reviewed for flake8 compliance.

## v2.0.1
- Added `ApiKeyCycle` utility for rotating OpenAI keys.
- Formatted entire codebase with Black and removed E203 ignore from flake8.

## v2.0.2
- Updated all documentation for the v2.0.2 release.
- Bumped the package version in `setup.py`.

## v2.0.3
- Added global error handling with log files and admin notifications.
- Implemented command permission checks and cooldown configuration.
- New `status` command to check overall bot health.
- Activity logging and `audit` command for moderators.
- Installer color prompts realigned and token validation improved.
