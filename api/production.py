"""
Configurações de produção para Vercel
Otimizações para evitar overload
"""

import os
from pathlib import Path

# Configurações de produção
PRODUCTION_CONFIG = {
    # Limites de memória e tempo
    'MAX_FILE_SIZE': 10 * 1024 * 1024,  # 10MB
    'MAX_PROCESSING_TIME': 25,  # 25 segundos
    'MAX_MEMORY_USAGE': 512,  # 512MB
    
    # Cache e limpeza
    'CACHE_TIMEOUT': 300,  # 5 minutos
    'AUTO_CLEANUP': True,
    
    # Processamento
    'CHUNK_SIZE': 1000,  # Processa em chunks
    'MAX_ROWS': 50000,  # Máximo de linhas por arquivo
    
    # Logs
    'LOG_LEVEL': 'WARNING',
    'ENABLE_DEBUG': False,
    
    # Segurança
    'ALLOWED_EXTENSIONS': {'csv', 'xlsx', 'xls'},
    'MAX_FILES': 4,
}

# Variáveis de ambiente
def get_env_config():
    """Obtém configurações do ambiente"""
    return {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', ''),
        'VERCEL_ENV': os.getenv('VERCEL_ENV', 'production'),
        'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
    }

# Otimizações para pandas
def optimize_pandas():
    """Aplica otimizações para pandas no Vercel"""
    import pandas as pd
    
    # Configurações para economizar memória
    pd.options.mode.chained_assignment = None
    pd.options.mode.use_inf_as_na = True
    
    # Limita threads para evitar sobrecarga
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'

# Verificação de recursos
def check_resources():
    """Verifica recursos disponíveis"""
    import psutil
    
    memory = psutil.virtual_memory()
    cpu_count = psutil.cpu_count()
    
    return {
        'memory_available': memory.available,
        'memory_percent': memory.percent,
        'cpu_count': cpu_count,
        'can_process': memory.available > 100 * 1024 * 1024  # 100MB mínimo
    }

# Configurações de logging
def setup_production_logging():
    """Configura logging para produção"""
    import logging
    
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Remove logs desnecessários
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    logging.getLogger('pandas').setLevel(logging.ERROR)
