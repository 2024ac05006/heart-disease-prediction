
# Heart Disease Prediction System

An end-to-end machine learning pipeline and REST API for predicting heart disease risk. This project includes data preprocessing, model training, a containerized FastAPI application, Kubernetes deployment manifests, and a complete observability stack using Prometheus and Grafana.

## Project Structure
```text
heart-disease-prediction/
├── .github/workflows/main.yml       # CI/CD Pipeline
├── data/                            # Dataset and download scripts
├── deployment/                      # Kubernetes manifests (deployment, service)
├── models/                          # Serialized ML pipeline (.pkl)
├── notebooks/                       # EDA and Training notebooks
├── src/                             # FastAPI application and Prometheus config
├── test/                            # Pytest unit tests
├── screenshots/                     # Architecture and dashboard proofs
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

### Step 1: Clone the Repository

Clone this repository to your local machine and navigate into the project directory:

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd heart-disease-prediction

```

### Step 2: Local Environment Setup

To run the Jupyter notebooks or local tests, set up a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

```

### Step 3: Build the Docker Image

Build the isolated environment for the FastAPI application. This step proves the model serves correctly in an isolated container.

```bash
docker build -t heart-disease-api .

```

### Step 4: Deploy to Kubernetes

Deploy the containerized application and expose it via a LoadBalancer service to ensure stable routing on local machines.
*(Note: Make sure to enable Kubernets in Docker Desktop: Click on Gear icon, go to Kubernets and enable it. Click on Apply.).*

Run this command to force Kubernetes to use Docker Desktop:
```bash
kubectl config use-context docker-desktop
```
Apply the deployment and service configuration:
```bash
kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/service.yaml
```

*(Note: Wait about 15-30 seconds for the pods to initialize and the LoadBalancer to assign an IP).*

### Step 5: Launch the Observability Stack

Start Prometheus (for metrics scraping) and Grafana (for visualization) using Docker. Ensure you run this from the root directory so the path to `src/prometheus.yml` resolves correctly.

**Start Prometheus:**

```bash
docker run -d --name prometheus -p 9090:9090 -v ${PWD}/src/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

```

**Start Grafana:**

```bash
docker run -d --name grafana -p 3000:3000 grafana/grafana

```

---

## Accessing the System

Once all services are running, you can access the different components of the architecture via your web browser:

1. **FastAPI Swagger UI (Testing the Model):** [http://localhost:8080/docs](https://www.google.com/search?q=http://localhost:8080/docs)
*Use this interface to send test JSON payloads and receive heart disease predictions.*
2. **Raw API Metrics:** [http://localhost:8080/metrics](https://www.google.com/search?q=http://localhost:8080/metrics)
3. **Prometheus Server:** [http://localhost:9090](https://www.google.com/search?q=http://localhost:9090)
4. **Grafana Dashboards:** [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000)
*(Default login: admin / admin). Configure Prometheus as a data source using `http://host.docker.internal:9090` and build dashboards to track API Latency, Data Drift, and Model Health.*

### Experiment Tracking (MLflow)
This project uses MLflow to track model hyperparameters, metrics (Accuracy, F1-Score), and artifacts during the training phase. 

To view the experiment tracking dashboard locally:
1. Ensure your virtual environment is active and dependencies are installed.
2. Run the following command from the root directory of the project:
   ```bash
   mlflow ui

Open your browser and navigate to: http://127.0.0.1:5000

---

## Cleanup and Teardown

To stop all services and clean up your local environment, run the following commands:

**Delete Kubernetes resources:**

```bash
kubectl delete -f deployment/service.yaml
kubectl delete -f deployment/deployment.yaml

```

**Stop and remove monitoring containers:**

```bash
docker stop prometheus grafana
docker rm prometheus grafana

```