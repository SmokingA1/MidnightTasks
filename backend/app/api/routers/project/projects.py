from uuid import UUID
from typing import List

from fastapi import APIRouter, status, HTTPException, Path, Query

from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate, Message
from app.api.deps import SessionDep, CurrentUser
from app.services.project.project import (
    get_project_by_id,
    get_projects,
    create_project,
    update_project_by_id,
    delete_project_by_id,
)

router = APIRouter(prefix="/project", tags=["Project"])

@router.get("/", response_model=List[ProjectRead])
async def read_projects(
    db: SessionDep,
    page: int = Query(1, description="The number of page is required."),
    limit: int = Query(20, description="The number of qty projects is required."),
):
    """
    Receive projects with pagination.
    """

    db_projects = await get_projects(db=db, page=page, limit=limit)

    return db_projects


@router.get("/{project_id}", response_model=ProjectRead)
async def read_project(
    db: SessionDep,
    project_id: UUID,
):
    """
    Receive project by ID.
    """

    db_project = await get_project_by_id(db=db, project_id=project_id)
    print('Info project HERE: ', db_project)
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Such project not found!")
    
    return db_project


@router.post("/", response_model=ProjectRead)
async def create_new_project(
    db: SessionDep,
    project_create: ProjectCreate,
):
    """
    Creating new project.
    """
    
    created_project = await create_project(db=db, project_create=project_create)

    return created_project


@router.put("/{project_id}", response_model=ProjectRead)
async def update_existing_project(
    db: SessionDep,
    project_id: UUID,
    project_update: ProjectUpdate,
):
    """
    Updating project by ID
    """

    db_project = await get_project_by_id(db=db, project_id=project_id)

    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found!")
    
    updated_project = await update_project_by_id(db=db, project_id=project_id, project_update=project_update)

    if not updated_project:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while updating project!"
        )
    
    return updated_project


@router.delete("/{project_id}", response_model=Message)
async def delete_existing_project(
    db: SessionDep,
    project_id: UUID,
):
    """
    Deleting project by ID.
    """

    db_project = await get_project_by_id(db=db, project_id=project_id)

    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proejct not found!")
    
    deleted_project = await delete_project_by_id(db=db, project_id=project_id)
    
    if not deleted_project:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while deleting project!"
        )

    return Message(data="Project deleted successfully!")

