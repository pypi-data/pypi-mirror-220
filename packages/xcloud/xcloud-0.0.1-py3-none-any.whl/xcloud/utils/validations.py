from xcloud.utils.requests_utils import do_request
from xcloud.config import Config

# This function is not in config utils to avoid circular imports
def is_config_valid(api_key: str, workspace_id: str):        
    response = do_request(
        url=f"{Config.AUTH_BASE_URL_X_BACKEND}/v1/auth/verify",
        http_method="post",
        headers={
            "x-api-key": api_key,
            # Every user should have at least read permissions
            "x-original-method": "GET",
            "x-original-url": "https://dev.xcloud-api.stochastic.ai/executor/backend/v1/jobs/"
        },
        xcloud_auth=False,
        workspace_id=workspace_id,
        throw_error=False
    )
    
    try:
        response.raise_for_status()
        return True
    except:
        return False