from beanie import PydanticObjectId

def get_analytics_cache_key(user_id: PydanticObjectId):
    return f"transaction_stats:{str(user_id)}"

def get_transactions_cache_key(user_id: PydanticObjectId):
    return f"transactions:{str(user_id)}"