# Bass Boost API - FastAPI

Esta é uma API FastAPI profissional para aumentar o grave de arquivos de música MP3, estruturada seguindo as melhores práticas do FastAPI.

## 📁 Estrutura do Projeto

```
bass-boost-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação principal FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── bass_boost.py   # Endpoint de processamento de áudio
│   │       └── health.py       # Endpoints de sistema
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configurações centralizadas
│   ├── models/
│   │   ├── __init__.py
│   │   └── audio_models.py     # Modelos Pydantic
│   ├── services/
│   │   ├── __init__.py
│   │   └── audio_service.py    # Lógica de processamento de áudio
│   └── utils/
│       └── __init__.py
├── main.py                     # Ponto de entrada
├── start.py                    # Script de inicialização
├── requirements.txt            # Dependências
├── config.env.example          # Template de configuração
└── README.md
```

## 🚀 Instalação e Execução

### 1. Instalar dependências:
```bash
pip install -r requirements.txt
```

### 2. Executar a aplicação:

**Opção 1 - Script principal:**
```bash
python main.py
```

**Opção 2 - Script otimizado:**
```bash
python start.py
```

**Opção 3 - Uvicorn direto:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📖 Uso da API

### Endpoint Principal

**POST /audio/bass_boost**

Processa um arquivo MP3 aplicando boost no grave.

#### Parâmetros:
- `file`: Arquivo MP3 (máximo 50MB)
- `boost_number`: Valor para ajustar o grave (entre -50 e 50, padrão: 5)

#### Exemplo usando curl:
```bash
curl -X POST "http://localhost:8000/audio/bass_boost" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sua_musica.mp3" \
     -F "boost_number=5" \
     --output musica_com_grave_aumentado.mp3
```

### Outros Endpoints

- **GET /** - Informações da API
- **GET /health** - Verificação de saúde da API
- **GET /docs** - Documentação interativa (Swagger UI)
- **GET /redoc** - Documentação alternativa (ReDoc)


## ⚙️ Configurações

As configurações estão centralizadas em `app/core/config.py` e podem ser customizadas via variáveis de ambiente ou arquivo `.env`:

```env
# Exemplo de .env
APP_NAME=Bass Boost API
APP_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
DEBUG=true
MAX_FILE_SIZE=52428800  # 50MB
```

## ✨ Recursos

### Funcionalidades Principais:
- ✅ **Upload seguro** de arquivos MP3 (até 50MB)
- ✅ **Processamento de áudio** com pydub e numpy
- ✅ **Boost de grave configurável** (-50 a +50)
- ✅ **Retorno otimizado** via StreamingResponse
- ✅ **Validação robusta** de entrada

### Recursos Técnicos:
- ✅ **Arquitetura modular** seguindo padrões FastAPI
- ✅ **Documentação automática** (Swagger UI + ReDoc)
- ✅ **Validação de tipos** com Pydantic
- ✅ **Tratamento de erros** profissional
- ✅ **Middleware CORS** configurável
- ✅ **Configuração centralizada** flexível
- ✅ **Logging e monitoramento** integrados
- ✅ **Hot reload** em desenvolvimento

## 🔄 Migração Flask → FastAPI

### Melhorias Implementadas:

1. **Estrutura Profissional:**
   - Separação de responsabilidades (services, models, endpoints)
   - Configurações centralizadas
   - Arquitetura modular

2. **Recursos Avançados:**
   - Validação automática com Pydantic
   - Documentação interativa automática
   - Middleware personalizado
   - Tratamento de exceções global

3. **Performance e Segurança:**
   - Processamento assíncrono
   - Validação de tamanho de arquivo
   - Headers de segurança
   - Tempo de resposta monitorado

4. **Developer Experience:**
   - Type hints completos
   - Hot reload em desenvolvimento
   - Logs estruturados
   - Documentação automática

## 🌐 URLs Importantes

Com a API rodando em http://localhost:8000:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🐳 Docker (Opcional)

Para containerização (criar Dockerfile se necessário):
```bash
# TODO: Adicionar suporte Docker
```

---

**Desenvolvido com FastAPI seguindo as melhores práticas de desenvolvimento de APIs modernas.**
