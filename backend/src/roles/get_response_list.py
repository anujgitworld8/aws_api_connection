# Method to get a list from list of tuple [()]
async def get_response_list(user_details):
    return [item for tuple in user_details for item in tuple]
