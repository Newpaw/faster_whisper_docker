# main.py
# This is the main FastAPI application.
# We’re using background tasks for transcription because we don’t have a supercomputer at our disposal.

from fastapi import FastAPI, File, UploadFile, Depends, BackgroundTasks, HTTPException
from .auth import get_current_username
from .tasks import create_transcription_job, get_job_status

app = FastAPI()


@app.post("/transcribe")
def transcribe_audio_endpoint(
    background_tasks: BackgroundTasks,  # Non-default argument comes first.
    file: UploadFile = File(...),
    user: str = Depends(get_current_username)
):
    """
    Start the transcription job for the uploaded MP3 file.
    The job will run on the background so that you can get back immediately.
    """
    job_id = create_transcription_job(file, background_tasks)
    return {
        "job_id": job_id,
        "message": "Transcription job started. Check status with GET /status/{job_id}"
    }


@app.get("/status/{job_id}")
def get_status(job_id: str, user: str = Depends(get_current_username)):
    """
    Retrieve the status and result of the transcription job.
    """
    job = get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found. Did you even submit a job?")
    return job
