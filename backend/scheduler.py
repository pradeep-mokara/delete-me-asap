from .redis_client import redis_client
from .models import Job


def enqueue_job(job: Job):
    queue_key = f"queue:{job.target}"
    redis_client.rpush(queue_key, str(job.id))
    redis_client.set(f"job:{job.id}:status", "queued")
    redis_client.sadd(f"group:{job.app_version_id}", str(job.id))

