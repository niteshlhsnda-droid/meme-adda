// Meme Adda dashboard — renders trends.json (watch.py output), the template
// library (templates/templates.json) and the production queue
// (state/queue.json + state/posted.json). Vanilla JS, no build step —
// Pages serves the repo root at /meme-adda/, so all fetches are relative.
(function () {
  "use strict";

  var SITE = "https://niteshlhsnda-droid.github.io/meme-adda/?utm_source=whatsapp&utm_medium=share&utm_campaign=trend-dashboard";
  var SHARE_TEXT = "😂 Meme Adda ka Trend Adda dekho — aaj ke verified meme trends, sabse pehle! 👇\n" + SITE;

  function setShareLinks() {
    var href = "https://wa.me/?text=" + encodeURIComponent(SHARE_TEXT);
    ["wa-share-top", "wa-share-bottom"].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.href = href;
    });
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function badge(t) {
    if (t.seeded) return '<span class="badge seeded">seeded template</span>';
    var label = t.label || "watch";
    var flame = label === "verified" ? "🔥 verified" : label === "rising" ? "📈 rising" : "👀 watch";
    return '<span class="badge ' + esc(label) + '">' + flame + "</span>";
  }

  function renderTrends(data) {
    var box = document.getElementById("trends");
    document.getElementById("generated-at").textContent =
      "Last updated: " + (data.generated_at_ist || "—") + " · " + (data.trend_count || 0) + " trends tracked";
    if (!data.trends || !data.trends.length) {
      box.innerHTML = '<p class="loading">Abhi koi trend nahi mila — next watch run jald aayega.</p>';
    } else {
      box.innerHTML = data.trends.map(function (t) {
        var title = t.url
          ? '<a href="' + esc(t.url) + '" target="_blank" rel="noopener">' + esc(t.title) + "</a>"
          : esc(t.title);
        var srcs = (t.sources || []).join(", ");
        return '<div class="trend">' + badge(t) + "<div>" + title +
          '<div class="sub">' + esc(t.kind || "") + (srcs ? " · sources: " + esc(srcs) : "") + "</div></div></div>";
      }).join("");
    }
    var st = data.source_status || {};
    document.getElementById("source-status").textContent =
      "Sources: " + Object.keys(st).map(function (k) { return k + " — " + st[k]; }).join(" · ");
  }

  function renderTemplates(list) {
    var box = document.getElementById("templates");
    if (!list || !list.length) {
      box.innerHTML = '<p class="loading">Template library khaali hai.</p>';
      return;
    }
    box.innerHTML = list.map(function (t) {
      return '<div class="tpl"><div class="name">' + esc(t.name) + '</div>' +
        '<div class="origin">' + esc(t.origin || "") + " · " + esc(t.format || "") +
        " · used " + (t.use_count || 0) + "×</div>" +
        (t.rights_note ? '<div class="rights">⚖️ ' + esc(t.rights_note) + "</div>" : "") + "</div>";
    }).join("");
  }

  function renderQueue(queue, posted) {
    var box = document.getElementById("queue");
    document.getElementById("posted-count").textContent =
      "Abhi tak posted (read-back verified): " + (posted ? posted.length : 0);
    if (!queue || !queue.length) {
      box.innerHTML = '<p class="loading">Queue khaali hai — production phase me pehla meme yahi line up hoga. 🎬</p>';
      return;
    }
    box.innerHTML = queue.map(function (q) {
      return '<div class="queue-item"><span class="stage">' + esc(q.stage || "queued") + "</span><br>" +
        esc(q.title || q.id || "") + "</div>";
    }).join("");
  }

  function getJson(path) {
    return fetch(path, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error(path + " -> " + r.status);
      return r.json();
    });
  }

  setShareLinks();
  getJson("trends.json").then(renderTrends).catch(function (e) {
    document.getElementById("trends").innerHTML =
      '<p class="loading">Trends load nahi hue (' + esc(e.message) + ").</p>";
  });
  getJson("templates/templates.json").then(renderTemplates).catch(function () {
    document.getElementById("templates").innerHTML = '<p class="loading">Templates load nahi hue.</p>';
  });
  Promise.all([getJson("state/queue.json").catch(function () { return []; }),
               getJson("state/posted.json").catch(function () { return []; })])
    .then(function (res) { renderQueue(res[0], res[1]); });
})();
