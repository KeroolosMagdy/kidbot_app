from helpers import get_settings
class BaseDataModel:
    def __init__(self,dp_client=object):
        self.dp_client = dp_client
        self.app_settings = get_settings()
    