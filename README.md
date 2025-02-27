# MMOps Lifecycle

## Setup

1. **Activate Virtual Environment** (Windows):
   ```sh
   .\.venv\Scripts\activate
   ```

2. **Start MLflow Tracking Server**:
   ```sh
   mlflow server --backend-store-uri sqlite:///mlflow.db
   ```
   This command starts an MLflow server with SQLite as the backend store.

3. **Run FastAPI Server**:
   ```sh
   uvicorn serving:app --host 0.0.0.0 --port 8000 --reload
   ```
   This command starts the FastAPI service and makes it accessible on `http://0.0.0.0:8000`.

4. **Run PyLint for Code Quality Analysis**:
   ```sh
   pylint --score=yes src/ > test/test_report/pylint_report.txt
   ```
   This command runs PyLint on the `src/` directory and saves the report to `test/test_report/pylint_report.txt`.

5. **Run Tests with Coverage Report**:
   ```sh
   pytest --cov=. --cov-report=html
   ```
   This command runs all tests and generates a coverage report in an HTML format.

6. **Start Evidently AI UI**:
   ```sh
   evidently ui
   ```
   This command launches the Evidently AI dashboard to monitor data quality and drift.

## Additional Notes
- Ensure all dependencies are installed using:
  ```sh
  pip install -r requirements.txt
  ```
- Modify the `mlflow server` command if using a different backend (e.g., PostgreSQL, MySQL).
- Use `--host 127.0.0.1` instead of `0.0.0.0` for local access only.

---

## Troubleshooting
- If any command fails, check if the required dependencies are installed.
- Use `pip list` to verify installed packages.
- Run `deactivate` to exit the virtual environment if needed.

Happy Coding! 🚀

