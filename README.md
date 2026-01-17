
## Docker

### What is docker?
- docker gives you isolated container from the rest of the system
- Create docker image: loading image of "hello world":
- Everytime we run a docker container, we create a container from a doctor image, which contain everything a container has--> ```bash docker run -it ubuntu``` --> we use docker image to create a container --> container is **stateless** - it doesn't save 
- ubuntu is a docker image; ```bash python:3.13.11-slim``` is also an image
- so how do we install python? -- later
- ```bash rm -rf``` - delete everything

### How to map a python script (in my local drive) to a docker container
- Use the `-v` flag to mount (map) your local folder into the container
- Syntax: `docker run -it -v $(pwd)/test:/app/test python:3.13.11-slim`
- **Left side** (`$(pwd)/test`) = your local folder path
- **Right side** (`/app/test`) = where it appears inside the container
- `/app` is just a convention (could be `/workspace`, `/src`, etc.)
- Files sync automatically between local machine and container

### Docker Volume Mapping Example
```bash
docker run -it \
  --rm \
  -v $(pwd)/test:/app/test \
  --entrypoint=bash \
  python:3.13.11-slim
```

### Container Statelessness
- Containers don't save changes (they're temporary/stateless)
- Each `docker run` creates a fresh container from the image
- Solution: Use `-v` (volume mount) to sync files with local machine
- Without `-v`: changes are lost when container stops
- With `-v`: changes save to your local folder

----

## Data Pipeline & Parquet

### What is a Data Pipeline?
- A pipeline is a **series of steps** that process data
- Input → Transform → Output
- Example: Read data → Add columns → Save to file

### What is Parquet?
- **Parquet** is a binary file format for efficient data storage
- Advantages over CSV:
  - Smaller file size (compressed)
  - Faster to read/write
  - Better for large datasets
- Use cases: Data warehouses, big data processing

### Mini Pipeline Example

**File: [`pipeline.py`]

```python
import sys
import pandas as pd

# Get month from command line argument
print(sys.argv)
month = sys.argv[1]
print(f"Month is {month}")

# Create sample DataFrame
df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
print(df.head())

# Add month column
df['month'] = month

# Save to Parquet format
df.to_parquet(f"output_day_{sys.argv[1]}.parquet")
```

### How to Run the Pipeline

**Using Python directly:**
```bash
python pipeline.py 12
```

Output:
```
['pipeline.py', '12']
Month is 12
   day  num_passengers
0    1               3
1    2               4
```

This creates a file: `output_day_12.parquet`

---

## UV - handles virtual environment automatically

### What is UV?
- **UV** is a fast Python package manager and script runner
- Alternative to `pip` and `python` commands
- Faster, more efficient, manages dependencies better

### Installation
```bash
pip install uv
```

### Using UV to Run Scripts

**Use:**
```bash
uv run python pipeline.py 10
```

### UV Features
- Automatically manages Python versions
- Caches dependencies for faster runs
- Handles virtual environments automatically
- Works cross-platform (Windows, Mac, Linux)

### When to Use UV
- Running Python scripts (faster than `python`)
- Managing project dependencies
- Working in Docker (UV is lighter weight)

## Data pipeline - we will create a minipipeline, which we will be using to dockerise








-------------- Python Related Learning -----------------------------------

## Python Command-Line Arguments (sys.argv)

### Understanding sys.argv
- `sys.argv` is a **list** that contains all command-line arguments
- `sys.argv[0]` = script name
- `sys.argv[1]` = first argument
- `sys.argv[2]` = second argument, etc.

### Example
```python
import sys
print(sys.argv)
month = sys.argv[1]
print(f"Month is {month}")
```

Running:
```bash
python script.py 12
```
Output:
```
['script.py', '12']
Month is 12
```

### Important Notes
- All arguments are **strings** (text)
- Use `int()` to convert to numbers: `int(sys.argv[1])`
- Always check if argument exists before using it

---

## Creating & Running Docker Images with Dockerfile

### What is a Dockerfile?
- A **Dockerfile** is a text file with instructions to **build a Docker image**
- It's like a recipe: "start with this base image, install this, copy files, run this command"
- Image = Blueprint (reusable)
- Container = Instance (running copy of the image)

### Creating a Dockerfile

**File: `Dockerfile` (no extension)**

```dockerfile
FROM python:3.13.11-slim
RUN pip install pandas pyarrow

WORKDIR /app 

COPY pipeline.py pipeline.py

ENTRYPOINT ["python", "pipeline.py"]
```

### Dockerfile Commands Explained

| Command | Purpose |
|---------|---------|
| `FROM` | Base image to start from |
| `RUN` | Execute command during build (install packages) |
| `WORKDIR` | Set working directory inside container |
| `COPY` | Copy files from local machine to container |
| `ENTRYPOINT` | Default command to run when container starts |
| `CMD` | Default arguments (can be overridden) |
| `EXPOSE` | Document which ports the app uses |
| `ENV` | Set environment variables |

### Building a Docker Image

**From the folder with your Dockerfile:**

```bash
cd /workspaces/de-2026-docker/pipeline
docker build -t test:pandas .
```

Breakdown:
- `docker build` = Build an image from Dockerfile
- `-t test:pandas` = Tag the image as `test:pandas` (name:version)
- `.` = Current directory (where Dockerfile is)

---

## Running Docker Images

### Run a container from your image

```bash
docker run test:pandas 12
```

This runs the `test:pandas` image and passes `12` as an argument to `pipeline.py`.

Output:
```
['pipeline.py', '12']
Month is 12
   day  num_passengers
0    1               3
1    2               4
output_day_12.parquet
```

---

### Common Docker Run Options

```bash
docker run -it test:pandas 12
```

| Flag | Meaning |
|------|---------|
| `-it` | Interactive terminal (see output) |
| `-v` | Volume mount (sync local folder) |
| `-e` | Environment variable |
| `-p` | Port mapping |
| `--rm` | Remove container after it exits |

### Example: Run and save output to local folder

```bash
docker run -it -v $(pwd):/app test:pandas 12
```

This:
1. Runs the pipeline with argument `12`
2. Syncs the `/app` folder inside container with your local folder
3. The parquet file appears on your local machine

---

### Mapping vs Copying in Dockerfile

**Mapping (Development):**
```bash
docker run -it -v $(pwd)/pipeline:/app python:3.13.11-slim python /app/pipeline.py 12
```
- Live changes, no rebuild needed
- Good for testing

**Copying (Production):**
```dockerfile
COPY pipeline.py pipeline.py
```
- Changes baked into image
- Must rebuild to update
- Good for deployment

---

## Pipeline Workflow

```
1. Create Dockerfile
   ↓
2. Build image: docker build -t test:pandas .
   ↓
3. Run container: docker run test:pandas 12
   ↓
4. Output: output_day_12.parquet
```

---




