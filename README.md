# AI Finance Controller

A full-stack, AI-powered financial reconciliation and operations platform built specifically for the Razorpay hackathon. This system deterministically reconciles payments, invoices, routes, and settlements using Razorpay's APIs, and leverages a Neo4j financial knowledge graph and OpenAI to provide AI-driven insights and anomaly detection.

## 🚀 Architecture & Tech Stack

*   **Frontend (Apps/Web)**: Next.js 15, React 19, Tailwind CSS v4, shadcn/ui. Premium dark-mode glassmorphism design.
*   **Backend (Apps/API)**: FastAPI, Python 3.13, SQLAlchemy (Async), Alembic.
*   **Orchestration**: Temporal (reliable workflow execution for the reconciliation pipeline).
*   **Database Layers**:
    *   **PostgreSQL**: Relational truth for invoices, payments, settlements, and Route splits.
    *   **Neo4j**: Financial Knowledge Graph for AI context.
    *   **Redis**: Caching and background task queuing.
*   **AI Agents**: OpenAI (GPT-4o) structured outputs for root-cause investigation and natural language Q&A.

## 📂 Project Structure

```text
finance-controller/
├── apps/
│   ├── api/                  # FastAPI Backend
│   │   ├── app/              # Core backend logic (matching, graph, agents, routes)
│   │   └── alembic/          # Database migrations
│   └── web/                  # Next.js Frontend
├── data/
│   └── generator/            # Synthetic dataset generator for testing
├── docker-compose.yml        # Full infrastructure orchestration
├── .env                      # Environment variables configuration
└── README.md                 # Project documentation
```

## 🛠️ Quick Start

### 1. Prerequisites
Ensure you have Docker and Docker Compose installed on your system. 

### 2. Configuration
Copy the `.env.example` to `.env` (already done by default in this workspace). You can toggle between Razorpay Test and Live modes directly in the `.env` file:
```ini
RAZORPAY_MODE=test  # Or 'live'
RAZORPAY_TEST_KEY_ID=rzp_test_yourkey...
RAZORPAY_TEST_KEY_SECRET=your_test_secret...
OPENAI_API_KEY=sk-...
```

### 3. Run the Stack
Start all the services (PostgreSQL, Redis, Neo4j, Temporal, FastAPI, Next.js) using Docker Compose:

```bash
docker-compose up -d
```

### 4. Access the Applications
*   **Frontend Dashboard**: `http://localhost:3000`
*   **Backend API**: `http://localhost:8000`
*   **Temporal UI**: `http://localhost:8080`
*   **Neo4j Browser**: `http://localhost:7474` (Login: `neo4j` / `password123`)

## 🧠 Core Features

*   **Deterministic Route Math Engine**: Perfectly recreates Razorpay Route's split calculations, including PG fee deduction, GST logic, and handling post-payout refunds leading to negative balances.
*   **Multi-Stage Reconciliation Engine**: Reconciles transactions via exact matches, normalized reference matching, and rounding-tolerant financial amount matching.
*   **AI Financial Graph**: Translates raw transactional data into a fully connected graph database, empowering the AI to "walk the graph" to trace missing funds and explain discrepancies.
*   **Webhook Pipeline**: Listens to Razorpay webhooks (e.g., `payment.captured`, `settlement.processed`) and securely triggers Temporal workflows for background processing.
