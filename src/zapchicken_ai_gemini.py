import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import re
from collections import Counter
import warnings
import json
import requests
warnings.filterwarnings('ignore')

from .zapchicken_processor import ZapChickenProcessor

class ZapChickenAIGemini:
    """Sistema de IA com Gemini API - Análises Avançadas e Gratuitas"""
    
    def __init__(self, processor: ZapChickenProcessor, api_key: str = None):
        self.processor = processor
        self.api_key = api_key
        self.conversation_history = []
        self.insights_cache = {}
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        
    def process_question(self, question: str) -> str:
        """Processa pergunta usando Gemini API"""
        try:
            # Se não tem API key, usa análise básica
            if not self.api_key:
                return self._fallback_analysis(question)
            
            # Prepara dados para o Gemini
            data_summary = self._prepare_data_summary()
            
            # Constrói prompt para o Gemini
            prompt = self._build_gemini_prompt(question, data_summary)
            
            # Chama Gemini API
            response = self._call_gemini_api(prompt)
            
            return response
            
        except Exception as e:
            # Fallback para análise básica em caso de erro
            return self._fallback_analysis(question)
    
    def _prepare_data_summary(self) -> str:
        """Prepara resumo dos dados para o Gemini"""
        try:
            # Debug: verificar se o processador tem dados
            if not hasattr(self.processor, 'dataframes') or self.processor.dataframes is None:
                return "❌ Processador não tem dados carregados. Processe os dados primeiro."
            
            pedidos_df = self.processor.dataframes.get('pedidos')
            itens_df = self.processor.dataframes.get('itens')
            clientes_df = self.processor.dataframes.get('clientes')
            
            # Debug: verificar quais dataframes estão disponíveis
            available_dfs = []
            if pedidos_df is not None and not pedidos_df.empty:
                available_dfs.append(f"pedidos ({len(pedidos_df)} registros)")
            if itens_df is not None and not itens_df.empty:
                available_dfs.append(f"itens ({len(itens_df)} registros)")
            if clientes_df is not None and not clientes_df.empty:
                available_dfs.append(f"clientes ({len(clientes_df)} registros)")
            
            if not available_dfs:
                return "❌ Nenhum dado encontrado. Verifique se os arquivos foram processados corretamente."
            
            summary = f"📊 RESUMO DOS DADOS DA ZAPCHICKEN:\n\n"
            summary += f"📁 DataFrames disponíveis: {', '.join(available_dfs)}\n\n"
            
            if pedidos_df is not None and not pedidos_df.empty:
                pedidos_df['Data Fechamento'] = pd.to_datetime(pedidos_df['Data Fechamento'])
                
                summary += f"🛒 PEDIDOS:\n"
                summary += f"• Total de pedidos: {len(pedidos_df):,}\n"
                summary += f"• Receita total: R$ {pedidos_df['Total'].sum():,.2f}\n"
                summary += f"• Ticket médio: R$ {pedidos_df['Total'].mean():.2f}\n"
                summary += f"• Período: {pedidos_df['Data Fechamento'].min().strftime('%d/%m/%Y')} a {pedidos_df['Data Fechamento'].max().strftime('%d/%m/%Y')}\n"
                summary += f"• Clientes únicos: {pedidos_df['Cliente'].nunique():,}\n"
                
                # Top origens
                origem_analise = pedidos_df['Origem'].value_counts().head(3)
                summary += f"• Principais origens: {origem_analise.to_dict()}\n\n"
                
                # Análise temporal
                vendas_diarias = pedidos_df.groupby('Data Fechamento')['Total'].sum()
                summary += f"• Média diária: R$ {vendas_diarias.mean():.2f}\n"
                summary += f"• Maior dia: R$ {vendas_diarias.max():.2f}\n"
                summary += f"• Menor dia: R$ {vendas_diarias.min():.2f}\n"
                
                # Análise por origem
                vendas_por_origem = pedidos_df.groupby('Origem')['Total'].agg(['sum', 'count', 'mean']).round(2)
                summary += f"• Vendas por origem:\n"
                for origem, data in vendas_por_origem.iterrows():
                    summary += f"  - {origem}: R$ {data['sum']:,.2f} ({data['count']} pedidos, ticket R$ {data['mean']:.2f})\n"
                
                # Análise mensal
                pedidos_df['Mes'] = pedidos_df['Data Fechamento'].dt.to_period('M')
                vendas_mensais = pedidos_df.groupby('Mes')['Total'].sum()
                summary += f"• Vendas mensais: {vendas_mensais.to_dict()}\n\n"
            
            if itens_df is not None and not itens_df.empty:
                summary += f"🛍️ PRODUTOS:\n"
                summary += f"• Total de itens vendidos: {itens_df['Qtd.'].sum():,}\n"
                
                # Verifica se as colunas existem (com tratamento para espaços)
                nome_prod_col = 'Nome Prod.' if 'Nome Prod.' in itens_df.columns else 'Nome Prod'
                cat_prod_col = 'Cat. Prod.' if 'Cat. Prod.' in itens_df.columns else 'Cat. Prod'
                
                if nome_prod_col in itens_df.columns:
                    summary += f"• Produtos únicos: {itens_df[nome_prod_col].nunique():,}\n"
                else:
                    summary += f"• Produtos únicos: {itens_df.shape[0]:,}\n"
                    
                if cat_prod_col in itens_df.columns:
                    summary += f"• Categorias: {itens_df[cat_prod_col].nunique():,}\n"
                else:
                    summary += f"• Categorias: N/A\n"
                
                # Top produtos (se a coluna existir)
                if nome_prod_col in itens_df.columns:
                    try:
                        top_produtos = itens_df.groupby(nome_prod_col)['Qtd.'].sum().nlargest(10)
                        summary += f"• Top 10 produtos por quantidade:\n"
                        for i, (produto, qtd) in enumerate(top_produtos.items(), 1):
                            summary += f"  {i}. {produto}: {qtd} unidades\n"
                    except:
                        summary += f"• Top produtos: Erro ao processar\n"
                else:
                    summary += f"• Top produtos: Coluna não encontrada\n"
                
                # Top produtos por valor
                try:
                    itens_df['Valor Total'] = itens_df['Qtd.'] * itens_df['Valor Un. Item']
                    top_produtos_valor = itens_df.groupby(nome_prod_col)['Valor Total'].sum().nlargest(5)
                    summary += f"• Top 5 produtos por valor:\n"
                    for i, (produto, valor) in enumerate(top_produtos_valor.items(), 1):
                        summary += f"  {i}. {produto}: R$ {valor:,.2f}\n"
                except:
                    summary += f"• Top produtos por valor: Erro ao processar\n"
                
                summary += "\n"
            
            if clientes_df is not None and not clientes_df.empty:
                summary += f"👥 CLIENTES:\n"
                summary += f"• Total de clientes: {len(clientes_df):,}\n"
                
                # Análise de bairros
                if 'Bairro' in clientes_df.columns:
                    top_bairros = clientes_df['Bairro'].value_counts().head(5)
                    summary += f"• Top 5 bairros: {top_bairros.to_dict()}\n"
                
                # Top clientes por valor gasto
                try:
                    clientes_por_valor = pedidos_df.groupby('Cliente')['Total'].sum().nlargest(10)
                    summary += f"• Top 10 clientes por valor gasto:\n"
                    for i, (cliente, valor) in enumerate(clientes_por_valor.items(), 1):
                        summary += f"  {i}. {cliente}: R$ {valor:,.2f}\n"
                except:
                    summary += f"• Top clientes: Erro ao processar\n"
                
                # Análise de frequência de compra
                try:
                    freq_compra = pedidos_df['Cliente'].value_counts()
                    summary += f"• Análise de frequência:\n"
                    summary += f"  - Clientes com 1 pedido: {len(freq_compra[freq_compra == 1])}\n"
                    summary += f"  - Clientes com 2-5 pedidos: {len(freq_compra[(freq_compra >= 2) & (freq_compra <= 5)])}\n"
                    summary += f"  - Clientes com 6+ pedidos: {len(freq_compra[freq_compra >= 6])}\n"
                except:
                    summary += f"• Análise de frequência: Erro ao processar\n"
                
                summary += "\n"
            
            return summary
            
        except Exception as e:
            return f"❌ Erro ao preparar dados: {str(e)}"
    
    def _build_gemini_prompt(self, question: str, data_summary: str) -> str:
        """Constrói prompt otimizado para o Gemini"""
        
        system_prompt = f"""
Você é um especialista em Business Intelligence e análise de dados para restaurantes/food service. 
Você está analisando dados da ZapChicken, um negócio de delivery de comida.

IMPORTANTE: Use APENAS os dados fornecidos abaixo. NÃO faça suposições ou estimativas. 
Se os dados não estiverem disponíveis, diga claramente "Dados não disponíveis".

DADOS DISPONÍVEIS:
{data_summary}

INSTRUÇÕES ESPECÍFICAS:
1. Use EXATAMENTE os números e dados fornecidos acima
2. NÃO faça estimativas ou suposições
3. Se pedir dados específicos que não estão na lista, diga "Dados não disponíveis"
4. Apresente os dados em formato de tabela quando possível
5. Use os valores reais dos dados fornecidos
6. Seja preciso e específico com os números
7. Use emojis para tornar a resposta visual
8. Estruture com títulos claros
9. Formate valores monetários com R$ e separadores de milhares
10. Use formatação markdown para tabelas bem estruturadas
11. Adicione insights estratégicos baseados nos dados
12. Use cores e formatação para destacar informações importantes

PERGUNTA DO USUÁRIO: {question}

FORMATAÇÃO ESPECÍFICA:
- Use tabelas markdown bem estruturadas
- Formate valores monetários: R$ 1.234,56
- Use emojis para categorias: 🛒 Pedidos, 🛍️ Produtos, 👥 Clientes, 💰 Financeiro
- Adicione insights estratégicos após cada tabela
- Use **negrito** para destacar valores importantes
- Estruture com títulos claros usando ###

EXEMPLO DE FORMATAÇÃO:
### 💰 Resumo Financeiro
| Mês | Receita Total |
|-----|---------------|
| Fevereiro/2025 | **R$ 30.118,61** |
| Março/2025 | **R$ 41.458,60** |

**💡 Insight:** Março foi o mês com maior receita, com crescimento de 37,6% em relação a fevereiro.

### 🛒 Top Produtos
| Produto | Quantidade | Valor |
|---------|------------|-------|
| Produto A | 500 | **R$ 25.000,00** |

**💡 Insight:** Este produto representa 15% da receita total.

INSIGHTS ESTRATÉGICOS A INCLUIR:
- 🎯 **Oportunidades:** Identifique produtos/clientes com potencial
- 📈 **Tendências:** Analise crescimento/queda nos dados
- 💡 **Recomendações:** Sugira ações específicas baseadas nos dados
- ⚠️ **Alertas:** Destaque pontos de atenção
- 🚀 **Estratégias:** Proponha melhorias baseadas nos insights

IMPORTANTE: Responda usando APENAS os dados fornecidos. Se algo não estiver nos dados, diga claramente.
"""
        
        return system_prompt
    
    def _call_gemini_api(self, prompt: str) -> str:
        """Chama a API do Gemini"""
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                }
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
                else:
                    return "❌ Resposta vazia da API Gemini"
            else:
                return f"❌ Erro na API Gemini: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Erro ao chamar Gemini API: {str(e)}"
    
    def _fallback_analysis(self, question: str) -> str:
        """Análise básica quando Gemini não está disponível"""
        try:
            pedidos_df = self.processor.dataframes.get('pedidos')
            if pedidos_df is None or pedidos_df.empty:
                return "❌ Dados não disponíveis. Processe os dados primeiro."
            
            question_lower = question.lower()
            
            # Análise básica baseada em palavras-chave
            if any(word in question_lower for word in ['venda', 'comprou', 'pedido']):
                total_vendas = pedidos_df['Total'].sum()
                ticket_medio = pedidos_df['Total'].mean()
                return f"""
📊 **ANÁLISE BÁSICA DE VENDAS**

• Total de Vendas: R$ {total_vendas:,.2f}
• Ticket Médio: R$ {ticket_medio:.2f}
• Total de Pedidos: {len(pedidos_df):,}

💡 **Para análises mais avançadas, configure uma API key do Gemini!**
"""
            
            elif any(word in question_lower for word in ['cliente', 'inativo']):
                total_clientes = pedidos_df['Cliente'].nunique()
                return f"""
👥 **ANÁLISE BÁSICA DE CLIENTES**

• Total de Clientes Únicos: {total_clientes:,}
• Pedidos por Cliente: {len(pedidos_df) / total_clientes:.1f}

💡 **Para análise RFM e segmentação, configure uma API key do Gemini!**
"""
            
            else:
                return f"""
🤖 **IA ZapChicken - Modo Básico**

Pergunta: "{question}"

📊 **Dados Disponíveis:**
• {len(pedidos_df):,} pedidos processados
• R$ {pedidos_df['Total'].sum():,.2f} em vendas totais

💡 **Para análises avançadas com IA, configure uma API key do Gemini!**

🔧 **Como configurar:**
1. Acesse: https://makersuite.google.com/app/apikey
2. Crie uma API key gratuita
3. Configure na aplicação
4. Desfrute de análises muito mais inteligentes!
"""
                
        except Exception as e:
            return f"❌ Erro na análise básica: {str(e)}"
    
    def set_api_key(self, api_key: str):
        """Define a API key do Gemini"""
        self.api_key = api_key
        return "✅ API key do Gemini configurada com sucesso!"
    
    def get_api_status(self) -> str:
        """Verifica status da API"""
        if not self.api_key:
            return "❌ API key não configurada"
        
        try:
            # Teste simples da API
            test_prompt = "Responda apenas: 'API funcionando'"
            response = self._call_gemini_api(test_prompt)
            
            if "API funcionando" in response:
                return "✅ API Gemini funcionando perfeitamente"
            else:
                return f"⚠️ API respondeu, mas inesperadamente: {response[:100]}..."
                
        except Exception as e:
            return f"❌ Erro na API: {str(e)}"
    
    def get_data_status(self) -> str:
        """Verifica status dos dados carregados"""
        try:
            if not hasattr(self.processor, 'dataframes') or self.processor.dataframes is None:
                return "❌ Processador não tem dados carregados"
            
            pedidos_df = self.processor.dataframes.get('pedidos')
            itens_df = self.processor.dataframes.get('itens')
            clientes_df = self.processor.dataframes.get('clientes')
            
            status = []
            if pedidos_df is not None and not pedidos_df.empty:
                status.append(f"✅ Pedidos: {len(pedidos_df)} registros")
            else:
                status.append("❌ Pedidos: não encontrado")
                
            if itens_df is not None and not itens_df.empty:
                status.append(f"✅ Itens: {len(itens_df)} registros")
            else:
                status.append("❌ Itens: não encontrado")
                
            if clientes_df is not None and not clientes_df.empty:
                status.append(f"✅ Clientes: {len(clientes_df)} registros")
            else:
                status.append("❌ Clientes: não encontrado")
            
            return "\n".join(status)
            
        except Exception as e:
            return f"❌ Erro ao verificar dados: {str(e)}"
