import requests
from .config import API_BASE_URL


def submit_job(org_id, app_version_id, test_path, target, priority, max_retries):
    payload = {
        "org_id": org_id,
        "app_version_id": app_version_id,
        "test_path": test_path,
        "target": target,
        "priority": priority,
        "max_retries": max_retries,
    }

    res = requests.post(f"{API_BASE_URL}/jobs/submit", json=payload)
    res.raise_for_status()
    return res.json()["job_id"]


def get_job_status(job_id):
    res = requests.get(f"{API_BASE_URL}/jobs/{job_id}/status")
    res.raise_for_status()
    return res.json()["status"]

