### Requirement: Display system tray icon
The system SHALL show a persistent icon in the system tray (notification area) when the application is running.

#### Scenario: Application starts
- **WHEN** the application is launched
- **THEN** a tray icon appears in the system notification area within 2 seconds

#### Scenario: Tray icon tooltip
- **WHEN** the user hovers over the tray icon
- **THEN** the tooltip shows the name of the currently active AWS profile (e.g., "AWS: prod")

### Requirement: Profile selection menu
The system SHALL display a dropdown menu with all available AWS profiles when the tray icon is clicked.

#### Scenario: Menu lists all profiles
- **WHEN** the user clicks the tray icon
- **THEN** a menu appears listing every profile name found in the AWS config files

#### Scenario: Active profile indicated
- **WHEN** the menu is shown
- **THEN** the currently active profile is visually marked (e.g., checkmark or bullet prefix)

#### Scenario: Selecting a profile
- **WHEN** the user clicks a profile name in the menu
- **THEN** the system calls the default-profile-switcher to update the AWS files and updates the tray tooltip

### Requirement: Refresh profiles
The system SHALL re-read the AWS config files each time the tray menu is opened to pick up any external changes.

#### Scenario: Profile added externally
- **WHEN** a new profile is added to `~/.aws/credentials` by another tool while the app is running
- **THEN** the next menu open shows the updated profile list without restarting the app

### Requirement: Quit option
The system SHALL provide a "Quit" menu item that terminates the application cleanly.

#### Scenario: User quits application
- **WHEN** the user clicks "Quit" in the tray menu
- **THEN** the tray icon is removed and the process exits with code 0

### Requirement: Error notification
The system SHALL display a disabled or highlighted menu item indicating an error when a profile switch fails.

#### Scenario: Switch fails
- **WHEN** the profile switcher reports an error (e.g., read-only file)
- **THEN** the tray menu shows an error label (e.g., "Error: file not writable") and the previous default is preserved
