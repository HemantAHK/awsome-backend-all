from fastapi import APIRouter

router = APIRouter()


@router.post("", name="user:create")
async def create_user() -> None:
    return None
    # Check if the user already exists in the database

    # If user already exists, return an error response

    # If user does not exist
    # Parse request body to get user
    # Insert user data into the database


@router.get("", name="user:get_all")
async def get_all_users() -> None:

    # If filter is provided:
    # - Parse and validate filter paramenters
    # - Apply filter to the query to retrive filter
    # If filter is not provided, return all users
    return None


@router.get("/{user_id}", name="user:get_one")
async def get_user() -> None:

    # Retrive user from the databse using user_id

    # If user does not exist, return not found response

    # If user exists, return user details
    return None


@router.put("/{user_id}", name="user:update")
async def update_user() -> None:

    # Retrieve user from the database using user_id

    # If user does not exists, return not found response

    # Parse request body to get updated user data
    return None


@router.delete("/{user_id}", name="user:delete")
async def delete_user() -> None:

    # Retrieve user from the database using user_id

    # If user does not exist, return not found response

    # If user exists, set is_active=True to user data from the database
    return None


@router.delete("/{user_id}/delete", name="user:remove")
async def remove_user() -> None:

    # Retrive user from the databse using user_id

    # if user does not exist, return not response

    # If user exists, delete ser data from the datbase
    return None
