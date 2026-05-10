course:
  title: System Design for Data Engineers
  year: 2026
  description: |
    A top-down system design course that explains how modern data platforms
    are architected. The course zooms from enterprise data platforms into
    individual infrastructure layers including ingestion, processing,
    storage, serving, and scaling.

  learning_model:
    - Top-down architecture approach
    - Zoom into each data platform layer
    - Explain system design concepts first
    - Show architecture patterns
    - Then introduce real-world tools

modules:

  - module_id: 1
    title: Modern Data Platform Overview
    goal: Understand the big picture of how enterprise data platforms work.

    topics:
      - Why organizations build data platforms
      - Data flow inside modern organizations
      - Operational vs analytical systems
      - Batch vs streaming systems (high level)
      - Core layers of a data platform

    architecture_patterns:
      - Enterprise data platform architecture
      - End-to-end data flow architecture

    architecture_example: |
      Data Sources
          ↓
      Ingestion Layer
          ↓
      Processing Layer
          ↓
      Storage Layer
          ↓
      Serving Layer
          ↓
      Analytics / ML

  - module_id: 2
    title: Data Ingestion Layer
    goal: Understand how data enters a data platform.

    topics:
      - Ingestion architectures
      - Event driven systems
      - Change data capture (CDC)
      - API based ingestion
      - File based ingestion
      - Event streaming fundamentals

    architecture_patterns:
      - Event streaming architecture
      - CDC pipeline architecture
      - Microservice event ingestion

    architecture_example: |
      Applications
      Databases
      External APIs
            ↓
        Ingestion Layer
            ↓
      Event Streaming System
            ↓
        Downstream Processing

    tools_examples:
      - Kafka
      - AWS Kinesis
      - Debezium
      - Log based CDC systems

  - module_id: 3
    title: Data Processing Layer
    goal: Understand distributed data processing systems.

    topics:
      - Batch processing fundamentals
      - Stream processing fundamentals
      - DAG execution models
      - Stateful processing
      - Windowing strategies
      - Exactly-once processing semantics

    architecture_patterns:
      - Batch processing pipelines
      - Stream processing pipelines
      - Hybrid batch + streaming systems

    architecture_example: |
      Streaming System
            ↓
      Processing Engine
            ↓
      Data Transformations
            ↓
      Processed Datasets

    tools_examples:
      - Apache Spark
      - Apache Flink
      - Apache Beam

  - module_id: 4
    title: Data Storage Layer
    goal: Understand storage architectures for analytics systems.

    topics:
      - Data lake architecture
      - Data warehouse architecture
      - Lakehouse architecture
      - Columnar storage
      - Data partitioning
      - Table formats for big data

    architecture_patterns:
      - Data lake architecture
      - Medallion architecture
      - Lakehouse architecture

    architecture_example: |
      Raw Data (Bronze)
            ↓
      Cleaned Data (Silver)
            ↓
      Aggregated Data (Gold)

    tools_examples:
      - Delta Lake
      - Apache Iceberg
      - Snowflake
      - BigQuery

  - module_id: 5
    title: Data Serving and Consumption
    goal: Understand how processed data is served to applications and analytics systems.

    topics:
      - Analytical query engines
      - OLAP systems
      - Feature stores
      - Real-time serving layers
      - BI dashboards
      - Data APIs

    architecture_patterns:
      - OLAP query architecture
      - Real time analytics architecture
      - Feature store architecture

    architecture_example: |
      Data Storage
            ↓
      Query Engine
            ↓
      Serving Layer
            ↓
      Dashboards / ML / APIs

    tools_examples:
      - Presto
      - Trino
      - Apache Superset
      - Feature stores

  - module_id: 6
    title: Scaling and Operating Data Platforms
    goal: Understand how large scale data platforms are operated in production.

    topics:
      - Data partitioning strategies
      - Sharding strategies
      - Handling data skew
      - Fault tolerance
      - Observability for pipelines
      - Cost optimization
      - Reprocessing and backfills

    architecture_patterns:
      - Fault tolerant pipeline architecture
      - Distributed data platform architecture
      - Observability architecture

    architecture_example: |
      Distributed Data Platform
            ↓
      Monitoring Systems
            ↓
      Alerting
            ↓
      Auto Scaling and Recovery

    tools_examples:
      - Prometheus
      - Grafana
      - Monte Carlo
      - Kubernetes

capstone_project:
  title: Design a Modern Enterprise Data Platform

  requirements:
    - Process terabytes of data per day
    - Support batch and streaming pipelines
    - Provide real-time analytics dashboards
    - Support machine learning pipelines
    - Handle failures and scaling

  outcome:
    - Students design a full data platform architecture
    - Document system design decisions
    - Present architecture diagrams