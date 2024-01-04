# We're using the latest version of Prefect with Python 3.10
FROM prefecthq/prefect:2-python3.10

# Add our requirements.txt file to the image and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

# Add our flow code to the image
COPY prefect-env .

# Run our flow script when the container starts
CMD ["python", "hello.py"]

#to run, use docker run -e PREFECT_API_URL='https://api.prefect.cloud/api/accounts/36b1fc96-bae4-401a-90a5-a4fa71d1f311/workspaces/ababaa12-1784-4fea-a877-b39d2aa8325f' -e PREFECT_API_KEY='your key' prefect-docker-guide-image

