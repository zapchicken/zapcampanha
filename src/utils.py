"""
Utilitários para o projeto ZapCampanhas
"""

import re
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

def validate_phone(phone: str) -> bool:
    """Valida se um número de telefone está no formato correto"""
    if not phone or pd.isna(phone):
        return False
    
    # Remove caracteres especiais
    clean_phone = re.sub(r'[^\d]', '', str(phone))
    
    # Verifica se tem entre 10 e 15 dígitos
    return 10 <= len(clean_phone) <= 15

def clean_phone(phone: str) -> str:
    """Limpa e formata um número de telefone"""
    if not phone or pd.isna(phone):
        return ""
    
    # Remove caracteres especiais
    clean_phone = re.sub(r'[^\d]', '', str(phone))
    
    # Adiciona código do país se não tiver
    if clean_phone.startswith('0'):
        clean_phone = '55' + clean_phone[1:]
    elif not clean_phone.startswith('55') and len(clean_phone) == 11:
        clean_phone = '55' + clean_phone
    
    return clean_phone

def display_dataframe_info(df: pd.DataFrame, title: str = "Informações do DataFrame"):
    """Exibe informações sobre um DataFrame de forma formatada"""
    table = Table(title=title)
    table.add_column("Coluna", style="cyan")
    table.add_column("Tipo", style="magenta")
    table.add_column("Não Nulos", style="green")
    table.add_column("Únicos", style="yellow")
    
    for col in df.columns:
        table.add_row(
            col,
            str(df[col].dtype),
            str(df[col].count()),
            str(df[col].nunique())
        )
    
    console.print(table)

def show_progress(description: str = "Processando..."):
    """Context manager para mostrar progresso"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    )

def save_dataframe(df: pd.DataFrame, output_path: Path, filename: str, format: str = "xlsx"):
    """Salva um DataFrame no formato especificado"""
    output_file = output_path / f"{filename}.{format}"
    
    if format.lower() == "xlsx":
        df.to_excel(output_file, index=False, engine="openpyxl")
    elif format.lower() == "csv":
        df.to_csv(output_file, index=False, encoding="utf-8")
    else:
        raise ValueError(f"Formato não suportado: {format}")
    
    console.print(f"[green]Arquivo salvo: {output_file}")
    return output_file

def load_excel_file(file_path: Path, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """Carrega um arquivo Excel"""
    try:
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
        else:
            df = pd.read_excel(file_path, engine="openpyxl")
        
        console.print(f"[green]Arquivo carregado: {file_path}")
        return df
    except Exception as e:
        console.print(f"[red]Erro ao carregar {file_path}: {e}")
        raise

