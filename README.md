# Predictive Service Triage

A portfolio data-analytics project that predicts and triages vehicle service incidents from telemetry, warranty, and repair-order data, built end to end with SQL, Python, and Power BI to mirror the day-to-day toolkit of a Tesla Data/Service Analyst role.

## Why this project exists

This repo is a direct response to a real Tesla job posting, captured in docs/tesla_job_description.md. See docs/00_role_alignment.md for the full requirement-to-evidence mapping, following the flow: Tesla requirement, then Data Analytics, then SQL + Python + Power BI, then Project evidence.

## Project goal

Given raw vehicle telemetry, historical service tickets, and warranty/repair-order records, this project builds a pipeline that cleans and joins multi-source data in SQL, engineers features and trains a triage/severity model in Python, and surfaces the results (incident volume, predicted severity, root-cause drivers, and turnaround-time impact) in an interactive Power BI dashboard for a service-operations audience.

## Repository structure

README.md is this file. Makefile holds one-command setup, lint, test, and run entrypoints. docs/00_role_alignment.md maps Tesla requirements to project evidence, docs/tesla_job_description.md captures the source job description, and docs/LOG.md is the running build log. data/ holds raw and processed data (gitignored). notebooks/ holds exploratory analysis and modeling notebooks. sql/ holds schema, ingestion, and feature-engineering SQL. src/ is the importable Python package for ETL, features, model, and scoring. tests/ holds unit tests for src/. reports/ holds generated summary reports. config/ holds config files for paths, thresholds, and connection settings. powerbi/ holds the dashboard file and data-model documentation.

## Getting started

Run "make setup" to create a virtual environment and install dependencies, "make lint" to run linters, "make test" to run unit tests, and "make run" to run the end-to-end pipeline.

## Status

See docs/LOG.md for build history and next steps.
