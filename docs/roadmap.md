# Learning Roadmap

This document defines the learning sequence and implementation milestones for the FastAPI Fundamental project.

## Guiding Principles

1. Learn Python fundamentals before relying on framework abstractions.
2. Practice each concept with small, focused examples.
3. Understand HTTP and REST API behavior before implementing CRUD.
4. Keep application data in memory; do not introduce a database.
5. Test locally before deploying to a remote server.
6. Document meaningful technical decisions and trade-offs.
7. Deploy the finished API to AWS EC2 and verify it through a public endpoint.

## Phase 0 — Development Environment

**Goal:** Prepare a reproducible local development environment.

Topics:
- Python installation on Windows
- Python interpreter and package management
- Virtual environments with `venv`
- `pip` and dependency management
- Git repository setup
- Project structure and `.gitignore`

Deliverables:
- Working Python environment
- Initialized Git repository
- Project documentation

## Phase 1 — Python Fundamentals

**Goal:** Understand the language features needed to build and maintain a simple API.

Topics:
- Variables and basic data types
- Strings and common operations
- Lists, tuples, sets, and dictionaries
- Conditional statements and loops
- Functions, parameters, return values, and scope
- Modules and imports
- Exceptions and error handling
- File and package organization
- Type hints
- Basic object-oriented programming
- Decorators and their use cases

Deliverables:
- Small runnable examples for each topic
- Exercises demonstrating the concepts
- A clear understanding of how Python features apply to API development

## Phase 2 — HTTP and FastAPI Fundamentals

**Goal:** Understand how FastAPI maps Python functions to HTTP endpoints.

Topics:
- HTTP methods and status codes
- REST API fundamentals
- FastAPI application setup
- Path and query parameters
- Request bodies
- Pydantic models and input validation
- Response models
- Error handling with `HTTPException`
- Automatic OpenAPI documentation
- Basic dependency injection

Deliverables:
- A runnable FastAPI application
- Initial endpoints
- Interactive API documentation at `/docs`

## Phase 3 — In-Memory CRUD API

**Goal:** Implement a complete CRUD API without a database.

Resource: `items`

Endpoints:
- `POST /items` — create an item
- `GET /items` — list items
- `GET /items/{item_id}` — retrieve an item
- `PUT /items/{item_id}` — update an item
- `DELETE /items/{item_id}` — delete an item
- `GET /health` — check application health

Topics:
- Python lists and dictionaries for temporary storage
- Unique identifier generation
- Request validation
- Resource-not-found handling
- Appropriate HTTP status codes
- Separation of API concerns from business logic

Deliverables:
- Complete CRUD behavior
- Consistent response and error handling
- A documented endpoint contract

Limitation: In-memory data is temporary and is lost when the application process restarts.

## Phase 4 — Automated Testing

**Goal:** Verify API behavior and prevent regressions.

Topics:
- pytest fundamentals
- FastAPI TestClient
- Testing successful requests
- Testing invalid inputs
- Testing missing resources
- Testing CRUD lifecycle behavior
- Test isolation and resetting in-memory data

Deliverables:
- Automated tests for every endpoint
- Coverage of common error cases
- Repeatable local test execution

## Phase 5 — AWS EC2 Deployment

**Goal:** Deploy and run the API on a remote Linux server.

Topics:
- AWS account and cost considerations
- EC2 instance selection
- SSH key management
- Security groups and network access
- Linux command-line basics
- Python environment setup on Linux
- Application deployment
- Uvicorn process management
- Environment configuration
- Basic server logs and troubleshooting

Deliverables:
- Running FastAPI application on EC2
- Publicly accessible API endpoint
- Verified CRUD operations from an external client

## Phase 6 — Deployment Reliability Basics

**Goal:** Understand the minimum operational practices needed to keep the API running.

Topics:
- Running the application as a managed service with systemd
- Restart behavior
- Application logs
- Health checks
- Basic Nginx reverse proxy concepts
- HTTPS and domain configuration concepts
- Safe handling of secrets and SSH access

Deliverables:
- Application starts reliably after a service restart
- Documented deployment and troubleshooting steps
- A clear understanding of remaining production limitations

## Completion Criteria

The project is complete when:

- [ ] Python fundamentals have been practiced.
- [ ] The FastAPI CRUD API works locally.
- [ ] Automated tests pass.
- [ ] No database is required.
- [ ] The API is deployed to AWS EC2.
- [ ] Endpoints are verified remotely.
- [ ] Deployment instructions are documented.
- [ ] AWS resources and potential ongoing costs are understood.

## Future Projects

Advanced topics should be developed in separate repositories when needed, including database integration, authentication, Docker-based deployment, and more complex backend architecture.