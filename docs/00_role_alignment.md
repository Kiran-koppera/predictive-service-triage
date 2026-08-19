# Role Alignment Matrix: Tesla Service Analytics

| Tesla Job Requirement | Core Competency | Tech Stack & Methodology | Project Evidence Location |
| :--- | :--- | :--- | :--- |
| **Field Failure & Service Analytics** | Vehicle failure rate tracking, telemetry data extraction, and warranty triage. | SQL (window functions, aggregations, CTEs, star-schema modeling) | `sql/01_service_failure_queries.sql`<br>`data/` |
| **Predictive Triage & Machine Learning** | Ticket classification, failure prediction, and maintenance SLA prioritization. | Python (`pandas`, `scikit-learn`, `xgboost`) | `notebooks/01_eda.ipynb`<br>`notebooks/02_predictive_triage_model.ipynb` |
| **Data Pipelines & Workflow Automation** | Metric hygiene, data transformation, and automated processing. | Modular Python scripts, environment configs | `src/data_preprocessing.py`<br>`src/feature_engineering.py`<br>`config/` |
| **BI & Executive Dashboarding** | Interactive reporting, failure trend monitoring, and operational SLAs. | Power BI (`.pbix`), DAX metrics, data visualization | `powerbi/service_triage_dashboard.pbix`<br>`reports/` |
| **Reproducibility & MLOps Practices** | Version control, testing, automated builds, and documentation. | Git, `pytest`, `Makefile` targets | `tests/test_pipeline.py`<br>`Makefile`<br>`README.md` |
