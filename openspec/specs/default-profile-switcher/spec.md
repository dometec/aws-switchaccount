### Requirement: Switch default profile in credentials file
The system SHALL overwrite the `[default]` section in `~/.aws/credentials` with the key-value pairs from the selected named profile, leaving all other sections unchanged.

#### Scenario: Successful switch in credentials file
- **WHEN** user selects profile `"prod"` and `~/.aws/credentials` contains a `[prod]` section
- **THEN** the `[default]` section is replaced with `[prod]`'s key-value pairs and the file is saved atomically

#### Scenario: Selected profile missing from credentials file
- **WHEN** user selects profile `"staging"` but `~/.aws/credentials` has no `[staging]` section
- **THEN** credentials file is not modified and an error is reported to the UI

### Requirement: Switch default profile in config file
The system SHALL overwrite the `[default]` section in `~/.aws/config` with the key-value pairs from the `[profile <name>]` section, leaving all other sections unchanged.

#### Scenario: Successful switch in config file
- **WHEN** user selects profile `"prod"` and `~/.aws/config` contains `[profile prod]`
- **THEN** the `[default]` section in config is replaced with `[profile prod]`'s key-value pairs and saved atomically

#### Scenario: Profile absent from config file
- **WHEN** user selects profile `"dev"` but `~/.aws/config` has no `[profile dev]` section
- **THEN** config file is not modified; the credentials switch may still proceed independently

### Requirement: Atomic file write
The system SHALL write changes to a temporary file in the same directory and rename it over the original to prevent partial writes.

#### Scenario: Write succeeds
- **WHEN** the switcher writes updated content
- **THEN** a temp file is created, flushed, and atomically renamed to the target path

#### Scenario: Write fails mid-operation
- **WHEN** an I/O error occurs before rename completes
- **THEN** the original file is left intact and an error is surfaced to the UI

### Requirement: File writability check
The system SHALL verify that both AWS files are writable before attempting a switch and report an error if not.

#### Scenario: File is read-only
- **WHEN** `~/.aws/credentials` has no write permission for the current user
- **THEN** the switch is aborted and a human-readable error message is shown in the tray menu or notification
