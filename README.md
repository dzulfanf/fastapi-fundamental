# FastAPI Fundamental

A hands-on learning project for understanding Python fundamentals,
building a REST API with FastAPI, and deploying it to an AWS EC2
instance.

## Goals

-   Learn Python fundamentals through practical exercises.
-   Understand the fundamentals of FastAPI and REST API development.
-   Build a simple CRUD API without a database.
-   Practice automated testing and API validation.
-   Learn the basics of deploying and running an application on AWS EC2.

## Project Scope

**Included:** - Python syntax, data types, collections, and control
flow - Functions, modules, exceptions, decorators, and type hints -
FastAPI routing and request handling - Request validation and response
handling with Pydantic - In-memory CRUD operations - Automated testing
with pytest and FastAPI TestClient - AWS EC2 deployment and basic Linux
server operations - `systemd` service management and Nginx reverse proxy
configuration

**Out of scope:** - Database integration and ORM - Authentication and
authorization - Redis and message queues - Microservices and complex
backend architecture

## Technology Stack

-   Python
-   FastAPI
-   Uvicorn
-   Pydantic
-   pytest
-   Git
-   AWS EC2
-   Ubuntu Server
-   `systemd`
-   Nginx

## Getting Started

### Prerequisites

-   Python 3.12 or a compatible Python version
-   Git
-   Visual Studio Code or another code editor

### Setup

Clone the repository:

``` bash
git clone https://github.com/dzulfanf/fastapi-fundamental.git
cd fastapi-fundamental
```

Create a virtual environment:

``` bash
python -m venv .venv
```

Activate it on Windows PowerShell:

``` powershell
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

``` bash
source .venv/bin/activate
```

Install dependencies:

``` bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the application from the repository root:

``` bash
python -m uvicorn app.main:app --app-dir src --reload
```

Local endpoints: - API root: `http://127.0.0.1:8000/` - Health check:
`http://127.0.0.1:8000/health` - Swagger UI:
`http://127.0.0.1:8000/docs`

Stop the development server with `Ctrl+C`.

## Deployment

The API has been deployed to AWS EC2 using Ubuntu Server, `systemd`, and
Nginx as a reverse proxy.

See the [AWS EC2 Deployment Guide](docs/deployment/aws-ec2.md) for
step-by-step instructions covering EC2 setup, SSH, server preparation,
dependency installation, `systemd`, Nginx, network access, verification,
and troubleshooting.

**Security:** Never commit private SSH keys, credentials, access tokens,
or other secrets to this repository.

## Learning Roadmap

See [docs/roadmap.md](docs/roadmap.md) for the learning phases and
implementation milestones.

## Current Limitations

-   CRUD data is stored in memory and is lost when the application
    process restarts.
-   The current EC2 deployment uses HTTP. Configure a domain and HTTPS
    before using it for sensitive or production traffic.
-   This is a learning project, not a production-hardened service.

## License

To be determined.
