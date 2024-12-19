# Peanut-Server README

## Overview

**Peanut-Server** is a Python-based Flask server designed to handle version management for software installers. It allows developers to manage and distribute versions of their applications, organized into different branches, providing a seamless way to deploy and update software across various environments. Each application can have multiple branches (e.g., `stable`, `beta`, `dev`), and each branch can have multiple versions.

## Features

- **Version Management:** Manage versions for each application, with the ability to store and retrieve specific versions for installation.
- **Branch Support:** Each application can have multiple branches (e.g., `stable`, `beta`, `dev`, ect), allowing you to manage different stages of development and deployment.
- **Flask-based Server:** A lightweight and easy-to-use API server built with Flask.
- **Installer Distribution:** Provide installers for specific versions and branches to users, making it easy to distribute updates.
- **JSON API:** Interact with the server using a simple RESTful API that provides version details, available branches, and download links.

## Installation

### Prerequisites

- Python 3.12 or later
- pip (Python package installer)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/LoganNeel/Peanut-server.git
    cd Peanut-server
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables for the Flask server configuration. You can copy and modify the `.env.example` file or set them directly as environment variables.

    Example:

    ```bash
    DEVELOPER_KEY={Put key here}
    PROJECT_ROOT={Put path to project storage here}
    ```

5. Run the server:

    ```bash
    flask run
    ```

    The server will start on `http://127.0.0.1:5000` by default.


# Roadmap for Update Versioning Server

## Phase 1: Foundation
- [x] **Initial Setup**
  - Set up server environment and database.
  - Configure basic versioning structure.
- [x] **Core Features**
  - Implement route-based update handling.
  - Integrate with AutoUpdater for XML-based configurations.
  - Create admin interface for managing updates.
- [x] **Testing**
  - Perform unit tests on versioning routes.
  - Validate compatibility with AutoUpdater.

## Phase 2: Expanding
- [x] **Set Repo Public**
- [ ] **Add Private Routes**
    - Support for creating randomized download link
    - Support for support for setting expirations on download link
    - Support for custom download link 'rules'

