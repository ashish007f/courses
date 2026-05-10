# Lab: Implementing a High-Scale Core Banking Data Platform

## Overview

This lab provides hands-on experience building an enterprise data platform based on architectural patterns from the course in data-engineering folder. We'll implement a simplified core banking system mimicking Thought Machine Vault 5+ as the real-time data source, focusing on data products and patterns rather than production-grade deployment. 
Code structure *MUST* be modular as well.New folder for each module.
Use *uv* for python project management.

**Key Focus Areas:**
- Data ingestion patterns (streaming and batch)
- Data modeling (Medallion architecture with Data Vault)
- Serving layers (OLTP, OLAP, vector search)
- Governance and orchestration
- Cloud-native storage patterns

**Time Estimate:** 4-6 hours (focused implementation)

## Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Basic knowledge of PySpark, Kafka, and SQL
- Access to cloud storage (AWS S3 or MinIO for local)

## Technical Stack

- **Streaming:** PySpark Structured Streaming, Kafka
- **OLTP:** PostgreSQL
- **OLAP:** ClickHouse
- **Vector Store:** Weaviate (open-source)
- **Storage:** MinIO, Apache Iceberg
- **Orchestration:** Apache Airflow
- **Governance:** OpenMetaData (open-source data catalog)
- **Core Banking Simulator:** Custom Python app mimicking Thought Machine Vault APIs

## Lab Modules

### Module 1: Core Banking Simulator Setup + Data Ingestion

**Objective:** Create a mock Thought Machine Vault system generating real-time banking events.

**Data Products:**
- Account creation/updates
- Balance changes
- Transaction events (deposits, withdrawals, transfers)

**Implementation:**
- Python FastAPI app with endpoints for account operations
- Simulated event generation using Faker library
- Kafka producer integration for real-time events

**Patterns:** Event-driven architecture, API-first design

### Module 2: Unified Stream-Based Data Procesing

**Objective:** Ingest both real-time events and batch files through the same PySpark streaming logic.

**Data Products:**
- Unified raw event stream (accounts, transactions, balances)
- Bounded batch file events normalized into the stream
- Initial data quality checks and common enrichment

**Implementation:**
- Kafka topics for different event types
- Batch file source read as a file stream
- PySpark Structured Streaming jobs for ingestion
- Schema validation, enrichment, and same downstream Bronze landing zone for both sources

**Patterns:** Kappa architecture, unified stream processing

### Module 3: Lakehouse Storage with Iceberg

**Objective:** Implement Medallion architecture on S3.

**Data Products:**
- Bronze: Raw ingested data from both real-time streams and batch file replay
- Silver: Cleaned and integrated data (Data Vault model)
- Gold: Business-ready datasets

**Implementation:**
- Apache Iceberg tables on MinIO
- PySpark jobs for data transformations using a single unified logic path for both stream and batch
- Time travel and schema evolution demos

**Patterns:** Lakehouse architecture, data vault modeling


### Module 4: OLTP Layer - Transactional Storage

**Objective:** Store current state in PostgreSQL for operational queries.

**Data Products:**
- Current account balances
- Customer profiles
- Active transaction logs

**Implementation:**
- PostgreSQL schema design
- PySpark jobs for reverse ETL to Postgres
- Connection pooling and indexing

**Patterns:** OLTP optimization, data synchronization

### Module 5: OLAP Layer - Analytical Storage

**Objective:** Build analytical datasets in ClickHouse for complex queries.

**Data Products:**
- Historical transaction aggregations
- Customer behavior analytics
- Fraud detection features

**Implementation:**
- ClickHouse table designs with appropriate engines
- Data pipeline from Kafka to ClickHouse via PySpark
- Materialized views for pre-computed aggregations

**Patterns:** Star schema, columnar storage optimization

### Module 6: Vector Store Integration

**Objective:** Enable semantic search on banking data.

**Data Products:**
- Transaction embeddings for anomaly detection
- Customer profile similarity matching

**Implementation:**
- Weaviate setup and schema definition
- Embedding generation using sentence transformers
- Vector indexing and similarity search APIs

**Patterns:** Vector databases, AI-powered analytics

*Module 4, 5, 6 are Data serving layers*

### Module 7: Orchestration with Airflow

**Objective:** Coordinate all data pipelines.

**Data Products:**
- Scheduled batch processes
- Pipeline monitoring dashboards

**Implementation:**
- Airflow DAGs for daily/ hourly jobs
- Dependencies between streaming and batch processes
- Error handling and retries

**Patterns:** Workflow orchestration, dependency management

### Module 8: Data Governance

**Objective:** Implement metadata management and lineage.

**Data Products:**
- Data catalog with business glossary
- Lineage tracking across pipelines

**Implementation:**
- OpenMetadat integration
- Metadata extraction from PySpark jobs
- Governance policies and access controls

**Patterns:** Data governance, metadata management

## Data Products and Patterns Summary

### Core Patterns Implemented
1. **Event-Driven Ingestion:** Real-time capture from banking simulator (API push pattern)
2. **Medallion Architecture:** Bronze → Silver → Gold data layers
3. **Polyglot Persistence:** OLTP (Postgres) + OLAP (ClickHouse) + Vector (Weaviate)
4. **Lakehouse Foundation:** Iceberg on MinIO for unified analytics
5. **Data Vault Modeling:** Business key management in Silver layer

### Key Data Products
- **Real-Time Dashboard:** Current balances and recent transactions
- **Fraud Detection Model:** Aggregated velocity checks
- **Customer 360 View:** Unified customer profile across systems
- **Regulatory Reporting:** Historical audit trails with PIT recovery

## Success Criteria

- End-to-end data flow from banking simulator to all storage layers
- Sub-second query performance on OLAP datasets
- Real-time updates reflected in OLTP within 5 seconds
- Vector similarity search working for transaction patterns
- Complete pipeline orchestration with Airflow
- Data lineage visible in governance tool


---

**Lab Author:** [Your Name]  
**Based on Course:** Enterprise Data Platform Architectural Patterns  
**Experience Level:** Intermediate (Tech Lead)  
**Status:** Lab Blueprint v1.0