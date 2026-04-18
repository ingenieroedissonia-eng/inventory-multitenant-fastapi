# auth-multirole-fastapi

REST API for multi-role authentication with JWT, built with FastAPI and deployed on Google Cloud Run.

## Description

Authentication system with role-based access control (RBAC). Supports admin, manager and viewer roles with granular permission matrix. Built with Clean Architecture and SOLID principles.

## Live Demo

Swagger UI: https://maiie-system-247946064488.us-central1.run.app/docs

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login and get JWT token |
| GET | /auth/me | Get current user info |
| GET | /auth/check-permission | Verify role permission |

## Stack

- Python 3.11
- FastAPI
- JWT + bcrypt
- Google Cloud Run
- Clean Architecture

---

Built by Edisson A.G.C. — AI Engineering Applied to Commerce — Bogotá, Colombia
