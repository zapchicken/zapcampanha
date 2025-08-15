"""
Processador de planilhas Excel para o projeto ZapCampanhas
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .utils import (
    setup_logging, 
    display_dataframe_info, 
    show_progress, 
    load_excel_file,
    validate_phone,
    clean_phone
)

console = Console()
logger = setup_logging()

class ExcelProcessor:
    """Classe para processar múltiplas planilhas Excel"""
    
    def __init__(self, input_dir: Path):
        self.input_dir = input_dir
        self.dataframes = {}
        self.processed_data = {}
    
    def load_all_excel_files(self) -> Dict[str, pd.DataFrame]:
        """Carrega todos os arquivos Excel do diretório de entrada"""
        excel_files = list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.xls"))
        
        if not excel_files:
            console.print("[yellow]Nenhum arquivo Excel encontrado no diretório de entrada!")
            return {}
        
        with show_progress("Carregando arquivos Excel...") as progress:
            task = progress.add_task("Processando...", total=len(excel_files))
            
            for file_path in excel_files:
                try:
                    # Carrega todas as abas do arquivo
                    excel_file = pd.ExcelFile(file_path)
                    
                    for sheet_name in excel_file.sheet_names:
                        df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
                        key = f"{file_path.stem}_{sheet_name}"
                        self.dataframes[key] = df
                        
                        console.print(f"[green]✓[/green] Carregado: {key} ({len(df)} linhas)")
                
                except Exception as e:
                    console.print(f"[red]✗[/red] Erro ao carregar {file_path}: {e}")
                
                progress.update(task, advance=1)
        
        return self.dataframes
    
    def display_loaded_files(self):
        """Exibe informações sobre os arquivos carregados"""
        if not self.dataframes:
            console.print("[yellow]Nenhum arquivo carregado!")
            return
        
        table = Table(title="Arquivos Excel Carregados")
        table.add_column("Arquivo", style="cyan")
        table.add_column("Linhas", style="green")
        table.add_column("Colunas", style="magenta")
        
        for key, df in self.dataframes.items():
            table.add_row(key, str(len(df)), str(len(df.columns)))
        
        console.print(table)
    
    def analyze_dataframes(self):
        """Analisa todos os DataFrames carregados"""
        for key, df in self.dataframes.items():
            console.print(f"\n[bold cyan]Análise: {key}[/bold cyan]")
            display_dataframe_info(df, f"Estrutura de {key}")
            
            # Mostra primeiras linhas
            console.print(f"\n[bold]Primeiras 5 linhas:[/bold]")
            console.print(df.head().to_string())
    
    def find_phone_columns(self) -> Dict[str, List[str]]:
        """Encontra colunas que podem conter números de telefone"""
        phone_columns = {}
        
        for key, df in self.dataframes.items():
            potential_phone_cols = []
            
            for col in df.columns:
                col_lower = col.lower()
                # Verifica se o nome da coluna sugere telefone
                if any(word in col_lower for word in ['telefone', 'phone', 'celular', 'whatsapp', 'contato']):
                    potential_phone_cols.append(col)
                else:
                    # Verifica se a coluna contém dados que parecem telefones
                    sample_data = df[col].dropna().astype(str).head(10)
                    phone_count = sum(1 for val in sample_data if validate_phone(val))
                    if phone_count > 0:
                        potential_phone_cols.append(col)
            
            if potential_phone_cols:
                phone_columns[key] = potential_phone_cols
        
        return phone_columns
    
    def clean_phone_data(self, phone_columns: Dict[str, List[str]]) -> Dict[str, pd.DataFrame]:
        """Limpa e padroniza dados de telefone"""
        cleaned_data = {}
        
        with show_progress("Limpando dados de telefone...") as progress:
            task = progress.add_task("Processando...", total=len(phone_columns))
            
            for key, cols in phone_columns.items():
                df = self.dataframes[key].copy()
                
                for col in cols:
                    if col in df.columns:
                        # Limpa os telefones
                        df[f"{col}_limpo"] = df[col].apply(clean_phone)
                        # Remove linhas com telefones inválidos
                        df = df[df[f"{col}_limpo"].str.len() > 0]
                
                cleaned_data[key] = df
                progress.update(task, advance=1)
        
        return cleaned_data
    
    def merge_dataframes(self, cleaned_data: Dict[str, pd.DataFrame], merge_strategy: str = "union") -> pd.DataFrame:
        """Combina múltiplos DataFrames baseado na estratégia especificada"""
        if not cleaned_data:
            return pd.DataFrame()
        
        if merge_strategy == "union":
            # Une todos os DataFrames
            merged_df = pd.concat(cleaned_data.values(), ignore_index=True)
        elif merge_strategy == "intersection":
            # Mantém apenas colunas comuns
            common_cols = set.intersection(*[set(df.columns) for df in cleaned_data.values()])
            merged_df = pd.concat([df[list(common_cols)] for df in cleaned_data.values()], ignore_index=True)
        else:
            raise ValueError(f"Estratégia de merge não suportada: {merge_strategy}")
        
        # Remove duplicatas
        merged_df = merged_df.drop_duplicates()
        
        return merged_df
    
    def generate_leads_report(self, final_df: pd.DataFrame) -> Dict[str, Any]:
        """Gera relatório sobre os leads processados"""
        report = {
            "total_leads": len(final_df),
            "colunas": list(final_df.columns),
            "telefones_validos": 0,
            "telefones_invalidos": 0
        }
        
        # Conta telefones válidos
        phone_cols = [col for col in final_df.columns if 'telefone' in col.lower() or 'phone' in col.lower()]
        for col in phone_cols:
            if col in final_df.columns:
                valid_phones = final_df[col].apply(validate_phone).sum()
                report["telefones_validos"] += valid_phones
                report["telefones_invalidos"] += len(final_df) - valid_phones
        
        return report

