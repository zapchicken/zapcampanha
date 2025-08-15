import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

from .zapchicken_processor import ZapChickenProcessor

class ZapChickenAIVercel:
    """Sistema de IA Ultra-Leve para Vercel - Sem Machine Learning"""
    
    def __init__(self, processor: ZapChickenProcessor):
        self.processor = processor
        self.conversation_history = []
        self.insights_cache = {}
        
    def process_question(self, question: str) -> str:
        """Processa pergunta com análise estatística avançada"""
        question_lower = question.lower()
        
        # Análise de vendas
        if any(word in question_lower for word in ['comprou', 'vendeu', 'venda', 'pedido', 'data']):
            return self.analyze_sales_vercel(question)
        
        # Análise de clientes
        elif any(word in question_lower for word in ['inativo', 'inatividade', 'reativar', 'cliente']):
            return self.analyze_customers_vercel(question)
        
        # Análise de ticket médio
        elif any(word in question_lower for word in ['ticket', 'médio', 'alto', 'premium', 'valor']):
            return self.analyze_ticket_vercel(question)
        
        # Análise geográfica
        elif any(word in question_lower for word in ['bairro', 'cidade', 'local', 'geográfico', 'região']):
            return self.analyze_geographic_vercel(question)
        
        # Análise de produtos
        elif any(word in question_lower for word in ['produto', 'item', 'mais vendido', 'categoria']):
            return self.analyze_products_vercel(question)
        
        # Previsões e tendências
        elif any(word in question_lower for word in ['tendência', 'previsão', 'futuro', 'crescimento', 'predição']):
            return self.analyze_predictions_vercel(question)
        
        # Análise de sazonalidade
        elif any(word in question_lower for word in ['sazonal', 'sazonalidade', 'estação', 'período']):
            return self.analyze_seasonality_vercel(question)
        
        # Estratégias de marketing
        elif any(word in question_lower for word in ['marketing', 'estratégia', 'campanha', 'roi', 'lucro']):
            return self.generate_marketing_strategy_vercel(question)
        
        # Relatório executivo
        elif any(word in question_lower for word in ['relatório', 'completo', 'executivo', 'dashboard']):
            return self.generate_executive_report_vercel()
        
        # Pergunta não reconhecida
        else:
            return self.handle_unknown_question_vercel(question)
    
    def analyze_sales_vercel(self, question: str) -> str:
        """Análise avançada de vendas sem ML"""
        try:
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # Análise temporal
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'])
            vendas_diarias = pedidos_df.groupby('Data Fechamento')['Total'].sum().reset_index()
            vendas_mensais = pedidos_df.groupby(pedidos_df['Data Fechamento'].dt.to_period('M'))['Total'].sum()
            
            # Estatísticas básicas
            total_vendas = pedidos_df['Total'].sum()
            ticket_medio = pedidos_df['Total'].mean()
            total_pedidos = len(pedidos_df)
            
            # Análise de crescimento
            if len(vendas_mensais) > 1:
                crescimento = ((vendas_mensais.iloc[-1] - vendas_mensais.iloc[-2]) / vendas_mensais.iloc[-2]) * 100
                tendencia = "📈 Crescente" if crescimento > 0 else "📉 Decrescente"
            else:
                crescimento = 0
                tendencia = "➡️ Estável"
            
            # Análise por origem
            origem_analise = pedidos_df['Origem'].value_counts()
            origem_principal = origem_analise.index[0] if not origem_analise.empty else "N/A"
            
            # Análise de horários
            pedidos_df['Hora'] = pedidos_df['Data Fechamento'].dt.hour
            hora_pico = pedidos_df['Hora'].mode().iloc[0] if not pedidos_df['Hora'].mode().empty else 0
            
            response = f"""
🎯 **ANÁLISE AVANÇADA DE VENDAS**

📊 **Métricas Principais:**
• Total de Vendas: R$ {total_vendas:,.2f}
• Ticket Médio: R$ {ticket_medio:.2f}
• Total de Pedidos: {total_pedidos:,}
• Crescimento Mensal: {crescimento:.1f}% ({tendencia})

📈 **Análise Temporal:**
• Período Analisado: {pedidos_df['Data Fechamento'].min().strftime('%d/%m/%Y')} a {pedidos_df['Data Fechamento'].max().strftime('%d/%m/%Y')}
• Média Diária: R$ {vendas_diarias['Total'].mean():.2f}
• Hora de Pico: {hora_pico}h

🛒 **Análise por Origem:**
• Origem Principal: {origem_principal}
• Distribuição: {origem_analise.head(3).to_dict()}

💡 **Insights Estratégicos:**
• Foque em {origem_principal} para maximizar vendas
• Horário de pico: {hora_pico}h - otimize operações
• Ticket médio pode ser melhorado com upselling
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro na análise de vendas: {str(e)}"
    
    def analyze_customers_vercel(self, question: str) -> str:
        """Análise avançada de clientes sem ML"""
        try:
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # RFM Analysis (sem ML)
            hoje = datetime.now()
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'])
            
            client_analysis = pedidos_df.groupby('Cliente').agg({
                'Data Fechamento': 'max',
                'Código': 'count',
                'Total': 'sum'
            }).reset_index()
            
            client_analysis.columns = ['cliente', 'ultima_compra', 'frequencia', 'valor_total']
            client_analysis['recency'] = (hoje - client_analysis['ultima_compra']).dt.days
            client_analysis['ticket_medio'] = client_analysis['valor_total'] / client_analysis['frequencia']
            
            # Segmentação manual
            def segmentar_cliente(row):
                if row['recency'] <= 30 and row['frequencia'] >= 3 and row['valor_total'] >= 500:
                    return 'Diamante'
                elif row['recency'] <= 60 and row['frequencia'] >= 2 and row['valor_total'] >= 300:
                    return 'Ouro'
                elif row['recency'] <= 90 and row['frequencia'] >= 1 and row['valor_total'] >= 150:
                    return 'Prata'
                else:
                    return 'Bronze'
            
            client_analysis['segmento'] = client_analysis.apply(segmentar_cliente, axis=1)
            
            # Estatísticas
            total_clientes = len(client_analysis)
            clientes_inativos = len(client_analysis[client_analysis['recency'] > 90])
            clientes_premium = len(client_analysis[client_analysis['segmento'].isin(['Diamante', 'Ouro'])])
            
            # Análise de churn
            churn_rate = (clientes_inativos / total_clientes) * 100 if total_clientes > 0 else 0
            
            # Valor perdido
            valor_perdido = client_analysis[client_analysis['recency'] > 90]['valor_total'].sum()
            
            response = f"""
👥 **ANÁLISE AVANÇADA DE CLIENTES**

📊 **Segmentação RFM:**
• Total de Clientes: {total_clientes:,}
• Clientes Premium (Ouro/Diamante): {clientes_premium:,} ({clientes_premium/total_clientes*100:.1f}%)
• Clientes Inativos (>90 dias): {clientes_inativos:,} ({churn_rate:.1f}%)

💰 **Análise de Valor:**
• Valor Total dos Clientes: R$ {client_analysis['valor_total'].sum():,.2f}
• Valor Perdido (Inativos): R$ {valor_perdido:,.2f}
• Ticket Médio por Cliente: R$ {client_analysis['valor_total'].mean():.2f}

🏆 **Distribuição por Segmento:**
{client_analysis['segmento'].value_counts().to_string()}

⚠️ **Alertas Estratégicos:**
• Taxa de Churn: {churn_rate:.1f}% - Ação necessária!
• {clientes_inativos} clientes precisam de reativação
• Potencial de recuperação: R$ {valor_perdido:,.2f}

🎯 **Recomendações:**
• Campanha de reativação para {clientes_inativos} clientes inativos
• Programa de fidelidade para clientes Prata
• VIP para clientes Diamante/Ouro
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro na análise de clientes: {str(e)}"
    
    def analyze_ticket_vercel(self, question: str) -> str:
        """Análise de ticket médio sem ML"""
        try:
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # Análise por cliente
            ticket_por_cliente = pedidos_df.groupby('Cliente').agg({
                'Total': ['sum', 'mean', 'count']
            }).reset_index()
            ticket_por_cliente.columns = ['cliente', 'valor_total', 'ticket_medio', 'frequencia']
            
            # Segmentação manual por ticket
            def segmentar_ticket(row):
                if row['ticket_medio'] >= 100:
                    return 'Ultra Premium'
                elif row['ticket_medio'] >= 70:
                    return 'Premium'
                elif row['ticket_medio'] >= 50:
                    return 'Regular'
                else:
                    return 'Ocasionais'
            
            ticket_por_cliente['segmento_ticket'] = ticket_por_cliente.apply(segmentar_ticket, axis=1)
            
            # Estatísticas
            ticket_geral = pedidos_df['Total'].mean()
            ticket_mediana = pedidos_df['Total'].median()
            ticket_max = pedidos_df['Total'].max()
            ticket_min = pedidos_df['Total'].min()
            
            # Análise sazonal
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'])
            pedidos_df['Mes'] = pedidos_df['Data Fechamento'].dt.month
            ticket_por_mes = pedidos_df.groupby('Mes')['Total'].mean()
            
            mes_maior_ticket = ticket_por_mes.idxmax()
            mes_menor_ticket = ticket_por_mes.idxmin()
            
            response = f"""
💰 **ANÁLISE AVANÇADA DE TICKET MÉDIO**

📊 **Métricas Gerais:**
• Ticket Médio Geral: R$ {ticket_geral:.2f}
• Ticket Mediano: R$ {ticket_mediana:.2f}
• Maior Pedido: R$ {ticket_max:.2f}
• Menor Pedido: R$ {ticket_min:.2f}

🏆 **Segmentação por Ticket:**
{ticket_por_cliente['segmento_ticket'].value_counts().to_string()}

📈 **Análise Sazonal:**
• Mês com Maior Ticket: {mes_maior_ticket} (R$ {ticket_por_mes.max():.2f})
• Mês com Menor Ticket: {mes_menor_ticket} (R$ {ticket_por_mes.min():.2f})
• Variação Sazonal: {((ticket_por_mes.max() - ticket_por_mes.min()) / ticket_por_mes.min() * 100):.1f}%

💡 **Insights Estratégicos:**
• {len(ticket_por_cliente[ticket_por_cliente['segmento_ticket'] == 'Ultra Premium'])} clientes Ultra Premium
• Potencial de upselling: R$ {ticket_por_cliente[ticket_por_cliente['ticket_medio'] < 50]['valor_total'].sum():,.2f}
• Foque em {mes_maior_ticket} para campanhas premium
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro na análise de ticket: {str(e)}"
    
    def analyze_geographic_vercel(self, question: str) -> str:
        """Análise geográfica sem ML"""
        try:
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # Análise por bairro
            bairro_analise = pedidos_df.groupby('Bairro').agg({
                'Total': ['sum', 'count', 'mean']
            }).reset_index()
            bairro_analise.columns = ['bairro', 'valor_total', 'quantidade_pedidos', 'ticket_medio']
            
            # Top bairros
            top_bairros_valor = bairro_analise.nlargest(5, 'valor_total')
            top_bairros_pedidos = bairro_analise.nlargest(5, 'quantidade_pedidos')
            
            # Análise por cidade
            cidade_analise = pedidos_df.groupby('Cidade').agg({
                'Total': ['sum', 'count']
            }).reset_index()
            cidade_analise.columns = ['cidade', 'valor_total', 'quantidade_pedidos']
            
            response = f"""
🗺️ **ANÁLISE GEOGRÁFICA AVANÇADA**

🏆 **Top 5 Bairros por Valor:**
{top_bairros_valor[['bairro', 'valor_total', 'quantidade_pedidos']].to_string(index=False)}

📊 **Top 5 Bairros por Pedidos:**
{top_bairros_pedidos[['bairro', 'quantidade_pedidos', 'valor_total']].to_string(index=False)}

🌆 **Análise por Cidade:**
{cidade_analise.to_string(index=False)}

💡 **Insights Estratégicos:**
• Bairro mais lucrativo: {top_bairros_valor.iloc[0]['bairro']} (R$ {top_bairros_valor.iloc[0]['valor_total']:,.2f})
• Bairro com mais pedidos: {top_bairros_pedidos.iloc[0]['bairro']} ({top_bairros_pedidos.iloc[0]['quantidade_pedidos']} pedidos)
• Foque marketing em {top_bairros_valor.iloc[0]['bairro']} para maximizar receita
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro na análise geográfica: {str(e)}"
    
    def analyze_products_vercel(self, question: str) -> str:
        """Análise de produtos sem ML"""
        try:
            itens_df = self.processor.dataframes.get('itens')
            if itens_df is None or itens_df.empty:
                return "❌ Dados de itens não disponíveis. Processe os dados primeiro."
            
            # Análise por produto
            produto_analise = itens_df.groupby('Nome Prod.').agg({
                'Qtd.': 'sum',
                'Valor Tot. Item': 'sum'
            }).reset_index()
            produto_analise.columns = ['produto', 'quantidade_vendida', 'valor_total']
            
            # Top produtos
            top_produtos_qtd = produto_analise.nlargest(10, 'quantidade_vendida')
            top_produtos_valor = produto_analise.nlargest(10, 'valor_total')
            
            # Análise por categoria
            categoria_analise = itens_df.groupby('Cat. Prod.').agg({
                'Qtd.': 'sum',
                'Valor Tot. Item': 'sum'
            }).reset_index()
            categoria_analise.columns = ['categoria', 'quantidade_vendida', 'valor_total']
            
            response = f"""
🛍️ **ANÁLISE AVANÇADA DE PRODUTOS**

🏆 **Top 10 Produtos por Quantidade:**
{top_produtos_qtd[['produto', 'quantidade_vendida', 'valor_total']].to_string(index=False)}

💰 **Top 10 Produtos por Valor:**
{top_produtos_valor[['produto', 'valor_total', 'quantidade_vendida']].to_string(index=False)}

📊 **Análise por Categoria:**
{categoria_analise.to_string(index=False)}

💡 **Insights Estratégicos:**
• Produto mais vendido: {top_produtos_qtd.iloc[0]['produto']} ({top_produtos_qtd.iloc[0]['quantidade_vendida']} unidades)
• Produto mais lucrativo: {top_produtos_valor.iloc[0]['produto']} (R$ {top_produtos_valor.iloc[0]['valor_total']:,.2f})
• Categoria mais vendida: {categoria_analise.loc[categoria_analise['quantidade_vendida'].idxmax(), 'categoria']}
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro na análise de produtos: {str(e)}"
    
    def analyze_predictions_vercel(self, question: str) -> str:
        """Análise preditiva simples sem ML"""
        try:
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # Análise de tendência simples
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'])
            vendas_diarias = pedidos_df.groupby('Data Fechamento')['Total'].sum().reset_index()
            
            if len(vendas_diarias) < 7:
                return "❌ Dados insuficientes para análise preditiva (mínimo 7 dias)"
            
            # Tendência simples
            vendas_recentes = vendas_diarias.tail(7)
            vendas_anteriores = vendas_diarias.tail(14).head(7)
            
            media_recente = vendas_recentes['Total'].mean()
            media_anterior = vendas_anteriores['Total'].mean()
            
            tendencia = ((media_recente - media_anterior) / media_anterior) * 100 if media_anterior > 0 else 0
            
            # Previsão simples
            previsao_30_dias = media_recente * 30
            
            response = f"""
🔮 **ANÁLISE PREDITIVA SIMPLES**

📊 **Análise de Tendência:**
• Média Últimos 7 dias: R$ {media_recente:.2f}
• Média 7 dias anteriores: R$ {media_anterior:.2f}
• Tendência: {tendencia:+.1f}% ({'📈 Crescente' if tendencia > 0 else '📉 Decrescente' if tendencia < 0 else '➡️ Estável'})

🎯 **Previsão para Próximos 30 dias:**
• Receita Estimada: R$ {previsao_30_dias:,.2f}
• Pedidos Estimados: {int(previsao_30_dias / vendas_diarias['Total'].mean())}

⚠️ **Limitações:**
• Análise baseada em média móvel simples
• Não considera sazonalidade complexa
• Para análise mais precisa, use dados históricos maiores

💡 **Recomendações:**
• {'Aumente estoque e equipe' if tendencia > 5 else 'Mantenha operação atual' if tendencia > -5 else 'Analise causas da queda'}
• Prepare-se para {previsao_30_dias:,.0f} em receita
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro na análise preditiva: {str(e)}"
    
    def analyze_seasonality_vercel(self, question: str) -> str:
        """Análise de sazonalidade sem ML"""
        try:
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'])
            
            # Análise por dia da semana
            pedidos_df['Dia Semana'] = pedidos_df['Data Fechamento'].dt.day_name()
            vendas_dia_semana = pedidos_df.groupby('Dia Semana')['Total'].sum()
            
            # Análise por mês
            pedidos_df['Mes'] = pedidos_df['Data Fechamento'].dt.month
            vendas_mes = pedidos_df.groupby('Mes')['Total'].sum()
            
            # Análise por hora
            pedidos_df['Hora'] = pedidos_df['Data Fechamento'].dt.hour
            vendas_hora = pedidos_df.groupby('Hora')['Total'].sum()
            
            response = f"""
📅 **ANÁLISE DE SAZONALIDADE**

📊 **Vendas por Dia da Semana:**
{vendas_dia_semana.to_string()}

📈 **Vendas por Mês:**
{vendas_mes.to_string()}

🕐 **Vendas por Hora:**
{vendas_hora.to_string()}

💡 **Insights Sazonais:**
• Melhor dia: {vendas_dia_semana.idxmax()} (R$ {vendas_dia_semana.max():,.2f})
• Pior dia: {vendas_dia_semana.idxmin()} (R$ {vendas_dia_semana.min():,.2f})
• Hora de pico: {vendas_hora.idxmax()}h (R$ {vendas_hora.max():,.2f})
• Variação semanal: {((vendas_dia_semana.max() - vendas_dia_semana.min()) / vendas_dia_semana.min() * 100):.1f}%
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro na análise de sazonalidade: {str(e)}"
    
    def generate_marketing_strategy_vercel(self, question: str) -> str:
        """Estratégias de marketing sem ML"""
        try:
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # Análise básica para estratégias
            total_vendas = pedidos_df['Total'].sum()
            ticket_medio = pedidos_df['Total'].mean()
            total_clientes = pedidos_df['Cliente'].nunique()
            
            # Clientes inativos
            hoje = datetime.now()
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'])
            clientes_inativos = pedidos_df.groupby('Cliente')['Data Fechamento'].max()
            clientes_inativos = clientes_inativos[(hoje - clientes_inativos).dt.days > 90]
            
            response = f"""
🎯 **ESTRATÉGIAS DE MARKETING AVANÇADAS**

📊 **Cenário Atual:**
• Receita Total: R$ {total_vendas:,.2f}
• Ticket Médio: R$ {ticket_medio:.2f}
• Total de Clientes: {total_clientes:,}
• Clientes Inativos: {len(clientes_inativos):,}

🚀 **Estratégia 1: Reativação de Clientes**
• Investimento Estimado: R$ {len(clientes_inativos) * 50:,.2f}
• ROI Esperado: 300-500%
• Ação: Campanha personalizada para {len(clientes_inativos)} clientes inativos
• Desconto: 15% no primeiro pedido

💰 **Estratégia 2: Upselling Premium**
• Investimento: R$ {total_clientes * 20:,.2f}
• ROI Esperado: 200-400%
• Ação: Promoção de produtos premium
• Foco: Aumentar ticket médio de R$ {ticket_medio:.2f} para R$ {ticket_medio * 1.3:.2f}

🎁 **Estratégia 3: Programa de Fidelidade**
• Investimento: R$ {total_clientes * 30:,.2f}
• ROI Esperado: 150-300%
• Ação: Sistema de pontos e recompensas
• Benefício: Retenção de clientes

📱 **Estratégia 4: Marketing Digital**
• Investimento: R$ {total_clientes * 10:,.2f}
• ROI Esperado: 100-250%
• Ação: Campanhas no WhatsApp e redes sociais
• Foco: Novos clientes e reativação

📈 **Projeção de Resultados:**
• Receita Adicional Esperada: R$ {total_vendas * 0.3:,.2f} (+30%)
• Novos Clientes: {int(total_clientes * 0.2):,} (+20%)
• Ticket Médio: R$ {ticket_medio * 1.15:.2f} (+15%)
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro na geração de estratégias: {str(e)}"
    
    def generate_executive_report_vercel(self) -> str:
        """Relatório executivo completo sem ML"""
        try:
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados de pedidos não disponíveis. Processe os dados primeiro."
            
            # Métricas principais
            total_vendas = pedidos_df['Total'].sum()
            total_pedidos = len(pedidos_df)
            ticket_medio = pedidos_df['Total'].mean()
            total_clientes = pedidos_df['Cliente'].nunique()
            
            # Análise temporal
            pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'])
            periodo_inicio = pedidos_df['Data Fechamento'].min()
            periodo_fim = pedidos_df['Data Fechamento'].max()
            
            # Análise de origem
            origem_analise = pedidos_df['Origem'].value_counts()
            
            response = f"""
📋 **RELATÓRIO EXECUTIVO COMPLETO**

📊 **Métricas Principais:**
• Receita Total: R$ {total_vendas:,.2f}
• Total de Pedidos: {total_pedidos:,}
• Ticket Médio: R$ {ticket_medio:.2f}
• Total de Clientes: {total_clientes:,}

📅 **Período Analisado:**
• De: {periodo_inicio.strftime('%d/%m/%Y')}
• Até: {periodo_fim.strftime('%d/%m/%Y')}
• Duração: {(periodo_fim - periodo_inicio).days} dias

🛒 **Análise por Origem:**
{origem_analise.to_string()}

🎯 **Principais Insights:**
• Origem principal: {origem_analise.index[0]} ({origem_analise.iloc[0]} pedidos)
• Média diária: R$ {total_vendas / (periodo_fim - periodo_inicio).days:.2f}
• Pedidos por cliente: {total_pedidos / total_clientes:.1f}

💡 **Recomendações Estratégicas:**
1. Foque em {origem_analise.index[0]} para maximizar vendas
2. Implemente programa de fidelidade
3. Campanha de reativação para clientes inativos
4. Otimização de horários de pico
5. Expansão de produtos premium

📈 **Projeções:**
• Crescimento esperado: 20-30% com estratégias implementadas
• ROI estimado: 200-400% em campanhas de marketing
• Potencial de mercado: R$ {total_vendas * 1.5:,.2f} (+50%)
"""
            
            return response
            
        except Exception as e:
            return f"❌ Erro no relatório executivo: {str(e)}"
    
    def handle_unknown_question_vercel(self, question: str) -> str:
        """Tratamento de perguntas não reconhecidas"""
        return f"""
🤖 **IA ZapChicken - Versão Vercel**

Não entendi sua pergunta: "{question}"

💡 **Perguntas que posso responder:**

📊 **Análise de Vendas:**
• "Quem comprou em [data]?"
• "Como estão as vendas?"
• "Qual o total de vendas?"

👥 **Análise de Clientes:**
• "Quantos clientes inativos temos?"
• "Quais os melhores clientes?"
• "Como reativar clientes?"

💰 **Análise Financeira:**
• "Qual o ticket médio?"
• "Quais os produtos mais vendidos?"
• "Como aumentar o faturamento?"

🗺️ **Análise Geográfica:**
• "Quais os melhores bairros?"
• "Onde devo focar marketing?"

📈 **Previsões:**
• "Qual a tendência de vendas?"
• "Como será o próximo mês?"

🎯 **Estratégias:**
• "Gere estratégias de marketing"
• "Relatório executivo completo"

Tente reformular sua pergunta usando essas palavras-chave!
"""
