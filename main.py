#!/usr/bin/env python3
"""
ZapCampanhas - Automação para processamento de planilhas Excel
Arquivo principal que orquestra todo o processo
"""

import sys
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from config.settings import INPUT_DIR, OUTPUT_DIR
from src.excel_processor import ExcelProcessor
from src.lead_generator import LeadGenerator
from src.zapchicken_processor import ZapChickenProcessor
from src.zapchicken_ai_advanced import ZapChickenAI
from src.utils import setup_logging

console = Console()
logger = setup_logging()

def show_banner():
    """Exibe o banner do projeto"""
    banner_text = Text("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 ZAPCAMPANHAS 🚀                        ║
║                                                              ║
║    Automação para Processamento de Planilhas Excel          ║
║    Business Intelligence para ZapChicken                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """, style="bold cyan")
    
    panel = Panel(banner_text, border_style="cyan")
    console.print(panel)

@click.group()
@click.version_option(version="2.0.0")
def cli():
    """ZapCampanhas - Automação para processamento de planilhas Excel"""
    pass

@cli.command()
@click.option('--input-dir', '-i', default=str(INPUT_DIR), 
              help='Diretório com as planilhas de entrada')
@click.option('--output-dir', '-o', default=str(OUTPUT_DIR), 
              help='Diretório para salvar os resultados')
@click.option('--analyze', '-a', is_flag=True, 
              help='Analisa as planilhas sem processar')
@click.option('--merge-strategy', '-m', default='union', 
              type=click.Choice(['union', 'intersection']),
              help='Estratégia para combinar planilhas')
def process(input_dir, output_dir, analyze, merge_strategy):
    """Processa planilhas Excel e gera lista de leads (modo genérico)"""
    show_banner()
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Verifica se o diretório de entrada existe
    if not input_path.exists():
        console.print(f"[red]❌ Diretório de entrada não encontrado: {input_path}")
        return
    
    # Verifica se há arquivos Excel
    excel_files = list(input_path.glob("*.xlsx")) + list(input_path.glob("*.xls"))
    if not excel_files:
        console.print(f"[yellow]⚠️  Nenhum arquivo Excel encontrado em: {input_path}")
        console.print("[yellow]Coloque suas planilhas na pasta 'data/input' e tente novamente.")
        return
    
    console.print(f"[green]📁 Diretório de entrada: {input_path}")
    console.print(f"[green]📁 Diretório de saída: {output_path}")
    console.print(f"[green]📊 Arquivos Excel encontrados: {len(excel_files)}")
    
    # Inicializa processadores
    processor = ExcelProcessor(input_path)
    generator = LeadGenerator(output_path)
    
    try:
        # Carrega todas as planilhas
        console.print("\n[bold cyan]📥 CARREGANDO PLANILHAS...[/bold cyan]")
        dataframes = processor.load_all_excel_files()
        
        if not dataframes:
            console.print("[red]❌ Nenhuma planilha foi carregada com sucesso!")
            return
        
        # Exibe informações dos arquivos carregados
        processor.display_loaded_files()
        
        if analyze:
            console.print("\n[bold cyan]🔍 ANÁLISE DETALHADA...[/bold cyan]")
            processor.analyze_dataframes()
            return
        
        # Encontra colunas de telefone
        console.print("\n[bold cyan]📱 PROCURANDO COLUNAS DE TELEFONE...[/bold cyan]")
        phone_columns = processor.find_phone_columns()
        
        if not phone_columns:
            console.print("[yellow]⚠️  Nenhuma coluna de telefone identificada automaticamente!")
            console.print("[yellow]O processamento continuará, mas pode não gerar resultados válidos.")
        
        # Limpa dados de telefone
        console.print("\n[bold cyan]🧹 LIMPANDO DADOS...[/bold cyan]")
        cleaned_data = processor.clean_phone_data(phone_columns)
        
        # Combina planilhas
        console.print(f"\n[bold cyan]🔗 COMBINANDO PLANILHAS ({merge_strategy})...[/bold cyan]")
        merged_df = processor.merge_dataframes(cleaned_data, merge_strategy)
        
        if merged_df.empty:
            console.print("[red]❌ Nenhum dado válido encontrado após o processamento!")
            return
        
        # Padroniza colunas
        console.print("\n[bold cyan]📋 PADRONIZANDO COLUNAS...[/bold cyan]")
        standardized_df = generator.standardize_columns(merged_df)
        
        # Cria formato para WhatsApp
        console.print("\n[bold cyan]📱 CRIANDO FORMATO WHATSAPP...[/bold cyan]")
        whatsapp_df = generator.create_whatsapp_format(standardized_df)
        
        if whatsapp_df.empty:
            console.print("[red]❌ Nenhum lead válido com telefone encontrado!")
            return
        
        # Gera segmentos
        console.print("\n[bold cyan]📊 GERANDO SEGMENTOS...[/bold cyan]")
        segments = generator.generate_segments(whatsapp_df, 'cidade' if 'cidade' in whatsapp_df.columns else None)
        
        # Cria relatório
        report = generator.create_summary_report(whatsapp_df, segments)
        
        # Salva resultados
        console.print("\n[bold cyan]💾 SALVANDO RESULTADOS...[/bold cyan]")
        saved_files = generator.save_leads(whatsapp_df, "leads_whatsapp", "xlsx", True)
        
        # Exibe resumo
        generator.display_leads_summary(whatsapp_df, report)
        
        console.print(f"\n[bold green]✅ PROCESSAMENTO CONCLUÍDO![/bold green]")
        console.print(f"[green]📁 Arquivos salvos em: {output_path}")
        console.print(f"[green]📊 Total de leads processados: {len(whatsapp_df)}")
        
        # Lista arquivos salvos
        console.print("\n[bold]📄 Arquivos gerados:[/bold]")
        for file_path in saved_files:
            console.print(f"  📄 {file_path.name}")
        
    except Exception as e:
        console.print(f"[red]❌ Erro durante o processamento: {e}")
        logger.error(f"Erro no processamento: {e}", exc_info=True)

@cli.command()
@click.option('--input-dir', '-i', default=str(INPUT_DIR), 
              help='Diretório com as planilhas de entrada')
@click.option('--output-dir', '-o', default=str(OUTPUT_DIR), 
              help='Diretório para salvar os resultados')
@click.option('--dias-inatividade', '-d', default=30, type=int,
              help='Dias para considerar cliente inativo')
@click.option('--ticket-minimo', '-t', default=50.0, type=float,
              help='Ticket médio mínimo para análise')
def zapchicken(input_dir, output_dir, dias_inatividade, ticket_minimo):
    """Processa dados específicos da ZapChicken com Business Intelligence"""
    show_banner()
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Verifica se o diretório de entrada existe
    if not input_path.exists():
        console.print(f"[red]❌ Diretório de entrada não encontrado: {input_path}")
        return
    
    console.print(f"[green]📁 Diretório de entrada: {input_path}")
    console.print(f"[green]📁 Diretório de saída: {output_path}")
    console.print(f"[green]⚙️  Dias de inatividade: {dias_inatividade}")
    console.print(f"[green]💰 Ticket médio mínimo: R$ {ticket_minimo:.2f}")
    
    # Inicializa processador da ZapChicken
    processor = ZapChickenProcessor(input_path, output_path)
    
    # Configura parâmetros
    processor.config['dias_inatividade'] = dias_inatividade
    processor.config['ticket_medio_minimo'] = ticket_minimo
    
    try:
        # Carrega arquivos da ZapChicken
        console.print("\n[bold cyan]📥 CARREGANDO ARQUIVOS ZAPCHICKEN...[/bold cyan]")
        dataframes = processor.load_zapchicken_files()
        
        if not dataframes:
            console.print("[red]❌ Nenhum arquivo da ZapChicken foi carregado!")
            console.print("[yellow]Certifique-se de que os arquivos estão na pasta de entrada:")
            console.print("[yellow]• contacts.csv (Google Contacts)")
            console.print("[yellow]• Lista-Clientes*.xls*")
            console.print("[yellow]• Todos os pedidos*.xls*")
            console.print("[yellow]• Historico_Itens_Vendidos*.xls*")
            return
        
        # Exibe arquivos carregados
        console.print(f"\n[bold green]✅ {len(dataframes)} arquivos carregados com sucesso![/bold green]")
        
        # Processa dados
        console.print("\n[bold cyan]🔍 PROCESSANDO DADOS...[/bold cyan]")
        
        # 1. Novos clientes
        console.print("\n[bold]1️⃣  Analisando novos clientes...[/bold]")
        novos_clientes = processor.find_new_clients()
        if not novos_clientes.empty:
            console.print(f"[green]✓[/green] {len(novos_clientes)} novos clientes encontrados")
        else:
            console.print("[yellow]ℹ️  Nenhum novo cliente encontrado")
        
        # 2. Clientes inativos
        console.print("\n[bold]2️⃣  Analisando clientes inativos...[/bold]")
        inativos = processor.analyze_inactive_clients()
        if not inativos.empty:
            console.print(f"[red]⚠️  {len(inativos)} clientes inativos há mais de {dias_inatividade} dias")
        else:
            console.print("[green]✓[/green] Nenhum cliente inativo encontrado")
        
        # 3. Clientes alto ticket
        console.print("\n[bold]3️⃣  Analisando ticket médio...[/bold]")
        alto_ticket = processor.analyze_ticket_medio()
        if not alto_ticket.empty:
            console.print(f"[blue]💎 {len(alto_ticket)} clientes com ticket médio > R$ {ticket_minimo:.2f}")
        else:
            console.print("[yellow]ℹ️  Nenhum cliente com alto ticket encontrado")
        
        # 4. Análise geográfica
        console.print("\n[bold]4️⃣  Analisando dados geográficos...[/bold]")
        geo_data = processor.analyze_geographic_data()
        if geo_data:
            console.print(f"[green]✓[/green] {len(geo_data['bairros_analise'])} bairros analisados")
        else:
            console.print("[yellow]ℹ️  Dados geográficos insuficientes")
        
        # 5. Preferências
        console.print("\n[bold]5️⃣  Analisando preferências...[/bold]")
        preferences = processor.analyze_preferences()
        if preferences:
            console.print(f"[green]✓[/green] {len(preferences['produtos_mais_vendidos'])} produtos analisados")
        else:
            console.print("[yellow]ℹ️  Dados de preferências insuficientes")
        
        # 6. Sugestões de IA
        console.print("\n[bold]6️⃣  Gerando sugestões de IA...[/bold]")
        suggestions = processor.generate_ai_suggestions()
        
        # Exibe sugestões
        console.print("\n[bold cyan]🤖 SUGESTÕES DE IA:[/bold cyan]")
        for category, items in suggestions.items():
            if items:
                console.print(f"\n[bold]{category.upper()}:[/bold]")
                for item in items:
                    console.print(f"  • {item}")
        
        # 7. Salva relatórios
        console.print("\n[bold cyan]💾 SALVANDO RELATÓRIOS...[/bold cyan]")
        saved_files = processor.save_reports()
        
        console.print(f"\n[bold green]✅ PROCESSAMENTO ZAPCHICKEN CONCLUÍDO![/bold green]")
        console.print(f"[green]📁 {len(saved_files)} relatórios salvos em: {output_path}")
        
        # Lista arquivos salvos
        console.print("\n[bold]📄 Relatórios gerados:[/bold]")
        for file_path in saved_files:
            console.print(f"  📄 {file_path.name}")
        
        # Sugere próximo passo
        console.print(f"\n[bold cyan]🎯 PRÓXIMO PASSO:[/bold cyan]")
        console.print(f"[yellow]Execute: python main.py chat")
        console.print(f"[yellow]Para usar o assistente de IA e fazer perguntas sobre seus dados!")
        
    except Exception as e:
        console.print(f"[red]❌ Erro durante o processamento: {e}")
        logger.error(f"Erro no processamento ZapChicken: {e}", exc_info=True)

@cli.command()
@click.option('--input-dir', '-i', default=str(INPUT_DIR), 
              help='Diretório com as planilhas de entrada')
@click.option('--output-dir', '-o', default=str(OUTPUT_DIR), 
              help='Diretório para salvar os resultados')
def chat(input_dir, output_dir):
    """Inicia o chat com IA para análise dos dados da ZapChicken"""
    show_banner()
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    console.print("[bold cyan]🤖 INICIANDO ZAPCHICKEN AI...[/bold cyan]")
    
    # Inicializa processador
    processor = ZapChickenProcessor(input_path, output_path)
    
    try:
        # Carrega dados
        console.print("\n[bold]📥 Carregando dados...[/bold]")
        dataframes = processor.load_zapchicken_files()
        
        if not dataframes:
            console.print("[red]❌ Nenhum arquivo da ZapChicken encontrado!")
            console.print("[yellow]Execute primeiro: python main.py zapchicken")
            return
        
        # Inicializa IA
        ai = ZapChickenAI(processor)
        
        # Inicia chat
        ai.chat_interface()
        
    except Exception as e:
        console.print(f"[red]❌ Erro ao iniciar chat: {e}")
        logger.error(f"Erro no chat: {e}", exc_info=True)

@cli.command()
@click.option('--input-dir', '-i', default=str(INPUT_DIR), 
              help='Diretório com as planilhas de entrada')
def analyze(input_dir):
    """Analisa as planilhas sem processar"""
    show_banner()
    
    input_path = Path(input_dir)
    
    if not input_path.exists():
        console.print(f"[red]❌ Diretório de entrada não encontrado: {input_path}")
        return
    
    processor = ExcelProcessor(input_path)
    
    try:
        console.print("\n[bold cyan]📥 CARREGANDO PLANILHAS...[/bold cyan]")
        dataframes = processor.load_all_excel_files()
        
        if not dataframes:
            console.print("[red]❌ Nenhuma planilha foi carregada!")
            return
        
        processor.display_loaded_files()
        processor.analyze_dataframes()
        
    except Exception as e:
        console.print(f"[red]❌ Erro durante a análise: {e}")
        logger.error(f"Erro na análise: {e}", exc_info=True)

@cli.command()
def setup():
    """Configura o ambiente inicial"""
    show_banner()
    
    console.print("[bold cyan]🔧 CONFIGURANDO AMBIENTE...[/bold cyan]")
    
    # Cria diretórios necessários
    directories = [INPUT_DIR, OUTPUT_DIR]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]✓[/green] Diretório criado: {directory}")
    
    console.print(f"\n[bold green]✅ AMBIENTE CONFIGURADO![/bold green]")
    console.print(f"[yellow]📁 Coloque suas planilhas Excel em: {INPUT_DIR}")
    console.print(f"[yellow]📁 Os resultados serão salvos em: {OUTPUT_DIR}")
    console.print(f"\n[bold cyan]🎯 PARA ZAPCHICKEN:[/bold cyan]")
    console.print(f"[yellow]1. Coloque os 4 arquivos da ZapChicken em: {INPUT_DIR}")
    console.print(f"[yellow]2. Execute: python main.py zapchicken")
    console.print(f"[yellow]3. Para chat com IA: python main.py chat")
    console.print(f"[yellow]4. Para interface web: python main.py web")

@cli.command()
def web():
    """Inicia a interface web do ZapCampanhas"""
    show_banner()

    console.print("[bold cyan]🌐 INICIANDO INTERFACE WEB...[/bold cyan]")
    console.print("📱 Acesse: http://localhost:5000")
    console.print("🔄 Pressione Ctrl+C para parar o servidor")

    try:
        from web_app_flask import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        console.print(f"[red]❌ Erro ao importar web_app_flask: {e}[/red]")
        console.print("[yellow]💡 Execute: pip install flask[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Erro ao iniciar servidor web: {e}[/red]")

if __name__ == '__main__':
    cli()

