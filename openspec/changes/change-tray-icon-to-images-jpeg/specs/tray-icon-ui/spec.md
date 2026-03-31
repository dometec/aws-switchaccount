## MODIFIED Requirements

### Requirement: Display system tray icon
The system SHALL show a persistent icon in the system tray (notification area) when the application is running. The icon image SHALL be loaded from the static file `images.jpeg` located in the project root.

#### Scenario: Application starts
- **WHEN** the application is launched
- **THEN** a tray icon appears in the system notification area within 2 seconds

#### Scenario: Tray icon uses images.jpeg
- **WHEN** the application is launched
- **THEN** the tray icon displays the image loaded from `images.jpeg` (not a programmatically generated shape)

#### Scenario: Tray icon tooltip
- **WHEN** the user hovers over the tray icon
- **THEN** the tooltip shows the name of the currently active AWS profile (e.g., "AWS: prod")
