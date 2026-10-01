EIGEN — AI Email Operations

«AUTOMATING IMPACT»

An AI-powered email operations and workflow automation system built by EIGEN.

EIGEN transforms unstructured business emails into structured data, automated workflows, and actionable business operations.

How It Works

EMAIL
  ↓
INGEST
  ↓
CLASSIFY
  ↓
EXTRACT
  ↓
WORKFLOW
  ↓
ACTION
  ↓
LOG

Example:

Customer Email
      ↓
AI Classification
      ↓
SALES_LEAD
      ↓
Extract Lead Information
      ↓
Create CRM Lead
      ↓
Notify Sales
      ↓
Generate Reply Draft

Core Features

- AI email classification
- Structured information extraction
- Configurable workflow engine
- Human-in-the-loop review
- Automated response drafting
- Notifications & external integrations
- Idempotent processing
- Multi-tenant architecture
- Audit logging
- Security & prompt-injection protection

Initial Workflows

- Sales Lead → Create lead → Notify sales → Draft response
- Customer Support → Create ticket → Assign → Draft response
- Invoice → Extract details → Store → Notify finance
- General Enquiry → Classify → Generate draft → Review

Tech Stack

Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic

AI

- LLM API with structured outputs

Email

- Gmail API (initial integration)

Testing

- pytest

Deployment

- Docker + cloud infrastructure

Architecture

Gmail / Outlook
       ↓
EIGEN Backend
       ↓
AI Service
       ↓
Workflow Engine
       ↓
┌──────┼────────┐
CRM  Notifications  Internal Systems
       ↓
   PostgreSQL

Philosophy

«AI understands. Software decides and executes.»

EIGEN is designed as a reusable automation layer rather than a one-off AI email bot.

Different clients should be supported primarily through configuration and integrations, without rebuilding the core system.

Status

🚧 In Development

EIGEN — Automating Impact