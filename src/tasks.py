# tasks.py
# This module handles job creation and processing.
# We store jobs in a simple dictionary because, honestly, we’re not running a high-end job queue here.

import uuid
import os
import shutil
from .transcription import transcribe_audio

# In-memory store for jobs. In a real production app, use a database or a proper queue.
jobs = {}


def create_transcription_job(upload_file, background_tasks):
    """
    Saves the uploaded file and creates a transcription job.
    The transcription is scheduled to run on the background.
    """
    # Generate a unique job ID because nothing good ever comes without a unique ID.
    job_id = str(uuid.uuid4())
    file_location = f"temp_{job_id}.mp3"
    
    # Save the uploaded file to disk. Yes, we write it to disk because memory is overrated.
    with open(file_location, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    
    # Initialize job status.
    jobs[job_id] = {"status": "queued", "result": None}
    
    # Schedule the transcription task to run in the background.
    background_tasks.add_task(transcribe_job, job_id, file_location)
    return job_id


def transcribe_job(job_id, file_path):
    """
    This function runs the actual transcription process.
    It updates the job status accordingly.
    """
    jobs[job_id]["status"] = "processing"
    try:
        result = transcribe_audio(file_path)
        # Mark job as completed.
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
    except Exception as e:
        # In case of an error, mark the job as failed.
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["result"] = {"error": str(e)}
    finally:
        # Clean up the temporary file. We wouldn’t want to leave a mess on your machine.
        if os.path.exists(file_path):
            os.remove(file_path)


def get_job_status(job_id):
    """
    Retrieves the current status (and result, if available) of the job.
    """
    return jobs.get(job_id)
