"""
Gerador de leads para campanhas de WhatsApp
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .utils import setup_logging, display_dataframe_info, show_progress, save_dataframe

console = Console()
logger = setup_logging()

class LeadGenerator:
    """Classe para gerar listas de leads otimizadas para WhatsApp"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
    
    def filter_valid_leads(self, df: pd.DataFrame, phone_columns: List[str]) -> pd.DataFrame:
        """Filtra leads com telefones válidos"""
        if df.empty:
            return df
        
        # Cria uma máscara para telefones válidos
        valid_mask = pd.Series([False] * len(df), index=df.index)
        
        for col in phone_columns:
            if col in df.columns:
                # Verifica se a coluna tem dados
                if not df[col].isna().all():
                    # Cria coluna temporária para validação
                    temp_col = df[col].astype(str).str.replace(r'[^\d]', '', regex=True)
                    valid_mask |= (temp_col.str.len() >= 10) & (temp_col.str.len() <= 15)
        
        filtered_df = df[valid_mask].copy()
        
        console.print(f"[green]Leads válidos: {len(filtered_df)} de {len(df)}")
        return filtered_df
    
    def standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Padroniza nomes de colunas"""
        column_mapping = {
            # Mapeamento de nomes de colunas comuns
            'nome': 'nome',
            'name': 'nome',
            'cliente': 'nome',
            'customer': 'nome',
            'telefone': 'telefone',
            'phone': 'telefone',
            'celular': 'telefone',
            'whatsapp': 'telefone',
            'email': 'email',
            'e-mail': 'email',
            'cidade': 'cidade',
            'city': 'cidade',
            'estado': 'estado',
            'state': 'estado',
            'uf': 'estado',
            'endereco': 'endereco',
            'address': 'endereco',
            'empresa': 'empresa',
            'company': 'empresa',
            'observacoes': 'observacoes',
            'notes': 'observacoes',
            'obs': 'observacoes'
        }
        
        # Renomeia colunas que correspondem ao mapeamento
        new_columns = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in column_mapping:
                new_columns[col] = column_mapping[col_lower]
            else:
                new_columns[col] = col
        
        df_renamed = df.rename(columns=new_columns)
        return df_renamed
    
    def create_whatsapp_format(self, df: pd.DataFrame, phone_column: str = 'telefone') -> pd.DataFrame:
        """Cria formato otimizado para WhatsApp"""
        if df.empty:
            return df
        
        whatsapp_df = df.copy()
        
        # Garante que temos uma coluna de telefone
        if phone_column not in whatsapp_df.columns:
            # Procura por colunas que podem conter telefones
            phone_cols = [col for col in whatsapp_df.columns 
                         if any(word in col.lower() for word in ['telefone', 'phone', 'celular', 'whatsapp'])]
            
            if phone_cols:
                phone_column = phone_cols[0]
            else:
                console.print("[red]Nenhuma coluna de telefone encontrada!")
                return whatsapp_df
        
        # Limpa e formata telefones
        whatsapp_df['telefone_whatsapp'] = whatsapp_df[phone_column].astype(str).apply(
            lambda x: self._format_whatsapp_phone(x)
        )
        
        # Remove linhas sem telefone válido
        whatsapp_df = whatsapp_df[whatsapp_df['telefone_whatsapp'].str.len() > 0]
        
        # Cria link do WhatsApp
        whatsapp_df['link_whatsapp'] = whatsapp_df['telefone_whatsapp'].apply(
            lambda x: f"https://wa.me/{x}" if x else ""
        )
        
        return whatsapp_df
    
    def _format_whatsapp_phone(self, phone: str) -> str:
        """Formata telefone para WhatsApp"""
        if pd.isna(phone) or not phone:
            return ""
        
        # Remove caracteres especiais
        clean_phone = str(phone).replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        
        # Remove tudo que não for número
        clean_phone = ''.join(filter(str.isdigit, clean_phone))
        
        # Adiciona código do país se necessário
        if clean_phone.startswith('0'):
            clean_phone = '55' + clean_phone[1:]
        elif not clean_phone.startswith('55') and len(clean_phone) == 11:
            clean_phone = '55' + clean_phone
        
        # Verifica se tem tamanho válido
        if 12 <= len(clean_phone) <= 15:
            return clean_phone
        
        return ""
    
    def generate_segments(self, df: pd.DataFrame, segment_by: str = None) -> Dict[str, pd.DataFrame]:
        """Gera segmentos de leads baseado em critérios"""
        segments = {}
        
        if not segment_by or segment_by not in df.columns:
            # Segmento único
            segments['todos'] = df
        else:
            # Segmenta por valores únicos na coluna especificada
            unique_values = df[segment_by].dropna().unique()
            
            for value in unique_values:
                segment_name = str(value).lower().replace(' ', '_')
                segment_df = df[df[segment_by] == value]
                segments[segment_name] = segment_df
        
        return segments
    
    def create_summary_report(self, df: pd.DataFrame, segments: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Cria relatório resumido dos leads"""
        report = {
            "total_leads": len(df),
            "segmentos": {},
            "colunas_principais": list(df.columns),
            "telefones_validos": 0
        }
        
        # Conta telefones válidos
        phone_cols = [col for col in df.columns if 'telefone' in col.lower()]
        for col in phone_cols:
            if col in df.columns:
                report["telefones_validos"] += df[col].notna().sum()
        
        # Informações dos segmentos
        for segment_name, segment_df in segments.items():
            report["segmentos"][segment_name] = {
                "quantidade": len(segment_df),
                "percentual": round((len(segment_df) / len(df)) * 100, 2) if len(df) > 0 else 0
            }
        
        return report
    
    def save_leads(self, df: pd.DataFrame, filename: str = "leads_whatsapp", 
                   format: str = "xlsx", include_segments: bool = True) -> List[Path]:
        """Salva leads em diferentes formatos"""
        saved_files = []
        
        # Salva arquivo principal
        main_file = save_dataframe(df, self.output_dir, filename, format)
        saved_files.append(main_file)
        
        if include_segments and not df.empty:
            # Cria segmentos por cidade se existir
            if 'cidade' in df.columns:
                segments = self.generate_segments(df, 'cidade')
                
                for segment_name, segment_df in segments.items():
                    if len(segment_df) > 0:
                        segment_file = save_dataframe(
                            segment_df, 
                            self.output_dir, 
                            f"{filename}_{segment_name}", 
                            format
                        )
                        saved_files.append(segment_file)
        
        return saved_files
    
    def display_leads_summary(self, df: pd.DataFrame, report: Dict[str, Any]):
        """Exibe resumo dos leads processados"""
        console.print("\n[bold cyan]📊 RESUMO DOS LEADS[/bold cyan]")
        
        # Tabela principal
        summary_table = Table(title="Estatísticas Gerais")
        summary_table.add_column("Métrica", style="cyan")
        summary_table.add_column("Valor", style="green")
        
        summary_table.add_row("Total de Leads", str(report["total_leads"]))
        summary_table.add_row("Telefones Válidos", str(report["telefones_validos"]))
        summary_table.add_row("Colunas", str(len(report["colunas_principais"])))
        
        console.print(summary_table)
        
        # Tabela de segmentos
        if report["segmentos"]:
            segment_table = Table(title="Segmentos")
            segment_table.add_column("Segmento", style="cyan")
            segment_table.add_column("Quantidade", style="green")
            segment_table.add_column("Percentual", style="yellow")
            
            for segment_name, segment_info in report["segmentos"].items():
                segment_table.add_row(
                    segment_name,
                    str(segment_info["quantidade"]),
                    f"{segment_info['percentual']}%"
                )
            
            console.print(segment_table)
        
        # Mostra primeiras linhas
        if not df.empty:
            console.print(f"\n[bold]Primeiras 5 linhas dos leads:[/bold]")
            display_cols = ['nome', 'telefone', 'cidade', 'link_whatsapp']
            available_cols = [col for col in display_cols if col in df.columns]
            
            if available_cols:
                console.print(df[available_cols].head().to_string())
            else:
                console.print(df.head().to_string())

