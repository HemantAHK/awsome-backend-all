from typing import Dict, Union, List, Any
from typing import Optional

from fastapi import APIRouter, Body, Depends, Query, Request, HTTPException, status

from app.api.dependencies.database import get_repository
from app.api.dependencies.limiter import limiter
from app.api.dependencies.paginated import (
    PaginatedListResponse,
    compute_offset,
    paginated_response,
)
from app.api.dependencies.samples import valid_sample_id
from app.repositories.sample import SamplesRepository
from app.schemas.sample import Sample, SampleInCreate, SampleInResponse, SampleInUpdate

router = APIRouter()


@router.post("", name="sample:create")
# @limiter.limit("1/second")
async def create_sample(
    request: Request,
    payload: SampleInCreate,
    samples_repo: SamplesRepository = Depends(
        get_repository(SamplesRepository)
    ),
) -> SampleInResponse:
    """
    Create a sample.
    """
    return await samples_repo.add(payload=payload)


@router.get("", name="sample:get_all")
@limiter.limit("10/minute")
async def get_all_samples(
    request: Request,
    page: int = Query(1, description="Page number (starts from 1)"),
    size: int = Query(10, description="Number of items per page"),
    filter_params: Optional[str] = Query(
        None, description="Query filter params"),
    samples_repo: SamplesRepository = Depends(
        get_repository(SamplesRepository)
    ),
) -> PaginatedListResponse[SampleInResponse]:
    """
    Get all samples.
    """
    samples = await samples_repo.get_all(
        filters=filter_params,
        offset=compute_offset(page, size),
        limit=size,
    )

    return paginated_response(
        crud_data=samples, page=page, items_per_page=size
    )


@router.get("/{sample_id}", name="sample:get_one")
@limiter.limit("1/second")
async def get_sample(
    request: Request, current_sample: Sample = Depends(valid_sample_id)
) -> SampleInResponse:
    """
    Get a sample.
    """
    if current_sample.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="sample is deleted",
        )

    return current_sample


@router.put("/{sample_id}", name="sample:update")
@limiter.limit("1/second")
async def update_sample(
    request: Request,     payload: SampleInUpdate,
    current_sample: Sample = Depends(valid_sample_id),    samples_repo: SamplesRepository = Depends(
        get_repository(SamplesRepository)
    )
) -> SampleInResponse:
    """
    Update a sample.
    """

    if current_sample.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="sample is deleted",
        )

    return await samples_repo.update(obj=current_sample, **payload.__dict__)


@router.delete("/{sample_id}", name="sample:delete")
@limiter.limit("1/second")
async def delete_sample(
    request: Request, current_sample: Sample = Depends(valid_sample_id),     samples_repo: SamplesRepository = Depends(
        get_repository(SamplesRepository)
    )
) -> None:

    """
    Delete a sample.
    """

    if current_sample.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="sample is deleted",
        )

    return await samples_repo.delete(uuid=str(current_sample.uuid))


@router.delete("/{sample_id}/delete", name="sample:remove")
@limiter.limit("1/second")
async def remove_sample(
    request: Request, current_sample: Sample = Depends(valid_sample_id), samples_repo: SamplesRepository = Depends(
        get_repository(SamplesRepository)
    )
) -> None:

    """
    Remove a sample.
    """

    return await samples_repo.remove(uuid=str(current_sample.uuid))
