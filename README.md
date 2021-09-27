# Project Status Manager

![status: completed](https://img.shields.io/badge/status-completed-success)

## About this Project

A tool to configure my project statuses and automatically push them to GitHub.

Status options:

- in-progress
- on-hold
- plan-to-finish
- dropped
- completed

### Built with

- Python

## Getting Started

### Prerequisites

- Python

### Installation

1. Create a Python virtual environment.

```
python3 -m venv .venv
```

2. Activate the virtual environment.

```
// On Windows
.venv/Scripts/Activate

// On Mac
source .venv/bin/activate
```

## Usage

1. Modify the bottom of `app.py` to tell it what to do (e.g. auto load the project statuses or update them).

2. Update the statuses of any project in `projects.config.json`.

3. Run `python3 app.py`.

4. You will be prompted to confirm any commits & pushes to GitHub. Carefully check the changes.

## Roadmap

No planned features.

- [ ] CLI?

## Release History

- v1.0.0
  - Core complete
