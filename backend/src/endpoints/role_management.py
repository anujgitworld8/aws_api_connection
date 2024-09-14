# backend/src/routers/role_management.py

from fastapi import APIRouter, Depends, HTTPException, Response, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..connections.config import get_db
from ..common.models import Role, UserRole, Permission
from ..common.auth import Auth

router = APIRouter(prefix="/v1")
security = HTTPBearer()
auth_handler = Auth()

@router.get("/permissions", tags=["Role Management"])
async def get_user_permissions(
    response: Response,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """API to fetch permission details for a specific role."""
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    if user_id:
        user_roles = db.query(UserRole).filter_by(user_id=user_id).all()
        permissions = db.query(Permission).join(UserRole, UserRole.role_id == Permission.id).filter(UserRole.user_id == user_id).all()
        
        permission_details = [perm.permission_name for perm in permissions]
        role_details = [role.role_name for role in user_roles]
        
        return {
            "detail": {
                "userRole": role_details,
                "userPermissions": permission_details,
                "statusCode": 200,
            }
        }

@router.get("/roles", tags=["Role Management"])
async def get_roles(db: Session = Depends(get_db)):
    """API to fetch all available roles."""
    roles = db.query(Role).all()
    return {"roles": [role.role_name for role in roles]}
