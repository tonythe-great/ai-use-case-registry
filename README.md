# AI Use-Case Registry

A beginner-friendly web application for tracking and managing AI use cases within an organization.

## Features

- Register AI use cases with detailed metadata
- Automatic risk tier computation based on data sensitivity
- Simple HTML form interface
- RESTful API for programmatic access
- SQLite database for easy setup

## Requirements

- Python 3.11

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:
- Web interface: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | HTML form interface |
| POST | `/usecases` | Create a new use case |
| GET | `/usecases` | List all use cases |
| GET | `/usecases/{id}` | Get a specific use case |
| PATCH | `/usecases/{id}` | Update a use case |
| DELETE | `/usecases/{id}` | Delete a use case |

## Use Case Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Name of the use case |
| `owner` | string | Person responsible |
| `business_unit` | string | Department or team |
| `purpose` | string | Description of the use case |
| `model_type` | string | Type of AI model used |
| `vendor` | string | AI provider or vendor |
| `data_types` | list | Types of data processed |
| `data_residency` | string | Where data is stored |
| `external_sharing` | string | "yes" or "no" |
| `risk_tier` | string | Computed: "low", "medium", or "high" |
| `status` | string | "draft", "pending", "approved", or "rejected" |
| `created_at` | datetime | Auto-generated |
| `updated_at` | datetime | Auto-updated |

## Risk Tier Computation

Risk is computed automatically based on:
- **High risk**: PII, health data, financial data, biometric data, or external sharing
- **Medium risk**: Customer or employee data with compliant residency
- **Low risk**: Public or internal data only, no external sharing

## Project Structure

```
ai-use-case-registry/
├── app/
│   ├── main.py          # FastAPI application and routes
│   ├── db.py            # Database configuration
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic validation schemas
│   ├── risk.py          # Risk tier computation logic
│   └── templates/
│       └── index.html   # HTML form interface
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version specification
└── README.md            # This file
```

## Example API Usage

### Create a use case

```bash
curl -X POST http://127.0.0.1:8000/usecases \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Customer Support Chatbot",
    "owner": "Jane Doe",
    "business_unit": "Customer Service",
    "purpose": "Automated customer support using LLM",
    "model_type": "LLM",
    "vendor": "Anthropic",
    "data_types": ["Customer Data"],
    "data_residency": "US",
    "external_sharing": "no",
    "status": "draft"
  }'
```

### List all use cases

```bash
curl http://127.0.0.1:8000/usecases
```

### Get a specific use case

```bash
curl http://127.0.0.1:8000/usecases/1
```

### Update a use case

```bash
curl -X PATCH http://127.0.0.1:8000/usecases/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
```

### Delete a use case

```bash
curl -X DELETE http://127.0.0.1:8000/usecases/1
```
