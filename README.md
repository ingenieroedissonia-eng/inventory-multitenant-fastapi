auth-multirole-fastapi
REST API for multi-role authentication with JWT, built with FastAPI and deployed on Google Cloud Run.
Description
Authentication system with role-based access control (RBAC). Supports admin, manager and viewer roles with granular permission matrix. Built with Clean Architecture and SOLID principles.
Live Demo
Swagger UI: https://maiie-system-247946064488.us-central1.run.app/docs
Endpoints
MethodEndpointDescriptionPOST/auth/registerRegister new userPOST/auth/loginLogin and get JWT tokenGET/auth/meGet current user infoGET/auth/check-permissionVerify role permission
Stack

Python 3.11
FastAPI
JWT + bcrypt
Google Cloud Run
Clean Architecture

Usage
Login and get token
curl -X POST https://maiie-system-247946064488.us-central1.run.app/auth/login -H "Content-Type: application/json" -d '{"email": "admin@example.com", "password": "secret"}'
Check permission
curl https://maiie-system-247946064488.us-central1.run.app/auth/check-permission -H "Authorization: Bearer token"

Built by Edisson A.G.C. — AI Engineering Applied to Commerce — Bogotá, Colombia
