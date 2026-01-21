from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt
from src.config.config import Settings

def criar_token(token_data: dict) -> str:
    try:
        expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE)
        token_data.update({"exp": expire})
        encode_jwt = jwt.encode(token_data, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        return encode_jwt
    except JWTError:
        raise HTTPException(status_code=400, detail="Erro ao criar Token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def verificador_token(token:str) -> dict:
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
    