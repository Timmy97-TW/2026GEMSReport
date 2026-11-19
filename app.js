/* GEMS Research · iGEM 2026 Report — single-page app, no build step at runtime.
   Data comes from data/*.js (window.RESULTS, window.REPORT, window.TEAMS, window.TRENDS). */
(function () {
  "use strict";

  var LANG = "en";
  var RESULTS = window.RESULTS || {};
  var REPORT = window.REPORT || {};
  var TEAMS = window.TEAMS || [];
  var TRENDS = window.TRENDS || { academic: {}, industry: {} };

  /* ---------- i18n helpers ---------- */
  function L(en, zh) { return LANG === "zh" ? (zh || en) : en; }
  // field lookup with _zh fallback
  function T(o, k) {
    if (!o) return "";
    if (LANG === "zh") { var z = o[k + "_zh"]; if (z) return z; }
    return o[k] || "";
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  // **bold** and *italic* -> tags; everything else stays escaped.
  // Bold runs first so its asterisks are consumed before the italic pass.
  function rich(s) {
    return esc(s)
      .replace(/\*\*([^*]+?)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[^*\w])\*([^*\n]+?)\*(?![*\w])/g, "$1<em>$2</em>");
  }
  function paras(s) {
    if (!s) return "";
    return String(s).split(/\n{2,}/).map(function (p) {
      return "<p>" + rich(p.trim()) + "</p>";
    }).join("");
  }

  var SECLBL = {
    "Undergrad": ["Undergrad", "大學組"],
    "Overgrad": ["Overgrad", "研究生組"],
    "High School": ["High School", "高中組"]
  };
  function secLabel(s) { var p = SECLBL[s]; return p ? L(p[0], p[1]) : s; }

  /* ---------- tabs ---------- */
  var TABS = [
    { id: "overview", en: "Overview", zh: "總覽", icon: "M3 12h4l3 8 4-16 3 8h4" },
    { id: "drylab", en: "Dry Lab", zh: "乾實驗室", icon: "M9 3v6l-5 9a2 2 0 0 0 2 3h12a2 2 0 0 0 2-3l-5-9V3M8 3h8" },
    { id: "good", en: "Science for Good", zh: "科學向善", icon: "M20 9c0 6-8 11-8 11S4 15 4 9a8 8 0 0 1 16 0z" },
    { id: "teams", en: "Team Files", zh: "團隊檔案", icon: "M16 20v-2a4 4 0 0 0-8 0v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8" },
    { id: "academic", en: "Academic Trends", zh: "學術趨勢", icon: "M4 19V5m0 14h16M8 15l3-5 3 3 5-8" },
    { id: "industry", en: "Industry Trends", zh: "產業趨勢", icon: "M3 21V9l6-4v4l6-4v16M3 21h18M9 21v-4h4v4" },
    { id: "roadmap", en: "Drylab Roadmap", zh: "Drylab 路線圖", icon: "M4 6h16M4 12h10M4 18h7M18 12l3 3-3 3" }
  ];
  var CUR = "overview";

  function renderTabs() {
    document.getElementById("tabbar").innerHTML = TABS.map(function (t) {
      return '<button class="tab' + (t.id === CUR ? " on" : "") + '" data-t="' + t.id + '">' +
        '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="' + t.icon + '"/></svg>' +
        esc(L(t.en, t.zh)) + "</button>";
    }).join("");
  }

  /* ---------- small builders ---------- */
  function chips(arr, cls, max) {
    if (!arr || !arr.length) return "";
    var a = max ? arr.slice(0, max) : arr;
    var extra = max && arr.length > max ? '<span class="chip">+' + (arr.length - max) + "</span>" : "";
    return '<div class="chips">' + a.map(function (x) {
      return '<span class="chip ' + (cls || "") + '">' + esc(x) + "</span>";
    }).join("") + extra + "</div>";
  }
  function img(src, alt) {
    if (!src) return "";
    return '<img loading="lazy" referrerpolicy="no-referrer" src="' + esc(src) + '" alt="' + esc(alt || "") +
      '" onerror="var p=this.closest(\'.shot,.ph,.evph\');if(p)p.classList.add(\'hide\');this.remove()">';
  }
  function sechead(k, en, zh, sub_en, sub_zh) {
    return '<div class="sechead"><div class="k">' + esc(L(k, k)) + '</div><h2>' + esc(L(en, zh)) + "</h2>" +
      (sub_en ? "<p>" + rich(L(sub_en, sub_zh)) + "</p>" : "") + "</div>";
  }
  function box(k_en, k_zh, body, cls) {
    if (!body) return "";
    return '<div class="box ' + (cls || "") + '"><div class="k">' + esc(L(k_en, k_zh)) + "</div><p>" + rich(body) + "</p></div>";
  }

  /* ---------- OVERVIEW ---------- */
  function viewOverview() {
    var gp = RESULTS.grandPrize || {};
    var t10 = RESULTS.top10 || {};
    var nTeams = TEAMS.length;
    var withDry = TEAMS.filter(function (t) { return t.dry && (t.dry.frameworks || t.dry.software); }).length;
    var nTrend = (TRENDS.academic.trends || []).length + (TRENDS.industry.trends || []).length;

    var h = '<section class="hero"><div class="wrap">' +
      '<div class="eyebrow"><span class="dot"></span>' + esc(L("iGEM 2026 · Paris · Grand Jamboree", "iGEM 2026 · 巴黎 · Grand Jamboree")) + "</div>" +
      "<h1>" + L('What the <span class="gt">dry lab</span> won with in 2026 — and where GEMS Research goes next.',
                 '2026 年，<span class="gt">乾實驗室</span>贏在哪裡 — 以及 GEMS Research 的下一步。') + "</h1>" +
      '<p class="lede">' + rich(L(
        "A working review of the iGEM 2026 Top 10 teams across all three sections, every special prize winner and nominee, and the academic and industry currents around them. Two questions run through it: how teams turn biology into computation, and how they turn science into something a community can actually use. Written for everyone at GEMS Research, not just for one season.",
        "本報告檢視 iGEM 2026 三個組別的 Top 10 團隊、所有特別獎得主與入圍隊伍，以及其背後的學術與產業趨勢。貫穿全文的兩個問題是：團隊如何把生物學轉化為運算，以及如何把科學轉化為社群真正用得上的東西。這份報告是寫給 GEMS Research 全體研究人員的，而不只是為了某一屆競賽。")) + "</p>" +
      '<div class="statrow">' +
      stat(30, L("Top 10 teams reviewed", "Top 10 團隊")) +
      stat(nTeams, L("Team files researched", "已完成團隊檔案")) +
      stat(21, L("Special prize categories", "特別獎項目")) +
      stat(nTrend, L("Trends tracked", "追蹤趨勢")) +
      stat(withDry, L("Dry lab profiles", "乾實驗室剖析")) +
      "</div></div></section>";

    // the findings index sits above the results, as the executive layer
    h += reportSections("overview", { before: 20 });

    // grand prize
    h += '<section class="sec"><div class="wrap">' +
      sechead("Headline results", "The 2026 podium", "2026 年頒獎台",
        "Three sections, three Grand Prizes. Read the villages as much as the names — they show where the competition's centre of gravity sat this year.",
        "三個組別、三座大獎。看 village 比看隊名更有意義——它顯示了今年競賽的重心所在。") +
      '<div class="grid g3">';
    ["Undergrad", "Overgrad", "High School"].forEach(function (s) {
      var g = gp[s]; if (!g) return;
      h += '<div class="card lift"><div class="k">' + esc(secLabel(s)) + "</div>" +
        "<h4>" + esc(g.winner) + '</h4><p style="margin-top:4px">' +
        '<span class="chip win">' + esc(L("Grand Prize", "總冠軍")) + "</span></p>" +
        '<p style="font-size:13.5px;color:var(--ink3)">' + esc(g.village) + " · " + esc(g.country) + "</p>" +
        (g.runnersUp || []).map(function (r) {
          return '<p style="margin:8px 0 0;font-size:14px"><b style="color:var(--ink);font-weight:620">' + esc(r.team) +
            '</b> <span style="color:var(--ink3);font-size:12.5px">' + esc(L(r.rank, r.rank.replace("1st Runner-up", "亞軍").replace("2nd Runner-up", "季軍"))) + "</span></p>";
        }).join("") + "</div>";
    });
    h += "</div>";

    // top 10 table
    h += '<h3 class="sub">' + esc(L("The Top 10, by section", "各組 Top 10")) + "</h3>" +
      '<div class="grid g3">';
    ["Undergrad", "Overgrad", "High School"].forEach(function (s) {
      var list = t10[s] || [];
      h += '<div class="card"><div class="k">' + esc(secLabel(s)) + "</div>" +
        '<div style="display:flex;flex-direction:column;gap:7px;margin-top:4px">' +
        list.map(function (n) {
          var t = teamByName(n);
          var isGems = n === "GEMS-Taiwan";
          return '<div style="display:flex;align-items:baseline;gap:8px;font-size:14.5px' + (isGems ? ";font-weight:700" : "") + '">' +
            (t ? '<a href="#" data-team="' + esc(t.id) + '">' + esc(n) + "</a>" : "<span>" + esc(n) + "</span>") +
            (isGems ? '<span class="chip g" style="font-size:10px;padding:2px 7px">' + esc(L("us", "我們")) + "</span>" : "") +
            "</div>";
        }).join("") + "</div></div>";
    });
    h += "</div></div></section>";

    // the written framing follows the results
    h += reportSections("overview", { from: 20 });

    return h;
  }
  function stat(n, l) {
    return '<div class="stat"><div class="n tnum">' + esc(n) + '</div><div class="l">' + esc(l) + "</div></div>";
  }

  /* Render REPORT blocks tagged for a tab. `range` narrows by the block's
     `order` (default 50), so a summary block can sit above hand-built markup
     and the rest below it. */
  function reportSections(tab, range) {
    var lo = range && range.from != null ? range.from : -Infinity;
    var hi = range && range.before != null ? range.before : Infinity;
    var blocks = (REPORT.sections || []).filter(function (b) {
      var o = b.order == null ? 50 : b.order;
      return b.tab === tab && o >= lo && o < hi;
    });
    return blocks.map(function (b) {
      var h = '<section class="sec"><div class="wrap">' +
        sechead(b.kicker || "", T(b, "title"), T(b, "title"), T(b, "lede"), T(b, "lede"));
      if (b.body) h += '<div class="panel" style="max-width:none">' + paras(T(b, "body")) + "</div>";
      if (b.cards && b.cards.length) {
        h += '<div class="grid ' + (b.cards.length > 3 ? "g3" : "g2") + '" style="margin-top:16px">' +
          b.cards.map(function (c) {
            return '<div class="card lift">' + (c.kicker ? '<div class="k">' + esc(T(c, "kicker")) + "</div>" : "") +
              "<h4>" + esc(T(c, "title")) + "</h4>" + paras(T(c, "body")) +
              (c.chips ? chips(c.chips, "b") : "") +
              (c.link ? '<p style="margin-top:12px"><a href="#' + esc(c.link) + '" style="font-size:13.5px;font-weight:620">' +
                esc(T(c, "linkText") || L("Read the analysis →", "閱讀完整分析 →")) + "</a></p>" : "") +
              "</div>";
          }).join("") + "</div>";
      }
      if (b.table) {
        h += '<div class="scrollx" style="margin-top:16px"><table class="tbl"><thead><tr>' +
          b.table.head.map(function (x, i) { return "<th>" + esc(LANG === "zh" && b.table.head_zh ? b.table.head_zh[i] : x) + "</th>"; }).join("") +
          "</tr></thead><tbody>" +
          (LANG === "zh" && b.table.rows_zh ? b.table.rows_zh : b.table.rows).map(function (r) {
            return "<tr>" + r.map(function (c, i) { return "<td>" + (i === 0 ? "<b>" + rich(c) + "</b>" : rich(c)) + "</td>"; }).join("") + "</tr>";
          }).join("") + "</tbody></table></div>" + scrollHint();
      }
      if (b.checklist && b.checklist.length) {
        h += '<h3 class="sub">' + esc(L("Checklist", "檢查清單")) + "</h3>" +
          '<div class="grid g2">' + (LANG === "zh" && b.checklist_zh ? b.checklist_zh : b.checklist).map(function (c, i) {
            return '<div class="card" style="display:flex;gap:13px;align-items:flex-start">' +
              '<span style="flex:none;width:25px;height:25px;border-radius:8px;background:linear-gradient(135deg,var(--blue),var(--teal));color:#fff;font-size:12px;font-weight:700;display:grid;place-items:center">' +
              (i + 1) + '</span><p style="margin:2px 0 0">' + rich(c) + "</p></div>";
          }).join("") + "</div>";
      }
      if (b.antipatterns && b.antipatterns.length) {
        h += '<h3 class="sub">' + esc(L("Effort that did not pay off", "投入了卻沒有回報的事")) + "</h3>" +
          '<div class="grid g2">' + (LANG === "zh" && b.antipatterns_zh ? b.antipatterns_zh : b.antipatterns).map(function (c) {
            return '<div class="card" style="display:flex;gap:12px;align-items:flex-start;box-shadow:inset 0 0 0 1px rgba(229,72,77,.18)">' +
              '<span style="flex:none;color:var(--rose);font-weight:700;font-size:15px;line-height:1.5">×</span>' +
              '<p style="margin:0">' + rich(c) + "</p></div>";
          }).join("") + "</div>";
      }
      if (b.partners && b.partners.length) {
        h += '<h3 class="sub">' + esc(L("Collaboration proposals", "合作提案")) + "</h3>" +
          '<div class="grid g2">' + b.partners.map(function (p) {
            return '<div class="card lift"><h4>' + esc(T(p, "name")) + "</h4><p>" + rich(T(p, "why")) + "</p>" +
              (p.firstProject ? '<div class="take" style="margin-top:10px"><div class="k">' +
                esc(L("First project", "第一個合作專案")) + "</div><p>" + rich(T(p, "firstProject")) + "</p></div>" : "") + "</div>";
          }).join("") + "</div>";
      }
      if (b.method) {
        h += '<p style="margin-top:22px;font-size:13px;color:var(--ink3);max-width:60em"><b style="color:var(--ink2)">' +
          esc(L("Method and limits.", "方法與限制。")) + "</b> " + rich(T(b, "method")) + "</p>";
      }
      return h + "</div></section>";
    }).join("");
  }

  /* ---------- DRY LAB / SCIENCE FOR GOOD: evidence galleries ---------- */
  function evidenceView(kind) {
    // kind: "dry" | "good"
    var fields = kind === "dry"
      ? [["frameworks", "Computational frameworks", "運算框架"], ["datascience", "Data science", "資料科學"],
         ["dataviz", "Data visualisation", "資料視覺化"], ["software", "Software & hardware", "軟體與硬體"]]
      : [["ihp", "Integrated Human Practices", "整合式人類實踐"], ["publicEngagement", "Public engagement", "公眾參與"],
         ["realWorld", "Real-world application", "真實世界應用"]];

    var h = reportSections(kind === "dry" ? "drylab" : "good");

    fields.forEach(function (f) {
      var rows = TEAMS.filter(function (t) { return t[kind] && t[kind][f[0]] && String(t[kind][f[0]]).length > 60; })
        .sort(function (a, b) { return (b.rank || 0) - (a.rank || 0) || String(b[kind][f[0]]).length - String(a[kind][f[0]]).length; });
      if (!rows.length) return;
      // On the Science for Good tab these are iGEM's own judging categories, kept
      // because that is honestly what the team files contain. The lead-in says
      // why a GEMS reader is looking at them: as worked examples for the
      // programme, not as a rubric to score ourselves against.
      var lead = kind === "good"
        ? L(rows.length + " teams documented this well enough to borrow from. Read them as worked examples for the programme above, not as a rubric. Click a team for the full file.",
            "共 " + rows.length + " 支團隊在這方面的紀錄足以直接借用。請把它們當作上面那個長期計畫的實作範例來讀，而不是一張評分表。點擊團隊可展開完整檔案。")
        : L(rows.length + " teams documented this well enough to learn from. Click a team for the full file.",
            "共 " + rows.length + " 支團隊在這方面的紀錄足以作為學習對象。點擊團隊可展開完整檔案。");
      h += '<section class="sec"><div class="wrap">' +
        sechead(kind === "good" ? L("Worked examples", "實作範例") : L("Evidence", "案例"), f[1], f[2], lead) +
        '<div class="grid g2">' +
        rows.slice(0, 18).map(function (t) {
          var im = (t.images || [])[0];
          return '<div class="card lift ev" data-team="' + esc(t.id) + '" style="cursor:pointer">' +
            (im ? '<figure class="evph">' + img(im.url, t.team + " — " + (im.caption || "")) + "</figure>" : "") +
            '<div class="k">' + esc(t.team) + " · " + esc(secLabel(t.section)) + "</div>" +
            "<h4>" + esc(T(t, "projectTitle") || t.team) + "</h4>" +
            "<p>" + rich(clip(T(t[kind], f[0]), 460)) + "</p>" +
            chips(awardList(t, true), "win", 2) + "</div>";
        }).join("") + "</div></div></section>";
    });
    return h;
  }
  function clip(s, n) {
    s = String(s || "");
    if (s.length <= n) return s;
    var cut = s.slice(0, n);
    var i = cut.lastIndexOf(". ");
    return (i > n * 0.5 ? cut.slice(0, i + 1) : cut.trimEnd() + "…");
  }
  // a wide table scrolls sideways on a phone; say so, because a cut-off column is invisible
function scrollHint() {
  return '<p class="scrollhint">' + esc(L("Swipe sideways to see the whole table.", "左右滑動可看完整表格。")) + "</p>";
}

function isWin(a) { return /winner|grand prize|top 10/i.test(a); }
  /* Award strings are generated in English and translated alongside; filter on
     the English so the test stays one regex, then display in the active language. */
  function awardList(t, winOnly) {
    var en = t.awards || [], zh = t.awards_zh || [], out = [];
    for (var i = 0; i < en.length; i++) {
      if (winOnly && !isWin(en[i])) continue;
      out.push(LANG === "zh" ? (zh[i] || en[i]) : en[i]);
    }
    return out;
  }

  /* ---------- TEAMS ---------- */
  var FILTER = { sec: "all", award: "all", q: "" };
  function viewTeams() {
    // the browsable index first — it is what the tab is for — then the analyses
    return '<section class="sec"><div class="wrap">' +
      sechead(L("Team files", "團隊檔案"), "Every team we studied", "我們研究過的每一支團隊",
        "Researched from each team's own iGEM 2026 wiki. Filter by section or award, or search for a technique — \"AlphaFold\", \"ODE\", \"workshop\", \"policy\".",
        "資料來自各隊 iGEM 2026 官方 wiki。可依組別或獎項篩選，或直接搜尋技術關鍵字——「AlphaFold」、「ODE」、「workshop」、「policy」。") +
      '<div class="filters" id="filters"></div>' +
      '<div class="grid g3" id="teamgrid"></div>' +
      '<p style="margin-top:20px;color:var(--ink3);font-size:13px" id="teamcount"></p>' +
      "</div></section>" +
      reportSections("teams");
  }
  var AWARDF = [
    ["all", "All awards", "全部獎項", null],
    ["top10", "Top 10", "Top 10", /top 10/i],
    ["model", "Best Model", "最佳模型", /best model/i],
    ["software", "Best Software", "最佳軟體", /best software/i],
    ["measurement", "Best Measurement", "最佳測量", /best measurement/i],
    ["hardware", "Best Hardware", "最佳硬體", /best hardware/i],
    ["ihp", "Best IHP", "最佳人類實踐", /integrated human practices/i],
    ["education", "Best Education", "最佳教育", /best education/i],
    ["entre", "Entrepreneurship", "創業", /entrepreneur/i],
    ["sdg", "Sustainable Dev.", "永續發展", /sustainable/i]
  ];
  function paintFilters() {
    var f = document.getElementById("filters"); if (!f) return;
    var secs = [["all", "All sections", "全部組別"], ["Undergrad", "Undergrad", "大學組"],
                ["Overgrad", "Overgrad", "研究生組"], ["High School", "High School", "高中組"]];
    f.innerHTML = secs.map(function (s) {
      return '<button class="fbtn' + (FILTER.sec === s[0] ? " on" : "") + '" data-f="sec" data-v="' + s[0] + '">' + esc(L(s[1], s[2])) + "</button>";
    }).join("") +
      '<span style="width:8px"></span>' +
      AWARDF.map(function (a) {
        return '<button class="fbtn' + (FILTER.award === a[0] ? " on" : "") + '" data-f="award" data-v="' + a[0] + '">' + esc(L(a[1], a[2])) + "</button>";
      }).join("") +
      '<input class="fsearch" id="q" placeholder="' + esc(L("Search technique, tool, topic…", "搜尋技術、工具、主題…")) + '" value="' + esc(FILTER.q) + '">';
  }
  function filtered() {
    var re = AWARDF.filter(function (a) { return a[0] === FILTER.award; })[0];
    re = re && re[3];
    var q = FILTER.q.trim().toLowerCase();
    return TEAMS.filter(function (t) {
      if (FILTER.sec !== "all" && t.section !== FILTER.sec) return false;
      if (re && !(t.awards || []).some(function (a) { return re.test(a); })) return false;
      if (q) {
        var hay = [t.team, t.projectTitle, t.tagline, t.summary, t.country, t.village,
                   (t.awards || []).join(" "), JSON.stringify(t.dry || {}), JSON.stringify(t.good || {})].join(" ").toLowerCase();
        if (hay.indexOf(q) < 0) return false;
      }
      return true;
    });
  }
  function paintTeams() {
    var g = document.getElementById("teamgrid"); if (!g) return;
    var list = filtered().sort(function (a, b) { return (b.rank || 0) - (a.rank || 0) || a.team.localeCompare(b.team); });
    g.innerHTML = list.map(teamCard).join("") ||
      '<p style="color:var(--ink3)">' + esc(L("No team matches that filter.", "沒有符合條件的團隊。")) + "</p>";
    var c = document.getElementById("teamcount");
    if (c) c.textContent = L(list.length + " of " + TEAMS.length + " teams shown.", "顯示 " + list.length + " / " + TEAMS.length + " 支團隊。");
  }
  function teamCard(t) {
    var im = (t.images || [])[0];
    return '<article class="tcard" data-team="' + esc(t.id) + '" style="cursor:pointer">' +
      '<div class="ph">' + (im ? img(im.url, t.team) : '<div class="no">' + esc(t.team) + "</div>") + "</div>" +
      '<div class="bd"><div class="nm"><h4>' + esc(t.team) + '</h4><span class="sec-l">' + esc(secLabel(t.section)) + "</span></div>" +
      (t.projectTitle ? '<div class="pt">' + esc(T(t, "projectTitle")) + "</div>" : "") +
      '<p class="sm">' + rich(clip(T(t, "summary"), 190)) + "</p>" +
      chips(awardList(t, true), "win", 2) +
      '<div class="ft"><span style="color:var(--ink3)">' + esc(t.country || "") + "</span>" +
      '<span class="more">' + esc(L("Open file →", "展開檔案 →")) + "</span></div></div></article>";
  }

  /* ---------- team detail sheet ---------- */
  function openTeam(id) {
    if (FULL.state !== "done" && FULL.state !== "error") {
      loadFull(function () { openTeam(id); });
      return;
    }
    var t = TEAMS.filter(function (x) { return String(x.id) === String(id); })[0];
    if (!t) return;
    var h = '<div class="sh-head"><div><div style="font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3)">' +
      esc(secLabel(t.section)) + (t.country ? " · " + esc(t.country) : "") + (t.village ? " · " + esc(t.village) : "") + "</div>" +
      '<h2 style="font-size:28px;font-weight:700;margin-top:6px">' + esc(t.team) + "</h2>" +
      (t.projectTitle ? '<div style="font-size:17px;font-weight:620;color:var(--blue);margin-top:4px">' + esc(T(t, "projectTitle")) + "</div>" : "") +
      (t.tagline ? '<p style="font-size:14.5px;color:var(--ink2);margin:7px 0 0;max-width:46em">' + rich(T(t, "tagline")) + "</p>" : "") +
      "</div><button class='x' id='shx' aria-label='Close'>×</button></div><div class='sh-body'>";

    h += chips(awardList(t), "win");
    if (t.summary) h += "<h3>" + esc(L("The project", "專案概述")) + "</h3>" + paras(T(t, "summary"));

    if (t.images && t.images.length) {
      h += '<div class="shots">' + t.images.map(function (m) {
        return '<figure class="shot" style="margin:0">' + img(m.url, m.caption) +
          '<figcaption class="cap">' + rich(T(m, "caption") || "") +
          (m.credit ? '<br><span style="color:var(--ink4)">' + esc(m.credit) + "</span>" : "") + "</figcaption></figure>";
      }).join("") + "</div>";
    }

    var d = t.dry || {};
    if (d.frameworks || d.datascience || d.dataviz || d.software) {
      h += "<h3>" + esc(L("Computation, modelling & data", "運算、建模與資料")) + "</h3>";
      if (d.frameworks) h += "<p><strong>" + esc(L("Frameworks", "運算框架")) + ".</strong> " + rich(T(d, "frameworks")) + "</p>";
      if (d.datascience) h += "<p><strong>" + esc(L("Data science", "資料科學")) + ".</strong> " + rich(T(d, "datascience")) + "</p>";
      if (d.dataviz) h += "<p><strong>" + esc(L("Visualisation", "視覺化")) + ".</strong> " + rich(T(d, "dataviz")) + "</p>";
      if (d.software) h += "<p><strong>" + esc(L("Software & hardware", "軟體與硬體")) + ".</strong> " + rich(T(d, "software")) + "</p>";
      h += chips((d.techniques || []).concat(d.stack || []), "v");
    }

    var g = t.good || {};
    if (g.ihp || g.publicEngagement || g.realWorld) {
      h += "<h3>" + esc(L("Science for good", "科學向善")) + "</h3>";
      if (g.ihp) h += "<p><strong>" + esc(L("Integrated Human Practices", "整合式人類實踐")) + ".</strong> " + rich(T(g, "ihp")) + "</p>";
      if (g.publicEngagement) h += "<p><strong>" + esc(L("Public engagement", "公眾參與")) + ".</strong> " + rich(T(g, "publicEngagement")) + "</p>";
      if (g.realWorld) h += "<p><strong>" + esc(L("Real-world application", "真實世界應用")) + ".</strong> " + rich(T(g, "realWorld")) + "</p>";
      h += chips(g.partners || [], "g");
    }

    if (t.gemsTakeaway) {
      h += '<div class="take" style="margin-top:22px"><div class="k">' + esc(L("For GEMS Research", "給 GEMS Research")) +
        "</div><p>" + rich(T(t, "gemsTakeaway")) + "</p></div>";
    }

    h += '<p style="margin-top:22px;font-size:13px;color:var(--ink3)">' +
      (t.wiki ? '<a href="' + esc(t.wiki) + '" target="_blank" rel="noopener">' + esc(L("Team wiki ↗", "團隊 wiki ↗")) + "</a> · " : "") +
      (t.id ? '<a href="https://teams.igem.org/' + esc(t.id) + '" target="_blank" rel="noopener">' + esc(L("iGEM team page ↗", "iGEM 團隊頁 ↗")) + "</a>" : "") +
      "</p></div>";

    var sh = document.getElementById("sheet");
    document.getElementById("sheetIn").innerHTML = h;
    if (!sh.open) sh.showModal();
    sh.scrollTop = 0;
    document.getElementById("shx").onclick = function () { sh.close(); };
  }

  /* ---------- TRENDS ---------- */
  function viewTrends(which) {
    var d = TRENDS[which] || {};
    var list = d.trends || [];
    var isAc = which === "academic";
    var h = reportSections(which);
    h += '<section class="sec"><div class="wrap">' +
      sechead(isAc ? L("Academic", "學術") : L("Industry", "產業"),
        isAc ? "Where the science is going" : "Where the money is going",
        isAc ? "科學的走向" : "資金的走向",
        isAc ? "Tracked from the Nature portfolio synthetic-biology feed and the preprint servers behind it."
             : "Tracked from SynBioBeta and the funding, product and policy news around it.",
        isAc ? "追蹤來源為 Nature 合成生物學主題與其背後的預印本伺服器。"
             : "追蹤來源為 SynBioBeta 及相關的募資、產品與政策新聞。");

    if (!list.length) {
      h += '<div class="load"><div class="spin"></div>' + esc(L("Research in progress — this tab fills as the analysts report back.", "研究進行中——分析完成後本頁會自動更新。")) + "</div>";
      return h + "</div></section>";
    }

    var MAT = { emerging: ["Emerging", "萌芽", "v"], accelerating: ["Accelerating", "加速中", "b"], mainstream: ["Mainstream", "主流", "g"] };
    h += '<div class="grid g2">' + list.map(function (tr) {
      var m = MAT[tr.maturity] || MAT.accelerating;
      return '<article class="trend"><div class="top"><h4>' + esc(T(tr, "title")) + "</h4>" +
        '<span class="chip ' + m[2] + '" style="flex:none">' + esc(L(m[0], m[1])) + "</span></div>" +
        (tr.oneLine ? '<p class="one">' + rich(T(tr, "oneLine")) + "</p>" : "") +
        '<div class="bd">' + paras(T(tr, "body")) + "</div>" +
        box("Why it matters", "為何重要", T(tr, "whyItMatters")) +
        box("GEMS action", "GEMS 行動", T(tr, "gemsAction"), "act") +
        ((tr.refs && tr.refs.length) ? '<div class="refs">' + tr.refs.slice(0, 5).map(function (r) {
          return '<a href="' + esc(r.url) + '" target="_blank" rel="noopener"><span class="d">↗</span><span>' +
            esc(r.title) + (r.venue || r.outlet ? ' <span style="color:var(--ink4)">· ' + esc(r.venue || r.outlet) + "</span>" : "") + "</span></a>";
        }).join("") + "</div>" : "") +
        "</article>";
    }).join("") + "</div>";

    if (d.companiesToWatch && d.companiesToWatch.length) {
      h += '<h3 class="sub">' + esc(L("Companies to watch", "值得關注的公司")) + "</h3>" +
        '<div class="scrollx"><table class="tbl"><thead><tr><th>' + esc(L("Company", "公司")) + "</th><th>" +
        esc(L("What they do", "業務")) + "</th><th>" + esc(L("Why it matters to us", "與我們的關聯")) + "</th></tr></thead><tbody>" +
        d.companiesToWatch.map(function (c) {
          return "<tr><td><b>" + (c.url ? '<a href="' + esc(c.url) + '" target="_blank" rel="noopener">' + esc(c.name) + "</a>" : esc(c.name)) +
            "</b></td><td>" + rich(T(c, "what")) + "</td><td>" + rich(T(c, "why")) + "</td></tr>";
        }).join("") + "</tbody></table></div>" + scrollHint();
    }
    if (d.careerPaths && d.careerPaths.length) {
      h += '<h3 class="sub">' + esc(L("Dry-lab career paths, 2026", "2026 乾實驗室職涯路徑")) + "</h3>" +
        '<div class="grid g3">' + (LANG === "zh" && d.careerPaths_zh ? d.careerPaths_zh : d.careerPaths).map(function (c, i) {
          return '<div class="card"><div class="k">' + (i + 1) + "</div><p>" + rich(c) + "</p></div>";
        }).join("") + "</div>";
    }
    if (d.openQuestions && d.openQuestions.length) {
      h += '<h3 class="sub">' + esc(L("Open questions a student team could attack", "學生團隊可以挑戰的開放問題")) + "</h3>" +
        '<div class="grid g2">' + (LANG === "zh" && d.openQuestions_zh ? d.openQuestions_zh : d.openQuestions).map(function (q) {
          return '<div class="card"><p>' + rich(q) + "</p></div>";
        }).join("") + "</div>";
    }
    if (d.readingList && d.readingList.length) {
      h += '<h3 class="sub">' + esc(L("Reading list", "延伸閱讀")) + "</h3><div class=\"refs\" style=\"gap:9px\">" +
        d.readingList.map(function (r) {
          return '<a href="' + esc(r.url) + '" target="_blank" rel="noopener" style="font-size:14px"><span class="d">↗</span><span><b style="color:var(--ink);font-weight:620">' +
            esc(r.title) + "</b> " + (r.venue || r.outlet ? '<span style="color:var(--ink4)">· ' + esc(r.venue || r.outlet) + "</span>" : "") +
            (r.why ? '<br><span style="color:var(--ink3);font-size:13px">' + rich(T(r, "why")) + "</span>" : "") + "</span></a>";
        }).join("") + "</div>";
    }
    return h + "</div></section>";
  }

  /* ---------- ROADMAP ---------- */
  function viewRoadmap() {
    var h = reportSections("roadmap");
    var ph = REPORT.roadmap || [];
    if (ph.length) {
      h += '<section class="sec"><div class="wrap">' +
        sechead(L("Plan", "計畫"), "The Drylab roadmap", "Drylab 路線圖",
          "Four phases, written so that any researcher at GEMS can pick up a phase and start.",
          "四個階段，寫法是讓 GEMS 任何一位研究人員都能直接接手開始。") +
        '<div class="rm">' + ph.map(function (p, i) {
          return '<div class="phase"><div class="hd"><span class="n">' + (i + 1) + "</span><h4>" + esc(T(p, "title")) +
            '</h4><span class="w">' + esc(T(p, "when")) + "</span></div>" +
            '<div class="bd">' + (p.lede ? "<p style='margin:0 0 13px;color:var(--ink2);font-size:15px'>" + rich(T(p, "lede")) + "</p>" : "") +
            "<ul>" + (LANG === "zh" && p.items_zh ? p.items_zh : p.items || []).map(function (it) {
              return "<li>" + rich(it) + "</li>";
            }).join("") + "</ul>" +
            (p.outcome ? '<div class="take" style="margin-top:14px"><div class="k">' + esc(L("Done looks like", "完成的樣子")) +
              "</div><p>" + rich(T(p, "outcome")) + "</p></div>" : "") +
            "</div></div>";
        }).join("") + "</div></div></section>";
    }
    return h;
  }

  /* ---------- lazy-loaded full team records ----------
     data/teams.js carries a light index so the first paint stays small; the full
     prose lives in data/teams-full.js and is fetched the first time a tab or a
     detail sheet actually needs it. */
  var FULL = { state: "idle", waiting: [] };
  function needsFull(tab) { return tab === "drylab" || tab === "good" || tab === "teams"; }
  function loadFull(then) {
    if (FULL.state === "done") { then && then(); return; }
    if (then) FULL.waiting.push(then);
    if (FULL.state === "loading") return;
    FULL.state = "loading";
    var s = document.createElement("script");
    s.src = "data/teams-full.js" + (window.BUILD ? "?v=" + window.BUILD : "");
    s.onload = function () {
      var f = window.TEAMS_FULL || {};
      TEAMS = TEAMS.map(function (t) { return f[t.id] ? f[t.id] : t; });
      window.TEAMS = TEAMS;
      FULL.state = "done";
      var q = FULL.waiting; FULL.waiting = [];
      q.forEach(function (fn) { fn(); });
    };
    s.onerror = function () {
      // the index alone still renders something useful — fail visibly, not silently
      FULL.state = "error";
      var q = FULL.waiting; FULL.waiting = [];
      q.forEach(function (fn) { fn(); });
    };
    document.head.appendChild(s);
  }

  /* ---------- router ---------- */
  function render() {
    if (needsFull(CUR) && FULL.state !== "done") {
      renderTabs();
      document.getElementById("main").innerHTML =
        '<div class="load"><div class="spin"></div>' +
        esc(FULL.state === "error"
          ? L("Could not load the team files.", "無法載入團隊檔案。")
          : L("Loading team files…", "載入團隊檔案…")) + "</div>";
      applyStatic();
      if (FULL.state !== "error") { loadFull(render); return; }
    }
    renderTabs();
    var m = document.getElementById("main"), h;
    if (CUR === "overview") h = viewOverview();
    else if (CUR === "drylab") h = evidenceView("dry");
    else if (CUR === "good") h = evidenceView("good");
    else if (CUR === "teams") h = viewTeams();
    else if (CUR === "academic") h = viewTrends("academic");
    else if (CUR === "industry") h = viewTrends("industry");
    else h = viewRoadmap();
    m.innerHTML = h;
    if (CUR === "teams") { paintFilters(); paintTeams(); }
    applyStatic();
    window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
  }
  function go(id, push) {
    if (!TABS.some(function (t) { return t.id === id; })) id = "overview";
    CUR = id;
    if (push !== false) history.replaceState(null, "", "#" + id);
    render();
  }
  function teamByName(n) { return TEAMS.filter(function (t) { return t.team === n; })[0]; }

  /* ---------- language ---------- */
  function applyStatic() {
    document.querySelectorAll("[data-en]").forEach(function (el) {
      var v = LANG === "zh" ? (el.getAttribute("data-zh") || el.getAttribute("data-en")) : el.getAttribute("data-en");
      el.textContent = v;
    });
    var s = document.getElementById("stamp");
    if (s) s.textContent = L("Updated ", "更新於 ") + (REPORT.updated || "2026-11-19");
  }
  function setLang(l) {
    LANG = l;
    document.documentElement.setAttribute("lang", l === "zh" ? "zh-Hant" : "en");
    try { localStorage.setItem("gems-lang", l); } catch (e) {}
    var box = document.getElementById("lang");
    box.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.dataset.l === l); });
    moveThumb();
    render();
  }
  function moveThumb() {
    var box = document.getElementById("lang"), on = box.querySelector("button.on"), th = box.querySelector(".thumb");
    if (!on) return;
    th.style.width = on.offsetWidth + "px";
    th.style.transform = "translateX(" + (on.offsetLeft - 2) + "px)";
    requestAnimationFrame(function () { box.classList.add("ready"); });
  }

  /* ---------- events ---------- */
  document.addEventListener("click", function (e) {
    var tb = e.target.closest(".tab");
    if (tb) { go(tb.dataset.t); return; }
    var lg = e.target.closest("#lang button");
    if (lg) { setLang(lg.dataset.l); return; }
    var tm = e.target.closest("[data-team]");
    if (tm) { e.preventDefault(); openTeam(tm.dataset.team); return; }
    var fb = e.target.closest(".fbtn");
    if (fb) { FILTER[fb.dataset.f] = fb.dataset.v; paintFilters(); paintTeams(); return; }
    var sh = document.getElementById("sheet");
    if (sh && sh.open && e.target === sh) sh.close();
  });
  document.addEventListener("input", function (e) {
    if (e.target.id === "q") { FILTER.q = e.target.value; paintTeams(); }
  });
  window.addEventListener("hashchange", function () { go(location.hash.slice(1), false); });

  /* ---------- boot ---------- */
  try {
    var saved = localStorage.getItem("gems-lang");
    LANG = saved || (/^zh/i.test(navigator.language || "") ? "zh" : "en");
  } catch (e) { LANG = "en"; }
  document.documentElement.setAttribute("lang", LANG === "zh" ? "zh-Hant" : "en");
  document.getElementById("lang").querySelectorAll("button").forEach(function (b) {
    b.classList.toggle("on", b.dataset.l === LANG);
  });
  go(location.hash.slice(1) || "overview", false);
  moveThumb();
  window.addEventListener("resize", moveThumb);
})();
