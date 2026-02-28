from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db
from ..ifcxml_parser import IfcXmlParseError, parse_ifcxml
from ..security import require_write_role

router = APIRouter(tags=["ifcxml-import"])


@router.post(
    "/import/ifcxml",
    response_model=schemas.IfcImportSummary,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_write_role)],
)
async def import_ifcxml(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".xml"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload an ifcXML (.xml) file.",
        )

    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty")

    try:
        parsed_model = parse_ifcxml(content)
    except IfcXmlParseError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ifcXML import failed: {error}",
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected import error: {error}",
        ) from error

    return crud.import_ifc_model(db, parsed_model)
