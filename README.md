# AI Use-Case Registry

A beginner-friendly web application for tracking and managing AI use cases within an organization.

## Live Demo

**Executive Dashboard:** https://ai-use-case-registry.onrender.com/

**Registration Form:** https://ai-use-case-registry.onrender.com/register

## Features

- **Executive Dashboard** with real-time metrics and visualizations
  - Summary cards: Total Use Cases, High Risk Systems, Pending Approvals, External Data Sharing %
  - Interactive Chart.js pie chart showing risk distribution
  - High-risk items table with action buttons
  - Auto-refresh every 30 seconds
- **User-Friendly Registration Form** with guided input
  - Organized into 3 numbered sections: Basic Information, AI Model Details, Data & Privacy
  - Dropdown menus for Business Unit (17 departments) and Vendor (16+ AI providers)
  - Quick-select purpose templates (8 common use case types with pre-filled descriptions)
  - Expanded Model Type options (16 types organized by category)
  - Color-coded Data Types organized by risk level (High/Medium/Low)
  - Radio buttons with descriptions for External Sharing
- **Professional UI** built with Tailwind CSS
- Automatic risk tier computation based on data sensitivity
- Color-coded risk badges (red/yellow/green)
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
| GET | `/` | Executive dashboard |
| GET | `/register` | Use case registration form |
| GET | `/dashboard/stats` | Dashboard statistics (JSON) |
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

## Available Form Options

### Business Units
Technology: Engineering, IT, Data Science, Product, Security
Operations: Customer Service, Operations, Supply Chain, Quality Assurance
Business: Sales, Marketing, Finance, HR, Legal & Compliance
Other: Research & Development, Executive Office, Other

### Vendors/Providers
LLM Providers: OpenAI, Anthropic, Google, Meta, Cohere, Mistral AI
Cloud Platforms: AWS, Azure, GCP, IBM Watson
Specialized: Hugging Face, Stability AI, Midjourney, Salesforce Einstein
Other: Internal/In-house, Open Source, Other

### Model Types
Generative AI: LLM, Image Generation, Code Generation, Audio Generation
Analysis: Classification, Regression, Anomaly Detection, Forecasting
Language & Vision: NLP, Computer Vision, OCR, Speech Recognition
Other: Recommendation, Semantic Search, Chatbot, Other

### Data Types (by risk level)
High Risk: PII, Health Data, Financial Data, Biometric Data
Medium Risk: Customer Data, Employee Data, Usage Data, Location Data
Low Risk: Public Data, Aggregated Data, Product Data, Internal Documents

### Data Residency
Single Region: US, EU, UK, APAC, Canada, Australia
Multi-Region: International, Unknown/Vendor-managed

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
│       ├── dashboard.html  # Executive dashboard (Tailwind + Chart.js)
│       └── register.html   # Use case registration form
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
