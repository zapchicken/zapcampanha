"""
Configurações do projeto ZapCampanhas
"""

import os
from pathlib import Path

# Diretórios do projeto
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

# Configurações de processamento
DEFAULT_ENCODING = "utf-8"
EXCEL_ENGINE = "openpyxl"

# Configurações de saída
OUTPUT_FORMAT = "xlsx"  # xlsx, csv
OUTPUT_FILENAME = "leads_processados"

# Configurações de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configurações de validação
MIN_PHONE_LENGTH = 10
MAX_PHONE_LENGTH = 15

# Criar diretórios se não existirem
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

