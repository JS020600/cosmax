import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="QuickQuote - 해외 영업 견적서 자동 생성기",
    layout="wide",
)

# 항상 모바일 폭(단일 컬럼)으로 표시되며, 내부 JS가 콘텐츠 높이에 맞춰
# iframe 높이를 자동으로 조절하므로 내용이 늘어나도 잘리지 않습니다.
HTML_CODE = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QuickQuote - 해외 영업 견적서 자동 생성기</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --navy: #3b6fe0;
    --navy-light: #6c93ec;
    --navy-tint: #e4ecfc;
    --accent: #16b8a6;
    --accent-light: #d9f4f0;
    --accent-dark: #119484;
    --page-bg: #f5f7fb;
    --card-bg: #ffffff;
    --border: #e4e8f0;
    --text: #1f2937;
    --text-muted: #6b7280;
    --white: #ffffff;
    --danger: #e0503c;
  }

  * { box-sizing: border-box; }

  html {
    background: #d9dee6;
  }

  body {
    margin: 0 auto;
    max-width: 480px;
    min-height: 100vh;
    font-family: "Noto Sans KR", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 15px;
    line-height: 1.6;
    background: var(--page-bg);
    color: var(--text);
    box-shadow: 0 0 24px rgba(15, 44, 76, 0.12);
  }

  header {
    background: linear-gradient(135deg, var(--navy), var(--navy-light));
    color: var(--white);
    padding: 28px 20px;
    text-align: center;
  }

  header h1 {
    margin: 0 0 8px;
    font-size: 30px;
    font-weight: 900;
    letter-spacing: 0.3px;
  }

  header p {
    margin: 0;
    font-size: 15px;
    color: var(--navy-tint);
  }

  main {
    padding: 32px 16px 48px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  @media (max-width: 480px) {
    header h1 { font-size: 26px; }
    body { font-size: 15px; }
    input[type="text"], input[type="number"], select,
    .items-table input {
      font-size: 16px; /* prevents iOS Safari auto-zoom on focus */
    }
    .generate-btn, .download-btn { font-size: 16px; }
  }

  .card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(15, 44, 76, 0.06);
  }

  .card h2 {
    margin: 0 0 16px;
    font-size: 18px;
    font-weight: 700;
    color: var(--navy);
  }

  label {
    display: block;
    font-size: 14px;
    color: var(--text-muted);
    margin-bottom: 4px;
    margin-top: 14px;
  }

  label:first-of-type { margin-top: 0; }

  input[type="text"],
  input[type="number"],
  select {
    width: 100%;
    padding: 9px 10px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 15px;
    background: var(--page-bg);
    color: var(--text);
  }

  input:focus, select:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-light);
  }

  .rate-row {
    display: flex;
    gap: 10px;
  }
  .rate-row > div { flex: 1; }

  .items-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
  }

  .items-table th {
    text-align: left;
    font-size: 13px;
    color: var(--text-muted);
    padding: 6px 4px;
    border-bottom: 1px solid var(--border);
  }

  .items-table td {
    padding: 6px 4px;
    vertical-align: middle;
  }

  .items-table input {
    padding: 7px 8px;
    font-size: 14px;
  }

  .col-qty, .col-price { width: 22%; }
  .col-remove { width: 32px; text-align: center; }

  .remove-btn {
    background: none;
    border: none;
    color: var(--danger);
    font-size: 18px;
    cursor: pointer;
    line-height: 1;
  }

  .add-row-btn {
    margin-top: 10px;
    background: var(--accent-light);
    color: var(--accent);
    border: 1px dashed var(--accent);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    cursor: pointer;
    width: 100%;
  }

  .add-row-btn:hover { background: #c7ece5; }

  .generate-btn {
    margin-top: 20px;
    width: 100%;
    padding: 13px;
    background: var(--accent);
    color: var(--white);
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s ease;
  }

  .generate-btn:hover { background: var(--accent-dark); }

  /* Result / preview area */
  #result-card { display: none; }

  #result-card.visible { display: block; }

  .quote-doc {
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 24px;
    background: var(--white);
    font-size: 14px;
  }

  .quote-doc h3 {
    margin: 0 0 4px;
    color: var(--navy);
    font-size: 20px;
    font-weight: 900;
  }

  .quote-doc .quote-sub {
    color: var(--text-muted);
    margin-bottom: 18px;
  }

  .quote-doc table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 14px;
  }

  .quote-doc th, .quote-doc td {
    border-bottom: 1px solid var(--border);
    padding: 8px 6px;
    text-align: left;
  }

  .quote-doc th { color: var(--text-muted); font-weight: 600; }
  .quote-doc td.num, .quote-doc th.num { text-align: right; }

  .quote-total-row td {
    font-weight: 700;
    color: var(--navy);
    border-top: 2px solid var(--navy);
    border-bottom: none;
  }

  .download-btn {
    margin-top: 16px;
    width: 100%;
    padding: 12px;
    background: var(--accent);
    color: var(--white);
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
  }

  .download-btn:hover { background: var(--accent-dark); }

  .history-search {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
  }
  .history-search input { flex: 1; }

  .history-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .history-item {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
    padding: 12px 4px;
    border-bottom: 1px solid var(--border);
  }
  .history-item:last-child { border-bottom: none; }

  .history-item .h-buyer { font-weight: 600; }
  .history-item .h-meta { color: var(--text-muted); font-size: 13px; }
  .history-item .h-total { font-weight: 700; color: var(--navy); white-space: nowrap; }

  .history-empty {
    color: var(--text-muted);
    font-size: 14px;
    text-align: center;
    padding: 24px 10px;
  }

  .empty-hint {
    color: var(--text-muted);
    font-size: 13px;
    text-align: center;
    padding: 40px 10px;
  }

  @media print {
    header, .card:not(#result-card), .download-btn { display: none !important; }
    main { padding: 0; }
    #result-card { border: none; box-shadow: none; }
    body { background: var(--white); box-shadow: none; max-width: none; }
  }
</style>
</head>
<body>

<header>
  <h1>QuickQuote</h1>
  <p>정보만 입력하면 견적서가 바로 나오는, 해외 영업 담당자를 위한 견적서 자동 생성기</p>
</header>

<main>
  <section class="card" id="form-card">
    <h2>견적 정보 입력</h2>

    <label for="buyer">거래처명</label>
    <input type="text" id="buyer" placeholder="예: ABC Trading Co., Ltd.">

    <div class="rate-row">
      <div>
        <label for="currency">통화</label>
        <select id="currency">
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="JPY">JPY</option>
          <option value="CNY">CNY</option>
          <option value="KRW">KRW</option>
        </select>
      </div>
      <div>
        <label for="rate">환율 (1단위 → KRW)</label>
        <input type="number" id="rate" placeholder="예: 1350" step="0.01">
      </div>
    </div>

    <label>품목</label>
    <table class="items-table">
      <thead>
        <tr>
          <th>품목명</th>
          <th class="col-qty">수량</th>
          <th class="col-price">단가</th>
          <th class="col-remove"></th>
        </tr>
      </thead>
      <tbody id="items-body"></tbody>
    </table>
    <button type="button" class="add-row-btn" id="add-row-btn">+ 품목 추가</button>

    <button type="button" class="generate-btn" id="generate-btn">견적서 생성</button>
  </section>

  <section class="card" id="result-card">
    <h2>미리보기</h2>
    <div class="quote-doc" id="quote-doc"></div>
    <button type="button" class="download-btn" id="download-btn">PDF로 다운로드</button>
  </section>

  <section class="card" id="history-card">
    <h2>최근 견적 내역</h2>
    <div class="history-search">
      <input type="text" id="history-search-input" placeholder="거래처명으로 검색 후 Enter">
    </div>
    <ul class="history-list" id="history-list"></ul>
  </section>
</main>

<script>
  const itemsBody = document.getElementById('items-body');
  const addRowBtn = document.getElementById('add-row-btn');
  const generateBtn = document.getElementById('generate-btn');
  const downloadBtn = document.getElementById('download-btn');
  const resultCard = document.getElementById('result-card');
  const quoteDoc = document.getElementById('quote-doc');
  const historyList = document.getElementById('history-list');
  const historySearchInput = document.getElementById('history-search-input');

  const HISTORY_KEY = 'quickquote_history';

  function loadHistory() {
    try {
      return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
    } catch {
      return [];
    }
  }

  function saveHistory(history) {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
  }

  function renderHistory(history) {
    if (history.length === 0) {
      historyList.innerHTML = '<li class="history-empty">검색 결과가 없습니다</li>';
      return;
    }
    historyList.innerHTML = history.map(record => `
      <li class="history-item">
        <div>
          <div class="h-buyer">${record.buyer}</div>
          <div class="h-meta">${record.quoteNo} · ${record.date}</div>
        </div>
        <div class="h-total">${formatNumber(record.total)} ${record.currency}</div>
      </li>
    `).join('');
  }

  function renderAllHistory() {
    const history = loadHistory();
    if (history.length === 0) {
      historyList.innerHTML = '<li class="history-empty">아직 생성한 견적서가 없습니다</li>';
      return;
    }
    renderHistory(history);
  }

  historySearchInput.addEventListener('keypress', (e) => {
    if (e.key !== 'Enter') return;
    const keyword = historySearchInput.value.trim().toLowerCase();
    const history = loadHistory();
    if (!keyword) {
      renderAllHistory();
      return;
    }
    const filtered = history.filter(record => record.buyer.toLowerCase().includes(keyword));
    renderHistory(filtered);
  });

  renderAllHistory();

  function createItemRow() {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><input type="text" class="item-name" placeholder="품목명"></td>
      <td class="col-qty"><input type="number" class="item-qty" min="0" placeholder="0"></td>
      <td class="col-price"><input type="number" class="item-price" min="0" step="0.01" placeholder="0.00"></td>
      <td class="col-remove"><button type="button" class="remove-btn" title="삭제">&times;</button></td>
    `;
    tr.querySelector('.remove-btn').addEventListener('click', () => {
      if (itemsBody.children.length > 1) tr.remove();
    });
    itemsBody.appendChild(tr);
  }

  addRowBtn.addEventListener('click', createItemRow);
  createItemRow();
  createItemRow();

  function formatNumber(n) {
    return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  generateBtn.addEventListener('click', () => {
    const buyer = document.getElementById('buyer').value.trim() || '거래처명 미입력';
    const currency = document.getElementById('currency').value;
    const rate = parseFloat(document.getElementById('rate').value) || 0;

    const rows = Array.from(itemsBody.querySelectorAll('tr')).map(tr => {
      const name = tr.querySelector('.item-name').value.trim();
      const qty = parseFloat(tr.querySelector('.item-qty').value) || 0;
      const price = parseFloat(tr.querySelector('.item-price').value) || 0;
      return { name, qty, price, subtotal: qty * price };
    }).filter(item => item.name);

    if (rows.length === 0) {
      alert('품목을 최소 1개 이상 입력해주세요.');
      return;
    }

    const total = rows.reduce((sum, item) => sum + item.subtotal, 0);
    const totalKRW = total * rate;
    const today = new Date().toISOString().slice(0, 10);
    const quoteNo = 'QQ-' + today.replace(/-/g, '');

    const history = loadHistory();
    history.unshift({ buyer, currency, total, date: today, quoteNo });
    saveHistory(history);
    historySearchInput.value = '';
    renderAllHistory();

    let itemRowsHtml = rows.map(item => `
      <tr>
        <td>${item.name}</td>
        <td class="num">${item.qty}</td>
        <td class="num">${formatNumber(item.price)} ${currency}</td>
        <td class="num">${formatNumber(item.subtotal)} ${currency}</td>
      </tr>
    `).join('');

    quoteDoc.innerHTML = `
      <h3>QUOTATION</h3>
      <div class="quote-sub">${quoteNo} &nbsp;|&nbsp; 발행일: ${today} &nbsp;|&nbsp; 거래처: ${buyer}</div>
      <table>
        <thead>
          <tr><th>품목</th><th class="num">수량</th><th class="num">단가</th><th class="num">금액</th></tr>
        </thead>
        <tbody>
          ${itemRowsHtml}
          <tr class="quote-total-row">
            <td colspan="3">Total (${currency})</td>
            <td class="num">${formatNumber(total)} ${currency}</td>
          </tr>
          ${rate > 0 ? `
          <tr class="quote-total-row">
            <td colspan="3">Total (KRW 환산, 환율 ${rate})</td>
            <td class="num">${formatNumber(totalKRW)} KRW</td>
          </tr>` : ''}
        </tbody>
      </table>
    `;

    resultCard.classList.add('visible');
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  downloadBtn.addEventListener('click', () => {
    window.print();
  });

  // Streamlit embeds this page in a fixed-height iframe. Since the layout is
  // now a single mobile-width column, content height changes a lot as
  // items/preview/history are added, so we resize the iframe itself to match.
  function resizeFrame() {
    try {
      if (window.frameElement) {
        window.frameElement.style.height = document.documentElement.scrollHeight + 'px';
      }
    } catch (e) {}
  }
  window.addEventListener('load', resizeFrame);
  window.addEventListener('resize', resizeFrame);
  new ResizeObserver(resizeFrame).observe(document.body);
  setTimeout(resizeFrame, 100);
</script>

</body>
</html>
"""

components.html(HTML_CODE, height=900, scrolling=False)
