# Soccer Statistics Tracker

A personal soccer statistics tracking application built from the ground up in Python.

The goal of this project is simple: **track my soccer performance, store the data properly, and eventually use that data to understand and improve my performance.**

What started as a command-line program storing match information in JSON has evolved into a fully functional GUI application with a SQLite database, input validation, match management, statistics, and mobile support through Flet.

## Current Version — v2.5

**v2.5 is the completed single-user version of the application.**

The app currently supports:

* Add match records
* Edit existing matches
* Delete matches
* View all matches
* View individual match details
* View season statistics
* Match result tracking
* Goals and assists
* Minutes played
* Cards
* Player confidence
* Opponent and competition information
* Input validation
* Persistent SQLite storage
* Flet-based GUI
* iOS/mobile use
* Organized frontend/backend architecture

The application is currently designed around a single user and local database.

## Screens & Functionality

The application is organized around several core workflows:

### Match Management

Create, view, edit, and delete match records while validating the data before it reaches the database.

### Statistics

The application aggregates stored match data into season-level statistics, including results, goals, assists, minutes, confidence, and goal differential.

### Persistent Storage

Match data is stored using SQLite rather than temporary in-memory data or JSON files.

### Mobile

The application can be run through Flet on an iPhone, allowing match information to be entered and viewed away from the computer.

## Architecture

The project is separated into frontend and backend components:

```text
Soccer-Statistics-Tracker/
│
├── backend/
│   └── Database and application logic
│
├── frontend/
│   └── GUI, pages, and navigation
│
├── main.py
└── .gitignore
```

The separation is intentional: the interface should not need to know the implementation details of how data is stored.

## Tech Stack

* **Python** — primary programming language
* **Flet** — cross-platform GUI
* **SQLite** — local relational database
* **Git / GitHub** — version control and project history

## Project Evolution

This project has gone through several major stages:

```text
v1
JSON-based match storage + command-line interface
        ↓
v1.5
Migrated from JSON to SQLite
        ↓
v2
Input validation + functional SQLite database
        ↓
v2.1
Started Flet GUI
        ↓
v2.2
Connected GUI input to validation and database
        ↓
v2.3
Completed match viewing, season statistics, and deletion
        ↓
v2.4
Bug fixes and stability improvements
        ↓
v2.5
Edit Match + final bug fixes + mobile use + project restructuring
```

## Roadmap

### v3 — Cloud & Authentication

* User authentication
* Cloud PostgreSQL database
* User-specific data
* Cross-device synchronization
* Training session tracking infrastructure

A likely implementation is Supabase/PostgreSQL, although the final architecture has not been decided.

### v3.5 — Training & Analysis

Expand the application beyond match tracking.

Planned areas include:

* Training session tracking
* Training history
* Performance analysis
* More meaningful statistical insights
* Relationships between training and match performance

The long-term goal is not simply to **store statistics**, but to make the stored data useful.

### v4 — Product

Potential goals:

* Improved UI/UX
* Production-level reliability
* Monetization
* Public release
* iOS App Store distribution

The exact feature set and business model will depend on how the application develops and how other users actually use it.

## Why I Built This

I wanted something more useful than a programming exercise.

The original version was essentially a command-line statistics tracker with JSON storage. Over time, I kept replacing parts of it as I learned more:

**JSON → SQLite → GUI → mobile → better architecture**

Each version introduced a new technical problem to solve.

The project has also been intentionally built without relying on AI to generate the application for me. AI may be useful for research, debugging, or explaining concepts, but the architecture, implementation, and problem-solving process are my own.

## Current Status

**v2.5 — Complete**

The current version is considered the finished foundation for the project.

Future development will focus on turning the application from a personal single-user tracker into a multi-user platform capable of storing, analyzing, and eventually monetizing soccer performance data.
