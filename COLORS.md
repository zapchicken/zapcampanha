# 🎨 Paleta de Cores - ZapCampanhas

## 🎯 **Paleta Principal**

### **Cores Primárias**
- **Laranja Principal** `#FF8000` - Cor principal da marca
- **Laranja Secundário** `#FF4000` - Destaques e ações
- **Vermelho** `#FF0000` - Alertas e erros
- **Bordô** `#800000` - Elementos escuros

### **Cores Neutras**
- **Preto** `#000000` - Texto principal
- **Cinza Escuro** `#333333` - Texto secundário
- **Cinza Médio** `#666666` - Placeholders
- **Cinza Claro** `#CCCCCC` - Bordas
- **Branco** `#FFFFFF` - Fundo

### **Cores de Apoio**
- **Amarelo** `#F8CA00` - Avisos e destaque
- **Verde Oliva** `#8A9B0F` - Sucesso e confirmação
- **Roxo Escuro** `#490A3D` - Elementos premium

## 🎨 **Aplicação por Contexto**

### **Interface Web**
```css
/* Cores principais */
:root {
  --primary: #FF8000;      /* Botões principais */
  --secondary: #FF4000;    /* Botões secundários */
  --success: #8A9B0F;      /* Sucesso */
  --warning: #F8CA00;      /* Avisos */
  --danger: #FF0000;       /* Erros */
  --dark: #490A3D;         /* Elementos escuros */
  --text-primary: #000000; /* Texto principal */
  --text-secondary: #333333; /* Texto secundário */
  --background: #FFFFFF;   /* Fundo */
  --border: #CCCCCC;       /* Bordas */
}
```

### **Dashboard**
- **Header**: `#FF8000` (laranja principal)
- **Cards**: `#FFFFFF` (branco) com borda `#CCCCCC`
- **Botões**: `#FF8000` (primário), `#FF4000` (secundário)
- **Gráficos**: `#FF8000`, `#8A9B0F`, `#F8CA00`, `#490A3D`

### **Relatórios**
- **Títulos**: `#000000` (preto)
- **Dados**: `#333333` (cinza escuro)
- **Destaques**: `#FF8000` (laranja)
- **Alertas**: `#FF0000` (vermelho)

## 🎯 **Uso por Funcionalidade**

### **Upload e Processamento**
- **Área de upload**: `#FFFFFF` com borda `#CCCCCC`
- **Botão processar**: `#FF8000`
- **Progresso**: `#8A9B0F`
- **Erro**: `#FF0000`

### **Dashboard**
- **Métricas**: `#FF8000` (principal), `#8A9B0F` (secundário)
- **Gráficos**: Paleta completa
- **Status**: `#8A9B0F` (sucesso), `#F8CA00` (aviso), `#FF0000` (erro)

### **Relatórios**
- **Download**: `#FF8000`
- **Visualizar**: `#8A9B0F`
- **Status**: `#F8CA00` (processando), `#8A9B0F` (pronto)

### **IA Chat**
- **Input**: `#FFFFFF` com borda `#CCCCCC`
- **Enviar**: `#FF8000`
- **Mensagens**: `#F5F5F5` (fundo claro)
- **IA**: `#8A9B0F` (verde)

## 🎨 **Gradientes**

### **Gradiente Principal**
```css
background: linear-gradient(135deg, #FF8000 0%, #FF4000 100%);
```

### **Gradiente Secundário**
```css
background: linear-gradient(135deg, #8A9B0F 0%, #490A3D 100%);
```

### **Gradiente de Sucesso**
```css
background: linear-gradient(135deg, #8A9B0F 0%, #F8CA00 100%);
```

## 🎯 **Acessibilidade**

### **Contraste Mínimo**
- **Texto sobre laranja**: `#000000` (preto)
- **Texto sobre verde**: `#FFFFFF` (branco)
- **Texto sobre amarelo**: `#000000` (preto)

### **Estados Interativos**
- **Hover**: Escurecer 10%
- **Active**: Escurecer 20%
- **Disabled**: Opacidade 50%

## 🎨 **Implementação**

### **CSS Variables**
```css
:root {
  /* Cores principais */
  --zap-orange: #FF8000;
  --zap-orange-dark: #FF4000;
  --zap-red: #FF0000;
  --zap-bordeaux: #800000;
  
  /* Neutras */
  --zap-black: #000000;
  --zap-gray-dark: #333333;
  --zap-gray: #666666;
  --zap-gray-light: #CCCCCC;
  --zap-white: #FFFFFF;
  
  /* Apoio */
  --zap-yellow: #F8CA00;
  --zap-green: #8A9B0F;
  --zap-purple: #490A3D;
}
```

### **Classes Utilitárias**
```css
.bg-primary { background-color: var(--zap-orange); }
.bg-secondary { background-color: var(--zap-orange-dark); }
.bg-success { background-color: var(--zap-green); }
.bg-warning { background-color: var(--zap-yellow); }
.bg-danger { background-color: var(--zap-red); }
.bg-dark { background-color: var(--zap-purple); }

.text-primary { color: var(--zap-orange); }
.text-secondary { color: var(--zap-gray-dark); }
.text-success { color: var(--zap-green); }
.text-warning { color: var(--zap-yellow); }
.text-danger { color: var(--zap-red); }
```

---

**🎨 Esta paleta garante consistência visual e identidade de marca forte para o ZapCampanhas!**
