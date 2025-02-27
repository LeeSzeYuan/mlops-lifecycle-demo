# **Question 1**

## **Assumptions**

1.  **Unstructured data** refers to data in the form of images or video.
2.  **Open source/free tools** will be used for this proposal:
    -   **MLflow**:
        -   Experiment Tracking
        -   Model Versioning
        -   Model Registry
        -   Model Serving (Deployment handled by another team)
    -   **DVC**:
        -   Data Versioning
        -   ML Pipeline Management
    -   **Alibaba Cloud OSS**:
        -   Blob storage for datasets and model artifacts.
    -   **Alibaba Cloud RDS**:
        -   Backend database for MLflow.

----------

## **SOP for CI/CD**

### **Model Development (New Project)**

#### 1. **Code Repository Setup**

-   Use Git for version control with a clear project structure:
    
    ```
    data/               # DVC-tracked datasets
    └── processed/      # Processed/cleaned datasets
    models/             # MLflow-tracked model artifacts
    tests/              # Unit test cases
    notebooks/          # Jupyter Notebooks for development and experimentation
    src/                # Modularized scripts for data processing, training, and evaluation pipelines
    README.md           # High-level project documentation
    
    ```
    
-   Ensure `.gitignore` includes large data files managed by DVC.

----------

#### 2. **Git Strategies**

-   **Branching Strategy**:
    
    -   `main`: Stable & production-ready models and scripts.
        -   Changes only via Pull Requests from the `develop` branch.
        -   No direct commits from employees’ local repos.
    -   `develop`: Active development branch.
        -   Changes only via Pull Requests from `feature/*`, `hotfix/*`, and `bugfix/*` branches.
        -   No direct commits from employees’ local repos.
    -   `feature/*`: Branch for experimental/in-development features.
        -   Create a new branch for each feature or task.
        -   Naming convention: `feature/<task-name>`.
        -   Merge back into `develop` after feature completion.
    -   `hotfix/*`: Urgent fixes for production.
    -   `bugfix/*`: Non-urgent bug fixes.
-   **Pull Requests**:
    
    -   Must have at least **1 reviewer approval**.
    -   Must include links to work items/tickets.
    -   Should trigger automated Python linters (e.g. Pylint) to check for:
        -   Code quality.
        -   Code smells (dead code, duplicate code, etc.).

----------

#### 3. **Environment**

-   Specific versions of dependencies listed in:
    -   **Conda**: `environment.yml`
    -   **pip**: `requirements.txt`

----------

#### 4. **MLflow & DVC Setup**

-   **Install MLflow**:
    
    ```bash
    pip install mlflow
    ```
    
-   Configure **MLflow backend store** and **artifact store**:
    
    Backend store (parameters, metrics, model registry):
    
	```plaintext
    mysql+pymysql://user:password@rds_instance:3306/mlflow
    ```

    Model Artifact Store:
    
    ```plaintext
    oss://mlflow-artifacts/
    ```
    
-   Install **DVC**:
    
    ```bash
    pip install dvc
    ```
    
-   **Initialize Git** in the project directory (If haven't):
    
    ```bash
    git init
    git add .dvc               # Add DVC initialization files to Git
    git commit -m "Initialize DVC in the repo"  
    ```

-   **Initialize DVC** in the project directory:
    
    ```bash
    dvc init
    ```

-   Configure **remote storage** for datasets:
    
    ```bash
    dvc remote add -d alioss oss://bucket/path -a access_key -s secret_key
    ```

----------

#### 5. **Data Versioning with DVC**

-   Add **new dataset** to DVC tracking (first-time setup):

    ```bash
    dvc add data/dataset.csv
    ```

- **Commit the changes** to Git and DVC:

    ```bash
    git add .  # Adds DVC files and changes to Git
    git commit -m "Add new dataset for versioning"
    ```

- Push the dataset to **remote storage** (e.g. S3, ADLS etc):

    ```bash
    dvc remote add -d alioss oss://mybucket/dvcstore -a <access_key> -s <secret_key>
    dvc push
    ```

- **Store metadata** in Git:
  - DVC automatically tracks metadata in `.dvc` files.

    ```bash
    git add dataset.csv.dvc
    git commit -m "Track dataset versioning"
    ```

- Now, the dataset is versioned, and you can access the metadata by checking the `.dvc` file in the Git repository.

- To pull latest changes from Repo and DVC Remote, use `git pull` followed by ``dvc pull`
    ```bash
    git pull
    dvc pull <optional-data-path>
    ```

---

#### **6. Experiment Tracking with MLflow**

- Start an **experiment**:

    ```python
    mlflow.start_run()
    ```

- **Log parameters** used in model experimentation:

    ```python
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    ```

- **Log performance metrics**:

    ```python
    mlflow.log_metric("accuracy", accuracy)
    ```

- **Log the model**:

    ```python
    mlflow.sklearn.log_model(model, "model")
    ```

- Register the model in the **Model Registry**:

    ```python
    model_name = "RandomForestModel"
    mlflow.register_model("runs:/{}/model".format(mlflow.active_run().info.run_id), model_name)
    ```
---

#### **7. Converting Jupyter Notebooks (`.ipynb`) into Modularized Python Scripts for ML Pipelines**

- After Data Scientists develop the basic logic and models in Jupyter notebook, we should convert it into reusable and modular scripts
    - which then we can implement in ML pipelines

- Modularise the scripts into **categories**:
  - Data Ingestion
  - Data Cleaning & Transformation
  - Hyperparameter Tuning
  - Model Training
  - Model Testing
  - Model Selection

- If possible, we can **Develop a Python package** with commonly-used functions/scripts that can be **shared across project teams**.

- **Example**: Convert a commonly-used Data Quality Check script into a function for use in a pipeline:

  - **Missing Data**: Check for missing or null values.
  - **Duplicates**: Check for duplicate rows that may distort analysis.
  - **Inconsistent Data**: Identify inconsistencies or invalid values.
  - **Business Logic Validation**: Ensure data conforms to business logic.


---

#### **8. Converting to ML Pipeline**

- **A simple `illutrationCode/mlPipeline/dvc.yaml` file** illustrating how each stage of the pipeline communicates with each other:

    ```bash
    dvc repro
    ```

---

#### **9. Set up Unit Testing & Integration**

- **Store test cases** in a dedicated `tests/` directory in the repository.
- **Unit Testing**: Use the `pytest` library.
  - Testing individual components such as data processing and training functions to ensure these functions work properly.

    ```plaintext
    illustrationCode/tests/testPipeline.py
    ```

  - Testing model input and output verification.

- **Integration Testing**:
  - Use **Docker** to run integration tests.

---

#### **10. Set up Monitoring & Alerting**

- **Model Performance Metrics** to track:
    - Accuracy
    - Precision and Recall
    - Root Mean Squared Error (RMSE)

- **Operational Metrics** to track:
    - Deployment Time
    - Latency
        - Time taken for the model to generate predictions after receiving input.
    - Uptime percentage
    - Resource Usage (CPU, Memory, etc.)


- **Tools and Techniques for Monitoring**

    1. **A/B Testing**:
        - Direct a fraction of `user traffic` to the new model and the remaining fraction to the existing model.
        - Record and log **performance metrics** (e.g. accuracy, latency, etc.) of both models.
        - Perform statistical comparison.
            ```plaintext
            illustrationCode/tests/abtesting.py
            ```

    2. **Canary Releases**:
        - Release the new model to a `small group of users`.
        - Record and log **performance metrics** of new models.
        - Perform **statistical comparison** with existing models.


-  **Model Performance Metrics Monitoring**

    1. **`Prometheus` with `Grafana`**: For collecting and visualizing model metrics.

    2. Use **`Prometheus`** to collect metrics from model, data pipeline, and deployment environment.

    3. Use **`Grafana`** to create dashboards that show live performance data for quick troubleshooting.

    4. Set up alerts in **`Prometheus`** or other monitoring tools to notify teams of degraded performance or failures.
        - Use the performance of the model during training and validation as **performance baseline/alert threshold**:
            - Accuracy drops below the threshold.
            - Latency exceeds expected limits.
            - High resource usage (CPU, memory).

    5. **Example**:
        - `Prometheus` collects model performance metrics from your app.
        - Grafana displays the metrics in dashboards (e.g. accuracy, response time, CPU/memory usage).
        - If the metrics fall below a certain threshold, `Prometheus` triggers an alert (e.g. if accuracy drops below 80%).


- **Data Drift Detection Monitoring**

    1. Test whether new input data shares similar statistical properties to the training data.
    2. Check for **performance degradation**.
    3. A simple detection method is to compare the **mean and variance** of features.
    4. Store **drift detection results** in a monitoring dashboard (e.g. `Grafana`).
    5. Trigger alerts when drift is detected to notify the team for further investigation or model retraining.
    6. Integrate the above process into the ML model deployment pipeline.
    7. **Example**:
        ```plaintext
        illustrationCode/tests/driftDetection.py
        ```

> **Evidently AI**: Offers monitoring dashboards to visualize data drift.


- **Action Upon Alerts**

1. Create an automated pipeline that retrains the model if significant drift is detected.
2. Rollback the model if performance degradation crosses the threshold value.


---

- **Resource Usage Monitoring**

---


### **Other SOPs**

1. All cloud infrastructure must be provisioned using **IaC (Infrastructure as Code)** tools, e.g. **`Terraform`**.
2. **Data Labeling**:
   - Clear data labeling guidelines.
   - Continuously monitor the labeling process.
3. Enable **parallel training experiments**.
4. Enable the use of **GPU** for training models.
5. Set up **naming conventions** for models, datasets, and experiments:
   - Follow the **`PEP 8`** style guide for Python code.

