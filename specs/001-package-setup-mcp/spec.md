# Feature Specification: Package Setup, MCP Server & Mailing Integration

**Feature Branch**: `001-package-setup-mcp`  
**Created**: 2026-01-09  
**Status**: Draft  
**Input**: User description: "Package setup cleanup with MCP server and mailing system integration"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Clean Package Installation (Priority: P1)

A developer installs the `py-lead-generation` package and can immediately use it without encountering deprecated files, conflicting dependencies, or confusing directory structures. The package installs cleanly with all dependencies resolved from a single source (`pyproject.toml`).

**Why this priority**: Foundation for all other features; a clean, well-structured package is essential for usability and maintainability.

**Independent Test**: Can be tested by running `pip install .` in a fresh virtual environment and verifying imports work without errors.

**Acceptance Scenarios**:

1. **Given** a fresh Python 3.10+ environment, **When** user runs `pip install py-lead-generation`, **Then** package installs without dependency conflicts
2. **Given** the package is installed, **When** user imports `GoogleMapsEngine` and `YelpEngine`, **Then** imports succeed without errors
3. **Given** the repository is cloned, **When** user examines the structure, **Then** there are no deprecated folders (e.g., `archived/`) or duplicate dependency files

---

### User Story 2 - MCP Server for Lead Generation Tools (Priority: P2)

A developer or AI assistant uses the MCP (Model Context Protocol) server to access lead generation tools programmatically. The server exposes tools for searching leads, exporting data, and checking engine status without writing Python code directly.

**Why this priority**: Enables integration with AI assistants and automation workflows; extends package utility beyond direct Python usage.

**Independent Test**: Can be tested by starting the MCP server and calling available tools via the MCP protocol.

**Acceptance Scenarios**:

1. **Given** the MCP server is running, **When** a client requests the list of available tools, **Then** the server returns at least 2 tools (e.g., `search_leads`, `export_leads`)
2. **Given** the MCP server is running, **When** a client calls the `search_leads` tool with query and location, **Then** the server returns structured lead data or an appropriate error
3. **Given** the MCP server is running, **When** a client requests tool schemas, **Then** each tool has documented input/output schemas

---

### User Story 3 - Email Outreach via Gmail SMTP (Priority: P3)

A user sends personalized cold emails to collected leads using their Gmail account. The system supports configurable templates for subject and body, with placeholder substitution for lead-specific data (name, company, etc.).

**Why this priority**: Core value proposition—collected leads need to be contacted; email is the most common outreach channel.

**Independent Test**: Can be tested by sending a test email to a known address and verifying delivery.

**Acceptance Scenarios**:

1. **Given** valid Gmail SMTP credentials are configured, **When** user triggers email sending for a lead, **Then** email is sent successfully
2. **Given** an email template with placeholders, **When** sending to a lead with matching data, **Then** placeholders are replaced with actual lead information
3. **Given** invalid SMTP credentials, **When** user attempts to send email, **Then** system provides clear error message without crashing

---

### User Story 4 - Simple GUI for Lead Generation (Priority: P4)

A non-technical user launches a desktop application to search for leads, view results, and export data without using command line or writing code.

**Why this priority**: Expands user base beyond developers; provides accessible interface for business users.

**Independent Test**: Can be tested by launching the GUI, performing a search, and exporting results.

**Acceptance Scenarios**:

1. **Given** the GUI application is launched, **When** user enters search query and location, **Then** search executes and results display in the interface
2. **Given** search results are displayed, **When** user clicks export button, **Then** results are saved to a file
3. **Given** a search is in progress, **When** user observes the interface, **Then** progress indicator shows activity

---

### User Story 5 - 2GIS Engine Interface (Priority: P5)

A developer extends the package to support 2GIS as a lead source by implementing the established engine interface. The base interface and domain structure are in place, ready for implementation.

**Why this priority**: Lowest priority as it's interface-only (no implementation); prepares for future extension.

**Independent Test**: Can be tested by verifying the interface class exists and follows the engine pattern.

**Acceptance Scenarios**:

1. **Given** the 2GIS engine module exists, **When** developer inspects the code, **Then** it inherits from `AbstractEngine` and `BaseEngine`
2. **Given** the 2GIS engine interface, **When** developer reads the docstrings, **Then** required methods and constants are documented

---

### Edge Cases

- What happens when Gmail SMTP rate limits are exceeded? System should handle gracefully with backoff.
- How does the GUI handle network disconnection during a search? Display appropriate error state.
- What if MCP server receives malformed tool requests? Return structured error responses.
- How does the package handle installation on Python versions below 3.10? Clear error message at install time.

## Requirements *(mandatory)*

### Functional Requirements

**Package Structure & Setup**:
- **FR-001**: Package MUST have single source of truth for dependencies (`pyproject.toml` only)
- **FR-002**: Package MUST NOT contain deprecated or legacy folders (`archived/` removed)
- **FR-003**: Package MUST pass all linting checks (ruff) and type checks (mypy) in CI
- **FR-004**: Package MUST have consolidated CI/CD pipeline (remove duplicate publish workflows)
- **FR-005**: Package MUST include pre-commit configuration for consistent code quality

**MCP Server**:
- **FR-006**: MCP server MUST expose at least 2 tools for lead generation operations
- **FR-007**: MCP server MUST follow the Model Context Protocol specification
- **FR-008**: MCP server MUST have configurable host and port settings
- **FR-009**: MCP server MUST return structured responses with proper error handling

**Email Outreach**:
- **FR-010**: System MUST support Gmail SMTP for sending emails
- **FR-011**: System MUST support email templates with placeholder substitution
- **FR-012**: System MUST store SMTP credentials securely (environment variables or config file)
- **FR-013**: System MUST validate email addresses before sending

**GUI**:
- **FR-014**: GUI MUST provide input fields for search query and location
- **FR-015**: GUI MUST display search results in a readable format
- **FR-016**: GUI MUST support exporting results to CSV

**2GIS Interface**:
- **FR-017**: 2GIS engine MUST follow established engine architecture (inherit from base classes)
- **FR-018**: 2GIS engine MUST define required constants (`BASE_URL`, `FIELD_NAMES`, `FILENAME`)

**Testing**:
- **FR-019**: Package MUST have basic test suite with mocked tests passing in CI
- **FR-020**: Tests MUST cover package imports and basic engine instantiation

### Key Entities

- **Lead**: Business contact information (name, address, phone, email, website, source)
- **Engine**: Lead generation source implementation (Google Maps, Yelp, 2GIS)
- **EmailTemplate**: Configurable template with subject, body, and placeholders
- **SMTPConfig**: Gmail SMTP connection settings (host, port, credentials)
- **MCPTool**: Exposed functionality via Model Context Protocol

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Package installs successfully in under 60 seconds on standard network connection
- **SC-002**: All CI checks (lint, type-check, test) pass on Python 3.10, 3.11, and 3.12
- **SC-003**: MCP server responds to tool requests within 500ms (excluding actual scraping time)
- **SC-004**: Email sending completes within 10 seconds per message
- **SC-005**: GUI launches and displays main window within 3 seconds
- **SC-006**: 100% of package imports work without errors after installation
- **SC-007**: Zero deprecated files or folders remain in the repository
- **SC-008**: Test suite achieves 100% pass rate (with mocked tests)

## Assumptions

- Gmail SMTP is the primary email provider; other providers may be added later
- MCP server will use standard HTTP transport (default MCP implementation)
- GUI will use tkinter as it's included in Python standard library
- 2GIS implementation details will be defined in a future feature
- Users have Python 3.10 or higher installed
- Pre-commit hooks are optional for contributors but enforced in CI
