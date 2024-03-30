from fastapi import APIRouter

router = APIRouter()


@router.post("", name="auth:register")
async def register() -> None:

    # Check if the username is already taken

    # Check if the email is already taken

    # Create user in the database

    # Notify

    return None


@router.post("/token", name="auth:login")
async def create_access_token() -> None:

    # Attempt to fetch user from the database by email
    # If user does not exist, raise error

    # Check if password provided matches the user's password

    # Generate access token and refresh token

    # Set refresh token in cookie

    # Return response with UserInResponse model including user details and token

    return None


@router.post("/refresh", name="auth:refresh")
async def refresh_access_token() -> None:

    # Decode the refresh token to extract user data

    # Retrieve the user from the database

    # Generate a new access token for the user

    # Return the response with the new access token

    return None


@router.post("/logout", name="auth:logout")
async def logout() -> None:

    # Check if the refresh token cookie is missing

    # Delete the refresh token cookie

    # Add the revoked token to the set

    return None
