# Production Architecture Diagram – Minimal Template

This document defines the mandatory minimal structure for production
architecture diagrams in Web, Mobile, and Software Systems.

This template defines how the system must be thought, not a specific
technology.

## Mandatory Blocks (All Systems)

Every production diagram must include at least the following blocks.

### 1. Client / External Actor

Represents:

- Browser
- Mobile App
- External Service
- Hardware device

Must show:

- Entry point
- Communication protocol (HTTP, HTTPS, gRPC, etc.)

### 2. Serving Layer (Traffic Entry)

Represents components that receive real traffic:

- Nginx
- Load Balancer
- API Gateway
- Reverse Proxy

Rules:

- This layer receives production traffic
- Must not point directly to a development workspace
- Must be clearly marked as Serving Layer

### 3. Application Runtime (Live Runtime)

Represents the application logic being executed:

- Gunicorn / WSGI
- Node.js runtime
- Backend services
- ROS2 nodes (if applicable)

Rules:

- Must be marked as LIVE
- Must be separated from repository and build context

### 4. Production Runtime Environment

Represents the environment actually being served:

- Dedicated production directory (e.g. project-prod/)
- Docker container / volume
- Kubernetes pod / namespace
- VM runtime environment

Rules:

- This is what the Serving Layer points to
- Must be clearly identified as PRODUCTION

### 5. Repository / Development Workspace

Represents:

- Git repository
- Source code
- Scripts
- Build artifacts (pre-deployment)

Rules:

- Must be separated from production runtime
- Must not receive production traffic

### 6. Deployment Flow

Represents how changes reach production:

- Sync
- Copy
- Build
- Image deploy
- Rollout

Rules:

- Must be shown using arrows
- Direction must be explicit
- Updated components must be clearly identifiable

## Mandatory Relationships

The diagram must explicitly show:

- Traffic flow: Client → Serving Layer → Runtime
- Deployment flow: Repository → Production Runtime
- Clear separation between development and production

## Minimal Production Diagram Structure (Required)

Every production diagram must include, at minimum, the following visual
structure.

Mandatory boxes:

- Client / External Actor
- Serving Layer
- Application Runtime
- Production Runtime Environment
- Repository / Development Workspace

Mandatory arrows:

Traffic flow (solid arrows):

- Client → Serving Layer
- Serving Layer → Application Runtime
- Application Runtime → Production Runtime Environment

Deployment flow (dashed arrows or labeled arrows):

- Repository / Development Workspace → Production Runtime Environment

Mandatory annotations:

- The Production Runtime Environment must be labeled as LIVE
- The Serving Layer must be labeled as SERVING TRAFFIC
- The Repository must be labeled as NOT SERVED
- The deployment arrow must be labeled (deploy / sync / rollout)

This structure must be visually represented using a diagramming tool.
Textual or ASCII diagrams are not acceptable.

## Validation Rules

A production diagram is invalid if:

- Runtime and repository are not clearly separated
- Deployment flow is missing or implicit
- The serving component is not identifiable
- Development and production concerns are mixed

## Storage and Reference

- Diagrams must be stored under doc/
- Allowed formats: PNG, SVG
- The README must reference the diagram explicitly

Example: **doc/system-prod-env.png**

![doc/system-prod-env.png](../diagrams/templates/system-prod-env.png)

## Guiding Principle

If deployment cannot be explained using the diagram,
the system is not production-ready.
