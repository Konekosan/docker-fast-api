from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.app_config.database_config import get_db
from app.controller import admin_repository
from app.schema.permissions_schemas import RequestPermission
from app.schema.roles_schemas import RequestRole
from app.schema.roles_permissions_schema import RequestRolePermission
from app.schema.roles_usager_schema import RequestRoleUsager
from app.model.usager import Usager
from app.auth.auth import get_current_usager

admin_router = APIRouter()

@admin_router.get("/roles")
async def get(db:Session=Depends(get_db)):
    _roles = admin_repository.fetch_roles(db, 0, 100)
    return _roles, 200

@admin_router.get("/permissions")
async def get(db:Session=Depends(get_db)):
    _permissions = admin_repository.fetch_permissions(db, 0, 100)
    return _permissions, 200

# Creation d'un role
@admin_router.post("/create_role")
async def create(request: RequestRole, db:Session=Depends(get_db)):
    _permissions = admin_repository.add_role(db, request.parameter)
    return _permissions, 200

# Creation d'une permissions
@admin_router.post("/create_permissions")
async def create(request: RequestPermission, db:Session=Depends(get_db)):
    _permissions = admin_repository.add_permissions(db, request.parameter)
    return _permissions, 200

# assignation role sur un usager
@admin_router.post("/assign-role")
async def assign_role_to_user(request: RequestRoleUsager, db: Session = Depends(get_db)):
    _roles = admin_repository.assign_role_to_user(db, request.parameter)
    return _roles, 200

# assignation permission sur un role
@admin_router.post("/assign-permission")
async def assign_permission_to_role(request: RequestRolePermission, db: Session = Depends(get_db)):
    _permissions = admin_repository.assign_permission_to_role(db, request.parameter)
    return _permissions, 200

@admin_router.get("/me/permissions")
async def get_my_permissions(user: Usager = Depends(get_current_usager), db: Session = Depends(get_db)):
    if not user or (user.id is None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
        )
    permissions = admin_repository.get_user_permissions(user.id, db)
    return {"permissions": permissions}