import typer
import time
from .api import submit_job, get_job_status

app = typer.Typer()


@app.command()
def submit(
    org_id: str = typer.Option(..., help="Organization ID"),
    app_version_id: str = typer.Option(..., help="App version ID"),
    test_path: str = typer.Option(..., help="Path to test file"),
    target: str = typer.Option(..., help="Target environment (emulator, device, etc)"),
    priority: int = typer.Option(0, help="Optional priority (higher = sooner)"),
    max_retries: int = typer.Option(0, help="Optional retries (default is zero)")
):
    """Submit a test job."""
    job_id = submit_job(org_id, app_version_id, test_path, target, priority, max_retries)
    typer.echo(f"Job submitted! ID: {job_id}")


@app.command()
def status(job_id: str):
    """Check job status."""
    typer.echo(f"Checking status for job: {job_id}")
    job_status = get_job_status(job_id)
    typer.echo(f"Status: {job_status}")


@app.command()
def wait(job_id: str, timeout: int = typer.Option(300, help="Timeout in seconds")):
    """Wait until job finishes (success/failure)."""
    typer.echo(f"Waiting for job {job_id} (timeout = {timeout}s)...")
    start_time = time.time()

    while True:
        status = get_job_status(job_id)
        if status in ("success", "failed"):
            typer.echo(f"Job completed with status: {status}")
            raise typer.Exit(code=0 if status == "success" else 1)

        if time.time() - start_time > timeout:
            typer.echo("Timed out waiting for job.")
            raise typer.Exit(code=1)

        time.sleep(5)

