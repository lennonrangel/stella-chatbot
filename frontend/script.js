const BASE_URL = "http://127.0.0.1:5000";
const API_URL = `${BASE_URL}/api/chat`;

const messagesEl = document.getElementById("messages");
const inputEl    = document.getElementById("msg-input");
const sendBtn    = document.getElementById("send-btn");
const timeEl     = document.getElementById("header-time");
const interestelarBg = document.getElementById("interestelar-bg");

let SESSION_ID = localStorage.getItem("stellar_session");
let followupPendente = null;
let mibQuestionRow = null;
let mibResponsePromise = null;

/* ===== SESSÃO ===== */

async function initSession() {
  try {
    const res = await fetch(`${BASE_URL}/api/welcome`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sessao_id: SESSION_ID })
    });

    const data = await res.json();
    SESSION_ID = data.sessao_id;
    localStorage.setItem("stellar_session", SESSION_ID);

  } catch {
  }
}

/* ===== ESTRELAS ===== */

const canvas = document.getElementById("estrelas");
const ctx    = canvas.getContext("2d");
let stars    = [];

function resizeCanvas() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
  initStars();
}

function initStars() {
  stars = Array.from({ length: 180 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: Math.random() * 1.2 + 0.2,
    opacity: Math.random() * 0.7 + 0.1,
    speed: Math.random() * 0.015 + 0.003,
    phase: Math.random() * Math.PI * 2
  }));
}

function drawStars(t) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  stars.forEach(s => {
    const o = s.opacity * (0.6 + 0.4 * Math.sin(t * s.speed + s.phase));
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(220, 210, 190, ${o})`;
    ctx.fill();
  });

  requestAnimationFrame(drawStars);
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
requestAnimationFrame(drawStars);

/* ===== RELÓGIO ===== */

function updateClock() {
  const now = new Date();
  const h = String(now.getHours()).padStart(2, "0");
  const m = String(now.getMinutes()).padStart(2, "0");
  const s = String(now.getSeconds()).padStart(2, "0");
  timeEl.textContent = `${h}:${m}:${s}`;
}

setInterval(updateClock, 1000);
updateClock();

/* ===== UI ===== */

const welcomeEl = document.getElementById("boasvindas");

function hideWelcome() {
  if (!welcomeEl) return;
  welcomeEl.style.opacity = "0";
  setTimeout(() => welcomeEl.remove(), 400);
}

/* ===== BALÃO DE MENSAGEM DO USUÁRIO ===== */

function addUserMessage(text) {
  hideWelcome();

  const row = document.createElement("div");
  row.className = "message-row user-row";

  row.innerHTML = `
    <div class="msg-col">
      <div class="message user-msg">${escapeHtml(text)}</div>
    </div>
  `;

  messagesEl.appendChild(row);
  scrollBottom();
  return row;
}

/* ===== BALÃO DE MENSAGEM DO BOT ===== */

function addBotMessage(text, imagem = null, followupPergunta = null, source = null) {
  hideWelcome();

  const row = document.createElement("div");
  row.className = "message-row";

  const imagemHtml = Array.isArray(imagem)
    ? imagem.map(src => `<img src="${src}" alt="" class="msg-img">`).join("")
    : imagem
    ? `<img src="${imagem}" alt="" class="msg-img">`
    : "";

  const followupHtml = followupPergunta
    ? `<p class="msg-followup">${escapeHtml(followupPergunta)}</p>`
    : "";

  // Badge de fonte — mostra ao usuário de onde veio a resposta
  let sourceBadge = "";
  if (source === "knowledge_base") {
    sourceBadge = `<span class="source-badge source-kb" title="Resposta da Base de Conhecimento">Base de conhecimento</span>`;
  } else if (source === "llm") {
    sourceBadge = `<span class="source-badge source-llm" title="Resposta gerada pela IA">LLM</span>`;
  }

  // Formata texto: suporte a *negrito* e quebras de linha
  const formattedText = escapeHtml(text.trim())
    .replace(/\n/g, "<br>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");

  row.innerHTML = `
    <div class="msg-bot bot-av">✦</div>
    <div class="msg-col">
      <div class="message bot-msg">
        <p class="msg-text">${formattedText}</p>
        <div class="msg-footer">
          ${imagemHtml}
          ${followupHtml}
          ${sourceBadge}
        </div>
      </div>
    </div>
  `;

  messagesEl.appendChild(row);
  scrollBottom();
}

function showTyping() {
  const row = document.createElement("div");
  row.className = "message-row";
  row.id = "typing";

  row.innerHTML = `
    <div class="msg-bot bot-av">✦</div>
    <div class="msg-col">
      <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    </div>
  `;

  messagesEl.appendChild(row);
  scrollBottom();
}

function removeTyping() {
  const t = document.getElementById("typing");
  if (t) t.remove();
}

function scrollBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function normalizeText(text) {
  return text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

const INTERESTELAR_KEYWORDS = [
  "interestelar",
  "interstellar",
  "filme interestelar",
  "o filme interestelar",
];

function isInterestelarQuestion(text) {
  const lower = normalizeText(text);
  return INTERESTELAR_KEYWORDS.some(keyword =>
    lower.includes(normalizeText(keyword))
  );
}

function setInterestelarBackground(active) {
  if (!interestelarBg) return;

  document.body.classList.toggle("interestelar-mode", active);
  interestelarBg.classList.toggle("ativo", active);

  if (active) {
    const playPromise = interestelarBg.play();
    if (playPromise && typeof playPromise.catch === "function") {
      playPromise.catch(() => {});
    }
    return;
  }

  interestelarBg.pause();
  interestelarBg.currentTime = 0;
}

/* ===== ENVIO DA MENSAGEM ===== */

let loading = false;

async function sendMessage(text) {
  text = text.trim();
  if (!text || loading) return;

  setInterestelarBackground(isInterestelarQuestion(text));

  /* ── MIB Easter Egg check ── */
  if (isMibQuestion(text)) {
    inputEl.value = "";
    mibQuestionRow = addUserMessage(text);
    mibResponsePromise = fetchMibResponse(text);
    await triggerMibEasterEgg();
    return;
  }

  inputEl.value = "";
  addUserMessage(text);

  loading = true;
  sendBtn.disabled = true;
  showTyping();

  try {
    const delay = new Promise(resolve => setTimeout(resolve, 800));
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        sessao_id: SESSION_ID,
        followup_pendente: followupPendente
      })
    });

    const [data] = await Promise.all([res.json(), delay]);
    removeTyping();

    if (data.error) {
      addBotMessage("Ops, algo deu errado. Tenta de novo!", "default");
      return;
    }

    addBotMessage(data.response, data.imagem, data.followup_pergunta, data.source);

    // Salva o followup_data para a próxima mensagem
    if (data.followup_data && data.followup_data.proxima_tag) {
      followupPendente = data.followup_data;
    } else {
      followupPendente = null;
    }

  } catch {
    removeTyping();
    addBotMessage("Conexão com o cosmos falhou. Tenta novamente!", "default");
  } finally {
    loading = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

sendBtn.addEventListener("click", () => sendMessage(inputEl.value));
inputEl.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage(inputEl.value);
});

initSession();

/* ════════════════════════════════════════════════════════
  MIB EASTER EGG — Nave alienígena + GIF
  Dispara quando o usuário menciona MIB / Men in Black
  ════════════════════════════════════════════════════════ */

const MIB_KEYWORDS = [
  "mib", "men in black", "homens de preto", "homem de preto",
  "agente j", "agente k", "agent j", "agent k", "will smith mib",
  "neuralizador", "neuralyzer", "edgar o bug", "edgar bug",
  "worm alien", "worms mib", "vermes alien", "verminhos",
  "tommy lee jones mib", "frank o pug", "frank pug",
  "salvo pelo sino", "sede da mib", "mib sede"
];

function isMibQuestion(text) {
  const lower = text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  return MIB_KEYWORDS.some(kw =>
    lower.includes(kw.normalize("NFD").replace(/[\u0300-\u036f]/g, ""))
  );
}

/* ── Partículas de sucção ── */
function spawnSuckParticles() {
  const chatRect = document.querySelector(".chat-container").getBoundingClientRect();
  for (let i = 0; i < 22; i++) {
    setTimeout(() => {
      const p = document.createElement("div");
      p.className = "suck-particle";
      const x = chatRect.left + Math.random() * chatRect.width;
      const y = chatRect.top  + Math.random() * chatRect.height;
      p.style.cssText = `left:${x}px; top:${y}px; --dx:${(Math.random()-0.5)*40}px; --dy:-${200 + Math.random()*200}px; --dur:${0.5 + Math.random()*0.5}s`;
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 1200);
    }, i * 45);
  }
}

/* ── Sequência principal ── */
async function triggerMibEasterEgg() {
  const overlay   = document.getElementById("mib-overlay");
  const nave      = document.getElementById("mib-nave");
  const feixe     = document.getElementById("mib-feixe");
  const feixeL    = document.getElementById("mib-feixe-linhas");
  const painel    = document.getElementById("mib-painel");
  const chatBox   = document.querySelector(".chat-container");

  // 1. Escurece a tela
  overlay.classList.add("ativo");

  // 2. Nave desce
  await new Promise(r => {
    nave.classList.add("descendo");
    nave.addEventListener("animationend", r, { once: true });
  });

  // 3. Feixe aparece + partículas
  feixe.classList.add("ativo");
  feixeL.classList.add("ativo");
  spawnSuckParticles();

  // 4. Chat sobe sendo sugado
  await new Promise(r => setTimeout(r, 300));
  chatBox.classList.add("sendo-sugado");
  await new Promise(r => setTimeout(r, 900));

  // 5. Painel do GIF aparece
  painel.classList.add("visivel");
}

async function fetchMibResponse(text) {
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        sessao_id: SESSION_ID,
        followup_pendente: followupPendente
      })
    });
    return await res.json();
  } catch (err) {
    console.error("Erro ao buscar resposta do MIB:", err);
    return { error: true };
  }
}

/* ── Fechar o painel e restaurar ── */
async function fecharMib() {
  const overlay = document.getElementById("mib-overlay");
  const nave    = document.getElementById("mib-nave");
  const feixe   = document.getElementById("mib-feixe");
  const feixeL  = document.getElementById("mib-feixe-linhas");
  const painel  = document.getElementById("mib-painel");
  const chatBox = document.querySelector(".chat-container");

  // Painel sai
  painel.classList.remove("visivel");
  feixe.classList.remove("ativo");
  feixeL.classList.remove("ativo");

  // Nave sobe
  nave.classList.remove("descendo", "sugando");
  nave.classList.add("subindo");
  nave.addEventListener("animationend", () => {
    nave.classList.remove("subindo");
  }, { once: true });

  // Restaura o chat
  chatBox.classList.remove("sendo-sugado");
  chatBox.style.animation = "";
  chatBox.style.opacity   = "";
  chatBox.style.transform = "";

  // Remove overlay
  overlay.classList.remove("ativo");

  // Forçar reflow
  void chatBox.offsetWidth;

  // Mantém a pergunta no chat (apenas limpa a referência para a próxima pergunta)
  mibQuestionRow = null;

  // Se houver uma busca em andamento
  if (mibResponsePromise) {
    loading = true;
    sendBtn.disabled = true;
    showTyping();

    try {
      const data = await mibResponsePromise;
      removeTyping();

      if (!data || data.error) {
        addBotMessage("Ops, algo deu errado com a transmissão dos Homens de Preto. Tenta de novo!", "default");
      } else {
        addBotMessage(data.response, data.imagem, data.followup_pergunta, data.source);
        
        // Salva o followup_data para a próxima mensagem
        if (data.followup_data && data.followup_data.proxima_tag) {
          followupPendente = data.followup_data;
        } else {
          followupPendente = null;
        }
      }
    } catch {
      removeTyping();
      addBotMessage("Conexão com o cosmos falhou. Tenta novamente!", "default");
    } finally {
      loading = false;
      sendBtn.disabled = false;
      inputEl.focus();
      mibResponsePromise = null;
    }
  }
}

document.getElementById("mib-fechar-btn").addEventListener("click", fecharMib);
