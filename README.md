# Perfume AI Shop — Full-Stack DevOps Project

A full-stack e-commerce demo (React + Flask + PostgreSQL) with a lightweight, retrieval-based AI product assistant, deployed end-to-end on AWS using containers, Kubernetes (k3s), and full CI/CD automation.

## What this project demonstrates

A complete production-style pipeline — not just a working app, but the full path from `git push` to a live, containerized, Kubernetes-orchestrated deployment:
Git push → GitHub Actions (build + push images) → GHCR
│
Terraform (AWS EC2 + Elastic IP) ← Ansible ──────────┘
│
┌───────────┼─────────────────────┐
│ │ │
PostgreSQL k3s (Kubernetes) Nginx reverse proxy
(Podman) Backend + Frontend (frontend → backend)


## Stack

- **Frontend:** React (Vite) + Nginx, served as a static build with reverse-proxied API calls
- **Backend:** Flask + Gunicorn, SQLAlchemy ORM
- **Database:** PostgreSQL, running as a standalone Podman container (outside the cluster — a deliberate production-style choice: stateful workloads run separately from stateless app pods)
- **AI Assistant:** TF-IDF + cosine similarity (scikit-learn) — a lightweight, fully explainable retrieval-based product Q&A system, no external API required
- **Containers:** Podman, multi-stage builds
- **Orchestration:** k3s (lightweight Kubernetes), tuned for low-memory instances
- **IaC:** Terraform (EC2, Elastic IP, Security Group)
- **Configuration Management:** Ansible (Podman + k3s installation, PostgreSQL, Kubernetes manifests via Jinja2 templates)
- **CI/CD:** GitHub Actions → GitHub Container Registry (GHCR)

## Project structure
perfume-ai-shop/
├── backend/ # Flask API + AI assistant + SQLAlchemy models
├── frontend/ # React (Vite) app + Nginx reverse proxy config
├── terraform/ # AWS infrastructure (EC2, Elastic IP, Security Group)
├── ansible/
│ ├── roles/
│ │ ├── podman/ # Podman install (SPAL repo, systemd linger)
│ │ ├── k3s/ # Lightweight k3s install
│ │ └── deploy_app/ # PostgreSQL + K8s manifests (Jinja2 templated)
│ └── site.yml
└── .github/workflows/ # CI: build & push both images on every push


## Real problems solved along the way

This project involved genuine infrastructure debugging, not just following a tutorial:

- **Resource-constrained Kubernetes**: initial deployment on `t3.micro` (1GB RAM) caused k3s's control plane to become unresponsive under memory pressure. Diagnosed via CloudWatch metrics and systemd logs, resolved by disabling unnecessary k3s components (Traefik, ServiceLB, metrics-server) and upgrading to `t3.small`.
- **Stale kubeconfig certificates** after reinstalling k3s — fixed by ensuring Ansible regenerates the config rather than reusing a cached copy.
- **Dynamic internal IP injection**: rather than hardcoding a server's private IP (which changes on every `terraform destroy`/`apply`), the backend's database connection string is now templated with Ansible's `ansible_default_ipv4.address` fact.
- **Kubernetes NodePort range** wasn't open in the Security Group — traffic was silently dropped until the correct port range (30000–32767) was added.
- **Vite build-time environment variables**: the frontend's API URL needs to be baked in at build time, which required a `.env.production` file and careful Containerfile ordering.
- **Kubernetes image caching**: pods weren't picking up newly pushed `:latest` images due to the default `imagePullPolicy` — fixed by explicitly setting `imagePullPolicy: Always`.

## Running it yourself (high level)

```bash
# 1. Provision infrastructure
cd terraform && terraform apply -var="key_pair_name=<your-key>"

# 2. Configure the server and deploy everything
cd ../ansible && ansible-playbook -i inventory.ini site.yml

# 3. Access the app
# Frontend: http://<server-ip>:30080
# Backend API: http://<server-ip>:30500
```
