from fastapi import APIRouter

router = APIRouter()


@router.post("", name="tenant:create")
async def create_tenant() -> None:

    # Check if the tenant already exists in the database

    # If tenant already exists, return an error response

    # If tenant does not exist
    # Parse request body to get tenant data
    # insert tenant data into the database

    return None


@router.get("", name="tenant:get_all")
async def get_all_teanants() -> None:

    # If filter is provided:
    # - Parse and validate filter parameters
    # - Apply filter to the query to retrieve filtered tenants

    # If filter is not provided, return all tenants

    return None


@router.get("/{tenant_id}", name="tenant:get_one")
async def get_tenant() -> None:

    #   Retrieve tenant from the database using tenant_id

    # If tenant does not exist, return not found response

    # If tenant exists, return tenant details

    return None


@router.put("/{tenant_id}", name="tenant:update")
async def update_tenant() -> None:

    # Retrieve tenant from the database using tenant_id

    # If tenant does not exist, return not found response

    # Parse request body to get updated tenant data

    # If tenant exists, update tenant data in the database

    return None


@router.delete("/{tenant_id}", name="tenant:delete")
async def delete_tenant() -> None:

    # Retrieve tenant from the database using tenant_id

    # If tenant does not exist, return not found response

    # If tenant exists, set is_active=True to tenant data from the database

    return None


@router.delete("/{tenant_id}/delete", name="tenant:remove")
async def remove_tenant() -> None:

    # Retrieve tenant from the database using tenant_id

    # If tenant does not exist, return not found response

    # If tenant exists, delete tenant data from the database

    return None
