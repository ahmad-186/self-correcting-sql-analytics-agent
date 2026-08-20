# InsightAI --- Self-Correcting Natural Language SQL & Analytics Agent

InsightAI is an AI-powered business analytics application that lets
users ask questions about business data in natural language and receive
structured, business-oriented answers.

The system combines a React analytics dashboard, FastAPI backend,
LangGraph-based analytics workflow, PostgreSQL, SQL validation, result
analysis, visualization recommendation, and LLM-generated executive
insights.

> **Project status:** Core backend, analytics workflow, API
> documentation, automated tests, and React dashboard are implemented.
> Dockerization and deployment are the next milestone.

## Features

### Natural-Language Analytics

Ask questions such as:

-   Show total sales by product
-   Show all customers
-   Which products generate the most revenue?
-   Compare sales across cities

Users do not need to write SQL manually.

### Self-Correcting SQL Analytics Workflow

The agent workflow:

1.  Understands the user's question.
2.  Inspects the database schema.
3.  Generates SQL.
4.  Validates generated SQL.
5.  Detects validation/execution problems.
6.  Attempts self-correction.
7.  Executes the validated query.
8.  Analyzes the returned dataset.
9.  Recommends an appropriate visualization.
10. Generates an executive summary and key insights.

### Result Analysis

Returned data is analyzed for:

-   Row count
-   Column names
-   Numeric columns
-   Categorical columns
-   Datetime columns
-   Empty-result state

### Executive Insights

The system generates business-oriented:

-   Executive summaries
-   Key insights
-   Important numerical findings
-   Supported comparisons and patterns

### Visualization Recommendation

The system can recommend and render:

-   Bar charts
-   Line charts
-   Pie/donut-style visualizations
-   Tables

### React Analytics Dashboard

The dashboard provides:

-   Natural-language query input
-   Suggested questions
-   Loading/analysis state
-   KPI cards
-   Executive summary
-   Key insights
-   Interactive visualizations
-   Query result tables
-   Query history UI
-   Saved insights UI
-   Settings UI
-   Backend status indicator

Some non-core dashboard sections are currently UI-level features and are
not yet backed by persistent storage.

## Architecture

``` text
                         ┌──────────────────────┐
                         │    React Frontend    │
                         │   Analytics Dashboard│
                         └──────────┬───────────┘
                                    │
                                  HTTP
                                    │
                         ┌──────────▼───────────┐
                         │       FastAPI        │
                         │       REST API       │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │      LangGraph       │
                         │  Analytics Workflow  │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      Schema Inspection       SQL Generation        Validation /
                                                     Self-Correction
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    │
                         ┌──────────▼───────────┐
                         │      PostgreSQL      │
                         │    Business Data     │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │    Result Analysis   │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    ▼                                ▼
             Visualization                  Executive Summary
              Recommendation                 + Key Insights
                    │                                │
                    └───────────────┬────────────────┘
                                    ▼
                            React Dashboard
```

## Analytics Workflow

``` text
User Question
     │
     ▼
Schema Inspector
     │
     ▼
SQL Generator
     │
     ▼
Validation
     │
     ├── Invalid ──► Self-Correction ──► Validation
     │
     ▼
SQL Execution
     │
     ▼
Result Analysis
     │
     ├───────────────┐
     ▼               ▼
Visualization    Executive
Recommendation    Summary
     │               │
     └───────┬───────┘
             ▼
       React Dashboard
```

## Technology Stack

### Backend

-   Python
-   FastAPI
-   LangGraph
-   LangChain
-   PostgreSQL
-   SQLGlot
-   Pydantic
-   Pytest
-   HTTPX / FastAPI TestClient
-   Structured LLM output

### Frontend

-   React
-   Vite
-   JavaScript
-   Recharts
-   ESLint

### Development

-   Git / GitHub
-   VS Code
-   Docker --- next deployment milestone

## Project Structure

A simplified structure is:

``` text
Self Correcting Natural Language SQL and Analyst Agent/
│
├── app/
│   ├── config/
│   ├── graph/
│   ├── models/
│   ├── nodes/
│   ├── prompts/
│   ├── schemas/
│   └── ...
│
├── tests/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── ...
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── ...
│
├── .env
├── pyproject.toml
└── README.md
```

## Backend Setup

### Clone the repository

``` bash
git clone <YOUR_REPOSITORY_URL>
cd "Self Correcting Natural Language SQL and Analyst Agent"
```

### Create a Python environment

``` bash
python -m venv .venv
```

Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

``` bash
pip install -e .
```

Use the dependency installation command defined by the current
`pyproject.toml` if it differs.

### Configure environment variables

Create a `.env` file using the variables required by the current
application configuration.

Typical configuration includes:

``` env
DATABASE_URL=<POSTGRESQL_CONNECTION_STRING>
LLM_API_KEY=<YOUR_LLM_API_KEY>
```

Use the exact variable names defined by the project's configuration.

**Never commit real credentials or API keys to GitHub.**

### Start FastAPI

For a standard FastAPI entry point:

``` bash
uvicorn app.main:app --reload
```

The backend should then be available at:

``` text
http://127.0.0.1:8000
```

## API Documentation

When FastAPI is running, interactive API documentation is available at:

``` text
http://127.0.0.1:8000/docs
```

The OpenAPI schema is also available through FastAPI's standard OpenAPI
endpoint.

## Frontend Setup

``` bash
cd frontend
npm install
npm run dev
```

The Vite development server runs at:

``` text
http://localhost:5173
```

The frontend communicates with the FastAPI backend through the
configured API endpoint.

## Running Tests

Run the backend test suite with:

``` bash
pytest -q
```

The current project has automated tests covering core backend
functionality.

Example successful run:

``` text
13 passed
```

There may be dependency/deprecation warnings that do not currently cause
test failures.

## Example

A user can enter:

``` text
Show total sales by product
```

The request is processed through the analytics workflow and can produce:

``` text
Executive Summary

The analysis shows total sales across four products.

Key Insights

- Office Chair had the highest sales.
- Monitor 27" was another major contributor.
- Gaming Mouse had the lowest sales.

Total Sales by Product

[Interactive Chart]

Query Result

Product                 Total Sales
-----------------------------------
Monitor 27"             $250.00
Mechanical Keyboard      $90.00
Office Chair            $360.00
Gaming Mouse             $45.00
```

The actual values are generated from the connected database rather than
hardcoded into the analytics workflow.

## Safety and SQL Validation

Because SQL is generated with an LLM, validation is a critical part of
the architecture.

The project includes validation logic designed to:

-   Validate SQL syntax.
-   Restrict execution to appropriate read operations.
-   Validate referenced database objects against schema information.
-   Prevent invalid generated SQL from reaching execution.
-   Feed validation/execution failures back into the self-correction
    workflow.

For production deployment, additional protections such as read-only
database credentials, query timeouts, resource limits, and stronger
tenant isolation should be considered.

## Current Scope

The current version focuses on the complete analytics pipeline:

``` text
Natural Language
      ↓
AI Analytics Agent
      ↓
SQL
      ↓
Validation
      ↓
Execution
      ↓
Result Analysis
      ↓
Visualization
      ↓
Executive Insights
      ↓
Interactive Dashboard
```

The application currently operates against the configured database
rather than allowing each end user to connect arbitrary databases.

## Roadmap

### Phase 1 --- Core Analytics Agent

-   Natural-language analytics
-   Schema inspection
-   SQL generation
-   SQL validation
-   Self-correction
-   Query execution
-   Result analysis
-   Visualization recommendation
-   Executive summaries

**Status: Completed**

### Phase 2 --- Analytics Dashboard

-   React dashboard
-   Interactive query interface
-   KPI cards
-   Executive summaries
-   Key insights
-   Interactive visualizations
-   Result tables
-   Analysis history UI

**Status: Core implementation completed**

### Phase 3 --- Containerization

Planned:

-   Backend Dockerfile
-   Frontend Dockerfile
-   Docker Compose
-   Environment variable management
-   PostgreSQL container/deployment strategy
-   Local production-like testing

**Status: Next**

### Phase 4 --- Deployment

Planned:

-   Production deployment
-   HTTPS
-   Secrets management
-   Monitoring
-   Health checks
-   Production database configuration

### Phase 5 --- Multi-Database / SaaS Architecture

Potential future capabilities:

-   User database connections
-   PostgreSQL/MySQL support
-   Secure credential storage
-   Connection management
-   Multi-tenant isolation
-   Per-user data-source management
-   Database-level read-only users

This is intentionally outside the current deployment scope.

### Phase 6 --- Advanced Analytics

Potential future improvements:

-   Persistent query history
-   Persistent saved insights
-   Advanced KPI generation
-   Multi-agent architecture
-   Schema-aware semantic/hybrid retrieval
-   Additional visualization types
-   Scheduled reports
-   Exportable reports
-   Advanced business intelligence features

## Development Principles

The project is being developed incrementally, prioritizing a complete
working system before adding unnecessary complexity.

Key principles:

1.  Preserve separation between frontend and backend.
2.  Keep the analytics graph modular.
3.  Validate LLM-generated SQL before execution.
4.  Avoid hardcoding business data.
5.  Keep API contracts explicit.
6.  Add tests when introducing backend behavior.
7.  Keep secrets out of source control.

## Project Status

  Component                           Status
  ----------------------------------- -----------
  FastAPI backend                     Completed
  PostgreSQL integration              Completed
  LangGraph analytics workflow        Completed
  Schema inspection                   Completed
  SQL generation                      Completed
  SQL validation                      Completed
  SQL self-correction                 Completed
  Result analysis                     Completed
  Executive summary                   Completed
  Visualization recommendation        Completed
  Automated backend tests             Completed
  OpenAPI documentation               Completed
  CORS integration                    Completed
  React frontend                      Completed
  Interactive analytics dashboard     Completed
  Dockerization                       Next
  Deployment                          Planned
  Multi-database connections          Future
  Persistent history/saved insights   Future

## Contributing

This is primarily a personal engineering project.

When extending it:

1.  Preserve frontend/backend separation.
2.  Keep the LangGraph workflow modular.
3.  Validate LLM-generated SQL before execution.
4.  Avoid hardcoding business data.
5.  Keep API contracts explicit.
6.  Add tests for new backend behavior.
7.  Keep secrets out of source control.

## License

Add the appropriate license before public distribution.

## Author

**Ahmad Shahzad**

AI Engineering • Full-Stack AI • Agentic Systems • Automation
