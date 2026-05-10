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

## ✅ Module 1: Core Banking Simulator
We have successfully implemented the source system simulator with a Transactional Outbox.

## ✅ Module 2: Unified Stream-Based Data Processing
We have implemented a unified ingestion layer using PySpark Structured Streaming that consumes both real-time Kafka events and batch files, landing them into a Delta Lake Bronze layer.

### 1. New Infrastructure
- **MinIO:** Object storage for the Medallion architecture (Bronze, Silver, Gold buckets).
- **Delta Lake:** Storage format for the Bronze layer to ensure ACID compliance and schema enforcement.

### 2. Running the Ingestion Job
1.  Ensure Docker cluster is running (includes MinIO):
    ```bash
    docker-compose up -d
    ```
2.  Run the Unified Bronze Ingestion job:
    ```bash
    export PYTHONPATH=$PYTHONPATH:.
    uv run python ingestion/app/bronze_ingestion.py
    ```

    ```
    $SPARK_HOME/sbin/start-connect-server.sh \
  --packages "org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.1,org.apache.hadoop:hadoop-aws:3.4.0,io.delta:delta-spark_4.1_2.13:4.1.0" \
  --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
  --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
  --conf "spark.hadoop.fs.s3a.endpoint=http://localhost:9000" \
  --conf "spark.hadoop.fs.s3a.access.key=admin" \
  --conf "spark.hadoop.fs.s3a.secret.key=password" \
  --conf "spark.hadoop.fs.s3a.path.style.access=true" \
  --conf "spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem"

   ```

### 3. Unified Flow
- **Real-time:** Automatically consumes from `customers`, `accounts`, `transactions`, and `balances` Kafka topics.
- **Batch:** Monitors `vol/batch_landing/`. Dropping a JSON file here will trigger automatic ingestion, normalization, and archiving.

## 📡 API Flow & Data Products
... (rest of table) ...

## 🔜 Next Steps: Module 3
We will move to **Lakehouse Storage with Iceberg** to implement the Silver and Gold layers of our Medallion architecture on MinIO.

---
**Lab Author:** [Your Name]  
**Course:** Data Engineering Design Patterns  
**Status:** Module 1 Complete (Transactional Outbox Edition) ✅
