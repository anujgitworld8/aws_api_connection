from src.common.log_method import application_logger


# Method to check if the value is list or not and return the proper value
def get_attribute_val(attribute_val):
    archive_viewer_log = application_logger()
    try:
        if attribute_val and type(attribute_val) is list:
            return attribute_val[0]
        elif attribute_val and type(attribute_val) is not list:
            return attribute_val
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
