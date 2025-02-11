from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends

__all__ = ("router",)

from app.application.codes_service import CodesService
from app.domain.models.codes import Codes
from app.entrypoint.fastapi.schema.codes import CodeView

# import 时注意要引入全局变量和不是去dic中再实例化一个对象
from app.application import DIC

router = APIRouter(
    prefix="/codes",
    tags=["codes"],
)


def to_code_view_model(code):
    return CodeView(
        code_id=code.id,
        abbreviation=code.abbrev,
        description=code.description,
        created_at=code.created_at,
        updated_at=code.updated_at,
        code_type=code.code_type,
    )


@router.get("",
            description="Get all codes",
            response_model=list[CodeView],
            status_code=status.HTTP_200_OK)
@inject
async def list_codes(codes_service: CodesService = Depends(Provide[DIC.codes_service])) -> list[CodeView]:
    codes: list[Codes] = await codes_service.get_codes(0, 10)
    return [to_code_view_model(code) for code in codes]