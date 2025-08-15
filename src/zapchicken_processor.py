"""
Processador específico para dados da ZapChicken
Business Intelligence com análise preditiva e sugestões de marketing
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import re
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .utils import setup_logging, display_dataframe_info, show_progress, save_dataframe

console = Console()
logger = setup_logging()

class ZapChickenProcessor:
    """Processador especializado para dados da ZapChicken"""
    
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.dataframes = {}
        self.processed_data = {}
        
        # Configurações padrão (configuráveis)
        self.config = {
            'dias_inatividade': 30,
            'ticket_medio_minimo': 50.0,
            'periodo_analise_meses': 6,
            'raio_entrega_km': 17,
            'frequencia_alta_dias': 7,
            'frequencia_moderada_dias': 15,
            'frequencia_baixa_dias': 30
        }
    
    def load_zapchicken_files(self) -> Dict[str, pd.DataFrame]:
        """Carrega todos os arquivos da ZapChicken"""
        console.print("[bold cyan]📥 CARREGANDO ARQUIVOS ZAPCHICKEN...[/bold cyan]")
        
        # Procura pelos arquivos específicos
        files_found = {}
        
        # 1. Contacts (Google Contacts)
        contacts_files = list(self.input_dir.glob("*contacts*.csv")) + list(self.input_dir.glob("*contacts*.xls*"))
        if contacts_files:
            files_found['contacts'] = contacts_files[0]
        
        # 2. Lista Clientes
        clientes_files = list(self.input_dir.glob("*Lista-Clientes*.xls*"))
        if clientes_files:
            files_found['clientes'] = clientes_files[0]
        
        # 3. Todos os Pedidos
        pedidos_files = list(self.input_dir.glob("*Todos os pedidos*.xls*"))
        if pedidos_files:
            files_found['pedidos'] = pedidos_files[0]
        
        # 4. Histórico Itens
        itens_files = list(self.input_dir.glob("*Historico_Itens_Vendidos*.xls*"))
        if itens_files:
            files_found['itens'] = itens_files[0]
        
        # Verifica se os arquivos foram encontrados corretamente
        print(f"Arquivos encontrados:")
        for file_type, file_path in files_found.items():
            print(f"  {file_type}: {file_path.name}")
        
        # Carrega os arquivos
        with show_progress("Carregando arquivos...") as progress:
            task = progress.add_task("Processando...", total=len(files_found))
            
            for file_type, file_path in files_found.items():
                try:
                    if file_type == 'contacts':
                        df = pd.read_csv(file_path, encoding='utf-8')
                    else:
                        df = pd.read_excel(file_path, engine='openpyxl')
                    
                    self.dataframes[file_type] = df
                    console.print(f"[green]✓[/green] {file_type}: {file_path.name} ({len(df)} linhas)")
                    
                except Exception as e:
                    console.print(f"[red]✗[/red] Erro ao carregar {file_type}: {e}")
                
                progress.update(task, advance=1)
        
        return self.dataframes
    
    def clean_phone_number(self, phone: str) -> str:
        """Limpa e formata número de telefone"""
        if pd.isna(phone) or not phone:
            return ""
        
        # Remove caracteres especiais
        clean_phone = str(phone).replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        
        # Remove tudo que não for número
        clean_phone = ''.join(filter(str.isdigit, clean_phone))
        
        # Verifica se é válido (não é 00000000, 0000000000, etc.)
        if (clean_phone == '00000000' or 
            clean_phone == '0000000000' or 
            clean_phone == '00000000000' or
            len(clean_phone) < 10 or
            clean_phone.startswith('000')):
            return ""
        
        return clean_phone
    
    def extract_first_name(self, full_name: str) -> str:
        """Extrai primeiro nome"""
        if pd.isna(full_name) or not full_name:
            return ""
        
        # Remove caracteres especiais e espaços extras
        name = str(full_name).strip()
        
        # Se começa com LT_XX, extrai o nome após o espaço
        if name.startswith('LT_'):
            parts = name.split(' ', 1)
            if len(parts) > 1:
                return parts[1]
            return ""
        
        # Extrai primeiro nome
        first_name = name.split(' ')[0]
        
        # Filtra nomes inválidos
        invalid_names = ['-', '???????', 'null', 'none', 'nan', '']
        if first_name.lower() in [n.lower() for n in invalid_names]:
            return ""
        
        return first_name
    
    def normalize_neighborhood(self, bairro: str) -> str:
        """Normaliza nomes de bairros para corrigir variações"""
        if pd.isna(bairro) or not bairro:
            return ""
        
        bairro = str(bairro).strip().lower()
        
        # Mapeamento de variações conhecidas
        variations = {
            'fontanella': ['fontanela', 'fontanella', 'fortanella', 'fontanela'],
            'jardim dona luiza': ['jardim dona luiza', 'jardim d. luiza', 'dona luiza'],
            'nova jaguariuna': ['nova jaguariúna', 'nova jaguariuna'],
            'centro': ['centro', 'centro da cidade'],
            'zambom': ['zambom', 'jardim zambom'],
            'capotuna': ['capotuna', 'capotuna'],
            'triunfo': ['triunfo', 'jardim triunfo'],
            'nassif': ['nassif', 'nucleo res. dr. joao a nassif'],
            'capela de santo antonio': ['capela de santo antonio', 'capela santo antonio'],
            'chácara primavera': ['chácara primavera', 'chacara primavera', 'primavera'],
            'jardim europa': ['jardim europa', 'europa'],
            'jardim mauá ii': ['jardim mauá ii', 'jardim maua ii', 'mauá ii'],
            'jardim santa cruz': ['jardim santa cruz', 'santa cruz'],
            'roseira de cima': ['roseira de cima', 'roseira'],
            'tamboré': ['tamboré', 'tambore'],
            'nova jaguariúna': ['nova jaguariúna', 'nova jaguariuna']
        }
        
        # Procura por correspondências
        for normalized, variants in variations.items():
            if bairro in variants:
                return normalized
        
        return bairro
    
    def process_contacts(self) -> pd.DataFrame:
        """Processa arquivo de contatos do Google"""
        if 'contacts' not in self.dataframes:
            return pd.DataFrame()
        
        df = self.dataframes['contacts'].copy()
        
        # Encontra coluna de nome
        nome_col = None
        for col in ['First Name', 'Nome', 'nome', 'Name', 'name']:
            if col in df.columns:
                nome_col = col
                break
        
        if nome_col is None:
            print(f"Colunas disponíveis no arquivo de contatos: {list(df.columns)}")
            return pd.DataFrame()
        
        # Encontra coluna de telefone
        telefone_col = None
        for col in ['Phone 1 - Value', 'Telefone', 'telefone', 'Phone', 'phone', 'Fone', 'fone']:
            if col in df.columns:
                telefone_col = col
                break
        
        if telefone_col is None:
            print(f"❌ Nenhuma coluna de telefone encontrada no arquivo de contatos")
            return pd.DataFrame()
        
        # Renomeia colunas para facilitar o processamento
        df['nome'] = df[nome_col]
        df['telefone'] = df[telefone_col]
        
        # Limpa telefones
        df['telefone_limpo'] = df['telefone'].apply(self.clean_phone_number)
        
        # Remove telefones inválidos
        df = df[df['telefone_limpo'] != ""]
        
        # Identifica contatos com propaganda (LT_XX)
        df['recebe_propaganda'] = df['nome'].str.contains('^LT_', na=False)
        
        return df
    
    def process_clientes(self) -> pd.DataFrame:
        """Processa arquivo de clientes"""
        if 'clientes' not in self.dataframes:
            return pd.DataFrame()
        
        df = self.dataframes['clientes'].copy()
        
        # Encontra coluna de telefone (pode ter nomes diferentes)
        telefone_col = None
        for col in ['Fone Principal', 'Telefone', 'telefone', 'Fone', 'fone', 'Celular', 'celular', 'Phone', 'phone']:
            if col in df.columns:
                telefone_col = col
                break
        
        if telefone_col is None:
            print(f"Colunas disponíveis no arquivo de clientes: {list(df.columns)}")
            # Se não encontrar, tenta usar a primeira coluna que contenha 'telefone' no nome
            for col in df.columns:
                if 'telefone' in col.lower() or 'fone' in col.lower() or 'celular' in col.lower():
                    telefone_col = col
                    break
        
        if telefone_col is None:
            print("❌ Nenhuma coluna de telefone encontrada no arquivo de clientes")
            return pd.DataFrame()
        
        # Limpa telefones
        df['telefone_limpo'] = df[telefone_col].apply(self.clean_phone_number)
        
        # Remove telefones inválidos
        df = df[df['telefone_limpo'] != ""]
        
        # Extrai primeiro nome
        df['primeiro_nome'] = df['Nome'].apply(self.extract_first_name)
        
        # Normaliza bairros
        df['bairro_normalizado'] = df['Bairro'].apply(self.normalize_neighborhood)
        
        return df
    
    def process_pedidos(self) -> pd.DataFrame:
        """Processa arquivo de pedidos"""
        if 'pedidos' not in self.dataframes:
            return pd.DataFrame()
        
        df = self.dataframes['pedidos'].copy()
        
        # Encontra coluna de telefone (pode ter nomes diferentes)
        telefone_col = None
        for col in ['Telefone', 'telefone', 'Fone', 'fone', 'Celular', 'celular', 'Phone', 'phone']:
            if col in df.columns:
                telefone_col = col
                break
        
        if telefone_col is None:
            print(f"Colunas disponíveis no arquivo de pedidos: {list(df.columns)}")
            # Se não encontrar, tenta usar a primeira coluna que contenha 'telefone' no nome
            for col in df.columns:
                if 'telefone' in col.lower() or 'fone' in col.lower() or 'celular' in col.lower():
                    telefone_col = col
                    break
        
        if telefone_col is None:
            print("❌ Nenhuma coluna de telefone encontrada no arquivo de pedidos")
            return pd.DataFrame()
        
        # Limpa telefones
        df['telefone_limpo'] = df[telefone_col].apply(self.clean_phone_number)
        
        # Converte data de fechamento
        df['Data Fechamento'] = pd.to_datetime(df['Data Fechamento'], format='%d/%m/%Y', errors='coerce')
        
        # Remove pedidos sem telefone (mesa/comanda)
        df = df[df['telefone_limpo'] != ""]
        
        # Normaliza bairros
        df['bairro_normalizado'] = df['Bairro'].apply(self.normalize_neighborhood)
        
        # Calcula valor total (pedido + entrega)
        df['valor_total'] = df['Total'] + df['Valor Entrega']
        
        return df
    
    def process_itens(self) -> pd.DataFrame:
        """Processa arquivo de itens vendidos"""
        if 'itens' not in self.dataframes:
            return pd.DataFrame()
        
        df = self.dataframes['itens'].copy()
        
        # Converte data de fechamento
        df['Data Fec. Ped.'] = pd.to_datetime(df['Data Fec. Ped.'], format='%d/%m/%Y', errors='coerce')
        
        return df
    
    def find_new_clients(self) -> pd.DataFrame:
        """Encontra clientes que não estão na lista de contatos"""
        contacts_df = self.process_contacts()
        clientes_df = self.process_clientes()
        
        if contacts_df.empty or clientes_df.empty:
            return pd.DataFrame()
        
        # Filtra clientes com telefones válidos (não vazios e não 0000000000)
        clientes_validos = clientes_df[
            (clientes_df['telefone_limpo'] != "") & 
            (clientes_df['telefone_limpo'] != "0000000000") &
            (clientes_df['telefone_limpo'].str.len() >= 10)
        ].copy()
        
        # Encontra clientes que não estão nos contatos
        clientes_telefones = set(clientes_validos['telefone_limpo'])
        contacts_telefones = set(contacts_df['telefone_limpo'])
        
        novos_telefones = clientes_telefones - contacts_telefones
        
        # Filtra clientes novos
        novos_clientes = clientes_validos[clientes_validos['telefone_limpo'].isin(novos_telefones)].copy()
        
        # Filtra nomes válidos (não vazios, não "-", não "???????")
        novos_clientes = novos_clientes[
            (novos_clientes['primeiro_nome'] != "") &
            (novos_clientes['primeiro_nome'] != "-") &
            (novos_clientes['primeiro_nome'] != "???????") &
            (~novos_clientes['primeiro_nome'].isna())
        ].copy()
        
        # Formata para importar no Google Contacts
        novos_clientes['nome_google'] = 'LT_01 ' + novos_clientes['primeiro_nome']
        
        return novos_clientes[['nome_google', 'telefone_limpo']].rename(columns={
            'nome_google': 'nome',
            'telefone_limpo': 'telefone'
        })
    
    def analyze_inactive_clients(self, dias_inatividade: int = None) -> pd.DataFrame:
        """Analisa clientes inativos"""
        if dias_inatividade is None:
            dias_inatividade = self.config['dias_inatividade']
        
        pedidos_df = self.process_pedidos()
        
        if pedidos_df.empty:
            return pd.DataFrame()
        
        # Data limite
        data_limite = datetime.now() - timedelta(days=dias_inatividade)
        
        # Último pedido por cliente
        ultimo_pedido = pedidos_df.groupby('telefone_limpo')['Data Fechamento'].max().reset_index()
        ultimo_pedido.columns = ['telefone_limpo', 'ultimo_pedido']
        
        # Clientes inativos
        inativos = ultimo_pedido[ultimo_pedido['ultimo_pedido'] < data_limite].copy()
        
        # Adiciona informações do cliente
        clientes_df = self.process_clientes()
        inativos = inativos.merge(clientes_df[['telefone_limpo', 'primeiro_nome', 'bairro_normalizado', 'Qtd. Pedidos']], 
                                on='telefone_limpo', how='left')
        
        # Calcula dias de inatividade
        inativos['dias_inativo'] = (datetime.now() - inativos['ultimo_pedido']).dt.days
        
        return inativos
    
    def analyze_ticket_medio(self, valor_minimo: float = None) -> pd.DataFrame:
        """Analisa clientes por ticket médio"""
        if valor_minimo is None:
            valor_minimo = self.config['ticket_medio_minimo']
        
        pedidos_df = self.process_pedidos()
        
        if pedidos_df.empty:
            return pd.DataFrame()
        
        # Calcula ticket médio por cliente
        ticket_medio = pedidos_df.groupby('telefone_limpo').agg({
            'valor_total': ['mean', 'sum', 'count'],
            'Data Fechamento': 'max'
        }).reset_index()
        
        ticket_medio.columns = ['telefone_limpo', 'ticket_medio', 'valor_total', 'qtd_pedidos', 'ultimo_pedido']
        
        # Filtra por ticket médio mínimo
        clientes_alto_ticket = ticket_medio[ticket_medio['ticket_medio'] >= valor_minimo].copy()
        
        # Adiciona informações do cliente
        clientes_df = self.process_clientes()
        clientes_alto_ticket = clientes_alto_ticket.merge(clientes_df[['telefone_limpo', 'primeiro_nome', 'bairro_normalizado']], 
                                                        on='telefone_limpo', how='left')
        
        return clientes_alto_ticket
    
    def analyze_geographic_data(self) -> Dict[str, Any]:
        """Analisa dados geográficos"""
        pedidos_df = self.process_pedidos()
        
        if pedidos_df.empty:
            return {}
        
        # Análise por bairro
        bairros_analise = pedidos_df.groupby('bairro_normalizado').agg({
            'valor_total': ['sum', 'mean', 'count'],
            'telefone_limpo': 'nunique'
        }).reset_index()
        
        bairros_analise.columns = ['bairro', 'valor_total', 'ticket_medio', 'qtd_pedidos', 'clientes_unicos']
        
        # Top bairros
        top_bairros_valor = bairros_analise.nlargest(10, 'valor_total')
        top_bairros_pedidos = bairros_analise.nlargest(10, 'qtd_pedidos')
        
        return {
            'bairros_analise': bairros_analise,
            'top_bairros_valor': top_bairros_valor,
            'top_bairros_pedidos': top_bairros_pedidos
        }
    
    def analyze_preferences(self) -> Dict[str, Any]:
        """Analisa preferências por cliente"""
        pedidos_df = self.process_pedidos()
        itens_df = self.process_itens()
        
        if pedidos_df.empty or itens_df.empty:
            return {}
        
        # Verifica quais colunas existem no arquivo de itens
        print(f"Colunas disponíveis no arquivo de itens: {list(itens_df.columns)}")
        
        # Mapeia as colunas corretas baseado no que existe
        colunas_itens = []
        if 'Cod. Ped.' in itens_df.columns:
            colunas_itens.append('Cod. Ped.')
        if 'Nome Prod' in itens_df.columns:
            colunas_itens.append('Nome Prod')
        if 'Cat. Prod.' in itens_df.columns:
            colunas_itens.append('Cat. Prod.')
        if 'Qtd.' in itens_df.columns:
            colunas_itens.append('Qtd.')
        # Tenta diferentes variações da coluna de valor
        if 'Valor Tot. Item' in itens_df.columns:
            colunas_itens.append('Valor Tot. Item')
        elif 'Valor. Tot. Item' in itens_df.columns:
            colunas_itens.append('Valor. Tot. Item')
        elif 'Valor Tot Item' in itens_df.columns:
            colunas_itens.append('Valor Tot Item')
        elif 'Valor Total Item' in itens_df.columns:
            colunas_itens.append('Valor Total Item')
        elif 'Valor' in itens_df.columns:
            colunas_itens.append('Valor')
        
        if len(colunas_itens) < 4:
            print(f"Colunas insuficientes encontradas: {colunas_itens}")
            return {}
        
        # Conecta pedidos com itens
        pedidos_itens = pedidos_df[['Código', 'telefone_limpo']].merge(
            itens_df[colunas_itens], 
            left_on='Código', right_on='Cod. Ped.', how='inner'
        )
        
        if pedidos_itens.empty:
            return {}
        
        # Identifica a coluna de valor
        valor_col = None
        for col in ['Valor Tot. Item', 'Valor. Tot. Item', 'Valor Tot Item', 'Valor Total Item', 'Valor']:
            if col in pedidos_itens.columns:
                valor_col = col
                break
        
        if not valor_col:
            print("Nenhuma coluna de valor encontrada")
            return {}
        
        # Preferências por categoria
        preferencias_categoria = pedidos_itens.groupby(['telefone_limpo', 'Cat. Prod.']).agg({
            'Qtd.': 'sum',
            valor_col: 'sum'
        }).reset_index()
        
        # Top categorias por cliente
        top_categorias = preferencias_categoria.groupby('telefone_limpo').apply(
            lambda x: x.nlargest(3, 'Qtd.')
        ).reset_index(drop=True)
        
        # Produtos mais vendidos
        produtos_mais_vendidos = pedidos_itens.groupby('Nome Prod').agg({
            'Qtd.': 'sum',
            valor_col: 'sum'
        }).reset_index().nlargest(20, 'Qtd.')
        
        return {
            'preferencias_categoria': preferencias_categoria,
            'top_categorias': top_categorias,
            'produtos_mais_vendidos': produtos_mais_vendidos
        }
    
    def generate_ai_suggestions(self) -> Dict[str, Any]:
        """Gera sugestões de IA para melhorar vendas"""
        suggestions = {
            'reativacao': [],
            'campanhas_geograficas': [],
            'ofertas_personalizadas': [],
            'melhorias_gerais': []
        }
        
        # Análise de clientes inativos
        inativos = self.analyze_inactive_clients()
        if not inativos.empty:
            total_inativos = len(inativos)
            if total_inativos > 50:
                suggestions['reativacao'].append(
                    f"⚠️ {total_inativos} clientes inativos há mais de {self.config['dias_inatividade']} dias. "
                    f"Sugestão: Campanha de reativação com desconto de 20%"
                )
        
        # Análise geográfica
        geo_data = self.analyze_geographic_data()
        if geo_data:
            top_bairros = geo_data['top_bairros_pedidos'].head(3)
            for _, bairro in top_bairros.iterrows():
                suggestions['campanhas_geograficas'].append(
                    f"📍 {bairro['bairro']}: {bairro['qtd_pedidos']} pedidos. "
                    f"Sugestão: Campanha Meta direcionada para este bairro"
                )
        
        # Análise de ticket médio
        alto_ticket = self.analyze_ticket_medio()
        if not alto_ticket.empty:
            suggestions['ofertas_personalizadas'].append(
                f"💎 {len(alto_ticket)} clientes com ticket médio > R$ {self.config['ticket_medio_minimo']}. "
                f"Sugestão: Ofertas premium exclusivas"
            )
        
        # Análise de preferências
        preferences = self.analyze_preferences()
        if preferences:
            top_produtos = preferences['produtos_mais_vendidos'].head(5)
            suggestions['melhorias_gerais'].append(
                f"🔥 Produtos mais vendidos identificados. "
                f"Sugestão: Promover combos com estes itens"
            )
        
        return suggestions
    
    def save_reports(self) -> List[Path]:
        """Salva todos os relatórios"""
        saved_files = []
        
        # 1. Novos clientes para Google Contacts
        novos_clientes = self.find_new_clients()
        if not novos_clientes.empty:
            file_path = save_dataframe(novos_clientes, self.output_dir, "novos_clientes_google_contacts", "csv")
            saved_files.append(file_path)
        
        # 2. Clientes inativos
        inativos = self.analyze_inactive_clients()
        if not inativos.empty:
            file_path = save_dataframe(inativos, self.output_dir, "clientes_inativos", "xlsx")
            saved_files.append(file_path)
        
        # 3. Clientes alto ticket
        alto_ticket = self.analyze_ticket_medio()
        if not alto_ticket.empty:
            file_path = save_dataframe(alto_ticket, self.output_dir, "clientes_alto_ticket", "xlsx")
            saved_files.append(file_path)
        
        # 4. Análise geográfica
        geo_data = self.analyze_geographic_data()
        if geo_data:
            file_path = save_dataframe(geo_data['bairros_analise'], self.output_dir, "analise_geografica", "xlsx")
            saved_files.append(file_path)
        
        # 5. Preferências
        preferences = self.analyze_preferences()
        if preferences:
            file_path = save_dataframe(preferences['produtos_mais_vendidos'], self.output_dir, "produtos_mais_vendidos", "xlsx")
            saved_files.append(file_path)
        
        return saved_files
