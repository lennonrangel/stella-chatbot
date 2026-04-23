const BASE_URL = "http://127.0.0.1:5000";
const API_URL = `${BASE_URL}/api/chat`;

const messagesEl = document.getElementById("messages");
const inputEl    = document.getElementById("msg-input");
const sendBtn    = document.getElementById("send-btn");
const timeEl     = document.getElementById("header-time");

let SESSION_ID = localStorage.getItem("stellar_session");
let followupPendente = null;

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

  } catch (erro) {
    console.error("Erro ao iniciar sessão:", erro);
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

function drawStars(timestamp) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  stars.forEach(s => {
    const o = s.opacity * (0.6 + 0.4 * Math.sin(timestamp * s.speed + s.phase));
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
}

/* ===== BALÃO DE MENSAGEM DO BOT ===== */

function addBotMessage(text, imagem = null, followupPergunta = null) {
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

  row.innerHTML = `
    <div class="msg-bot bot-av">✦</div>
    <div class="msg-col">
      <div class="message bot-msg">
        <p class="msg-text">${escapeHtml(text).replace(/\n/g, "<br>")}</p>
        ${imagemHtml}
        ${followupHtml}
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

/* ===== ENVIO DA MENSAGEM ===== */

let loading = false;

let data;
data.followup_data = undefined;
data.followup_data.proxima_tag = undefined;

async function sendMessage(text) {
  text = text.trim();
  if (!text || loading) return;

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
    data.followup_pergunta = undefined;
    data.imagem = undefined;
    removeTyping();

    if (data.error) {
      addBotMessage("Ops, algo deu errado. Tenta de novo!", "default");
      return;
    }

    addBotMessage(data.response, data.imagem, data.followup_pergunta);

    // Salva o followup_data para a próxima mensagem
    if (data.followup_data && data.followup_data.proxima_tag) {
      followupPendente = data.followup_data;
    } else {
      followupPendente = null;
    }

  } catch (erro) {
    console.error("Erro ao enviar mensagem:", erro);
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
  if (e.key === "Enter") sendMessage(inputEl.value).then(r =>{} );
});

// Corrigindo a chamada da sessão para não ignorar a Promise
(async () => {
  await initSession();
})();
