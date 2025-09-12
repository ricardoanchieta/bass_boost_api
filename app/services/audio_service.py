"""
Serviço para processamento de áudio
"""
from pydub import AudioSegment
import numpy as np
import math
import io
from typing import Tuple
from fastapi import HTTPException, UploadFile
from ..core.config import settings


class AudioService:
    """Serviço para processamento de áudio"""
    
    @staticmethod
    def bass_line_freq(track) -> int:
        """
        Calcula a frequência da linha de grave baseada no track de áudio
        
        Args:
            track: Array de samples do áudio
            
        Returns:
            int: Fator de grave calculado
        """
        sample_track = list(track)
        est_mean = np.mean(sample_track)
        est_std = 3 * np.std(sample_track) / (math.sqrt(2))
        bass_factor = int(round((est_std - est_mean) * 0.005))
        return bass_factor
    
    @staticmethod
    async def validate_audio_file(file: UploadFile, contents: bytes = None) -> bytes:
        """
        Valida se o arquivo é válido para processamento
        
        Args:
            file: Arquivo enviado pelo usuário
            contents: Conteúdo do arquivo (opcional)
            
        Returns:
            bytes: Conteúdo validado do arquivo
            
        Raises:
            HTTPException: Se o arquivo não for válido
        """
        if not file or not file.filename:
            raise HTTPException(
                status_code=400, 
                detail="Nenhum arquivo foi enviado"
            )
        
        # Verificar extensão
        file_extension = file.filename.lower().split('.')[-1]
        if file_extension not in settings.allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Extensão de arquivo não suportada. Apenas arquivos {', '.join(settings.allowed_extensions).upper()} são aceitos"
            )
        
        # Ler conteúdo se não foi fornecido
        if contents is None:
            contents = await file.read()
        
        # Verificar se arquivo não está vazio
        if not contents or len(contents) == 0:
            raise HTTPException(
                status_code=400,
                detail="O arquivo enviado está vazio"
            )
        
        # Verificar tamanho do arquivo
        if len(contents) > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"Arquivo muito grande. Tamanho máximo permitido: {settings.max_file_size // (1024*1024)}MB"
            )
        
        # Verificar se é um arquivo de áudio válido
        try:
            # Determinar formato baseado na extensão
            audio_format = file_extension if file_extension != "m4a" else "mp4"
            
            # Tentar carregar o arquivo para validação
            test_audio = AudioSegment.from_file(io.BytesIO(contents), format=audio_format)
            
            # Verificar se tem duração válida
            if len(test_audio) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="O arquivo de áudio não possui conteúdo reproduzível ou está corrompido"
                )
            
            # Verificar duração máxima
            duration_seconds = len(test_audio) / 1000.0  # pydub usa millisegundos
            if duration_seconds > settings.max_duration_seconds:
                raise HTTPException(
                    status_code=400,
                    detail=f"Arquivo muito longo. Duração máxima permitida: {settings.max_duration_seconds // 60} minutos"
                )
                
        except Exception as e:
            # Tratar erros específicos de decodificação
            error_msg = str(e).lower()
            if "decoding failed" in error_msg or "header missing" in error_msg:
                raise HTTPException(
                    status_code=400,
                    detail="Arquivo MP3 inválido ou corrompido. Verifique se o arquivo não está danificado e tente novamente."
                )
            elif "could not find codec" in error_msg:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de arquivo não reconhecido. Certifique-se de enviar um arquivo MP3 válido."
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Não foi possível processar o arquivo de áudio: {str(e)}"
                )
        
        return contents
    
    @staticmethod
    async def process_bass_boost(file: UploadFile, boost_number: int) -> Tuple[io.BytesIO, str]:
        """
        Processa o arquivo de áudio aplicando boost no grave
        
        Args:
            file: Arquivo de áudio para processar
            boost_number: Valor do boost a ser aplicado
            
        Returns:
            Tuple[io.BytesIO, str]: Buffer com áudio processado e nome do arquivo
            
        Raises:
            HTTPException: Se houver erro no processamento
        """
        try:
            # Validar arquivo e obter conteúdo validado
            contents = await AudioService.validate_audio_file(file)
            
            # Determinar formato do arquivo
            file_extension = file.filename.lower().split('.')[-1]
            audio_format = file_extension if file_extension != "m4a" else "mp4"
            
            # Processar áudio
            sample = AudioSegment.from_file(io.BytesIO(contents), format=audio_format)
            
            # Verificar se o áudio tem samples válidos
            if sample.frame_count == 0:
                raise HTTPException(
                    status_code=400,
                    detail="O arquivo de áudio não contém dados válidos para processamento"
                )
            
            # Aplicar filtro de grave
            try:
                audio_samples = sample.get_array_of_samples()
                bass_freq = AudioService.bass_line_freq(audio_samples)
                
                # Garantir que bass_freq é válido
                if bass_freq <= 0:
                    bass_freq = 100  # Frequência padrão para graves
                    
                filtered = sample.low_pass_filter(bass_freq)
                
                # Combinar áudio original com filtro boosted
                combined = sample.overlay(filtered + boost_number)
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro durante o processamento de áudio (filtro de grave): {str(e)}"
                )
            
            # Criar buffer de saída
            try:
                output = io.BytesIO()
                combined.export(output, format='mp3', bitrate="192k")
                output.seek(0)
                
                # Verificar se a saída foi gerada corretamente
                if output.getvalue() == b'':
                    raise HTTPException(
                        status_code=500,
                        detail="Falha ao gerar arquivo de áudio processado"
                    )
                
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao exportar arquivo processado: {str(e)}"
                )
            
            # Gerar nome do arquivo processado
            filename_parts = file.filename.rsplit('.', 1)
            if len(filename_parts) == 2:
                name, ext = filename_parts
                processed_filename = f"{name}_bass_boosted.{ext}"
            else:
                processed_filename = f"{file.filename}_bass_boosted.mp3"
            
            return output, processed_filename
            
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            # Capturar qualquer outro erro não tratado
            error_msg = str(e).lower()
            if "decoding failed" in error_msg or "ffmpeg" in error_msg:
                raise HTTPException(
                    status_code=400, 
                    detail="Erro na decodificação do arquivo de áudio. Verifique se o arquivo MP3 não está corrompido."
                )
            else:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Erro interno durante o processamento: {str(e)}"
                )
