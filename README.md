# inventory-multitenant-fastapi

REST API for multi-tenant inventory management with stock tracking, built with FastAPI and deployed on Google Cloud Run.

## Description

Inventory management system with full multi-tenant isolation. Each tenant manages their own product catalog with stock control and low-stock reporting. Tenant identification via X-Tenant-ID header. Built with Clean Architecture and SOLID principles.

## Live Demo

Swagger UI: https://inventory-multitenant-api-247946064488.us-central1.run.app/docs

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/products | Create new product for tenant |
| GET | /api/v1/products | List all products by tenant |
| PUT | /api/v1/products/{id}/stock | Update product stock |
| GET | /api/v1/reports/inventory | Low stock inventory report |

## Stack

- Python 3.11
- FastAPI
- Multi-tenant architecture (X-Tenant-ID header)
- Google Cloud Run
- Clean Architecture

---

Built by Edisson A.G.C. — AI Engineering Applied to Commerce — Bogotá, Colombia
