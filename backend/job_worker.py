import time
from backend.db import SessionLocal
from backend.redis_client import redis_client
from backend.models import Job
from backend.test_runner import run_appwright_test

# List all supported job target queues
SUPPORTED_TARGETS = ["dummy", "emulator", "device", "browserstack"]


def requeue_job(target: str, job_id: str):
    """
    Pushes the job ID back into the queue for the specified target (e.g., 'dummy', 'device')
    """
    queue_key = f"queue:{target}"
    redis_client.rpush(queue_key, job_id)
    print(f"Job {job_id} pushed back to queue: {queue_key}")


def get_next_job_id(timeout=5):
    """
    Blocks until a job is available in any supported target queue.
    Returns (job_id, target) or (None, None) on timeout.
    """
    queue_keys = [f"queue:{target}" for target in SUPPORTED_TARGETS]

    result = redis_client.blpop(queue_keys, timeout=timeout)
    if result:
        queue_name, job_id = result
        # queue_name looks like b'queue:dummy' — extract target
        # Decode if bytes, else leave as string
        if isinstance(queue_name, bytes):
            queue_name = queue_name.decode()
        if isinstance(job_id, bytes):
            job_id = job_id.decode()
        target = queue_name.split(":")[1]
        return job_id, target

    return None, None


def process_job(job_id: str):
    if not job_id:
        print("Invalid job_id received. Skipping.")
        return

    with SessionLocal() as db:
        job: Job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            print(f"Job {job_id} not found.")
            return

        print(f"Running test for job {job.id} at path {job.test_path}")
        try:
            result = run_appwright_test(job.test_path)
            if str(result).lower() == "success":
                job.status = "success"
                print(f"Job {job.id} marked as success")
            else:
                raise RuntimeError("Test failed")
        except Exception as e:
            job.retry_count += 1
            print(f"Error on job {job.id}: {str(e)} (Retry {job.retry_count}/{job.max_retries})")

            if job.retry_count < job.max_retries:
                job.status = "queued"
                requeue_job(job.target, str(job.id))
                print(f"Requeued job {job.id} for retry")
            else:
                job.status = "failed"
                print(f"Job {job.id} permanently failed after {job.retry_count} attempts and marked as failed")

        db.commit()
    return "Ok"

def run_worker_loop():
    print("Worker started. Listening for jobs...")
    while True:
        job_id, target = get_next_job_id()
        if job_id is not None:
            process_job(job_id)
        else:
            print("No jobs found")
            time.sleep(1)


if __name__ == "__main__":
    run_worker_loop()
