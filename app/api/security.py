"""
Dependências de segurança para a API
"""
import os
from fastapi import Header, HTTPException, status


def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    """
    Exige a presença de uma API Key no header `X-API-Key`.
    - Se a variável de ambiente `API_KEY` não estiver definida, não bloqueia (modo permissivo).
    - Caso definida, o header deve corresponder exatamente ao valor configurado.
    """
    expected_api_key = os.environ.get("API_KEY")
    if not expected_api_key:
        return  # modo permissivo quando não configurado

    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )


