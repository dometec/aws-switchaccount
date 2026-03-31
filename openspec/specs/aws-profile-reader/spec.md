### Requirement: Parse credentials file profiles
The system SHALL read `~/.aws/credentials` and extract all named profile sections (any section other than `[default]`).

#### Scenario: Credentials file with multiple profiles
- **WHEN** `~/.aws/credentials` contains sections `[default]`, `[dev]`, `[prod]`
- **THEN** the reader returns the list `["dev", "prod"]` (excluding `[default]`)

#### Scenario: Credentials file does not exist
- **WHEN** `~/.aws/credentials` is absent
- **THEN** the reader returns an empty list and logs a warning

### Requirement: Parse config file profiles
The system SHALL read `~/.aws/config` and extract all named profiles declared as `[profile <name>]` sections.

#### Scenario: Config file with profile sections
- **WHEN** `~/.aws/config` contains `[profile staging]` and `[profile prod]`
- **THEN** the reader returns the list `["staging", "prod"]`

#### Scenario: Config file does not exist
- **WHEN** `~/.aws/config` is absent
- **THEN** the reader returns an empty list and logs a warning

### Requirement: Merge and deduplicate profile list
The system SHALL merge the profile names from both files, remove duplicates, and return a sorted list.

#### Scenario: Profiles present in both files
- **WHEN** credentials has `["dev", "prod"]` and config has `["prod", "staging"]`
- **THEN** the merged result is `["dev", "prod", "staging"]`

### Requirement: Identify current default profile
The system SHALL detect which named profile the `[default]` section currently mirrors by comparing key-value pairs.

#### Scenario: Default matches a named profile exactly
- **WHEN** `[default]` in credentials has the same `aws_access_key_id` as `[dev]`
- **THEN** the reader returns `"dev"` as the active profile

#### Scenario: Default does not match any named profile
- **WHEN** `[default]` credentials differ from all named profiles
- **THEN** the reader returns `None` as the active profile
