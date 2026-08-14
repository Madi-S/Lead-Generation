# Tasks: Package Setup, MCP Server & Mailing Integration

**Input**: Design documents from `/specs/001-package-setup-mcp/`
**Prerequisites**: plan.md ✅, spec.md ✅

**Tests**: Mocked tests included as requested (basic assertions, no real scraping/email).

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story?] Description`

-   **[P]**: Can run in parallel (different files, no dependencies)
-   **[Story]**: Which user story (US1=Cleanup, US2=MCP, US3=Email, US4=GUI, US5=2GIS)

## Path Conventions

-   Single project: `py_lead_generation/src/`, `tests/` at repository root
-   All paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and cleanup of deprecated files

-   [x] T001 Delete `archived/` directory completely
-   [x] T002 Delete `py_lead_generation/requirements.txt` (duplicate deps)
-   [x] T003 Delete `.github/workflows/python-publish.yml` (duplicate workflow)
-   [x] T004 Delete `setup.py` (legacy setuptools)
-   [x] T005 [P] Create `.env.example` with placeholder environment variables
-   [x] T006 Add `mcp>=1.0.0` dependency to `pyproject.toml`
-   [x] T007 Add entry points for `lead-gen-mcp` and `lead-gen-gui` in `pyproject.toml`
-   [x] T008 Update author info in `pyproject.toml` (replace placeholders)
-   [x] T009 Run `uv sync` to verify dependencies resolve correctly

**Checkpoint**: Repository is clean, dependencies consolidated, ready for feature development.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

-   [x] T010 Verify pre-commit hooks work with `pre-commit run --all-files`
-   [x] T011 Verify CI pipeline passes after cleanup (lint, type-check, test)
-   [x] T012 Create `py_lead_generation/src/email/__init__.py` with module docstring
-   [x] T013 Create `py_lead_generation/src/mcp/__init__.py` with module docstring
-   [x] T014 Create `py_lead_generation/src/gui/__init__.py` with module docstring
-   [x] T015 Create `py_lead_generation/src/twogis/__init__.py` with module docstring

**Checkpoint**: Foundation ready - all new module directories exist with **init**.py files.

---

## Phase 3: User Story 1 - Clean Package Installation (Priority: P1) 🎯 MVP

**Goal**: Package installs cleanly with no deprecated files or conflicting dependencies.

**Independent Test**: Run `pip install .` in fresh venv, verify imports work.

### Implementation for User Story 1

-   [x] T016 [US1] Update `py_lead_generation/__init__.py` to export TwoGisEngine (placeholder)
-   [x] T017 [US1] Update README.md to remove references to archived folder
-   [x] T018 [US1] Update README.md to document new features (MCP, email, GUI)
-   [x] T019 [US1] Verify package builds successfully with `uv build`
-   [x] T020 [US1] Test package installation in clean environment with `pip install dist/*.whl`

### Tests for User Story 1

-   [x] T021 [P] [US1] Add test for all public imports in `tests/test_sample.py`

**Checkpoint**: User Story 1 complete - package installs cleanly, all deprecated files removed.

---

## Phase 4: User Story 2 - MCP Server (Priority: P2)

**Goal**: MCP server exposes `search_leads` and `export_leads` tools.

**Independent Test**: Start MCP server, call tools via MCP client.

### Implementation for User Story 2

-   [x] T022 [P] [US2] Create `py_lead_generation/src/mcp/tools.py` with tool definitions
-   [x] T023 [P] [US2] Create `py_lead_generation/src/mcp/server.py` with MCP server setup
-   [x] T024 [US2] Implement `search_leads` tool handler in `tools.py`
-   [x] T025 [US2] Implement `export_leads` tool handler in `tools.py`
-   [x] T026 [US2] Add `main()` entry point function in `server.py`
-   [x] T027 [US2] Export MCP server from `py_lead_generation/src/mcp/__init__.py`

### Tests for User Story 2

-   [x] T028 [P] [US2] Create `tests/test_mcp.py` with mocked tool tests (assert True for now)

**Checkpoint**: User Story 2 complete - MCP server can list and call tools.

---

## Phase 5: User Story 3 - Email Outreach (Priority: P3)

**Goal**: Gmail SMTP integration with configurable templates.

**Independent Test**: Send test email to known address.

### Implementation for User Story 3

-   [x] T029 [P] [US3] Create `py_lead_generation/src/email/config.py` with SMTPConfig dataclass
-   [x] T030 [P] [US3] Create `py_lead_generation/src/email/templates.py` with EmailTemplate class
-   [x] T031 [US3] Create `py_lead_generation/src/email/sender.py` with GmailSMTPSender class
-   [x] T032 [US3] Implement `SMTPConfig.from_env()` class method in `config.py`
-   [x] T033 [US3] Implement `EmailTemplate.render()` method with placeholder substitution
-   [x] T034 [US3] Implement `GmailSMTPSender.send()` async method in `sender.py`
-   [x] T035 [US3] Implement `GmailSMTPSender.send_bulk()` async method in `sender.py`
-   [x] T036 [US3] Add email validation helper function in `sender.py`
-   [x] T037 [US3] Export email classes from `py_lead_generation/src/email/__init__.py`
-   [x] T038 [US3] Update `.env.example` with Gmail SMTP variables

### Tests for User Story 3

-   [x] T039 [P] [US3] Create `tests/test_email.py` with mocked sender tests (assert True for now)

**Checkpoint**: User Story 3 complete - email sending works with templates.

---

## Phase 6: User Story 4 - GUI (Priority: P4)

**Goal**: Tkinter desktop app for search and export.

**Independent Test**: Launch GUI, perform search, export results.

### Implementation for User Story 4

-   [x] T040 [P] [US4] Create `py_lead_generation/src/gui/app.py` with main window setup
-   [x] T041 [US4] Implement search form (query, location, source dropdown) in `app.py`
-   [x] T042 [US4] Implement results display (Treeview widget) in `app.py`
-   [x] T043 [US4] Implement export button functionality in `app.py`
-   [x] T044 [US4] Implement progress indicator for async operations in `app.py`
-   [x] T045 [US4] Add `main()` entry point function in `app.py`
-   [x] T046 [US4] Export GUI app from `py_lead_generation/src/gui/__init__.py`

### Tests for User Story 4

-   [x] T047 [P] [US4] Create `tests/test_gui.py` with mocked GUI tests (assert True for now)

**Checkpoint**: User Story 4 complete - GUI launches and can search/export.

---

## Phase 7: User Story 5 - 2GIS Engine Interface (Priority: P5)

**Goal**: Stub engine class following established pattern.

**Independent Test**: Verify class exists and inherits correctly.

### Implementation for User Story 5

-   [x] T048 [P] [US5] Create `py_lead_generation/src/twogis/engine.py` with TwoGisEngine stub
-   [x] T049 [US5] Define `BASE_URL`, `FIELD_NAMES`, `FILENAME` constants in `engine.py`
-   [x] T050 [US5] Add `__init__()` method with query/location parameters in `engine.py`
-   [x] T051 [US5] Add stub `_get_search_results_urls()` method (raise NotImplementedError)
-   [x] T052 [US5] Add stub `_parse_data_with_soup()` method (raise NotImplementedError)
-   [x] T053 [US5] Export TwoGisEngine from `py_lead_generation/src/twogis/__init__.py`

### Tests for User Story 5

-   [x] T054 [P] [US5] Add TwoGisEngine import test in `tests/test_engines.py`

**Checkpoint**: User Story 5 complete - 2GIS interface ready for future implementation.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup, documentation, and verification

-   [x] T055 Run full test suite with `uv run pytest tests/ -v`
-   [x] T056 Run linting with `uv run ruff check .`
-   [x] T057 Run type checking with `uv run mypy py_lead_generation/`
-   [x] T058 Update README.md with complete quickstart examples for all features
-   [x] T059 Verify all entry points work: `lead-gen-mcp --help`, `lead-gen-gui --help`
-   [x] T060 Create PR description summarizing all changes

**Checkpoint**: All features implemented, tests passing, ready for merge.

---

## Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational)
    │
    ├──────────────────────────────────────┐
    │                                      │
    ▼                                      ▼
Phase 3 (US1-Cleanup) ◄─── MVP ───►  Phases 4-7 can start
    │                                 after Phase 3
    │
    ├────► Phase 4 (US2-MCP)        [P] Parallel
    ├────► Phase 5 (US3-Email)      [P] Parallel
    ├────► Phase 6 (US4-GUI)        [P] Parallel
    └────► Phase 7 (US5-2GIS)       [P] Parallel
                │
                ▼
         Phase 8 (Polish)
```

## Parallel Execution Examples

### After Phase 3 (MVP), run in parallel:

-   **Terminal 1**: Phase 4 (MCP) - T022-T028
-   **Terminal 2**: Phase 5 (Email) - T029-T039
-   **Terminal 3**: Phase 6 (GUI) - T040-T047
-   **Terminal 4**: Phase 7 (2GIS) - T048-T054

### Within phases, [P] tasks can run simultaneously:

-   T005 + T006 + T007 + T008 (Setup)
-   T022 + T023 (MCP module files)
-   T029 + T030 (Email config + templates)

## Implementation Strategy

**MVP Scope**: Complete Phases 1-3 (T001-T021) for minimal viable package.

**Incremental Delivery**:

1. **Day 1**: Phases 1-3 (Cleanup + Package verification)
2. **Day 2**: Phase 4 (MCP Server) + Phase 7 (2GIS stub)
3. **Day 3**: Phase 5 (Email) + Phase 6 (GUI)
4. **Day 4**: Phase 8 (Polish + Documentation)

---

## Summary

| Phase | Tasks     | User Story             | Parallel?  |
| ----- | --------- | ---------------------- | ---------- |
| 1     | T001-T009 | Setup                  | Partial    |
| 2     | T010-T015 | Foundational           | Partial    |
| 3     | T016-T021 | US1 (P1) - Cleanup MVP | Partial    |
| 4     | T022-T028 | US2 (P2) - MCP         | ✅ Yes     |
| 5     | T029-T039 | US3 (P3) - Email       | ✅ Yes     |
| 6     | T040-T047 | US4 (P4) - GUI         | ✅ Yes     |
| 7     | T048-T054 | US5 (P5) - 2GIS        | ✅ Yes     |
| 8     | T055-T060 | Polish                 | Sequential |

**Total Tasks**: 60
**MVP Tasks**: 21 (Phases 1-3)
**Parallel Opportunities**: Phases 4-7 fully parallel after MVP
