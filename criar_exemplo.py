#!/usr/bin/env python3
"""
Script para criar planilhas de exemplo para teste do ZapCampanhas
"""

import pandas as pd
from pathlib import Path
import random

def criar_planilha_exemplo():
    """Cria planilhas de exemplo para teste"""
    
    # Dados de exemplo
    nomes = [
        "João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa", "Carlos Ferreira",
        "Lucia Rodrigues", "Roberto Almeida", "Fernanda Lima", "Ricardo Pereira", "Juliana Souza",
        "Marcos Santos", "Patricia Costa", "Andre Oliveira", "Camila Silva", "Diego Ferreira",
        "Vanessa Lima", "Thiago Almeida", "Carolina Rodrigues", "Felipe Pereira", "Amanda Costa"
    ]
    
    cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Brasília"]
    
    telefones = [
        "(11) 99999-9999", "(11) 88888-8888", "(21) 77777-7777", "(21) 66666-6666",
        "(31) 55555-5555", "(31) 44444-4444", "(71) 33333-3333", "(71) 22222-2222",
        "(61) 11111-1111", "(61) 00000-0000", "11987654321", "21987654321",
        "31987654321", "71987654321", "61987654321"
    ]
    
    emails = [
        "joao@email.com", "maria@email.com", "pedro@email.com", "ana@email.com",
        "carlos@email.com", "lucia@email.com", "roberto@email.com", "fernanda@email.com",
        "ricardo@email.com", "juliana@email.com", "marcos@email.com", "patricia@email.com",
        "andre@email.com", "camila@email.com", "diego@email.com"
    ]
    
    # Cria diretório de entrada se não existir
    input_dir = Path("data/input")
    input_dir.mkdir(parents=True, exist_ok=True)
    
    # Planilha 1: Clientes
    print("Criando planilha: clientes.xlsx")
    clientes_data = []
    for i in range(8):
        clientes_data.append({
            'nome': random.choice(nomes),
            'telefone': random.choice(telefones),
            'cidade': random.choice(cidades),
            'email': random.choice(emails),
            'status': 'ativo',
            'data_cadastro': '2024-01-15'
        })
    
    df_clientes = pd.DataFrame(clientes_data)
    df_clientes.to_excel(input_dir / "clientes.xlsx", index=False)
    
    # Planilha 2: Prospectos
    print("Criando planilha: prospectos.xlsx")
    prospectos_data = []
    for i in range(6):
        prospectos_data.append({
            'name': random.choice(nomes),
            'phone': random.choice(telefones),
            'city': random.choice(cidades),
            'e-mail': random.choice(emails),
            'interesse': random.choice(['alto', 'medio', 'baixo']),
            'origem': 'site'
        })
    
    df_prospectos = pd.DataFrame(prospectos_data)
    df_prospectos.to_excel(input_dir / "prospectos.xlsx", index=False)
    
    # Planilha 3: Contatos
    print("Criando planilha: contatos.xlsx")
    contatos_data = []
    for i in range(5):
        contatos_data.append({
            'cliente': random.choice(nomes),
            'celular': random.choice(telefones),
            'cidade': random.choice(cidades),
            'email': random.choice(emails),
            'observacoes': 'Contato via telefone',
            'ultimo_contato': '2024-01-10'
        })
    
    df_contatos = pd.DataFrame(contatos_data)
    df_contatos.to_excel(input_dir / "contatos.xlsx", index=False)
    
    # Planilha 4: Leads
    print("Criando planilha: leads.xlsx")
    leads_data = []
    for i in range(7):
        leads_data.append({
            'customer': random.choice(nomes),
            'whatsapp': random.choice(telefones),
            'city': random.choice(cidades),
            'email': random.choice(emails),
            'score': random.randint(1, 100),
            'fonte': random.choice(['facebook', 'instagram', 'google'])
        })
    
    df_leads = pd.DataFrame(leads_data)
    df_leads.to_excel(input_dir / "leads.xlsx", index=False)
    
    print(f"\n✅ Planilhas de exemplo criadas em: {input_dir}")
    print("📊 Arquivos criados:")
    print("  - clientes.xlsx (8 registros)")
    print("  - prospectos.xlsx (6 registros)")
    print("  - contatos.xlsx (5 registros)")
    print("  - leads.xlsx (7 registros)")
    print(f"\n🚀 Agora você pode testar o sistema com:")
    print("  python main.py process")

if __name__ == "__main__":
    criar_planilha_exemplo()

