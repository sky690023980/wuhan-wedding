// ===== 武汉婚庆服务商目录 - 主逻辑 =====

// 分类配置
const CATEGORIES = {
  photography: { name: '婚庆摄影', icon: '📷', desc: '记录婚礼每一个精彩瞬间' },
  'make-up':  { name: '婚礼化妆', icon: '💄', desc: '新娘精致妆容与造型设计' },
  venue:      { name: '婚礼场地', icon: '🏨', desc: '浪漫婚礼场地推荐' },
  planner:    { name: '婚庆策划', icon: '📋', desc: '一站式婚礼策划服务' },
  host:       { name: '婚礼主持', icon: '🎤', desc: '专业婚礼主持人' },
  dress:      { name: '婚纱礼服', icon: '👗', desc: '新娘婚纱与礼服租赁' },
  flower:     { name: '婚礼花艺', icon: '💐', desc: '婚礼鲜花布置与花艺设计' },
};

const DISTRICTS = ['武昌区','汉口区','汉阳区','青山区','洪山区','江夏区','硚口区','江汉区','江岸区','东西湖区','蔡甸区','黄陂区','新洲区'];

let allVendors = [];

// ===== 加载数据 =====
async function loadVendors() {
  try {
    // 兼容首页(根目录)和子页面(pages/)的相对路径
    const base = location.pathname.includes('/pages/') ? '../' : '';
    const resp = await fetch(base + 'data/vendors.json?t=' + Date.now());
    allVendors = await resp.json();
  } catch (e) {
    allVendors = getDemoData();
  }
  return allVendors;
}

// ===== 演示数据 =====
function getDemoData() {
  return [
    { id:1, name:'武汉巴黎婚纱摄影', category:'photography', district:'武昌区', address:'武汉市武昌区中南路88号', price:'¥3999起', priceNum:3999, rating:4.9, reviews:286, tags:['韩式风格','夜景外拍','一对一服务'], featured:true, desc:'专注婚纱摄影15年，韩式/中式/西式多风格选择，一对一专属服务。', phone:'1387100xxxx', verified:true },
    { id:2, name:'绣球花婚礼策划', category:'planner', district:'汉口区', address:'武汉市江汉区解放大道100号', price:'¥18888起', priceNum:18888, rating:4.8, reviews:152, tags:['中式婚礼','户外婚礼','定制策划'], featured:true, desc:'武汉本土婚礼策划品牌，中式婚礼设计独具匠心，已服务3000+新人。', phone:'1397100xxxx', verified:true },
    { id:3, name:'半岛婚纱礼服馆', category:'dress', district:'武昌区', address:'武汉市武昌区光谷步行街66号', price:'¥2888起', priceNum:2888, rating:4.7, reviews:98, tags:['高端定制','租赁改装','多品牌'], featured:false, desc:'汇集Vera Wang、蔡美月等国际品牌，专业试纱顾问一对一服务。', phone:'1377100xxxx', verified:true },
    { id:4, name:'武汉香格里拉大酒店', category:'venue', district:'汉口区', address:'武汉市江汉区建设大道700号', price:'¥6888起/桌', priceNum:6888, rating:4.6, reviews:412, tags:['五星级','户外草坪','容纳500人'], featured:true, desc:'武汉知名五星级酒店，户外草坪婚礼场地，可接待大型婚宴。', phone:'027-8580xxxx', verified:true },
    { id:5, name:'妍色新娘化妆造型', category:'make-up', district:'洪山区', address:'武汉市洪山区珞瑜路35号', price:'¥1888起', priceNum:1888, rating:4.9, reviews:203, tags:['韩式裸妆','试妆服务','跟妆全天'], featured:true, desc:'专注新娘化妆造型，韩式裸妆风格深受好评，提供试妆和婚礼当天跟妆。', phone:'1367100xxxx', verified:true },
    { id:6, name:'武汉爱琴海婚庆摄影', category:'photography', district:'汉阳区', address:'武汉市汉阳区龙阳大道199号', price:'¥2999起', priceNum:2999, rating:4.5, reviews:87, tags:['性价比高','内景丰富','快速出片'], featured:false, desc:'高性价比婚纱摄影，内景基地3000平米，快速出片无需漫长等待。', phone:'1357100xxxx', verified:false },
    { id:7, name:'花间堂婚礼花艺', category:'flower', district:'武昌区', address:'武汉市武昌区水果湖街12号', price:'¥3888起', priceNum:3888, rating:4.8, reviews:76, tags:['定制花艺','户外布置','韩式花门'], featured:false, desc:'专业婚礼花艺设计，韩式花门、背景墙、手捧花一站式定制。', phone:'1337100xxxx', verified:true },
    { id:8, name:'金话筒婚礼主持', category:'host', district:'江汉区', address:'武汉市江汉区万松园路58号', price:'¥2000起', priceNum:2000, rating:4.7, reviews:134, tags:['幽默风格','中式主持','流程把控'], featured:false, desc:'15年婚礼主持经验，幽默大气风格，擅长中式婚礼主持。', phone:'1397100xxxx', verified:true },
    { id:9, name:'武汉万达瑞华酒店', category:'venue', district:'武昌区', address:'武汉市武昌区水果湖街东湖路138号', price:'¥5888起/桌', priceNum:5888, rating:4.7, reviews:298, tags:['湖景宴会厅','五星级','容纳300人'], featured:false, desc:'东湖湖畔五星级酒店，湖景宴会厅浪漫典雅，是举办高端婚礼的理想之选。', phone:'027-8810xxxx', verified:true },
    { id:10, name:'遇见幸福婚纱摄影', category:'photography', district:'洪山区', address:'武汉市洪山区街道口商圈88号', price:'¥3599起', priceNum:3599, rating:4.6, reviews:175, tags:['轻奢风格','旅拍服务','底片全送'], featured:false, desc:'轻奢婚纱摄影品牌，提供武汉周边旅拍服务，底片全送无隐形消费。', phone:'1377100xxxx', verified:true },
  ];
}

// ===== 渲染分类卡片（首页）=====
function renderCatGrid() {
  const grid = document.getElementById('cat-grid');
  if (!grid) return;
  grid.className = 'cat-grid';
  grid.innerHTML = Object.entries(CATEGORIES).map(([key, cat]) => `
    <a href="pages/category.html?cat=${key}" class="cat-card">
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
  grid.innerHTML = featured.map(v => vendorCardHTML(v)).join('');
}

// ===== 商家卡片HTML =====
function vendorCardHTML(v, fromSubpage) {
  const cat = CATEGORIES[v.category] || {};
  // 根据当前页面层级确定链接前缀
  const isSubpage = fromSubpage !== undefined ? fromSubpage : location.pathname.includes('/pages/');
  const detailPath = isSubpage ? 'vendor.html' : 'pages/vendor.html';
  // 图片：优先使用 v.image，否则用分类色块占位
  const imgTag = v.image
    ? `<img src="${v.image}" alt="${v.name}" class="vendor-thumb" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">`
    : '';
  const fallbackDiv = `<div class="vendor-img-fallback" style="display:${v.image ? 'none' : 'flex'}">${cat.icon || '🏪'}</div>`;
  return `
    <a href="${detailPath}?id=${v.id}" class="vendor-card">
      <div class="vendor-img-wrap">
        ${imgTag}
        ${fallbackDiv}
        <div class="vendor-cat-badge">${cat.name || v.category}</div>
      </div>
      <div class="vendor-body">
        <div class="vendor-name">${v.verified ? '<span class="verified-icon">✓</span>' : ''} ${v.name}</div>
        <div class="vendor-meta">
          <span class="vendor-rating">★ ${v.rating}<em>（${v.reviews}条评价）</em></span>
          <span class="vendor-district-tag">📍 ${v.district}</span>
        </div>
        ${v.tags ? `<div class="vendor-tags">${v.tags.map(t => `<span class="vendor-tag">${t}</span>`).join('')}</div>` : ''}
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

// ===== 列表页逻辑 =====
async function loadCategoryPage() {
  const params = new URLSearchParams(location.search);
  const cat = params.get('cat') || '';
  const district = params.get('district') || '';
  const q = params.get('q') || '';

  // 设置标题
  const catInfo = CATEGORIES[cat];
  const h1 = document.getElementById('page-title');
  const desc = document.getElementById('page-desc');
  if (h1) h1.textContent = catInfo ? catInfo.name : (district || '全部商家');
  if (desc) desc.textContent = catInfo ? catInfo.desc : (district ? district + '的婚庆服务商' : '收录武汉优质婚庆服务商');

  // 下拉框初始化
  const catSelect = document.getElementById('filter-cat');
  const distSelect = document.getElementById('filter-district');
  if (catSelect) catSelect.value = cat;
  if (distSelect) distSelect.value = district;

  await loadVendors();
  renderVendorList({ cat, district, q });
}

function renderVendorList({ cat, district, q } = {}) {
  let list = allVendors;
  if (cat) list = list.filter(v => v.category === cat);
  if (district) list = list.filter(v => v.district === district);
  if (q) list = list.filter(v => v.name.includes(q) || (v.tags||[]).some(t => t.includes(q)) || (v.desc||'').includes(q));

  const grid = document.getElementById('vendor-list');
  if (!grid) return;
  grid.className = 'vendor-grid';
  document.getElementById('result-count').textContent = `共找到 ${list.length} 家服务商`;

  if (list.length === 0) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:60px;color:#999;">暂无符合条件的服务商，换个条件试试吧</div>';
    return;
  }
  grid.innerHTML = list.map(v => vendorCardHTML(v)).join('');
}

function applyFilters() {
  const cat = document.getElementById('filter-cat')?.value || '';
  const district = document.getElementById('filter-district')?.value || '';
  const q = document.getElementById('filter-q')?.value || '';
  const params = [];
  if (cat) params.push('cat=' + encodeURIComponent(cat));
  if (district) params.push('district=' + encodeURIComponent(district));
  if (q) params.push('q=' + encodeURIComponent(q));
  location.href = 'category.html' + (params.length ? '?' + params.join('&') : '');
}

// ===== 详情页逻辑 =====
async function loadVendorDetail() {
  const params = new URLSearchParams(location.search);
  const id = parseInt(params.get('id')) || 1;
  await loadVendors();
  const v = allVendors.find(x => x.id === id) || allVendors[0];
  if (!v) return;

  document.title = `${v.name} - 武汉婚庆服务商目录`;

  const cat = CATEGORIES[v.category] || {};
  const detail = document.getElementById('vendor-detail-content');
  if (!detail) return;

  // 生成画廊图片组（主图+4个缩略图，均使用Unsplash同主题图）
  const galleryImgs = v.image ? [v.image,
    v.image.replace('w=600', 'w=400') + '&sat=-30',
    v.image.replace('w=600', 'w=400') + '&hue=20',
    v.image.replace('w=600', 'w=400') + '&bri=10',
    v.image.replace('w=600', 'w=400') + '&con=10'
  ] : [];

  const fallbackIcon = cat.icon || '🏪';
  const mainImgHTML = galleryImgs[0]
    ? `<img src="${galleryImgs[0]}" alt="${v.name}" class="gallery-main-img" onerror="this.outerHTML='<div class=gallery-main-fallback>${fallbackIcon}</div>'">`
    : `<div class="gallery-main-fallback">${fallbackIcon}</div>`;

  const subImgsHTML = galleryImgs.slice(1).map((url, i) =>
    `<img src="${url}" alt="${v.name}案例${i+1}" class="gallery-sub-img" loading="lazy" onerror="this.style.opacity='.3'">`
  ).join('') || '<div class="sub-img" style="opacity:.3">案例图片</div>'.repeat(4);

  detail.innerHTML = `
    <div class="vendor-gallery">
      <div class="main-img">${mainImgHTML}</div>
      <div class="sub-imgs-row">${subImgsHTML}</div>
    </div>
    <div class="vendor-info">
      <h1>${v.verified ? '✅ ' : ''}${v.name}</h1>
      <div class="info-rating">★ ${v.rating}　${v.reviews}条真实评价</div>
      <div class="info-meta">📍 ${v.address}</div>
      <div class="info-meta">📞 ${v.phone}</div>
      <div class="info-meta">🏷️ 类别：${cat.name || v.category}</div>
      <div class="info-price">参考价格：${v.price}</div>
      <div style="margin:10px 0;">${v.tags ? v.tags.map(t => `<span class="vendor-tag">${t}</span>`).join('') : ''}</div>
      <p style="color:#666;font-size:13.5px;line-height:1.8;">${v.desc}</p>
      <button class="btn-contact" onclick="alert('功能开发中，请通过电话直接联系商家')">📞 联系商家</button>
    </div>
  `;

  // 渲染评价
  renderReviews(v);
  // 渲染推荐
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
      <div class="review-author">${r.author}　<span style="color:#ccc;">${r.date}</span></div>
      <div class="review-rating">${'★'.repeat(r.rating)}${'☆'.repeat(5-r.rating)}</div>
      <div class="review-text">${r.text}</div>
    </div>
  `).join('');
}

function renderRelated(v) {
  const box = document.getElementById('related-list');
  if (!box) return;
  const related = allVendors.filter(x => x.category === v.category && x.id !== v.id).slice(0, 3);
  if (related.length === 0) { box.innerHTML = ''; return; }
  box.innerHTML = '<h3 style="font-size:16px;margin-bottom:12px;">同类型推荐</h3>' + related.map(v => vendorCardHTML(v)).join('');
}

// ===== 统计数据 =====
function animateStats() {
  const el1 = document.getElementById('stat-vendors');
  const el2 = document.getElementById('stat-reviews');
  if (el1) animateNum(el1, allVendors.length || 10);
  if (el2) {
    const totalReviews = allVendors.reduce((s, v) => s + (v.reviews || 0), 0);
    animateNum(el2, totalReviews || 200);
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
  setTimeout(animateStats, 300);
}

// ===== 表单提交 =====
function initSubmitForm() {
  const form = document.getElementById('submit-form');
  if (!form) return;
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    console.log('商家入驻申请：', data);
    document.getElementById('submit-result').style.display = 'block';
    form.style.display = 'none';
  });
}

// 暴露全局函数
window.doSearch = doSearch;
window.applyFilters = applyFilters;
window.loadHomepage = loadHomepage;
window.loadCategoryPage = loadCategoryPage;
window.loadVendorDetail = loadVendorDetail;
window.initSubmitForm = initSubmitForm;
