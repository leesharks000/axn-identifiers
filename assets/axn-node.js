/* axn-node.js — node resolution for a stamper that works wherever it lives.
 *
 * THE POINT. An AXN is content-derived: the identity kernel is the SHA-256 of the
 * canonical bytes, computed here, in this browser, from your file. That
 * computation needs no server at all. What a server provides is only ever
 * ADDRESSING — a record address in a registry, and locations naming where
 * verified copies can be obtained.
 *
 * So this stamper is node-agnostic by construction. It tries each declared node
 * in turn for lookup and registration, reports WHICH node answered, and when no
 * node answers it still computes the kernel and emits the Seed A sidecar —
 * because the kernel is true or false independently of every registry,
 * including ours. An unreachable registry costs you an address, not an identity.
 *
 * Adding a node is adding a line. That is what makes the network a rhizome
 * rather than a hierarchy with a spare.
 */
const AXN_NODES = [
  { node: "alexanarch.org", role: "registry · mint · preserve",
    registry: "https://www.alexanarch.org/data/axn-central-registry.json",
    register: "https://www.alexanarch.org/api/register-symbolon",
    declaration: "https://www.alexanarch.org/.well-known/axn-node.json" }
  /* Peers append here. A node qualifies only under independent custody:
     separate operator, registrar, hosting account AND billing. Ten sites under
     one administrator are one site in disguise. */
];

const AXN_GLYPHS = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘", "⭐", "🌟", "💫", "☀️", "🌙", "🪐", "🌍", "🌊", "🔥", "💧", "🌪️", "⚡", "❄️", "🌋", "🏔️", "🌿", "🍃", "🌱", "🌾", "🪨", "💎", "🧊", "🌈", "☁️", "🏛️", "🏗️", "🧱", "🪜", "🚪", "🪟", "🏠", "🏰", "⛩️", "🕌", "🗼", "🌉", "⚓", "🛡️", "🔔", "🏺", "🔧", "🔩", "⚙️", "🔗", "🪝", "🧲", "⚖️", "🔬", "🔭", "🧪", "🧫", "🧬", "💡", "🔮", "🪄", "🗝️", "📜", "📖", "📝", "✏️", "🖊️", "📋", "📌", "📎", "🔖", "📚", "🗂️", "📦", "🏷️", "🪧", "📐", "📏", "🧭", "🗺️", "🏴", "🚩", "⛳", "🎯", "🔍", "👁️", "🔎", "🪞", "🗡️", "🛤️", "⛵", "🚀", "🛸", "🌀", "⌛", "⏰", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛", "⌛", "🔄", "🌸", "🌺", "🌻", "🌹", "🍀", "🌲", "🌳", "🍁", "🍂", "🍄", "🐚", "🪸", "🦋", "🐝", "🕊️", "🦅", "♠️", "❤️", "♦️", "♣️", "🎭", "🎪", "🎨", "🎵", "🎶", "🎹", "🎻", "🎺", "🥁", "🎲", "🃏", "🀄", "➕", "➖", "✖️", "➗", "♾️", "∮", "⊕", "⊗", "△", "▽", "◇", "○", "●", "□", "■", "▲", "🜁", "🝊", "☿", "♃", "♄", "♅", "♆", "☉", "☽", "♈", "♉", "♊", "♋", "♌", "♍", "♎", "👁‍🗨", "🤲", "👐", "🙏", "✊", "🤝", "👆", "👇", "👈", "👉", "🫵", "🖐️", "✋", "🫶", "🤙", "👋", "🚨", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚪", "⚫", "🟤", "💜", "💙", "💚", "💛", "🧡", "❤️", "🔺", "🔻", "◀️", "▶️", "🔼", "🔽", "⏩", "⏪", "⏫", "⏬", "↗️", "↘️", "↙️", "↖️", "🔃", "🔀", "🌅", "🌄", "🌃", "🌆", "🌇", "🏙️", "🌌", "🎆", "🎇", "✨", "🌠", "💥", "🔆", "🔅", "⭕", "❌", "🏁", "🎬", "🔚", "🔙", "🔛", "🔝", "🔜", "⏹️", "⏏️", "🔒", "🔓", "🔐", "🗿", "🪦", "♻️", "∞"];
const AXN_CLUSTERS = ["cel", "cel", "cel", "cel", "cel", "cel", "cel", "cel", "cel", "cel", "cel", "cel", "cel", "cel", "cel", "cel", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "ele", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "arc", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "ins", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "scr", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "nav", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "tem", "org", "org", "org", "org", "org", "org", "org", "org", "org", "org", "org", "org", "org", "org", "org", "org", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "sym", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "mat", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "alc", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "ges", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "sig", "str", "str", "str", "str", "str", "str", "str", "str", "str", "str", "str", "str", "str", "str", "str", "str", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "lim", "ter", "ter", "ter", "ter", "ter", "ter", "ter", "ter", "ter", "ter", "ter", "ter", "ter", "ter", "ter", "ter"];

async function axnKernel(bytes) {
  const d = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(d)).map(b => b.toString(16).padStart(2, "0")).join("");
}
function axnGlyphs(hex) {
  const out = [];
  for (let i = 0; i < 12; i += 2) out.push(AXN_GLYPHS[parseInt(hex.slice(i, i + 2), 16)]);
  return out.join("");
}
function axnClusters(hex) {
  const out = [];
  for (let i = 0; i < 12; i += 2) out.push(AXN_CLUSTERS[parseInt(hex.slice(i, i + 2), 16)]);
  return out;
}

/* Try every node in turn. Returns {node, data} or throws only when ALL fail —
 * and the caller is expected to continue without a registry, not to stop. */
async function axnFetchFirst(key, timeoutMs = 20000) {
  const errors = [];
  for (const n of AXN_NODES) {
    if (!n[key]) continue;
    try {
      const ctl = new AbortController();
      const t = setTimeout(() => ctl.abort(), timeoutMs);
      const r = await fetch(n[key], { signal: ctl.signal });
      clearTimeout(t);
      if (!r.ok) { errors.push(n.node + " HTTP " + r.status); continue; }
      const ct = (r.headers.get("content-type") || "").toLowerCase();
      if (ct.indexOf("json") === -1) { errors.push(n.node + " served " + ct); continue; }
      return { node: n.node, data: await r.json() };
    } catch (e) { errors.push(n.node + " " + (e.name || e.message)); }
  }
  throw new Error("no node answered — " + errors.join(" · "));
}

/* Registration is an address, not a verification. Failure here never
 * invalidates a kernel; it only means the identity is not yet addressed. */
async function axnRegister(seedA) {
  const errors = [];
  for (const n of AXN_NODES) {
    if (!n.register) continue;
    try {
      const r = await fetch(n.register, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(seedA)
      });
      const j = await r.json();
      if (r.ok) return { node: n.node, result: j };
      errors.push(n.node + ": " + (j.error || r.status));
    } catch (e) { errors.push(n.node + ": " + e.message); }
  }
  return { node: null, error: errors.join(" · ") };
}
