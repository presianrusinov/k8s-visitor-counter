Visitor Counter – Kubernetes Demo Application

This is a small demonstration project that deploys a simple Flask backend on a k3s Kubernetes cluster running in Hetzner Cloud. The application exposes a basic visit counter and is used to showcase the end-to-end workflow: writing a small service, containerizing it, publishing the image to GitHub Container Registry, and deploying it to Kubernetes using standard manifests.

The application provides two endpoints:

/ – basic health/landing response

/api/visits – returns a visit counter that increments on each request

The application code and Dockerfile are located in the backend/ directory.
The container image is built locally and pushed to GHCR as:

ghcr.io/presianrusinov/k8s-app-backend:latest

Kubernetes manifests are stored in the manifests/ directory and include the Deployment, Service, and Ingress configuration. The Ingress exposes the service publicly through the NGINX Ingress Controller.

Deployment is done with a simple:

kubectl apply -f manifests/

The application is publicly accessible at:

http://myk8s-presiyan.duckdns.org/

http://myk8s-presiyan.duckdns.org/api/visits

The project’s purpose is to provide a clean, working example of a Kubernetes setup with a real containerized service, an external container registry, and a publicly reachable endpoint. Additional improvements such as GitHub Actions automation, TLS certificates, and extended components can be added later as needed.
