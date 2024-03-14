from typing import Mapping

from fastapi import Depends, HTTPException, Path, status

from app.api.dependencies.database import get_repository
from app.repositories.sample import SamplesRepository
from app.schemas.sample import SampleInResponse, SampleInDB


async def valid_sample_id(
    samples_repo: SamplesRepository = Depends(
        get_repository(SamplesRepository)
    ),
    sample_id: str = Path(
        ...,
        min_length=5,
        title="Ticket Purchase ID",
        description="Minimum 5 characters",
    ),
) -> SampleInDB:

    return await samples_repo.get_in_db(uuid=sample_id)
