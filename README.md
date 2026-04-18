Tienes razón. En texto plano sin formato markdown:

inventory-multitenant-fastapi

REST API for multi-tenant inventory management with stock tracking, built with FastAPI and deployed on Google Cloud Run.

Description

Inventory management system with full multi-tenant isolation. Each tenant manages their own product catalog with stock control and low-stock reporting. Tenant identification via X-Tenant-ID header. Built with Clean Architecture and SOLID principles.

Live Demo

Swagger UI: https://maiie-system-247946064488.us-central1.run.app/docs

Endpoints

POST /products — Create new product for tenant
GET /products — List all products by tenant
PUT /products/{id}/stock — Update product stock in/out
GET /reports/inventory — Low stock inventory report

Stack

Python 3.11, FastAPI, Multi-tenant X-Tenant-ID header, Google Cloud Run, Clean Architecture

Usage

Create a product:
curl -X POST https://maiie-system-247946064488.us-central1.run.app/products -H "Content-Type: application/json" -H "X-Tenant-ID: tenant-1" -d '{"name": "Product A", "sku": "SKU001", "price": 10.0, "stock": 100, "category": "electronics"}'

Get inventory report:
curl https://maiie-system-247946064488.us-central1.run.app/reports/inventory -H "X-Tenant-ID: tenant-1"

Built by Edisson A.G.C. — AI Engineering Applied to Commerce — Bogotá, Colombia
