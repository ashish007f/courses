# High-Scale Core Banking Data Platform (Lab)

This project is an enterprise-grade data platform lab focused on teaching data engineering design patterns, principles, and the Medallion architecture. It simulates a high-scale core banking system (similar to Thought Machine Vault) as its primary real-time data source.

## 🏗 Architecture & Principles

The platform is built with **SOLID principles** and a **modular, decoupled architecture**:

-   **API-First Design:** All data is generated through a simulated Banking API (FastAPI).
-   **Transactional Outbox Pattern:** Every business action (Customer creation, Account opening, Deposits) is saved to PostgreSQL and an `outbox` table in a single atomic transaction.
-   **CDC (Change Data Capture):** Debezium monitors the `outbox` table and asynchronously streams events to Kafka.
-   **Separation of Identity vs. State:** 
    -   `Account` represents the **Identity** (Static Metadata).
    -   `BalanceChangeEvent` represents the **State** (Dynamic Delta).
-   **Audit vs. Delta Patterns:**
    -   `transactions` topic: Full audit trail of every intent.
    -   `balances` topic: Delta events for streaming aggregations.

## 🛠 Technical Stack

-   **Broker:** Kafka 7.8.0 (KRaft mode)
-   **Persistence:** PostgreSQL 16 (Source of Truth)
-   **CDC:** Debezium Connect 2.5
-   **Registry:** Confluent Schema Registry
-   **UI:** Confluent Control Center
-   **Simulator:** Python 3.12+ (FastAPI, SQLAlchemy Async, Pydantic, Faker)
-   **Tooling:** `uv` for lightning-fast Python package management

## 🚀 Module 1: Core Banking Simulator (Current State)

We have successfully implemented the source system simulator with a Transactional Outbox.

### 1. Running the Infrastructure
1.  Ensure Docker Desktop is running.
2.  Start the cluster:
    ```bash
    docker-compose up -d
    ```
3.  Access Control Center at: `http://localhost:9021`

### 2. Registering the Debezium Connector
Once the infrastructure is up, register the connector to start streaming from the Outbox:
```bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d '{
  "name": "banking-outbox-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "user",
    "database.password": "password",
    "database.dbname": "banking_db",
    "topic.prefix": "simulator",
    "table.include.list": "public.outbox",
    "plugin.name": "pgoutput",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
    "transforms.outbox.table.field.event.id": "id",
    "transforms.outbox.table.field.event.key": "id",
    "transforms.outbox.route.topic.replacement": "${routedByValue}",
    "transforms.outbox.route.by.field": "topic",
    "transforms.outbox.table.field.event.payload": "payload",
    "transforms.outbox.table.expand.json.payload": "true",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false"
  }
}'
```

### 3. Running the Simulator
1.  Install dependencies:
    ```bash
    uv sync
    ```
2.  Start the Simulator API:
    ```bash
    uv run uvicorn simulator.app.main:app --host 0.0.0.0 --port 8000
    ```
3.  Start the Simulation Script (Generates continuous data):
    ```bash
    uv run simulator/run_simulation.py
    ```

## 📡 API Flow & Data Products

| Entity | Action | Kafka Topic | Description |
| :--- | :--- | :--- | :--- |
| **Customer** | `POST /customers/simulate` | `customers` | Generates a new unique person identity. |
| **Account** | `POST /accounts/{cust_id}` | `accounts` | Creates a bank account linked to a customer. |
| **Transaction** | `POST /transactions/deposit` | `transactions` | Immutable audit record of the deposit. |
| **Balance** | (Triggered by Transacton) | `balances` | **The Delta:** New balance and amount changed. |

## 🔜 Next Steps: Module 2

We will now move to **Unified Stream-Based Ingestion** using PySpark Structured Streaming to process these Kafka topics and land them into a Bronze layer.

---
**Lab Author:** [Your Name]  
**Course:** Data Engineering Design Patterns  
**Status:** Module 1 Complete (Transactional Outbox Edition) ✅
