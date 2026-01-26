Visitor Counter on Kubernetes (k3s)

1. How to access the app
Public URL:
http://myk8s-presiyan.duckdns.org

API endpoint:
http://myk8s-presiyan.duckdns.org/api/visits

Direct IP note (ingress needs Host header):
If you call the server IP directly you may get 404 from nginx, because ingress routing is based on the Host header.
Use:
curl -i -H "Host: myk8s-presiyan.duckdns.org" http://46.224.36.151/api/visits


2. What this is:
This repo is a small “production-like” demo that runs a visitor counter API on a single-node Kubernetes cluster (k3s). The app is containerized, exposed through ingress-nginx, and automated with a simple CI pipeline that builds and pushes images to GitHub Container Registry (GHCR).

The goal is to show a realistic end-to-end flow: code → container image → cluster rollout.

3. Architecture
The backend runs as a Kubernetes Deployment in the default namespace.
Traffic comes in through ingress-nginx and is routed to the backend Service.
The public endpoint uses a hostname (DuckDNS) pointing to the server public IP.

4. Tech stack
Kubernetes: k3s (single-node)
Ingress: ingress-nginx
TLS automation: cert-manager (if enabled on the cluster)
Container registry: GHCR
CI: GitHub Actions (build and push image)
Deployment: kubectl rollout (currently run from a trusted machine with cluster access)

5. How to deploy (manual, stable)
This is the simplest and most reliable way to deploy without dealing with SSH access from GitHub runners.

1) Build happens in CI and produces an image tag like sha-abcdef1
2) On your control node (or any machine that has kubectl access to the cluster), run:
kubectl -n default set image deploy/backend backend=ghcr.io/presianrusinov/k8s-app-backend:sha-abcdef1
kubectl -n default rollout status deploy/backend --timeout=180s
kubectl -n default get pods -l app=backend -o wide

CI pipeline
On every push to main, GitHub Actions builds the backend container and pushes it to GHCR.
The image tag is based on the short commit SHA, for example:
ghcr.io/presianrusinov/k8s-app-backend:sha-123abcd

The workflow uses a registry token stored as a GitHub Actions secret:
GHCR_PAT must have permission to write packages.

Backups
Cluster manifests are periodically exported under backups/k8s/YYYY-MM-DD.
This helps restore the current working state quickly if something gets changed by mistake.

Notes about access and secrets
Kubernetes access (kubeconfig) and SSH keys are not stored in the repository.
Secrets are stored in GitHub Actions Secrets and on the cluster where needed.

Troubleshooting
If you get 404 when calling the server IP directly, but the Host header works, that is expected with ingress.
Example:
curl -i -H "Host: myk8s-presiyan.duckdns.org" http://46.224.36.151/api/visits

If the domain does not resolve, it is a DNS propagation or resolver issue, not the app.
Check with:
dig +short myk8s-presiyan.duckdns.org A

Next steps (optional)
Add a CD approach that does not rely on public SSH from GitHub-hosted runners.
The clean options are either a self-hosted runner on the control node or a GitOps tool like Argo CD / Flux.

