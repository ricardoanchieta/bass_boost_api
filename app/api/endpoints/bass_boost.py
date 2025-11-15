"""
Endpoint para processamento de bass boost
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import Annotated
import io

from ...services.audio_service import AudioService
from ...models.audio_models import ErrorResponse
from ...core.config import settings


router = APIRouter(
    prefix="/audio",
    tags=["Audio Processing"],
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)


@router.post(
    "/bass_boost",
    summary="Aumentar grave de arquivo de áudio",
    description="Processa um arquivo de áudio aplicando boost no grave conforme o valor especificado",
    response_description="Arquivo de áudio processado com grave aumentado"
)
async def bass_boost(
    file: UploadFile = File(
        description="Arquivo de áudio (MP3, WAV, M4A, FLAC)"
    ),
    boost_number: int = Form(
        default=settings.default_bass_boost,
        description="Valor para aumentar o grave (entre -50 e 50)"
    ),
):
    """
    Aumenta o grave de um arquivo de áudio
    
    - **file**: Arquivo de áudio válido (MP3, WAV, M4A, FLAC - máximo 50MB e 10 minutos)
    - **boost_number**: Valor para aumentar o grave (entre -50 e 50)
    
    Retorna o arquivo processado como resposta de streaming em formato MP3.
    
    **Possíveis erros:**
    - 400: Arquivo inválido, corrompido, formato não suportado ou muito longo
    - 413: Arquivo muito grande (> 50MB)
    - 500: Erro interno de processamento
    """
    
    try:
        # Validar intervalo do boost explicitamente (compatível com Pydantic v2 em Form)
        if not (settings.min_bass_boost <= boost_number <= settings.max_bass_boost):
            raise HTTPException(status_code=400, detail=f"boost_number deve estar entre {settings.min_bass_boost} e {settings.max_bass_boost}")
        # Processar áudio
        output, processed_filename = await AudioService.process_bass_boost(file, boost_number)
        
        # Retornar arquivo processado como streaming response
        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=\"{processed_filename}\"",
                "Content-Type": "audio/mpeg"
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions com as mensagens originais
        raise
    except Exception as e:
        # Capturar qualquer erro não previsto
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado no servidor: {str(e)}"
        )
