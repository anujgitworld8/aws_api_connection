from fastapi import APIRouter
from backend.src.endpoints import(
    aws_connection,
    check_connection_status,
    upload_data_file,
    fetch_data_file,
    delete_data_file,
    list_all_data_files,
    view_sensor_data
                                   )

router = APIRouter()

router.include_router(aws_connection.router)
router.include_router(check_connection_status.router)
router.include_router(upload_data_file.router)
router.include_router(fetch_data_file.router)
router.include_router(delete_data_file.router)
router.include_router(list_all_data_files.router)
router.include_router(view_sensor_data.router)

