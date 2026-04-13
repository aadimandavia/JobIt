from fastapi import APIRouter, Query
from typing import List
from app.models.job import get_all_jobs
from app.schemas.job_schema import JobResponse

router = APIRouter()

@router.get("/jobs", response_model=List[JobResponse])
def fetch_jobs(
    keyword: str = Query(None, description="Filter jobs by keyword in the title"),
    limit: int = Query(20, description="Number of results to return")
):
    return get_all_jobs(limit, keyword)
