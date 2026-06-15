# Stella — ChatBot de Curiosidades Cósmicas

Chatbot inteligente com arquitetura **BDI (Beliefs, Desires, Intentions)** desenvolvido para exploração de temas astronômicos e espaciais. A Stella combina uma **Base de Conhecimento** factual com um **LLM (Qwen2.5-7B-Instruct)** disponível no Hugging Face para oferecer respostas precisas e naturais.

---

## 🚀 Como Executar a Stella

### 1. Instalar Dependências

```powershell
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

---

### 2. Instalar o PyTorch com Suporte a GPU (CUDA) ⚠️

> O `pip install -r requirements.txt` instala o PyTorch na versão **CPU-only** por padrão.
> Para usar a GPU (recomendado), é necessário reinstalar manualmente com o índice correto.

**Passo 1** — Verifique a versão do CUDA do seu driver:
```powershell
nvidia-smi
```
Procure a linha `CUDA Version: X.X` no canto superior direito da tabela.

**Passo 2** — Reinstale o PyTorch com o comando correspondente:

```powershell
# CUDA 12.4 (drivers recentes — RTX 30xx, 40xx)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CUDA 11.8 (GPUs mais antigas)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Passo 3** — Confirme que a GPU foi detectada:
```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```
Saída esperada:
```
True
NVIDIA GeForce RTX XXXX
```

> **Sem GPU?** A Stella funciona normalmente em CPU, mas as respostas do LLM
> serão mais lentas (15–40s). Considere usar o modelo menor via variável de ambiente (ver seção 3).

---

### 3. Configurar o `.env`

Crie (ou edite) o arquivo `.env` na raiz do projeto:

```env
# ── Modo de operação ──────────────────────────────────────────
# auto   → tenta remoto primeiro; se falhar usa local  (padrão)
# local  → somente modelo local — sem internet, sem créditos
# remoto → somente HF Inference Providers
LLM_MODE=auto

# ── Modelo remoto (HF Inference Providers) ────────────────────
# Token: https://huggingface.co/settings/tokens
# Créditos gratuitos: https://huggingface.co/settings/billing
HF_TOKEN=seu_token_aqui
STELLA_REMOTE_MODEL=Qwen/Qwen2.5-7B-Instruct

# ── Modelo local (baixado uma vez, roda offline) ──────────────
# Escolha conforme seu hardware:
#   Qwen/Qwen2.5-1.5B-Instruct  → ~2 GB RAM  (PC fraco / CPU)
#   Qwen/Qwen2.5-3B-Instruct    → ~5 GB RAM  (CPU intermediário)
#   Qwen/Qwen2.5-7B-Instruct    → ~9 GB VRAM (GPU recomendado)
STELLA_LOCAL_MODEL=Qwen/Qwen2.5-7B-Instruct
```

> O modelo local é **baixado automaticamente do Hugging Face na primeira execução**
> e salvo em cache. Nas execuções seguintes, carrega direto do disco.

---

### 4. Iniciar a Stella

```powershell
python main.py
```

Acesse em: **http://127.0.0.1:5000**

---

## 🧠 Arquitetura do Projeto

A Stella utiliza uma estrutura modular em cinco camadas:

| Camada | Arquivos | Responsabilidade |
|--------|----------|-----------------|
| **Frontend** | `frontend/` | Interface do usuário no navegador |
| **API REST** | `backend/api/routes.py` | Endpoints Flask, roteamento de requisições |
| **Orquestrador BDI** | `backend/bot/` | Lógica de decisão: base → LLM |
| **PLN + Busca** | `backend/nlp/` | Tokenização, TF-IDF, similaridade de cosseno |
| **LLM** | `backend/llm/fallback_service.py` | Inferência remota (HF) e local (GPU/CPU) |
| **Persistência** | `backend/db/` | SQLite — sessões e histórico de mensagens |

### Fluxo de Decisão

```
Pergunta do usuário
       ↓
  Normalização PLN (RSLP + spaCy)
       ↓
  Classificador de Intenções (BDI)
       ↓
  Base de Conhecimento (TF-IDF + Aliases)
       ↓ score suficiente?
   ┌───┴───┐
  SIM     NÃO
   ↓       ↓
Resposta  LLM Fallback
da base   (remoto → local)
```

---

## 🛠️ Tecnologias Utilizadas

| Componente | Tecnologia |
|---|---|
| **Linguagem** | Python 3.13 |
| **Framework Web** | Flask + Flask-CORS |
| **LLM** | Qwen2.5-7B-Instruct (Hugging Face) |
| **Inferência** | Transformers + PyTorch (CUDA 12.4) |
| **Processamento de Texto** | spaCy + Stemmer RSLP |
| **Algoritmo de Busca** | TF-IDF + Similaridade de Cosseno + Alias Boost |
| **Banco de Dados** | SQLite |

---

## 🌟 Funcionalidades

1. **Respostas Factuais**: consulta a Base de Conhecimento antes de qualquer chamada ao LLM, garantindo precisão científica em fatos astronômicos.
2. **Fallback Inteligente**: perguntas fora do escopo da base são respondidas pelo LLM com contexto da sessão.
3. **Três modos de LLM**: `remoto` (HF Inference Providers), `local` (GPU/CPU) e `auto` (cascata automática).
4. **Memória de Sessão**: o bot lembra dos últimos temas discutidos para responder perguntas contextuais.
5. **Anti-alucinação**: superlativos e fatos críticos são sempre servidos pela base, bloqueando o LLM nesses casos.

---

## 🔧 Solução de Problemas

| Sintoma | Causa provável | Solução |
|---------|---------------|---------|
| Respostas lentas (>30s) | PyTorch CPU-only instalado | Reinstalar com CUDA (ver seção 2) |
| `CUDA disponível: False` | torch sem suporte a CUDA | Reinstalar com `--index-url` correto |
| `402 Payment Required` | Créditos HF esgotados | Mudar `LLM_MODE=local` no `.env` |
| `Model doesn't support task` | Versão antiga do `huggingface-hub` | `pip install --upgrade huggingface-hub` |
| Respostas incorretas sobre fatos | Modelo local 1B em fallback | Verificar logs — créditos HF podem ter acabado |