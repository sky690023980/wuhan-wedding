// ===== 武汉婚庆服务商目录 - 主逻辑 =====

// 分类配置（含渐变色，用于生成封面SVG）
const CATEGORIES = {
  photography: { name: '婚庆摄影', icon: '📷', desc: '记录婚礼每一个精彩瞬间', color1: '#ff9a9e', color2: '#fecfef' },
  'make-up':   { name: '婚礼化妆', icon: '💄', desc: '新娘精致妆容与造型设计', color1: '#f093fb', color2: '#f5576c' },
  venue:       { name: '婚礼场地', icon: '🏨', desc: '浪漫婚礼场地推荐',       color1: '#4facfe', color2: '#00f2fe' },
  hotel:       { name: '婚宴酒店', icon: '🥂', desc: '精致婚宴酒店推荐',       color1: '#43e97b', color2: '#38f9d7' },
  planner:     { name: '婚庆策划', icon: '📋', desc: '一站式婚礼策划服务',     color1: '#fa709a', color2: '#fee140' },
  host:        { name: '婚礼主持', icon: '🎤', desc: '专业婚礼主持人',         color1: '#a18cd1', color2: '#fbc2eb' },
  dress:       { name: '婚纱礼服', icon: '👗', desc: '新娘婚纱与礼服租赁',     color1: '#ffecd2', color2: '#fcb69f' },
  flower:      { name: '婚礼花艺', icon: '💐', desc: '婚礼鲜花布置与花艺设计', color1: '#a1c4fd', color2: '#c2e9fb' },
  'new-house': { name: '婚房布置', icon: '🏠', desc: '新房布置与喜庆装饰',     color1: '#ffecd2', color2: '#fcb69f' },
};

// 价格档次配置
const PRICE_LEVELS = {
  economy: { name: '经济实惠', label: '经济', color: '#4caf50', bg: '#e8f5e9', icon: '💚' },
  mid:     { name: '中等价位', label: '中等', color: '#ff9800', bg: '#fff3e0', icon: '🧡' },
  premium: { name: '高端定制', label: '高端', color: '#9c27b0', bg: '#f3e5f5', icon: '💜' },
};

const DISTRICTS = ['武昌区','汉口区','汉阳区','青山区','洪山区','江夏区','硚口区','江汉区','江岸区','东西湖区','蔡甸区','黄陂区','新洲区'];

let allVendors = [];

// 获取当前页面相对根目录的前缀（用于引用 images/ 等资源）
function getBase() {
  return location.pathname.includes('/pages/') ? '../' : '';
}

// ===== 生成内嵌SVG封面（data URI，100%可显示，无需外网）=====
function makeCoverSVG(v) {
  const cat = CATEGORIES[v.category] || { color1: '#fa709a', color2: '#fee140', name: '婚庆服务' };
  const c1 = cat.color1 || '#fa709a';
  const c2 = cat.color2 || '#fee140';
  // 取商家名前2个汉字
  const short = (v.name || '').replace(/[^\u4e00-\u9fa5]/g, '').slice(0, 2) || 'WD';
  const catName = cat.name || '';
  const district = v.district || '';
  const vName = (v.name || '').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  const svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200">',
    '<defs>',
    '<linearGradient id="gc' + v.id + '" x1="0%" y1="0%" x2="100%" y2="100%">',
    '<stop offset="0%" stop-color="' + c1 + '"/>',
    '<stop offset="100%" stop-color="' + c2 + '"/>',
    '</linearGradient>',
    '</defs>',
    '<rect width="600" height="200" fill="url(#gc' + v.id + ')"/>',
    '<circle cx="520" cy="40" r="100" fill="rgba(255,255,255,0.15)"/>',
    '<circle cx="60" cy="190" r="80" fill="rgba(255,255,255,0.10)"/>',
    '<circle cx="300" cy="100" r="120" fill="rgba(255,255,255,0.05)"/>',
    '<text x="300" y="84" font-size="50" text-anchor="middle" dominant-baseline="middle" fill="rgba(255,255,255,0.20)" font-weight="bold" font-family="serif">' + short + '</text>',
    '<text x="300" y="124" font-size="17" text-anchor="middle" dominant-baseline="middle" fill="rgba(255,255,255,0.92)" font-weight="600" font-family="PingFang SC,Microsoft YaHei,sans-serif">' + vName + '</text>',
    '<text x="300" y="153" font-size="12" text-anchor="middle" dominant-baseline="middle" fill="rgba(255,255,255,0.70)" font-family="PingFang SC,Microsoft YaHei,sans-serif">' + catName + (district ? ' · ' + district : '') + '</text>',
    '</svg>'
  ].join('');

  return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
}

// ===== 加载数据 =====
async function loadVendors() {
  try {
    const base = location.pathname.includes('/pages/') ? '../' : '';
    const resp = await fetch(base + 'data/vendors.json?t=' + Date.now());
    allVendors = await resp.json();
  } catch (e) {
    allVendors = getDemoData();
  }
  return allVendors;
}

// ===== 演示数据（fallback）=====
function getDemoData() {
  return [
    { id:1, name:'武汉巴黎婚纱摄影', category:'photography', district:'武昌区', address:'武汉市武昌区中南路88号', price:'¥3999起', priceNum:3999, rating:4.9, reviews:286, tags:['韩式风格','夜景外拍','一对一服务'], featured:true, desc:'专注婚纱摄影15年，韩式/中式/西式多风格选择，一对一专属服务。', phone:'1387100xxxx', verified:true },
    { id:2, name:'绣球花婚礼策划', category:'planner', district:'汉口区', address:'武汉市江汉区解放大道100号', price:'¥18888起', priceNum:18888, rating:4.8, reviews:152, tags:['中式婚礼','户外婚礼','定制策划'], featured:true, desc:'武汉本土婚礼策划品牌，中式婚礼设计独具匠心，已服务3000+新人。', phone:'1397100xxxx', verified:true },
    { id:3, name:'半岛婚纱礼服馆', category:'dress', district:'武昌区', address:'武汉市武昌区光谷步行街66号', price:'¥2888起', priceNum:2888, rating:4.7, reviews:98, tags:['高端定制','租赁改装','多品牌'], featured:false, desc:'汇集国际品牌，专业试纱顾问一对一服务。', phone:'1377100xxxx', verified:true },
    { id:4, name:'武汉香格里拉大酒店', category:'venue', district:'汉口区', address:'武汉市江汉区建设大道700号', price:'¥6888起/桌', priceNum:6888, rating:4.6, reviews:412, tags:['五星级','户外草坪','容纳500人'], featured:true, desc:'武汉知名五星级酒店，户外草坪婚礼场地，可接待大型婚宴。', phone:'027-8580xxxx', verified:true },
    { id:5, name:'妍色新娘化妆造型', category:'make-up', district:'洪山区', address:'武汉市洪山区珞瑜路35号', price:'¥1888起', priceNum:1888, rating:4.9, reviews:203, tags:['韩式裸妆','试妆服务','跟妆全天'], featured:true, desc:'专注新娘化妆造型，韩式裸妆风格深受好评。', phone:'1367100xxxx', verified:true },
  ];
}

// ===== 渲染分类卡片（首页）=====
function renderCatGrid() {
  const grid = document.getElementById('cat-grid');
  if (!grid) return;
  grid.className = 'cat-grid';
  const base = location.pathname.includes('/pages/') ? '' : 'pages/';
  grid.innerHTML = Object.entries(CATEGORIES).map(([key, cat]) => `
    <a href="${base}category.html?cat=${key}" class="cat-card">
      <div class="cat-icon">${cat.icon}</div>
      <h3>${cat.name}</h3>
      <p>${cat.desc}</p>
    </a>
  `).join('');
}

// ===== 渲染精选商家（首页）=====
function renderFeatured() {
  const grid = document.getElementById('featured-grid');
  if (!grid) return;
  const featured = allVendors.filter(v => v.featured).slice(0, 6);
  grid.className = 'vendor-grid';
  grid.innerHTML = featured.map(v => vendorCardHTML(v, false)).join('');
}

// ===== 商家卡片HTML =====
function vendorCardHTML(v, isSubpage) {
  const cat = CATEGORIES[v.category] || {};
  const pl = PRICE_LEVELS[v.price_level] || PRICE_LEVELS.mid;
  // 路径判断
  if (isSubpage === undefined) {
    isSubpage = location.pathname.includes('/pages/');
  }
  const detailPath = isSubpage ? 'vendor.html' : 'pages/vendor.html';
  const base = getBase();

  // 图片：优先用 v.image（本地SVG/图片），否则用内嵌SVG
  let imgSrc = v.image ? base + v.image : makeCoverSVG(v);
  const imgHTML = `<img src="${imgSrc}" alt="${v.name}" class="vendor-thumb"
    onerror="this.onerror=null;this.src='${makeCoverSVG(v)}'">`;

  // 价格档次标签
  const plBadge = `<span class="price-level-badge price-level-${v.price_level || 'mid'}">${pl.icon} ${pl.label}</span>`;

  // 子分类标签
  const subTypeTag = v.sub_type ? `<span class="vendor-tag vendor-tag-sub">${v.sub_type}</span>` : '';

  return `
    <a href="${detailPath}?id=${v.id}" class="vendor-card">
      <div class="vendor-img-wrap">
        ${imgHTML}
        <div class="vendor-cat-badge">${cat.name || v.category || ''}</div>
        <div class="vendor-price-badge">${plBadge}</div>
      </div>
      <div class="vendor-body">
        <div class="vendor-name">${v.verified ? '<span class="verified-icon">✓</span>' : ''} ${v.name}</div>
        <div class="vendor-meta">
          <span class="vendor-rating">★ ${v.rating}<em>（${v.reviews}条评价）</em></span>
          <span class="vendor-district-tag">📍 ${v.district}</span>
        </div>
        ${v.tags ? `<div class="vendor-tags">${subTypeTag}${v.tags.map(t => `<span class="vendor-tag">${t}</span>`).join('')}</div>` : (subTypeTag ? `<div class="vendor-tags">${subTypeTag}</div>` : '')}
        <div class="vendor-price">${v.price}</div>
      </div>
    </a>
  `;
}

// ===== 搜索（首页）=====
function doSearch() {
  const cat = document.getElementById('search-cat')?.value || '';
  const kw = document.getElementById('search-keyword')?.value || '';
  let url = 'pages/category.html';
  const params = [];
  if (cat) params.push('cat=' + encodeURIComponent(cat));
  if (kw) params.push('q=' + encodeURIComponent(kw));
  if (params.length) url += '?' + params.join('&');
  location.href = url;
}

// ===== 搜索联想（实时搜索建议）=====
const SEARCH_SUGGESTIONS_KEY = 'wh_wedding_search_history';

function getSearchHistory() {
  try { return JSON.parse(localStorage.getItem(SEARCH_SUGGESTIONS_KEY) || '[]'); } catch(e) { return []; }
}

function saveSearchHistory(keyword) {
  if (!keyword || keyword.length < 2) return;
  let history = getSearchHistory().filter(h => h !== keyword);
  history.unshift(keyword);
  if (history.length > 8) history = history.slice(0, 8);
  localStorage.setItem(SEARCH_SUGGESTIONS_KEY, JSON.stringify(history));
}

function clearSearchHistory() {
  localStorage.removeItem(SEARCH_SUGGESTIONS_KEY);
  hideSuggestions();
}

function initSearchSuggestions() {
  const input = document.getElementById('search-keyword');
  if (!input) return;

  // 创建建议下拉框
  let box = document.getElementById('search-suggestions');
  if (!box) {
    box = document.createElement('div');
    box.id = 'search-suggestions';
    box.className = 'search-suggestions';
    input.parentNode.parentNode.appendChild(box);
  }

  input.addEventListener('input', function() {
    const kw = this.value.trim();
    if (kw.length < 1) { hideSuggestions(); return; }
    showSuggestions(kw);
  });

  input.addEventListener('focus', function() {
    const kw = this.value.trim();
    if (kw.length < 1 && getSearchHistory().length > 0) {
      showHistorySuggestions();
    } else if (kw.length >= 1) {
      showSuggestions(kw);
    }
  });

  document.addEventListener('click', function(e) {
    if (!e.target.closest('.search-box')) hideSuggestions();
  });
}

async function showSuggestions(kw) {
  const box = document.getElementById('search-suggestions');
  if (!box) return;

  // 加载数据（如果还没加载）
  if (allVendors.length === 0) await loadVendors();

  const results = searchVendors(kw, 6);
  const history = getSearchHistory().filter(h => h.includes(kw)).slice(0, 2);

  let html = '';

  if (history.length > 0) {
    html += '<div class="suggestion-group"><div class="suggestion-label">搜索历史</div>';
    history.forEach(h => {
      html += `<div class="suggestion-item history-item" onclick="selectSuggestion('${escapeHtml(h)}')"><span>🕐</span><span>${highlightMatch(h, kw)}</span><span class="del-history" onclick="event.stopPropagation();removeHistory('${escapeHtml(h)}')">✕</span></div>`;
    });
    html += '</div>';
  }

  if (results.length > 0) {
    html += '<div class="suggestion-group"><div class="suggestion-label">商家推荐</div>';
    results.forEach(r => {
      const cat = CATEGORIES[r.category] || {};
      html += `<div class="suggestion-item" onclick="selectSuggestion('${escapeHtml(r.name)}')"><span>${cat.icon || '🏷️'}</span><span>${highlightMatch(r.name, kw)} <em>${r.district} · ${cat.name || ''} · ${r.price}</em></span></div>`;
    });
    html += '</div>';
  }

  // 匹配分类
  const catMatches = Object.entries(CATEGORIES).filter(([k, v]) => v.name.includes(kw) || k.includes(kw.toLowerCase()));
  if (catMatches.length > 0) {
    html += '<div class="suggestion-group"><div class="suggestion-label">服务类别</div>';
    catMatches.slice(0, 3).forEach(([k, v]) => {
      html += `<div class="suggestion-item" onclick="selectCategory('${k}')"><span>${v.icon}</span><span>${highlightMatch(v.name, kw)}</span></div>`;
    });
    html += '</div>';
  }

  // 匹配区域
  const districtMatches = DISTRICTS.filter(d => d.includes(kw));
  if (districtMatches.length > 0) {
    html += '<div class="suggestion-group"><div class="suggestion-label">区域</div>';
    districtMatches.slice(0, 3).forEach(d => {
      html += `<div class="suggestion-item" onclick="selectDistrict('${d}')"><span>📍</span><span>${highlightMatch(d, kw)}</span></div>`;
    });
    html += '</div>';
  }

  if (!html) {
    html = '<div class="suggestion-empty">未找到相关结果，试试其他关键词</div>';
  }

  box.innerHTML = html;
  box.style.display = 'block';
}

function showHistorySuggestions() {
  const box = document.getElementById('search-suggestions');
  if (!box) return;
  const history = getSearchHistory();
  if (history.length === 0) return;

  let html = '<div class="suggestion-group"><div class="suggestion-label">搜索历史</div>';
  history.forEach(h => {
    html += `<div class="suggestion-item history-item" onclick="selectSuggestion('${escapeHtml(h)}')"><span>🕐</span><span>${escapeHtml(h)}</span><span class="del-history" onclick="event.stopPropagation();removeHistory('${escapeHtml(h)}')">✕</span></div>`;
  });
  html += `<div class="suggestion-item clear-item" onclick="clearSearchHistory()"><span></span><span>清除搜索历史</span></div>`;
  html += '</div>';

  box.innerHTML = html;
  box.style.display = 'block';
}

function hideSuggestions() {
  const box = document.getElementById('search-suggestions');
  if (box) box.style.display = 'none';
}

function selectSuggestion(text) {
  const input = document.getElementById('search-keyword');
  if (input) input.value = text;
  saveSearchHistory(text);
  hideSuggestions();
  doSearch();
}

function selectCategory(cat) {
  const catSelect = document.getElementById('search-cat');
  if (catSelect) catSelect.value = cat;
  hideSuggestions();
  doSearch();
}

function selectDistrict(district) {
  const input = document.getElementById('search-keyword');
  if (input) input.value = district;
  hideSuggestions();
  doSearch();
}

function removeHistory(keyword) {
  let history = getSearchHistory().filter(h => h !== keyword);
  localStorage.setItem(SEARCH_SUGGESTIONS_KEY, JSON.stringify(history));
  showHistorySuggestions();
}

function escapeHtml(text) {
  return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#039;');
}

function highlightMatch(text, kw) {
  if (!kw) return escapeHtml(text);
  const escaped = escapeHtml(text);
  const kwEscaped = escapeHtml(kw);
  const regex = new RegExp('(' + kwEscaped.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
  return escaped.replace(regex, '<strong class="hl">$1</strong>');
}

// 智能搜索函数（支持名称、标签、描述、区域、拼音首字母等）
function searchVendors(keyword, limit) {
  if (!keyword) return [];
  limit = limit || 50;
  const kw = keyword.toLowerCase();

  return allVendors.filter(v => {
    // 名称匹配
    if (v.name.toLowerCase().includes(kw)) return true;
    // 区域匹配
    if (v.district && v.district.includes(kw)) return true;
    // 标签匹配
    if (v.tags && v.tags.some(t => t.toLowerCase().includes(kw))) return true;
    // 描述匹配
    if (v.desc && v.desc.toLowerCase().includes(kw)) return true;
    // 分类名匹配
    const cat = CATEGORIES[v.category];
    if (cat && cat.name.includes(kw)) return true;
    // 地址匹配
    if (v.address && v.address.toLowerCase().includes(kw)) return true;
    return false;
  }).slice(0, limit);
}

// ===== 列表页逻辑 =====
let currentSubType = '';

async function loadCategoryPage() {
  const params = new URLSearchParams(location.search);
  const cat = params.get('cat') || '';
  const district = params.get('district') || '';
  const q = params.get('q') || '';
  const price = params.get('price') || '';
  const subtype = params.get('subtype') || '';

  currentSubType = subtype;

  const catInfo = CATEGORIES[cat];
  const h1 = document.getElementById('page-title');
  const desc = document.getElementById('page-desc');
  if (h1) h1.textContent = catInfo ? catInfo.name : (district || '全部商家');
  if (desc) desc.textContent = catInfo ? catInfo.desc : (district ? district + '的婚庆服务商' : '收录武汉优质婚庆服务商');

  const catSelect = document.getElementById('filter-cat');
  const distSelect = document.getElementById('filter-district');
  const priceSelect = document.getElementById('filter-price');
  if (catSelect) catSelect.value = cat;
  if (distSelect) distSelect.value = district;
  if (priceSelect) priceSelect.value = price;

  await loadVendors();

  // 渲染子分类标签栏
  renderSubTypeBar(cat, subtype);

  renderVendorList({ cat, district, q, price, subtype });
}

function renderSubTypeBar(cat, activeSubType) {
  const bar = document.getElementById('sub-type-bar');
  if (!bar) return;

  if (!cat) {
    bar.style.display = 'none';
    return;
  }

  // 收集该分类下的所有 sub_type
  const subTypes = [...new Set(allVendors.filter(v => v.category === cat && v.sub_type).map(v => v.sub_type))].sort();

  if (subTypes.length === 0) {
    bar.style.display = 'none';
    return;
  }

  bar.style.display = 'flex';

  // 保留第一个 span（"风格："标签）
  let html = bar.querySelector('span').outerHTML;

  // "全部"按钮
  html += `<button class="sub-type-btn ${!activeSubType ? 'active' : ''}" onclick="selectSubType('')">全部</button>`;

  subTypes.forEach(st => {
    html += `<button class="sub-type-btn ${activeSubType === st ? 'active' : ''}" onclick="selectSubType('${escapeHtml(st)}')">${st}</button>`;
  });

  bar.innerHTML = html;
}

function selectSubType(subtype) {
  currentSubType = subtype;
  // 重新渲染子分类按钮状态
  const cat = document.getElementById('filter-cat')?.value || '';
  renderSubTypeBar(cat, subtype);
  // 重新筛选列表（不改URL，直接刷新）
  applyFiltersInline();
}

function applyFiltersInline() {
  const cat = document.getElementById('filter-cat')?.value || '';
  const district = document.getElementById('filter-district')?.value || '';
  const q = document.getElementById('filter-q')?.value || '';
  const price = document.getElementById('filter-price')?.value || '';
  renderVendorList({ cat, district, q, price, subtype: currentSubType });
}

function renderVendorList({ cat, district, q, price, subtype } = {}) {
  let list = allVendors;
  if (cat) list = list.filter(v => v.category === cat);
  if (district) list = list.filter(v => v.district === district);
  if (price) list = list.filter(v => v.price_level === price);
  if (subtype) list = list.filter(v => v.sub_type === subtype);
  if (q) {
    const kw = q.toLowerCase();
    list = list.filter(v =>
      v.name.toLowerCase().includes(kw) ||
      (v.tags||[]).some(t => t.toLowerCase().includes(kw)) ||
      (v.desc||'').toLowerCase().includes(kw) ||
      (v.district||'').includes(kw) ||
      (v.address||'').toLowerCase().includes(kw) ||
      (v.sub_type||'').toLowerCase().includes(kw)
    );
    // 保存搜索历史
    saveSearchHistory(q);
  }

  const grid = document.getElementById('vendor-list');
  if (!grid) return;
  grid.className = 'vendor-grid';
  const countEl = document.getElementById('result-count');
  if (countEl) {
    let hintText = `共找到 ${list.length} 家服务商`;
    if (q) hintText = `搜索"${q}"找到 ${list.length} 家服务商`;
    countEl.textContent = hintText;
  }

  if (list.length === 0) {
    const emptyMsg = q
      ? `<div style="grid-column:1/-1;text-align:center;padding:60px;color:#999;">
          <div style="font-size:48px;margin-bottom:16px;">🔍</div>
          <div style="font-size:16px;font-weight:600;color:#333;margin-bottom:8px;">未找到"${escapeHtml(q)}"相关的服务商</div>
          <div style="font-size:13px;">试试其他关键词，如"武昌""光谷""婚礼主持"等</div>
        </div>`
      : '<div style="grid-column:1/-1;text-align:center;padding:60px;color:#999;">暂无符合条件的服务商，换个条件试试吧</div>';
    grid.innerHTML = emptyMsg;
    return;
  }
  grid.innerHTML = list.map(v => vendorCardHTML(v, true)).join('');
}

function applyFilters() {
  const cat = document.getElementById('filter-cat')?.value || '';
  const district = document.getElementById('filter-district')?.value || '';
  const q = document.getElementById('filter-q')?.value || '';
  const price = document.getElementById('filter-price')?.value || '';
  const params = [];
  if (cat) params.push('cat=' + encodeURIComponent(cat));
  if (district) params.push('district=' + encodeURIComponent(district));
  if (q) params.push('q=' + encodeURIComponent(q));
  if (price) params.push('price=' + encodeURIComponent(price));
  if (currentSubType) params.push('subtype=' + encodeURIComponent(currentSubType));
  location.href = 'category.html' + (params.length ? '?' + params.join('&') : '');
}

// ===== 详情页逻辑 =====
async function loadVendorDetail() {
  const params = new URLSearchParams(location.search);
  const id = parseInt(params.get('id')) || 1;
  await loadVendors();
  const v = allVendors.find(x => x.id === id) || allVendors[0];
  if (!v) return;

  document.title = v.name + ' - 武汉婚庆服务商目录';

  const cat = CATEGORIES[v.category] || {};
  const detail = document.getElementById('vendor-detail-content');
  if (!detail) return;

  const base = getBase();

  // 主图（优先本地图片，失败用SVG）
  const svgSrc = makeCoverSVG(v);
  const mainSrc = v.image ? base + v.image : svgSrc;
  const mainImgHTML = `<img src="${mainSrc}" alt="${v.name}" class="gallery-main-img" onerror="this.src='${svgSrc}'">`;

  // 缩略图（优先 v.gallery，否则用SVG变体色块）
  let subImgsHTML;
  if (v.gallery && v.gallery.length > 0) {
    subImgsHTML = v.gallery.map((src, i) =>
      `<img src="${base + src}" alt="${v.name}案例${i+1}" class="gallery-sub-img" onerror="this.onerror=null;this.src='${makeCoverSVG(Object.assign({}, v, { id: v.id * 10 + i }))}'">`
    ).join('');
  } else {
    const subSVGs = [1,2,3].map(i => {
      const vv = Object.assign({}, v, { id: v.id * 10 + i });
      return makeCoverSVG(vv);
    });
    subImgsHTML = subSVGs.map((src, i) =>
      `<img src="${src}" alt="${v.name}案例${i+1}" class="gallery-sub-img">`
    ).join('');
  }

  detail.innerHTML = `
    <div class="vendor-gallery">
      <div class="main-img">${mainImgHTML}</div>
      <div class="sub-imgs-row">${subImgsHTML}</div>
    </div>
    <div class="vendor-info">
      <h1>${v.verified ? '<span class="verified-icon" style="font-size:16px;">✓</span> ' : ''}${v.name}</h1>
      <div class="info-rating">★ ${v.rating}&nbsp;&nbsp;${v.reviews} 条真实评价</div>
      <div class="info-meta">📍 ${v.address}</div>
      <div class="info-meta">📞 ${v.phone}</div>
      <div class="info-meta">🏷️ 类别：${cat.name || v.category}${v.sub_type ? ' · ' + v.sub_type : ''}</div>
      <div class="info-price-row">
        <div class="info-price">参考价格：${v.price}</div>
        ${v.price_level ? `<span class="price-level-badge price-level-${v.price_level}" style="font-size:13px;">${PRICE_LEVELS[v.price_level].icon} ${PRICE_LEVELS[v.price_level].name}</span>` : ''}
      </div>
      <div style="margin:10px 0;">${v.tags ? v.tags.map(t => `<span class="vendor-tag">${t}</span>`).join('') : ''}</div>
      <p style="color:#666;font-size:14px;line-height:1.85;margin-top:12px;">${v.desc}</p>
      <button class="btn-contact" onclick="alert('请直接拨打电话联系商家：${v.phone}')">📞 联系商家</button>
    </div>
  `;

  renderReviews(v);
  renderRelated(v);
}

function renderReviews(v) {
  const box = document.getElementById('reviews-list');
  if (!box) return;
  const demoReviews = [
    { author: '小**', rating: 5, text: '服务非常专业，整个过程很顺利，强烈推荐！', date: '2026-03-12' },
    { author: '李**', rating: 5, text: '效果超出预期，性价比很高，朋友都说好。', date: '2026-02-28' },
    { author: '王**', rating: 4, text: '整体满意，沟通顺畅，唯一不足是出片稍慢。', date: '2026-01-15' },
  ];
  box.innerHTML = demoReviews.map(r => `
    <div class="review-card">
      <div class="review-author">${r.author}&nbsp;&nbsp;<span style="color:#ccc;font-size:12px;">${r.date}</span></div>
      <div class="review-rating">${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)}</div>
      <div class="review-text">${r.text}</div>
    </div>
  `).join('');
  const countEl = document.getElementById('review-count');
  if (countEl) countEl.textContent = demoReviews.length;
}

function renderRelated(v) {
  const box = document.getElementById('related-list');
  if (!box) return;
  const related = allVendors.filter(x => x.category === v.category && x.id !== v.id).slice(0, 3);
  if (related.length === 0) { box.innerHTML = ''; return; }
  box.innerHTML = `<div class="detail-section"><h2>同类型推荐</h2><div class="vendor-grid">${related.map(r => vendorCardHTML(r, true)).join('')}</div></div>`;
}

// ===== 统计数据动画 =====
function animateStats() {
  const el1 = document.getElementById('stat-vendors');
  const el2 = document.getElementById('stat-reviews');
  if (el1) animateNum(el1, allVendors.length || 20);
  if (el2) {
    const total = allVendors.reduce((s, v) => s + (v.reviews || 0), 0);
    animateNum(el2, total || 5000);
  }
}

function animateNum(el, target) {
  let current = 0;
  const step = Math.ceil(target / 30);
  const timer = setInterval(() => {
    current += step;
    if (current >= target) { current = target; clearInterval(timer); }
    el.textContent = current;
  }, 30);
}

// ===== 首页初始化 =====
async function loadHomepage() {
  await loadVendors();
  renderCatGrid();
  renderFeatured();
  initSearchSuggestions();
  setTimeout(animateStats, 300);
}

// ===== 入驻表单 =====
function initSubmitForm() {
  const form = document.getElementById('submit-form');
  if (!form) return;
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    console.log('商家入驻申请：', data);
    const result = document.getElementById('submit-result');
    if (result) result.style.display = 'block';
    form.style.display = 'none';
  });
}

// 暴露全局
window.doSearch = doSearch;
window.applyFilters = applyFilters;
window.applyFiltersInline = applyFiltersInline;
window.selectSubType = selectSubType;
window.loadHomepage = loadHomepage;
window.loadCategoryPage = loadCategoryPage;
window.loadVendorDetail = loadVendorDetail;
window.initSubmitForm = initSubmitForm;
window.selectSuggestion = selectSuggestion;
window.selectCategory = selectCategory;
window.selectDistrict = selectDistrict;
window.clearSearchHistory = clearSearchHistory;
window.removeHistory = removeHistory;
