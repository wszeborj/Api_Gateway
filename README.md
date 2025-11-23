* [General info])(#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [More detailed information about modules](#more-detailed-information-about-modules)
* [Application view](#application-view)


## General info
<details>
<summary>Click here to see general information about <b>Project</b>!</summary>
<b>Api Gateway - Online Learning Platform API</b>.
designed to unify communication between microservices.
Built with <b>FastAPI</b> and <b>Pydantic v2</b>, and secured using <b>Auth0</b> for authentication and authorization.

The gateway currently connects to one service — <code>Course Service</code> — responsible for handling courses, lessons, and exercises.
</details>

## Tools & Technologies
<ul>
<li>Python</li>
<li>fastapi[standard]</li>
<li>uvicorn[standard]</li>
<li>pydantic</li>
<li>pydantic-settings</li>
<li>sqlalchemy</li>
<li>alembic</li>
<li>mypy</li>
</ul>

## Setup
Clone the repo
```bash
git clone https://github.com/wszeborj/api-gateway.git
```
Go to project folder
```bash
cd api-gateway
```
Install poetry
```bash
pip install poetry
```
Install all modules
```bash
poetry install
```

## Application features
<ul>
<li><b>Central Gateway:</b> Single entry point for all microservices</li>
<li><b>Auth0 Integration:</b> JWT-based authentication and authorization</li>
<li><b>Proxy Routing:</b> Intelligent forwarding of requests to backend microservices</li>
<li><b>Scalability:</b> Modular architecture ready for additional services</li>
<li><b>RESTful Endpoints:</b> Clean and consistent API design</li>
<li><b>Auto Documentation:</b> Built-in Swagger UI & ReDoc</li>
<li><b>Validation:</b> Pydantic models for request/response schemas</li>
<li><b>Async:</b> Fully asynchronous communication using HTTPX</li>
</ul>

## Application View
