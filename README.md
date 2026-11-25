
![Kubernetes Namespace Health Plugin](assets/readme-banner.png)


## Live Demo

**Try the deployed application:**  
https://kubernetes-namespace-health.onrender.com

Upload a Kubernetes YAML, YML, or JSON manifest to analyze CPU and memory resource configurations directly in your browser.


# Kubernetes Namespace Health Plugin

## Project Overview

Kubernetes Namespace Health Plugin is a lightweight Python-based tool that analyzes local Kubernetes YAML and JSON configuration files through both a command-line interface (CLI) and a browser-based web interface.

It identifies Pods and Namespaces, extracts CPU and memory resource requests and limits, and highlights missing or explicitly zero resource configurations.

The tool helps developers identify potential configuration issues through structured reports without manually inspecting every manifest.

**Note:** This tool analyzes local configuration files only. It does not connect to a live Kubernetes cluster.

## Key Features

- **YAML & JSON Support:** Analyzes Kubernetes configuration files in both formats.
- **Pod & Namespace Detection:** Identifies supported Kubernetes resources.
- **Resource Analysis:** Extracts CPU and memory resource requests and limits.
- **Missing Configuration Detection:** Identifies resource fields that are not configured.
- **Zero Value Detection:** Separately identifies explicitly configured zero values.
- **Multiple File Support:** Supports analysis of configuration files.
- **Terminal Report:** Displays results in a structured and readable table.
- **Browser-Based Interface:** Upload and analyze configuration files through a web browser.
- **File Upload Validation:** Accepts supported YAML and JSON files.
- **Error Handling:** Handles missing files, invalid configurations, and parsing errors.
- **Offline Analysis:** Works with local configuration files without requiring cluster access.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| PyYAML | YAML file parsing |
| JSON | JSON configuration parsing |
| Argparse | Command-line argument handling |
| Tabulate | Structured terminal tables |
| Dataclasses | Structured data representation |
| Flask | Browser-based web application |
| HTML | Web page structure |
| CSS | Web interface styling |
| Gunicorn | WSGI web server |
| Docker | Application containerization |
| Git & GitHub | Version control and collaboration |
| Unittest | Automated testing |
| Coverage.py | Test coverage measurement |

## Project Architecture

The plugin supports two ways of analyzing Kubernetes configuration files:

1. **CLI Workflow:** The user provides a local YAML or JSON file through the terminal. The Python analyzer processes it and generates a structured terminal report.
2. **Web Workflow:** The user uploads a YAML or JSON file through the Flask browser interface. Flask passes the file to the Python analyzer and displays the results in a browser-based report.

![Project Architecture](assets/architecture.png)

## Installation

### Prerequisites

Make sure you have the following installed:

- Python 3
- Git
- Docker (for containerized deployment)

### 1. Clone the repository

```bash
git clone https://github.com/praneeth0209/-KUBECTL-NAMESPACE-HEALTH-PLUGIN-FOR-KUBERNETES.git

cd -KUBECTL-NAMESPACE-HEALTH-PLUGIN-FOR-KUBERNETES
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## CLI Usage

The tool accepts local Kubernetes YAML or JSON files as command-line arguments.

### Analyze a YAML file

```bash
python main.py samples/01_valid_pod.yaml
```

### Analyze a JSON file

```bash
python main.py samples/your-file.json
```

Replace the example filename with an actual JSON file in your repository.

### Display CLI Help

```bash
python main.py --help
```

## Web Application Usage

The project also provides a browser-based interface using Flask.

### Interface Technologies

The browser interface is built using HTML and CSS.

- **HTML:** Provides the structure of the interface, including file upload controls and report sections.
- **CSS:** Styles the interface and manages its visual layout and presentation.
- **Flask:** Handles file uploads and connects the web interface to the Python analysis engine.

### 1. Start the application

Make sure the virtual environment is activated and dependencies are installed.

```bash
python app.py
```

### 2. Open the application

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

### 3. Analyze a configuration file

1. Open the web application.
2. Select a supported YAML or JSON configuration file.
3. Upload the file.
4. View the generated Kubernetes resource analysis report.

The browser interface uses the existing Python analyzer to process the uploaded configuration file.

## Sample Output

The tool generates structured reports containing Kubernetes resource information and CPU/memory configurations.

![Kubernetes CLI Sample Output](assets/sample-output-fixed.png)

The report includes:

- Resource kind
- Namespace
- Resource name
- Container name
- CPU requests and limits
- Memory requests and limits

Missing configurations are displayed as `[NONE]`, while explicitly configured zero values are displayed as `0`.

## Testing

The project uses Python's `unittest` framework for automated testing.

Run the test suite using:

```bash
python -m unittest discover -s tests
```

To measure test coverage:

```bash
python -m coverage run -m unittest discover -s tests

python -m coverage report -m --include="main.py"
```

## Docker Usage

The application can run inside a Docker container, packaging the Python application and its dependencies.

### 1. Build the Docker Image

```bash
docker build -t kubernetes-namespace-health:0.3.1 .
```

### 2. Run the Container

```bash
docker run --rm -p 5001:5000 --name namespace-health kubernetes-namespace-health:0.3.1
```

### 3. Open the Web Application

Open the following address in your browser:

```text
http://localhost:5001
```

The container runs the Flask application using Gunicorn on port `5000`. The host port `5001` is mapped to the container port.

### Docker Notes

- The Docker image includes the Python application and its dependencies.
- Gunicorn runs the Flask application inside the container.
- Port `5001` on the host maps to port `5000` in the container.
- The browser interface accepts supported YAML and JSON configuration files.
- No live Kubernetes cluster connection is required.

## Future Improvements

- Support additional Kubernetes resource types.
- Improve report customization.
- Add more configuration validation rules.
- Enhance automated testing and reporting.
- Improve browser-based analysis and reporting.
- Explore additional deployment options.
