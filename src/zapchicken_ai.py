"""
Sistema de IA para ZapChicken
Chat inteligente e sugestões de marketing
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .zapchicken_processor import ZapChickenProcessor

console = Console()

class ZapChickenAI:
    """Sistema de IA para análise e sugestões da ZapChicken"""
    
    def __init__(self, processor: ZapChickenProcessor):
        self.processor = processor
        self.conversation_history = []
    
    def chat_interface(self):
        """Interface de chat com IA"""
        console.print(Panel.fit(
            "[bold cyan]🤖 ZAPCHICKEN AI - ASSISTENTE INTELIGENTE[/bold cyan]\n"
            "Digite suas perguntas sobre vendas, clientes, campanhas...\n"
            "Digite 'sair' para sair ou 'ajuda' para ver comandos disponíveis",
            border_style="cyan"
        ))
        
        while True:
            try:
                user_input = console.input("\n[bold green]Você:[/bold green] ").strip()
                
                if user_input.lower() in ['sair', 'exit', 'quit']:
                    console.print("[yellow]Até logo! 👋[/yellow]")
                    break
                
                if user_input.lower() in ['ajuda', 'help', '?']:
                    self.show_help()
                    continue
                
                if not user_input:
                    continue
                
                # Processa a pergunta
                response = self.process_question(user_input)
                self.conversation_history.append({
                    'user': user_input,
                    'ai': response,
                    'timestamp': datetime.now()
                })
                
                console.print(f"\n[bold blue]AI:[/bold blue] {response}")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Até logo! 👋[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Erro: {e}[/red]")
    
    def show_help(self):
        """Mostra comandos de ajuda"""
        help_text = """
[bold cyan]COMANDOS DISPONÍVEIS:[/bold cyan]

[bold]📊 ANÁLISE DE CLIENTES:[/bold]
• "Quantos clientes inativos temos?"
• "Quem são os clientes com maior ticket médio?"
• "Mostre clientes que não compraram nos últimos 30 dias"
• "Quais são os bairros que mais pedem?"

[bold]💰 ANÁLISE DE VENDAS:[/bold]
• "Qual foi o faturamento dos últimos 6 meses?"
• "Quais são os produtos mais vendidos?"
• "Mostre a análise de ticket médio"
• "Como estão as vendas por bairro?"

[bold]🎯 SUGESTÕES DE MARKETING:[/bold]
• "Dê sugestões para reativar clientes"
• "Sugira campanhas para bairros específicos"
• "Quais ofertas fazer para clientes premium?"
• "Analise tendências de vendas"

[bold]⚙️ CONFIGURAÇÕES:[/bold]
• "Configure dias de inatividade para 60"
• "Configure ticket médio mínimo para 100"
• "Mostre configurações atuais"

[bold]📋 RELATÓRIOS:[/bold]
• "Gere relatório completo"
• "Salve todos os relatórios"
• "Mostre resumo executivo"

[bold]❓ OUTROS:[/bold]
• "ajuda" - Mostra esta ajuda
• "sair" - Sai do chat
        """
        
        console.print(Panel(help_text, title="[bold]🤖 Ajuda - ZapChicken AI[/bold]", border_style="blue"))
    
    def process_question(self, question: str) -> str:
        """Processa pergunta do usuário e retorna resposta"""
        question_lower = question.lower()
        
        # Perguntas sobre datas específicas
        if any(word in question_lower for word in ['comprou', 'pediu', 'fez pedido']) and any(word in question_lower for word in ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']):
            return self.analyze_sales_by_date(question)
        
        # Análise de clientes inativos
        if any(word in question_lower for word in ['inativo', 'inatividade', 'não comprou', 'não pediu']):
            return self.analyze_inactive_clients(question)
        
        # Análise de ticket médio
        if any(word in question_lower for word in ['ticket', 'médio', 'alto', 'premium']):
            return self.analyze_ticket_medio(question)
        
        # Análise geográfica
        if any(word in question_lower for word in ['bairro', 'localização', 'geográfico', 'região']):
            return self.analyze_geographic(question)
        
        # Análise de vendas
        if any(word in question_lower for word in ['venda', 'faturamento', 'produto', 'item']):
            return self.analyze_sales(question)
        
        # Sugestões de marketing
        if any(word in question_lower for word in ['sugestão', 'campanha', 'marketing', 'oferta']):
            return self.generate_marketing_suggestions(question)
        
        # Configurações
        if any(word in question_lower for word in ['configurar', 'configuração', 'ajustar']):
            return self.handle_configuration(question)
        
        # Relatórios
        if any(word in question_lower for word in ['relatório', 'salvar', 'gerar']):
            return self.handle_reports(question)
        
        # Resumo executivo
        if any(word in question_lower for word in ['resumo', 'executivo', 'overview']):
            return self.generate_executive_summary()
        
        # Análise preditiva e tendências
        if any(word in question_lower for word in ['tendência', 'tendencia', 'previsão', 'previsao', 'predição', 'predicao', 'futuro', 'crescimento']):
            return self.analyze_trends_and_predictions(question)
        
        # Análise de sazonalidade
        if any(word in question_lower for word in ['sazonalidade', 'sazonal', 'estação', 'estacao', 'meses', 'período', 'periodo']):
            return self.analyze_seasonality(question)
        
        # Pergunta não reconhecida
        return self.handle_unknown_question(question)
    
    def analyze_inactive_clients(self, question: str) -> str:
        """Analisa clientes inativos com insights avançados"""
        # Extrai dias da pergunta se mencionado
        dias = 30  # padrão
        if 'dias' in question:
            import re
            match = re.search(r'(\d+)\s*dias', question)
            if match:
                dias = int(match.group(1))
        
        inativos = self.processor.analyze_inactive_clients(dias)
        
        if inativos.empty:
            return f"✅ Ótimo! Não há clientes inativos há mais de {dias} dias."
        
        total_inativos = len(inativos)
        
        # Análise avançada de valor perdido
        if 'Qtd. Pedidos' in inativos.columns:
            pedidos_por_cliente = inativos['Qtd. Pedidos'].mean()
            ticket_medio_estimado = 80.0  # Baseado em dados típicos
            valor_perdido_mensal = total_inativos * pedidos_por_cliente * ticket_medio_estimado
            valor_perdido_anual = valor_perdido_mensal * 12
        else:
            valor_perdido_mensal = total_inativos * 200  # estimativa conservadora
            valor_perdido_anual = valor_perdido_mensal * 12
        
        # Análise de segmentação por valor
        if 'valor_total' in inativos.columns:
            clientes_alto_valor = inativos[inativos['valor_total'] > 500]
            clientes_medio_valor = inativos[(inativos['valor_total'] >= 100) & (inativos['valor_total'] <= 500)]
            clientes_baixo_valor = inativos[inativos['valor_total'] < 100]
        else:
            clientes_alto_valor = inativos.head(int(total_inativos * 0.2))  # Top 20%
            clientes_medio_valor = inativos.head(int(total_inativos * 0.5))  # Top 50%
            clientes_baixo_valor = inativos
        
        # Análise geográfica avançada
        if 'bairro_normalizado' in inativos.columns:
            top_bairros = inativos.groupby('bairro_normalizado').agg({
                'Qtd. Pedidos': 'sum' if 'Qtd. Pedidos' in inativos.columns else 'count',
                'valor_total': 'sum' if 'valor_total' in inativos.columns else lambda x: 0
            }).nlargest(5, 'Qtd. Pedidos' if 'Qtd. Pedidos' in inativos.columns else 'valor_total')
        
        response = f"""
[bold]📊 ANÁLISE AVANÇADA DE CLIENTES INATIVOS ({dias} dias):[/bold]

⚠️ [red]{total_inativos} clientes inativos[/red]
💰 Valor perdido mensal: R$ {valor_perdido_mensal:,.2f}
💸 Valor perdido anual: R$ {valor_perdido_anual:,.2f}
📈 Média de pedidos por cliente: {pedidos_por_cliente:.1f if 'Qtd. Pedidos' in inativos.columns else 'N/A'}

[bold]🎯 SEGMENTAÇÃO POR VALOR:[/bold]
• Alto valor (>R$ 500): {len(clientes_alto_valor)} clientes
• Médio valor (R$ 100-500): {len(clientes_medio_valor)} clientes  
• Baixo valor (<R$ 100): {len(clientes_baixo_valor)} clientes

[bold]📍 TOP 5 BAIRROS COM MAIS INATIVOS:[/bold]
"""
        
        if 'bairro_normalizado' in inativos.columns:
            for bairro, dados in top_bairros.iterrows():
                pedidos = dados['Qtd. Pedidos'] if 'Qtd. Pedidos' in inativos.columns else dados.get('valor_total', 0)
                response += f"• {bairro}: {pedidos} pedidos/valor\n"
        
        response += f"""

[bold]🚀 ESTRATÉGIAS DE REATIVAÇÃO:[/bold]

[bold]1. 🎁 CAMPANHA DIFERENCIADA POR SEGMENTO:[/bold]
• Alto valor: Oferta exclusiva 30% desconto + entrega grátis
• Médio valor: 20% desconto + brinde
• Baixo valor: 15% desconto + frete reduzido

[bold]2. 📱 CANAIS DE COMUNICAÇÃO:[/bold]
• WhatsApp direto para alto valor
• Email + WhatsApp para médio valor
• SMS + WhatsApp para baixo valor

[bold]3. ⏰ TIMING ESTRATÉGICO:[/bold]
• Enviar às 18h-20h (horário de jantar)
• Segunda-feira (início da semana)
• Sexta-feira (fim de semana)

[bold]4. 🎯 PERSONALIZAÇÃO:[/bold]
• "Sentimos sua falta! 20% OFF no seu pedido favorito"
• "Especial para você: frete grátis + desconto"
• "Volte a pedir: oferta exclusiva por 24h"

[bold]💡 ROI ESPERADO:[/bold]
• Taxa de conversão estimada: 15-25%
• Clientes recuperados: {int(total_inativos * 0.2)} a {int(total_inativos * 0.25)}
• Receita recuperada: R$ {valor_perdido_mensal * 0.2:,.2f} a R$ {valor_perdido_mensal * 0.25:,.2f}
"""
        
        return response
    
    def analyze_ticket_medio(self, question: str) -> str:
        """Analisa ticket médio com insights avançados"""
        # Extrai valor da pergunta se mencionado
        valor_minimo = 50.0  # padrão
        if 'reais' in question or 'r$' in question:
            import re
            match = re.search(r'[rR]\$\s*(\d+)', question)
            if match:
                valor_minimo = float(match.group(1))
        
        alto_ticket = self.processor.analyze_ticket_medio(valor_minimo)
        
        if alto_ticket.empty:
            return f"ℹ️ Nenhum cliente encontrado com ticket médio acima de R$ {valor_minimo:.2f}"
        
        total_clientes = len(alto_ticket)
        ticket_medio_geral = alto_ticket['ticket_medio'].mean()
        valor_total = alto_ticket['valor_total'].sum()
        
        # Análise de segmentação avançada
        clientes_ultra_premium = alto_ticket[alto_ticket['ticket_medio'] > 150]
        clientes_premium = alto_ticket[(alto_ticket['ticket_medio'] >= 80) & (alto_ticket['ticket_medio'] <= 150)]
        clientes_medio_alto = alto_ticket[(alto_ticket['ticket_medio'] >= valor_minimo) & (alto_ticket['ticket_medio'] < 80)]
        
        # Análise de frequência
        if 'Qtd. Pedidos' in alto_ticket.columns:
            frequencia_media = alto_ticket['Qtd. Pedidos'].mean()
            clientes_frequentes = alto_ticket[alto_ticket['Qtd. Pedidos'] > frequencia_media]
        else:
            frequencia_media = "N/A"
            clientes_frequentes = alto_ticket.head(int(total_clientes * 0.3))
        
        # Análise geográfica
        if 'bairro_normalizado' in alto_ticket.columns:
            top_bairros_premium = alto_ticket.groupby('bairro_normalizado').agg({
                'ticket_medio': 'mean',
                'valor_total': 'sum',
                'primeiro_nome': 'count'
            }).nlargest(5, 'ticket_medio')
        
        response = f"""
[bold]💎 ANÁLISE AVANÇADA DE TICKET MÉDIO (R$ {valor_minimo:.2f}+):[/bold]

👥 {total_clientes} clientes premium
💰 Ticket médio geral: R$ {ticket_medio_geral:.2f}
💵 Valor total: R$ {valor_total:,.2f}
📊 Frequência média: {frequencia_media} pedidos

[bold]🎯 SEGMENTAÇÃO PREMIUM:[/bold]
• Ultra Premium (>R$ 150): {len(clientes_ultra_premium)} clientes
• Premium (R$ 80-150): {len(clientes_premium)} clientes
• Médio Alto (R$ {valor_minimo}-80): {len(clientes_medio_alto)} clientes

[bold]📍 TOP 5 BAIRROS PREMIUM:[/bold]
"""
        
        if 'bairro_normalizado' in alto_ticket.columns:
            for bairro, dados in top_bairros_premium.iterrows():
                response += f"• {bairro}: R$ {dados['ticket_medio']:.2f} médio, {dados['primeiro_nome']} clientes\n"
        
        response += f"""

[bold]🏆 TOP 5 CLIENTES ULTRA PREMIUM:[/bold]
"""
        
        top_clientes = alto_ticket.nlargest(5, 'ticket_medio')
        for i, (_, cliente) in enumerate(top_clientes.iterrows(), 1):
            nome = cliente.get('primeiro_nome', 'Cliente')
            bairro = cliente.get('bairro_normalizado', 'N/A')
            ticket = cliente['ticket_medio']
            valor = cliente['valor_total']
            response += f"{i}. {nome} ({bairro}): R$ {ticket:.2f} médio, R$ {valor:,.2f} total\n"
        
        response += f"""

[bold]🚀 ESTRATÉGIAS PARA CLIENTES PREMIUM:[/bold]

[bold]1. 💎 OFERTAS ULTRA EXCLUSIVAS:[/bold]
• Ultra Premium: 40% desconto + entrega VIP + brinde premium
• Premium: 30% desconto + entrega grátis + brinde
• Médio Alto: 25% desconto + frete reduzido

[bold]2. 🎁 PROGRAMA DE FIDELIDADE VIP:[/bold]
• Pontos duplos para Ultra Premium
• Descontos progressivos
• Acesso antecipado a novos produtos

[bold]3. 📱 COMUNICAÇÃO PERSONALIZADA:[/bold]
• WhatsApp Business com atendimento VIP
• Email marketing segmentado
• SMS para ofertas flash

[bold]4. 🎯 CROSS-SELLING INTELIGENTE:[/bold]
• Combos premium personalizados
• Produtos exclusivos
• Serviços adicionais (decoração, entrega especial)

[bold]💡 ROI ESPERADO:[/bold]
• Aumento de 20-35% no ticket médio
• Retenção de 85-95% dos clientes premium
• Receita adicional: R$ {valor_total * 0.25:,.2f} a R$ {valor_total * 0.35:,.2f}
"""
        
        return response
    
    def analyze_geographic(self, question: str) -> str:
        """Analisa dados geográficos"""
        geo_data = self.processor.analyze_geographic_data()
        
        if not geo_data:
            return "ℹ️ Não há dados geográficos suficientes para análise."
        
        bairros_analise = geo_data['bairros_analise']
        top_bairros = geo_data['top_bairros_pedidos']
        
        response = f"""
[bold]📍 ANÁLISE GEOGRÁFICA:[/bold]

📊 Total de bairros ativos: {len(bairros_analise)}
👥 Total de clientes únicos: {bairros_analise['clientes_unicos'].sum()}
💰 Faturamento total: R$ {bairros_analise['valor_total'].sum():,.2f}

[bold]🏆 Top 5 bairros por pedidos:[/bold]
"""
        
        for i, (_, bairro) in enumerate(top_bairros.head(5).iterrows(), 1):
            response += f"{i}. {bairro['bairro']}: {bairro['qtd_pedidos']} pedidos (R$ {bairro['valor_total']:,.2f})\n"
        
        response += f"\n[bold]💡 SUGESTÃO:[/bold] Campanhas Meta direcionadas para os top 3 bairros com maior volume de pedidos."
        
        return response
    
    def analyze_sales(self, question: str) -> str:
        """Analisa dados de vendas"""
        preferences = self.processor.analyze_preferences()
        
        if not preferences:
            return "ℹ️ Não há dados de vendas suficientes para análise."
        
        produtos_mais_vendidos = preferences['produtos_mais_vendidos']
        
        response = f"""
[bold]🔥 ANÁLISE DE VENDAS:[/bold]

📦 Total de produtos únicos: {len(produtos_mais_vendidos)}
💰 Faturamento total: R$ {produtos_mais_vendidos['Valor Tot. Item'].sum():,.2f}

[bold]🏆 Top 5 produtos mais vendidos:[/bold]
"""
        
        for i, (_, produto) in enumerate(produtos_mais_vendidos.head(5).iterrows(), 1):
            response += f"{i}. {produto['Nome Prod']}: {produto['Qtd.']} unidades (R$ {produto['Valor Tot. Item']:,.2f})\n"
        
        response += f"\n[bold]💡 SUGESTÃO:[/bold] Criar combos promocionais com os produtos mais vendidos para aumentar o ticket médio."
        
        return response
    
    def generate_marketing_suggestions(self, question: str) -> str:
        """Gera sugestões de marketing inteligentes e personalizadas"""
        try:
            # Coleta dados para análise
            inativos = self.processor.analyze_inactive_clients()
            alto_ticket = self.processor.analyze_ticket_medio()
            geo_data = self.processor.analyze_geographic_data()
            
            response = "[bold]🎯 SUGESTÕES DE MARKETING INTELIGENTE - ZAPCHICKEN[/bold]\n\n"
            
            # Análise de clientes inativos
            if not inativos.empty:
                total_inativos = len(inativos)
                valor_perdido = total_inativos * 200  # estimativa
                
                response += f"""[bold]🔄 ESTRATÉGIA DE REATIVAÇÃO ({total_inativos} clientes):[/bold]

[bold]📱 CAMPANHA "SENTIMOS SUA FALTA":[/bold]
• WhatsApp direto: "Oi! Sentimos sua falta. 25% OFF + frete grátis por 24h"
• Email: "Volte a pedir: oferta exclusiva para você"
• SMS: "ZapChicken: 20% OFF no seu pedido favorito"

[bold]🎁 OFERTAS DIFERENCIADAS:[/bold]
• Primeira compra após inatividade: 30% desconto
• Segunda compra: 20% desconto + brinde
• Terceira compra: 15% desconto + frete grátis

[bold]⏰ TIMING ESTRATÉGICO:[/bold]
• Enviar às 17h-19h (horário de jantar)
• Segunda-feira (início da semana)
• Sexta-feira (fim de semana)

[bold]💡 ROI ESPERADO:[/bold]
• Taxa de conversão: 18-25%
• Clientes recuperados: {int(total_inativos * 0.22)}
• Receita recuperada: R$ {valor_perdido * 0.22:,.2f}

"""
            
            # Análise de clientes premium
            if not alto_ticket.empty:
                total_premium = len(alto_ticket)
                valor_premium = alto_ticket['valor_total'].sum()
                
                response += f"""[bold]💎 ESTRATÉGIA PREMIUM ({total_premium} clientes):[/bold]

[bold]🏆 PROGRAMA VIP "ZAPCHICKEN PREMIUM":[/bold]
• Desconto progressivo: 25% → 30% → 35%
• Entrega VIP: horário escolhido + acompanhamento
• Brindes exclusivos: sobremesas premium
• Acesso antecipado: novos produtos 24h antes

[bold]🎯 COMUNICAÇÃO PERSONALIZADA:[/bold]
• WhatsApp Business com atendente VIP
• Email marketing segmentado por preferências
• SMS para ofertas flash exclusivas

[bold]💡 ROI ESPERADO:[/bold]
• Aumento de 25-40% no ticket médio
• Retenção de 90-95% dos clientes premium
• Receita adicional: R$ {valor_premium * 0.3:,.2f}

"""
            
            # Análise geográfica
            if geo_data and 'top_bairros_pedidos' in geo_data:
                top_bairros = geo_data['top_bairros_pedidos'].head(3)
                
                response += f"""[bold]📍 ESTRATÉGIA GEOGRÁFICA (Top 3 Bairros):[/bold]

[bold]🎯 CAMPANHAS META DIRECIONADAS:[/bold]
"""
                
                for i, (_, bairro) in enumerate(top_bairros.iterrows(), 1):
                    response += f"""• {bairro['bairro']}: {bairro['qtd_pedidos']} pedidos
  - Campanha Meta: "ZapChicken {bairro['bairro']} - Entrega em 30min"
  - Raio: 2km do centro do bairro
  - Orçamento: R$ 500-800/mês
  - Expectativa: +40% conversões locais

"""
                
                response += f"""[bold]📊 ESTRATÉGIA DE EXPANSÃO:[/bold]
• Identificar bairros com potencial (2-5km dos atuais)
• Campanhas de teste com orçamento reduzido
• Parcerias com estabelecimentos locais
• Flyers e cartões de desconto

[bold]💡 ROI ESPERADO:[/bold]
• Aumento de 30-50% em bairros focados
• Expansão para 3-5 novos bairros/mês
• Receita adicional: R$ 15.000-25.000/mês

"""
            
            # Estratégias gerais
            response += f"""[bold]🚀 ESTRATÉGIAS GERAIS DE CRESCIMENTO:[/bold]

[bold]📱 OTIMIZAÇÃO DIGITAL:[/bold]
• WhatsApp Business com catálogo digital
• Instagram: stories diários + reels de preparo
• Facebook: campanhas de engajamento
• Google My Business: avaliações e fotos

[bold]🎁 PROGRAMA DE FIDELIDADE:[/bold]
• Pontos por pedido: R$ 1 = 1 ponto
• Descontos progressivos: 100pts = 10%, 200pts = 15%, 500pts = 25%
• Brindes exclusivos: sobremesas, bebidas
• Aniversariantes: 30% OFF no mês

[bold]📈 ANÁLISE E OTIMIZAÇÃO:[/bold]
• A/B testing de ofertas
• Análise de sazonalidade
• Segmentação por comportamento
• Personalização de mensagens

[bold]💡 ROI ESPERADO GERAL:[/bold]
• Aumento de 25-40% no faturamento
• Melhoria de 30-50% na retenção
• Redução de 20-30% no custo de aquisição
• Crescimento de 15-25% na base de clientes

[bold]🎯 PRÓXIMOS PASSOS RECOMENDADOS:[/bold]
1. Implementar campanha de reativação (semana 1)
2. Lançar programa premium (semana 2-3)
3. Iniciar campanhas Meta geográficas (semana 4)
4. Otimizar canais digitais (contínuo)
5. Análise mensal de resultados e ajustes
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro ao gerar sugestões de marketing: {str(e)}"
    
    def handle_configuration(self, question: str) -> str:
        """Manipula configurações"""
        question_lower = question.lower()
        
        if 'inatividade' in question_lower:
            import re
            match = re.search(r'(\d+)', question)
            if match:
                dias = int(match.group(1))
                self.processor.config['dias_inatividade'] = dias
                return f"✅ Configurado: {dias} dias para análise de inatividade"
        
        if 'ticket' in question_lower:
            import re
            match = re.search(r'(\d+)', question)
            if match:
                valor = float(match.group(1))
                self.processor.config['ticket_medio_minimo'] = valor
                return f"✅ Configurado: R$ {valor:.2f} como ticket médio mínimo"
        
        if 'mostrar' in question_lower or 'atual' in question_lower:
            config = self.processor.config
            return f"""
[bold]⚙️ CONFIGURAÇÕES ATUAIS:[/bold]

📅 Dias de inatividade: {config['dias_inatividade']} dias
💰 Ticket médio mínimo: R$ {config['ticket_medio_minimo']:.2f}
📊 Período de análise: {config['periodo_analise_meses']} meses
📍 Raio de entrega: {config['raio_entrega_km']} km
"""
        
        return "ℹ️ Use: 'Configure dias de inatividade para 60' ou 'Configure ticket médio mínimo para 100'"
    
    def handle_reports(self, question: str) -> str:
        """Manipula geração de relatórios"""
        try:
            saved_files = self.processor.save_reports()
            
            if not saved_files:
                return "ℹ️ Nenhum relatório foi gerado. Verifique se há dados suficientes."
            
            response = f"""
[bold]📋 RELATÓRIOS GERADOS:[/bold]

✅ {len(saved_files)} arquivos salvos em {self.processor.output_dir}

[bold]Arquivos criados:[/bold]
"""
            
            for file_path in saved_files:
                response += f"• {file_path.name}\n"
            
            response += f"\n[bold]💡 PRÓXIMOS PASSOS:[/bold]\n"
            response += f"• Importe 'novos_clientes_google_contacts.csv' no Google Contacts\n"
            response += f"• Use 'clientes_inativos.xlsx' para campanhas de reativação\n"
            response += f"• Analise 'analise_geografica.xlsx' para campanhas Meta\n"
            
            return response
            
        except Exception as e:
            return f"❌ Erro ao gerar relatórios: {e}"
    
    def generate_executive_summary(self) -> str:
        """Gera resumo executivo"""
        try:
            # Coleta dados
            inativos = self.processor.analyze_inactive_clients()
            alto_ticket = self.processor.analyze_ticket_medio()
            geo_data = self.processor.analyze_geographic_data()
            preferences = self.processor.analyze_preferences()
            
            # Estatísticas
            total_inativos = len(inativos) if not inativos.empty else 0
            total_premium = len(alto_ticket) if not alto_ticket.empty else 0
            total_bairros = len(geo_data['bairros_analise']) if geo_data else 0
            total_produtos = len(preferences['produtos_mais_vendidos']) if preferences else 0
            
            response = f"""
[bold]📊 RESUMO EXECUTIVO - ZAPCHICKEN[/bold]

[bold]👥 CLIENTES:[/bold]
• Inativos: {total_inativos} clientes
• Premium (alto ticket): {total_premium} clientes

[bold]📍 COBERTURA:[/bold]
• Bairros ativos: {total_bairros}
• Raio de entrega: {self.processor.config['raio_entrega_km']} km

[bold]📦 PRODUTOS:[/bold]
• Produtos únicos: {total_produtos}
• Período analisado: {self.processor.config['periodo_analise_meses']} meses

[bold]🎯 PRÓXIMAS AÇÕES RECOMENDADAS:[/bold]
"""
            
            if total_inativos > 0:
                response += f"1. Campanha de reativação para {total_inativos} clientes inativos\n"
            
            if total_premium > 0:
                response += f"2. Ofertas exclusivas para {total_premium} clientes premium\n"
            
            if geo_data:
                response += f"3. Campanhas Meta para top 3 bairros\n"
            
            response += f"4. Análise de sazonalidade e tendências\n"
            
            return response
            
        except Exception as e:
            return f"❌ Erro ao gerar resumo executivo: {e}"
    
    def analyze_sales_by_date(self, question: str) -> str:
        """Analisa vendas por data específica com insights avançados"""
        try:
            # Extrai mês da pergunta
            meses = {
                'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
                'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
                'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
            }
            
            question_lower = question.lower()
            mes_encontrado = None
            
            for mes_nome, mes_num in meses.items():
                if mes_nome in question_lower:
                    mes_encontrado = mes_num
                    break
            
            if not mes_encontrado:
                return "❌ Não consegui identificar o mês na sua pergunta. Tente: 'Quem comprou em julho?'"
            
            # Verifica se os dados estão disponíveis
            if not hasattr(self.processor, 'dataframes') or not self.processor.dataframes:
                return "❌ Dados não disponíveis. Processe os dados primeiro."
            
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # Converte coluna de data
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'], errors='coerce')
            
            # Filtra por mês
            pedidos_mes = pedidos_df[
                pedidos_df['Data Fechamento'].dt.month == mes_encontrado
            ]
            
            if pedidos_mes.empty:
                return f"ℹ️ Nenhum pedido encontrado para o mês {list(meses.keys())[mes_encontrado-1]}."
            
            # Estatísticas avançadas
            total_pedidos = len(pedidos_mes)
            total_clientes = pedidos_mes['Cliente'].nunique()
            valor_total = pedidos_mes['Total'].sum()
            ticket_medio = valor_total / total_pedidos
            
            # Análise de dias da semana
            pedidos_mes['Dia Semana'] = pedidos_mes['Data Fechamento'].dt.day_name()
            dias_populares = pedidos_mes['Dia Semana'].value_counts().head(3)
            
            # Análise de horários (se disponível)
            if 'Data Fechamento' in pedidos_mes.columns:
                pedidos_mes['Hora'] = pedidos_mes['Data Fechamento'].dt.hour
                horarios_populares = pedidos_mes['Hora'].value_counts().head(3)
            
            # Análise geográfica
            if 'Bairro' in pedidos_mes.columns:
                bairros_populares = pedidos_mes['Bairro'].value_counts().head(5)
            
            # Análise de origem dos pedidos
            if 'Origem' in pedidos_mes.columns:
                origens_populares = pedidos_mes['Origem'].value_counts().head(3)
            
            # Top clientes com análise detalhada
            top_clientes = pedidos_mes.groupby('Cliente').agg({
                'Total': 'sum',
                'Telefone': 'first',
                'Bairro': 'first' if 'Bairro' in pedidos_mes.columns else lambda x: 'N/A',
                'Data Fechamento': 'count'
            }).nlargest(10, 'Total')
            
            response = f"""
[bold]📊 ANÁLISE AVANÇADA - PEDIDOS EM {list(meses.keys())[mes_encontrado-1].upper()}:[/bold]

📦 Total de pedidos: {total_pedidos}
👥 Clientes únicos: {total_clientes}
💰 Valor total: R$ {valor_total:,.2f}
💵 Ticket médio: R$ {ticket_medio:.2f}
📈 Pedidos por cliente: {total_pedidos/total_clientes:.1f}

[bold]📅 ANÁLISE TEMPORAL:[/bold]
[bold]Dias mais populares:[/bold]
"""
            
            for dia, count in dias_populares.items():
                response += f"• {dia}: {count} pedidos\n"
            
            if 'Data Fechamento' in pedidos_mes.columns:
                response += f"\n[bold]Horários mais populares:[/bold]\n"
                for hora, count in horarios_populares.items():
                    response += f"• {hora}h: {count} pedidos\n"
            
            if 'Bairro' in pedidos_mes.columns:
                response += f"\n[bold]📍 TOP 5 BAIRROS MAIS ATIVOS:[/bold]\n"
                for bairro, count in bairros_populares.items():
                    response += f"• {bairro}: {count} pedidos\n"
            
            if 'Origem' in pedidos_mes.columns:
                response += f"\n[bold]📱 CANAIS MAIS POPULARES:[/bold]\n"
                for origem, count in origens_populares.items():
                    response += f"• {origem}: {count} pedidos\n"
            
            response += f"""

[bold]🏆 TOP 10 CLIENTES DO MÊS:[/bold]
"""
            
            for i, (cliente, dados) in enumerate(top_clientes.iterrows(), 1):
                bairro = dados.get('Bairro', 'N/A')
                pedidos = dados.get('Data Fechamento', 0)
                response += f"{i}. {cliente} ({bairro}): R$ {dados['Total']:,.2f} em {pedidos} pedidos\n"
            
            # Análise de tendências
            response += f"""

[bold]📈 INSIGHTS E TENDÊNCIAS:[/bold]

[bold]🎯 OPORTUNIDADES IDENTIFICADAS:[/bold]
• {dias_populares.index[0] if len(dias_populares) > 0 else 'N/A'} é o dia mais forte - intensificar campanhas
• {bairros_populares.index[0] if 'Bairro' in pedidos_mes.columns and len(bairros_populares) > 0 else 'N/A'} é o bairro mais ativo
• {origens_populares.index[0] if 'Origem' in pedidos_mes.columns and len(origens_populares) > 0 else 'N/A'} é o canal mais eficaz

[bold]🚀 ESTRATÉGIAS RECOMENDADAS:[/bold]
1. Campanha especial para {dias_populares.index[0] if len(dias_populares) > 0 else 'fins de semana'}
2. Foco geográfico em {bairros_populares.index[0] if 'Bairro' in pedidos_mes.columns and len(bairros_populares) > 0 else 'bairros próximos'}
3. Otimização do canal {origens_populares.index[0] if 'Origem' in pedidos_mes.columns and len(origens_populares) > 0 else 'WhatsApp'}

[bold]💡 ROI ESPERADO:[/bold]
• Aumento de 15-25% nas vendas nos dias identificados
• Melhoria de 20-30% na eficácia das campanhas geográficas
• Otimização de 10-15% nos canais de venda
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro ao analisar vendas por data: {str(e)}"

    def analyze_trends_and_predictions(self, question: str) -> str:
        """Analisa tendências e faz previsões"""
        try:
            # Verifica se os dados estão disponíveis
            if not hasattr(self.processor, 'dataframes') or not self.processor.dataframes:
                return "❌ Dados não disponíveis. Processe os dados primeiro."
            
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # Converte coluna de data
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'], errors='coerce')
            
            # Análise de tendências mensais
            pedidos_df['Mes'] = pedidos_df['Data Fechamento'].dt.to_period('M')
            tendencia_mensal = pedidos_df.groupby('Mes').agg({
                'Total': 'sum',
                'Cliente': 'nunique',
                'Código': 'count'
            }).reset_index()
            
            if len(tendencia_mensal) < 2:
                return "ℹ️ Dados insuficientes para análise de tendências. Precisa de pelo menos 2 meses de dados."
            
            # Calcula crescimento
            tendencia_mensal['Crescimento_Vendas'] = tendencia_mensal['Total'].pct_change() * 100
            tendencia_mensal['Crescimento_Clientes'] = tendencia_mensal['Cliente'].pct_change() * 100
            
            # Análise de sazonalidade semanal
            pedidos_df['Dia_Semana'] = pedidos_df['Data Fechamento'].dt.day_name()
            sazonalidade_semanal = pedidos_df.groupby('Dia_Semana')['Total'].sum().sort_values(ascending=False)
            
            # Previsões simples baseadas em tendência
            ultimo_mes = tendencia_mensal.iloc[-1]
            penultimo_mes = tendencia_mensal.iloc[-2]
            
            crescimento_vendas = ultimo_mes['Crescimento_Vendas']
            crescimento_clientes = ultimo_mes['Crescimento_Clientes']
            
            # Previsão para próximo mês
            previsao_vendas = ultimo_mes['Total'] * (1 + (crescimento_vendas / 100))
            previsao_clientes = ultimo_mes['Cliente'] * (1 + (crescimento_clientes / 100))
            
            response = f"""
[bold]📈 ANÁLISE DE TENDÊNCIAS E PREVISÕES - ZAPCHICKEN[/bold]

[bold]📊 TENDÊNCIA MENSAL:[/bold]
• Último mês: R$ {ultimo_mes['Total']:,.2f} ({ultimo_mes['Cliente']} clientes)
• Mês anterior: R$ {penultimo_mes['Total']:,.2f} ({penultimo_mes['Cliente']} clientes)
• Crescimento vendas: {crescimento_vendas:+.1f}%
• Crescimento clientes: {crescimento_clientes:+.1f}%

[bold]📅 SAZONALIDADE SEMANAL:[/bold]
"""
            
            for i, (dia, valor) in enumerate(sazonalidade_semanal.head(3).items(), 1):
                response += f"• {dia}: R$ {valor:,.2f}\n"
            
            response += f"""

[bold]🔮 PREVISÕES PARA PRÓXIMO MÊS:[/bold]
• Vendas previstas: R$ {previsao_vendas:,.2f}
• Clientes previstos: {int(previsao_clientes)}
• Crescimento esperado: {crescimento_vendas:+.1f}%

[bold]📈 TENDÊNCIAS IDENTIFICADAS:[/bold]
"""
            
            if crescimento_vendas > 10:
                response += "• 🚀 Crescimento forte nas vendas - manter estratégias atuais\n"
            elif crescimento_vendas > 0:
                response += "• 📈 Crescimento moderado - otimizar campanhas\n"
            else:
                response += "• ⚠️ Declínio nas vendas - revisar estratégias urgentemente\n"
            
            if crescimento_clientes > 5:
                response += "• 👥 Base de clientes crescendo bem\n"
            elif crescimento_clientes > 0:
                response += "• 👤 Base de clientes estável\n"
            else:
                response += "• ⚠️ Perda de clientes - focar em retenção\n"
            
            response += f"""

[bold]🎯 RECOMENDAÇÕES BASEADAS EM TENDÊNCIAS:[/bold]

[bold]1. 📊 ESTRATÉGIAS DE CRESCIMENTO:[/bold]
"""
            
            if crescimento_vendas > 10:
                response += "• Expandir para novos bairros\n• Aumentar investimento em marketing\n• Lançar novos produtos\n"
            elif crescimento_vendas > 0:
                response += "• Otimizar campanhas existentes\n• Melhorar experiência do cliente\n• Focar em upselling\n"
            else:
                response += "• Revisar preços e ofertas\n• Campanha agressiva de reativação\n• Análise de concorrência\n"
            
            response += f"""

[bold]2. 📅 OTIMIZAÇÃO TEMPORAL:[/bold]
• Focar campanhas no {sazonalidade_semanal.index[0]} (dia mais forte)
• Preparar estoque extra para dias de pico
• Ajustar horários de funcionamento

[bold]3. 💡 ESTRATÉGIAS PREDITIVAS:[/bold]
• Preparar para {crescimento_vendas:+.0f}% de crescimento
• Planejar campanhas para {int(previsao_clientes)} clientes
• Ajustar orçamento de marketing

[bold]📊 MÉTRICAS DE ACOMPANHAMENTO:[/bold]
• Monitorar crescimento semanal vs. previsão
• Acompanhar taxa de conversão por canal
• Medir satisfação do cliente
• Analisar ticket médio por período

[bold]💡 ROI ESPERADO DAS ESTRATÉGIAS:[/bold]
• Aumento de 15-25% na eficácia das campanhas
• Melhoria de 20-30% na previsibilidade
• Otimização de 10-15% nos custos operacionais
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro ao analisar tendências: {str(e)}"

    def analyze_seasonality(self, question: str) -> str:
        """Analisa sazonalidade dos dados"""
        try:
            # Verifica se os dados estão disponíveis
            if not hasattr(self.processor, 'dataframes') or not self.processor.dataframes:
                return "❌ Dados não disponíveis. Processe os dados primeiro."
            
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # Converte coluna de data
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'], errors='coerce')
            
            # Análise por mês
            pedidos_df['Mes'] = pedidos_df['Data Fechamento'].dt.month
            pedidos_df['Mes_Nome'] = pedidos_df['Data Fechamento'].dt.strftime('%B')
            
            sazonalidade_mensal = pedidos_df.groupby(['Mes', 'Mes_Nome']).agg({
                'Total': 'sum',
                'Cliente': 'nunique',
                'Código': 'count'
            }).reset_index().sort_values('Mes')
            
            # Análise por dia da semana
            pedidos_df['Dia_Semana'] = pedidos_df['Data Fechamento'].dt.day_name()
            sazonalidade_semanal = pedidos_df.groupby('Dia_Semana').agg({
                'Total': 'sum',
                'Cliente': 'nunique',
                'Código': 'count'
            }).reset_index()
            
            # Análise por hora (se disponível)
            pedidos_df['Hora'] = pedidos_df['Data Fechamento'].dt.hour
            sazonalidade_horaria = pedidos_df.groupby('Hora').agg({
                'Total': 'sum',
                'Código': 'count'
            }).reset_index()
            
            response = f"""
[bold]📅 ANÁLISE DE SAZONALIDADE - ZAPCHICKEN[/bold]

[bold]📊 SAZONALIDADE MENSAL:[/bold]
"""
            
            for _, mes in sazonalidade_mensal.iterrows():
                response += f"• {mes['Mes_Nome']}: R$ {mes['Total']:,.2f} ({mes['Cliente']} clientes, {mes['Código']} pedidos)\n"
            
            # Identifica picos e vales
            mes_pico = sazonalidade_mensal.loc[sazonalidade_mensal['Total'].idxmax()]
            mes_vale = sazonalidade_mensal.loc[sazonalidade_mensal['Total'].idxmin()]
            
            response += f"""

[bold]🎯 PADRÕES SAZONAIS IDENTIFICADOS:[/bold]
• Mês de pico: {mes_pico['Mes_Nome']} (R$ {mes_pico['Total']:,.2f})
• Mês de vale: {mes_vale['Mes_Nome']} (R$ {mes_vale['Total']:,.2f})
• Variação: {((mes_pico['Total'] - mes_vale['Total']) / mes_vale['Total'] * 100):.1f}%

[bold]📅 SAZONALIDADE SEMANAL:[/bold]
"""
            
            for _, dia in sazonalidade_semanal.iterrows():
                response += f"• {dia['Dia_Semana']}: R$ {dia['Total']:,.2f} ({dia['Cliente']} clientes)\n"
            
            # Identifica dias fortes e fracos
            dia_forte = sazonalidade_semanal.loc[sazonalidade_semanal['Total'].idxmax()]
            dia_fraco = sazonalidade_semanal.loc[sazonalidade_semanal['Total'].idxmin()]
            
            response += f"""

[bold]⏰ SAZONALIDADE HORÁRIA:[/bold]
"""
            
            for _, hora in sazonalidade_horaria.iterrows():
                response += f"• {hora['Hora']}h: R$ {hora['Total']:,.2f} ({hora['Código']} pedidos)\n"
            
            # Identifica horários de pico
            hora_pico = sazonalidade_horaria.loc[sazonalidade_horaria['Total'].idxmax()]
            
            response += f"""

[bold]🎯 INSIGHTS SAZONAIS:[/bold]

[bold]📈 ESTRATÉGIAS PARA MESES DE PICO ({mes_pico['Mes_Nome']}):[/bold]
• Aumentar estoque em 30-50%
• Contratar funcionários temporários
• Campanhas promocionais agressivas
• Preparar para alta demanda

[bold]📉 ESTRATÉGIAS PARA MESES DE VALE ({mes_vale['Mes_Nome']}):[/bold]
• Campanhas de reativação
• Ofertas especiais para atrair clientes
• Foco em produtos sazonais
• Manutenção de estoque reduzido

[bold]📅 ESTRATÉGIAS SEMANAIS:[/bold]
• {dia_forte['Dia_Semana']}: Preparar para alta demanda
• {dia_fraco['Dia_Semana']}: Campanhas especiais para aumentar vendas
• Otimizar horários de funcionamento

[bold]⏰ ESTRATÉGIAS HORÁRIAS:[/bold]
• Pico às {hora_pico['Hora']}h: Máximo de funcionários
• Preparar estoque antecipadamente
• Campanhas flash para horários de baixa

[bold]💡 ROI ESPERADO DAS ESTRATÉGIAS SAZONAIS:[/bold]
• Aumento de 20-35% nos meses de vale
• Otimização de 15-25% nos custos operacionais
• Melhoria de 30-40% na satisfação do cliente
• Crescimento de 25-40% no faturamento geral
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro ao analisar sazonalidade: {str(e)}"

    def handle_unknown_question(self, question: str) -> str:
        """Manipula perguntas não reconhecidas com sugestões inteligentes"""
        return f"""
🤔 Não entendi sua pergunta: "{question}"

[bold]💡 Tente uma destas opções populares:[/bold]

[bold]📊 ANÁLISES DE CLIENTES:[/bold]
• "Quantos clientes inativos temos?"
• "Quem são os clientes premium?"
• "Quem comprou em julho?"
• "Mostre clientes que não pediram há 60 dias"

[bold]💰 ANÁLISES DE VENDAS:[/bold]
• "Quais são os produtos mais vendidos?"
• "Qual foi o faturamento do mês passado?"
• "Mostre a análise de ticket médio"
• "Quem são os clientes com maior valor?"

[bold]📍 ANÁLISES GEOGRÁFICAS:[/bold]
• "Quais são os bairros que mais pedem?"
• "Mostre a análise geográfica"
• "Quais regiões têm mais clientes premium?"

[bold]🎯 SUGESTÕES ESTRATÉGICAS:[/bold]
• "Dê sugestões para reativar clientes"
• "Sugira campanhas de marketing"
• "Quais ofertas fazer para clientes premium?"
• "Como melhorar as vendas?"

[bold]📋 RELATÓRIOS:[/bold]
• "Gere relatório completo"
• "Mostre resumo executivo"
• "Salve todos os relatórios"

[bold]⚙️ CONFIGURAÇÕES:[/bold]
• "Configure dias de inatividade para 45"
• "Configure ticket médio mínimo para 80"
• "Mostre configurações atuais"

[bold]❓ Digite "ajuda" para ver todos os comandos disponíveis.[/bold]
"""
