Visitor Counter on k3s
This repository contains a lightweight production-style setup for a visitor counter application running on a single-node Kubernetes cluster. The project focuses on a clean infrastructure workflow, including containerization, automated builds, and ingress management.

Accessing the Application
The application is deployed and reachable at:

Public URL: http://myk8s-presiyan.duckdns.org

API Endpoint: http://myk8s-presiyan.duckdns.org/api/visits

Direct IP Access: The Ingress controller is configured for host-based routing. If you access the server via its public IP (46.224.36.151) directly, you will receive a 404. To verify the service via IP, use a custom Host header:

curl -i -H "Host: myk8s-presiyan.duckdns.org" http://46.224.36.151/api/visits

Note: In case of DuckDNS resolution delays, the IP + Host header method is the most reliable way to check the status.

Project Structure
This setup demonstrates a standard end-to-end deployment flow:

Backend: A containerized service running as a Kubernetes Deployment.

Networking: Internal communication via ClusterIP and external routing via ingress-nginx.

Environment: Hosted on Ubuntu 22.04.5 LTS using k3s (v1.33.6).

Tech Stack
Orchestration: k3s (Lightweight Kubernetes)

Ingress: ingress-nginx

Container Registry: GitHub Container Registry (GHCR)

CI Pipeline: GitHub Actions

Host OS: Ubuntu 22.04.5 LTS

Operational Notes: OS & Kernel Stability
The host system is deliberately kept on its current kernel and package versions to ensure cluster stability. In a Kubernetes environment, spontaneous OS updates (especially kernel-related) can lead to:

Networking issues: Breaking CNI (Container Network Interface) or iptables rules.

Container Runtime mismatches: Potential conflicts between containerd and updated system libraries.

Storage driver instability: Risks of breaking local path provisioning.

System-level updates are performed only during scheduled maintenance windows after compatibility testing to avoid unexpected downtime.

CI/CD Workflow
I've implemented a simple but secure CI/CD logic:

Build & Push: On every push to main, GitHub Actions builds the image, tags it with the specific commit SHA (e.g., sha-123abcd), and pushes it to GHCR.

Deployment: The rollout to the cluster is handled manually. This ensures that cluster credentials stay on the local trusted node and are not exposed to the GitHub environment.

To update the application version: kubectl -n default set image deploy/backend backend=ghcr.io/presianrusinov/k8s-app-backend:sha-abcdef1

Security and Backups
Infrastructure as Code: Kubernetes manifests are periodically backed up under backups/k8s/ to maintain a history of the cluster state.

Secrets Management: Sensitive information and kubeconfig files are kept strictly on the master node and are never committed to the repository.
