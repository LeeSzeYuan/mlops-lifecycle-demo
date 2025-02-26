# mlops-lifecycle-demo
To demo mlops lifecycle in a AI/ML project

To initialize **Git** and **DVC** for managing **data versioning** and **pipeline management**, follow these steps:

---

## **🚀 Step 1: Initialize Git & DVC**
### **1️⃣ Initialize Git**
First, create a new repo (or navigate to an existing one):

```bash
git init  # Initialize Git repository
git add .  # Stage all files
git commit -m "Initial commit"
```

---

### **2️⃣ Initialize DVC**
Run:

```bash
dvc init  # Initialize DVC
git commit -m "Initialize DVC"
```

DVC will create a `.dvc/` directory to manage configurations.

---

## **🗄 Step 2: Set Up Data Versioning**
### **3️⃣ Add Data to DVC**
For example, if your data is in the `data/` folder:

```bash
dvc add data/
```

This will:
✅ Create a **`data.dvc`** file (metadata about the data).  
✅ Move `data/` to `.gitignore` (Git won't track it, only DVC does).  

Commit the changes:

```bash
git add data.dvc .gitignore
git commit -m "Track data with DVC"
```

---

### **4️⃣ Set Up DVC Remote Storage (Optional)**
DVC needs a remote storage location to version large datasets. You can use **Google Drive, S3, Azure, etc.**  
For example, to set up **Google Drive**:

```bash
dvc remote add myremote gdrive://your-folder-id
dvc push  # Upload data to remote storage
```

Commit the configuration:

```bash
git commit .dvc/config -m "Configure DVC remote storage"
```

---

## **🛠 Step 3: Set Up DVC Pipeline**
### **5️⃣ Create a DVC Pipeline**
Define your **stages** in `dvc.yaml`. Example:

```yaml
stages:
  preprocess:
    cmd: python src/preprocess.py data/raw.parquet
    deps:
      - src/preprocess.py
      - data/raw.parquet
    outs:
      - data/processed.parquet

  train:
    cmd: python src/train.py data/processed.parquet
    deps:
      - src/train.py
      - data/processed.parquet
    outs:
      - models/model.pkl
```

Commit this:

```bash
git add dvc.yaml
git commit -m "Add DVC pipeline"
```

---

### **6️⃣ Run Pipeline & Track Changes**
Run the pipeline:

```bash
dvc repro
```

Push outputs (data & models) to remote storage:

```bash
dvc push
```

---

## **🔄 Step 4: How to Pull & Use the Data**
If cloning on a new machine:

```bash
git clone <repo_url>
dvc pull  # Download the latest data & models
```

---

### **✅ Summary**
| Step | Command |
|------|---------|
| Initialize Git | `git init && git commit -m "Initial commit"` |
| Initialize DVC | `dvc init && git commit -m "Initialize DVC"` |
| Track Data | `dvc add data/ && git commit -m "Track data with DVC"` |
| Set Up Remote | `dvc remote add myremote gdrive://your-folder-id && dvc push` |
| Define Pipeline | Edit `dvc.yaml`, then `git commit -m "Add DVC pipeline"` |
| Run Pipeline | `dvc repro && dvc push` |
| Pull Data (New Machine) | `git clone <repo_url> && dvc pull` |

---

Let me know if you need adjustments! 🚀

.\.venv\Scripts\activate

uvicorn serving:app --host 0.0.0.0 --port 8000 --reload
curl -X 'POST' 'http://0.0.0.0:8000/predict' -H 'Content-Type: application/json' -d '{"PULocationID": "138", "DOLocationID": "33", "trip_distance": 9.76}'


pylint --score=yes src/ > test/test_report/pylint_report.txt

pytest --cov=. --cov-report=html
xdg-open htmlcov/index.html  # Linux
open htmlcov/index.html      # macOS
start htmlcov\index.html