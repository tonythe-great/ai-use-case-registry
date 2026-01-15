# AI Use-Case Registry

A comprehensive web application for tracking and managing AI use cases within an organization, featuring an Enterprise AI Governance Intake System aligned with NIST AI Risk Management Framework.

## Live Demo

**AI Governance Intake System:** [https://ai-use-https://ai-use-case-registry.onrender.com/intake/1/report)


## Features

### Executive Dashboard
- Real-time metrics and visualizations
- Summary cards: Total Use Cases, High Risk Systems, Pending Approvals, External Data Sharing %
- Interactive Chart.js pie chart showing risk distribution
- High-risk items table with action buttons
- Auto-refresh every 30 seconds

### User-Friendly Registration Form
- Organized into 3 numbered sections: Basic Information, AI Model Details, Data & Privacy
- Dropdown menus for Business Unit (17 departments) and Vendor (16+ AI providers)
- Quick-select purpose templates (8 common use case types with pre-filled descriptions)
- Expanded Model Type options (16 types organized by category)
- Color-coded Data Types organized by risk level (High/Medium/Low)
- Radio buttons with descriptions for External Sharing

### Enterprise AI Governance Intake System (NEW)
- **10-Step Wizard** for comprehensive AI system assessment
- **User-Friendly Intake Form** with dropdown menus for easy input
- **NIST AI RMF Aligned** - Follows MAP phase of the AI Risk Management Framework
- **5 Assessment Sections:**
  1. Basic Information - System name, vendor, deployment stage
  2. Human Oversight - Decision classification, human-in-the-loop level
  3. Data & Privacy - Data types, retention policy, user training
  4. Ownership & Accountability - Executive sponsor, business/technical owners
  5. Compliance & Monitoring - Federal contracts, logging, incident response

#### Intake Form Features
- Grouped dropdown menus for AI vendors (Major Providers, Enterprise Platforms)
- Common use case templates with auto-populate
- User count range selector
- Data type checkboxes with visual risk indicators
- Color-coded section headers for easy navigation
- Mobile-responsive design
- Save Draft and Submit for Review functionality

### Professional UI
- Built with Tailwind CSS
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
uvicorn app.main:app --reload --port 8080
```

The application will be available at:
- Web interface: http://127.0.0.1:8080
- API documentation: http://127.0.0.1:8080/docs

## API Endpoints

### Use Case Registry

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

### AI Governance Intake System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/intake` | List all intake assessments |
| GET | `/intake/new` | Start a new intake assessment |
| GET | `/intake/{id}/step/{num}` | Wizard step (1-10) |
| POST | `/intake/{id}/step/{num}` | Save wizard step data |
| GET | `/intake/{id}/review` | Review intake before submission |
| GET | `/intake/{id}/report` | View/edit intake form with dropdowns |
| POST | `/api/intakes` | Create new intake (API) |
| GET | `/api/intakes/{id}` | Get intake details (API) |
| PATCH | `/api/intakes/{id}` | Update intake (API) |
| DELETE | `/api/intakes/{id}` | Delete intake (API) |
| POST | `/api/intakes/{id}/risks` | Add risk assessment |
| POST | `/api/intakes/{id}/artifacts` | Add required artifact |
| POST | `/api/intakes/{id}/actions` | Add action item |

## Intake Assessment Fields

| Field | Type | Description |
|-------|------|-------------|
| `system_name` | string | Name of the AI system |
| `business_purpose` | string | Business use case description |
| `vendor_name` | string | AI provider/vendor |
| `deployment_status` | string | planning, pilot, limited_production, full_production |
| `user_count` | integer | Number of users |
| `decision_classification` | string | informational, decision_support, semi_autonomous, fully_autonomous |
| `human_in_the_loop` | string | full_oversight, approval_required, exception_only, none |
| `approved_data_types` | list | Data types approved for use |
| `data_retention_policy` | string | zero_retention, 30_days, 90_days, 1_year, indefinite |
| `approving_authority` | string | Executive sponsor name |
| `business_owner` | string | Business owner name |
| `technical_owner` | string | Technical owner name |
| `readiness_status` | string | approved, conditional, not_ready, pending |

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

### AI Vendors (Intake System)
**Major AI Providers:** OpenAI, Microsoft (Copilot, Azure OpenAI), Google (Gemini, Vertex AI), Anthropic (Claude), Amazon (Bedrock, Q)
**Enterprise Platforms:** Salesforce (Einstein), ServiceNow, SAP, IBM (Watson)
**Other:** In-house/Custom Built, Other

### Business Units
Technology: Engineering, IT, Data Science, Product, Security
Operations: Customer Service, Operations, Supply Chain, Quality Assurance
Business: Sales, Marketing, Finance, HR, Legal & Compliance
Other: Research & Development, Executive Office, Other

### Vendors/Providers (Legacy Registry)
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
│   ├── main.py              # FastAPI application and routes
│   ├── db.py                # Database configuration
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── risk.py              # Risk tier computation logic
│   └── templates/
│       ├── dashboard.html   # Executive dashboard (Tailwind + Chart.js)
│       ├── register.html    # Use case registration form
│       └── intake/
│           ├── _wizard_layout.html    # Shared wizard layout
│           ├── list.html              # Intake list view
│           ├── report.html            # Intake form with dropdowns
│           ├── review.html            # Review before submission
│           ├── step_1_inventory.html  # AI System Inventory
│           ├── step_2_decision.html   # Decision Impact Classification
│           ├── step_3_data.html       # Data Sensitivity & Flow
│           ├── step_4_ownership.html  # Ownership & Accountability
│           ├── step_5_regulatory.html # Regulatory Context
│           ├── step_6_monitoring.html # Monitoring & Logging
│           ├── step_7_risks.html      # Risk Assessment
│           ├── step_8_artifacts.html  # Required Artifacts
│           ├── step_9_readiness.html  # Readiness Determination
│           └── step_10_actions.html   # Action Items
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python version specification
└── README.md                # This file
```

## Example API Usage

### Create a use case

```bash
curl -X POST http://127.0.0.1:8080/usecases \
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

### Create an intake assessment

```bash
curl -X POST http://127.0.0.1:8080/api/intakes \
  -H "Content-Type: application/json" \
  -d '{
    "system_name": "ChatGPT Enterprise",
    "business_purpose": "Information gathering and decision support",
    "vendor_name": "OpenAI",
    "deployment_status": "pilot",
    "user_count": 80,
    "decision_classification": "decision_support",
    "human_in_the_loop": "approval_required"
  }'
```

### List all use cases

```bash
curl http://127.0.0.1:8080/usecases
```

### Get a specific use case

```bash
curl http://127.0.0.1:8080/usecases/1
```

### Update a use case

```bash
curl -X PATCH http://127.0.0.1:8080/usecases/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
```

### Delete a use case

```bash
curl -X DELETE http://127.0.0.1:8080/usecases/1
```

## Framework Alignment

The Enterprise AI Governance Intake System is aligned with:
- **NIST AI Risk Management Framework (AI RMF)** - MAP Phase
- Enterprise governance best practices for AI adoption
- Risk-based approach to AI system assessment

## License

MIT License
