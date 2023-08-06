from pathlib import Path
from typing import Optional

from promptquality.get_metrics import get_metrics
from promptquality.helpers import (
    create_job,
    create_project,
    create_run,
    create_template,
    upload_dataset,
)
from promptquality.job_progress import job_progress
from promptquality.set_config import set_config
from promptquality.types.run import PromptMetrics
from promptquality.types.settings import Settings


def run(
    template: str,
    dataset: Path,
    project_name: Optional[str] = None,
    run_name: Optional[str] = None,
    template_name: Optional[str] = None,
    settings: Optional[Settings] = None,
    wait: bool = True,
) -> Optional[PromptMetrics]:
    config = set_config()
    # Create project.
    project_id = create_project(project_name, config)
    # Create template.
    template_version_id = create_template(
        template,
        project_id,
        template_name,
        config,
    )
    # Upload dataset.
    dataset_id = upload_dataset(
        dataset,
        project_id,
        template_version_id,
        config,
    )
    # Run prompt.
    run_id = create_run(
        project_id,
        run_name,
        config,
    )
    job_id = create_job(
        project_id,
        run_id,
        dataset_id,
        template_version_id,
        settings,
        config,
    )
    if wait:
        job_progress(job_id, config)
    print(f"🔭 View your prompt run on the Galileo console at: {config.run_url}")
    metrics = get_metrics(
        project_id=project_id, run_id=run_id, job_id=job_id, config=config
    )
    return metrics
