
# Heart Disease Prediction System

An end-to-end machine learning pipeline and REST API for predicting heart disease risk. This project includes data preprocessing, model training, a containerized FastAPI application, Kubernetes deployment manifests, and a complete observability stack using Prometheus and Grafana.

## Project Structure
```text
heart-disease-prediction/
├── .github/workflows/main.yml       # CI/CD Pipeline
├── data/                            # Dataset and download scripts
├── deployment/                      # Kubernetes manifests (deployment, service), prometheus and grafna manifests
├── models/                          # Serialized ML models (.pkl)
├── notebooks/                       # EDA and Training notebooks
├── src/                             # FastAPI application and Prometheus config
├── test/                            # Pytest unit tests
├── screenshots/                     # Screenshots for Docker, Kubernetes, Prometheus, Grafana, Swagger, MLFlow
├── Dockerfile                       # Container definition
├── requirements.txt                 # Python dependencies
└── Final_Report.pdf                 # Detailed project documentation

```

## Prerequisites

Ensure you have the following installed and running on your machine:

* **Python 3.10+**
* **Docker Desktop** (Ensure Hardware Virtualization / WSL2 is enabled in your BIOS/Settings)
* **Kubernetes** (Enabled via Docker Desktop settings)
* **Git**

---

## Step-by-Step Reproduction Guide

### Step 1: Clone Repository and Initialize Virtual Environment

```bash
git clone https://github.com/2024ac05006/heart-disease-prediction.git
cd heart-disease-prediction

python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

---

### Step 2: Download Dataset and Run Tests

```bash
python data/download_data.py
pytest tests/
```

---

### Step 3: Deploy FastAPI Application to Kubernetes

#### Build Docker Image

```bash
docker build -t heart-disease-api:latest .
```

#### Configure Kubernetes Context

```bash
kubectl config use-context docker-desktop
```

#### Deploy Application

```bash
kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/service.yaml
```

#### Verify Deployment

```bash
kubectl get pods
```

---

### Step 4: Deploy Prometheus

Execute the following commands to configure cluster permissions, deploy Prometheus, and expose the Prometheus Expression Browser.

#### 1. Apply Cluster Role and Service Account Permissions

```bash
kubectl apply -f prometheus-roles.yaml
```

#### 2. Deploy the Prometheus ConfigMap

```bash
kubectl apply -f prometheus-config.yaml
```

#### 3. Deploy Prometheus Components

```bash
kubectl apply -f prometheus-deployment.yaml
```

#### 4. Access Prometheus Locally

```bash
kubectl port-forward svc/prometheus-service 9090:9090
```

Prometheus will be available at:

```
http://localhost:9090
```

---

### Step 5: Deploy Grafana

Execute the following commands to deploy Grafana, expose the service, and access the dashboard.

#### 1. Deploy the Grafana Application

```bash
kubectl apply -f grafana-deployment.yaml
```

#### 2. Expose the Grafana Service

```bash
kubectl apply -f grafana-service.yaml
```

#### 3. Access Grafana Locally

```bash
kubectl port-forward svc/grafana-service 3000:3000
```

Grafana Dashboard will be available at:

```
http://localhost:3000
```

---

### Experiment Tracking (MLflow)
This project uses MLflow to track model hyperparameters, metrics (Accuracy, F1-Score), and artifacts during the training phase. 

To view the experiment tracking dashboard locally:
1. Ensure your virtual environment is active and dependencies are installed.
2. Run the following command from the root directory of the project:
   ```bash
   mlflow ui

Open your browser and navigate to: http://localhost:5000/

---

## Cleanup

To stop all services and clean up your local environment, run the following commands:

**heart-disease-api service cleanup:**

```bash
kubectl delete -f deployment/service.yaml
kubectl delete -f deployment/deployment.yaml

```

**Grafana cleanup:**

```bash
# Delete the Grafana service mapping
kubectl delete -f grafana-service.yaml

# Delete the Grafana deployment container resource
kubectl delete -f grafana-deployment.yaml

```

**Prmoetheus:**

```bash
# Delete the Prometheus deployment and service components
kubectl delete -f prometheus-deployment.yaml

# Remove the Prometheus ConfigMap scraping configuration
kubectl delete -f prometheus-config.yaml

# Strip ClusterRoles and ServiceAccount RBAC permissions
kubectl delete -f prometheus-roles.yaml
```