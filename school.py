HTML = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>نظام إدارة المدارس</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
:root {
  --primary: #1e3a5f;
  --primary-light: #2c5282;
  --accent: #c9a84c;
  --accent-light: #f6e9c8;
  --success: #22863a;
  --success-bg: #e6f4ea;
  --danger: #b91c1c;
  --danger-bg: #fef2f2;
  --warning: #92400e;
  --warning-bg: #fffbeb;
  --info: #1e40af;
  --info-bg: #eff6ff;
  --bg: #f4f6fa;
  --sidebar-bg: #1e3a5f;
  --card: #ffffff;
  --text: #1a202c;
  --muted: #64748b;
  --border: #e2e8f0;
  --sidebar-w: 240px;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Tajawal',sans-serif; background:var(--bg); color:var(--text); display:flex; min-height:100vh; font-size:15px; }

/* ── SIDEBAR ── */
.sidebar {
  width:var(--sidebar-w); min-height:100vh; background:var(--sidebar-bg);
  display:flex; flex-direction:column; position:fixed; right:0; top:0; bottom:0; z-index:100;
}
.sidebar-logo {
  padding:1.4rem 1.2rem 1rem;
  border-bottom:1px solid rgba(255,255,255,.1);
}
.sidebar-logo .logo-icon {
  width:42px; height:42px; border-radius:10px;
  background:var(--accent); display:flex; align-items:center; justify-content:center;
  font-size:22px; margin-bottom:.5rem;
}
.sidebar-logo h2 { color:#fff; font-size:1rem; font-weight:700; line-height:1.3; }
.sidebar-logo span { color:rgba(255,255,255,.5); font-size:.78rem; }

nav { flex:1; padding:.8rem 0; overflow-y:auto; }
.nav-section { padding:.4rem 1rem .2rem; font-size:.72rem; color:rgba(255,255,255,.35); letter-spacing:.08em; text-transform:uppercase; }
.nav-item {
  display:flex; align-items:center; gap:.7rem;
  padding:.65rem 1.2rem; cursor:pointer; transition:.15s;
  color:rgba(255,255,255,.65); font-size:.92rem; position:relative;
  border-right:3px solid transparent;
}
.nav-item:hover { background:rgba(255,255,255,.07); color:#fff; }
.nav-item.active { background:rgba(255,255,255,.12); color:#fff; border-right-color:var(--accent); font-weight:500; }
.nav-item .icon { font-size:1.2rem; width:22px; text-align:center; }
.nav-item .badge {
  margin-right:auto; background:var(--accent); color:#fff;
  font-size:.7rem; padding:1px 7px; border-radius:20px; font-weight:700;
}
.sidebar-footer {
  padding:1rem 1.2rem; border-top:1px solid rgba(255,255,255,.1);
  display:flex; align-items:center; gap:.8rem;
}
.avatar { width:36px; height:36px; border-radius:50%; background:var(--accent); display:flex; align-items:center; justify-content:center; font-weight:700; color:#fff; font-size:.85rem; flex-shrink:0; }
.sidebar-footer .info h4 { color:#fff; font-size:.85rem; font-weight:500; }
.sidebar-footer .info p { color:rgba(255,255,255,.4); font-size:.75rem; }

/* ── MAIN ── */
.main { margin-right:var(--sidebar-w); flex:1; display:flex; flex-direction:column; }
.topbar {
  background:var(--card); border-bottom:1px solid var(--border);
  padding:.8rem 1.8rem; display:flex; align-items:center; gap:1rem;
  position:sticky; top:0; z-index:50;
}
.topbar-title { font-size:1.15rem; font-weight:700; color:var(--primary); flex:1; }
.topbar-search {
  display:flex; align-items:center; gap:.5rem;
  background:var(--bg); border:1px solid var(--border);
  border-radius:8px; padding:.4rem .9rem; flex:1; max-width:280px;
}
.topbar-search input { border:none; background:transparent; outline:none; font-family:'Tajawal',sans-serif; font-size:.9rem; color:var(--text); width:100%; }
.topbar-search .si { color:var(--muted); font-size:1.1rem; }
.topbar-actions { display:flex; gap:.5rem; }
.btn-icon {
  width:36px; height:36px; border-radius:8px; border:1px solid var(--border);
  background:var(--card); cursor:pointer; display:flex; align-items:center; justify-content:center;
  color:var(--muted); font-size:1.1rem; transition:.15s; position:relative;
}
.btn-icon:hover { background:var(--bg); color:var(--primary); }
.notif-dot { position:absolute; top:6px; left:6px; width:8px; height:8px; border-radius:50%; background:#e74c3c; border:2px solid #fff; }

.content { padding:1.6rem 1.8rem; flex:1; }

/* ── PAGE SECTIONS ── */
.page { display:none; }
.page.active { display:block; }

/* ── STAT CARDS ── */
.stats-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.5rem; }
@media(max-width:900px){ .stats-grid { grid-template-columns:repeat(2,1fr); } }
.stat-card {
  background:var(--card); border-radius:12px; border:1px solid var(--border);
  padding:1.1rem 1.3rem; display:flex; flex-direction:column; gap:.3rem;
}
.stat-card .sc-label { font-size:.78rem; color:var(--muted); font-weight:500; }
.stat-card .sc-value { font-size:1.9rem; font-weight:700; color:var(--primary); line-height:1; }
.stat-card .sc-sub { font-size:.78rem; display:flex; align-items:center; gap:.3rem; }
.stat-card .sc-icon {
  width:38px; height:38px; border-radius:9px; display:flex; align-items:center;
  justify-content:center; font-size:1.2rem; align-self:flex-start; margin-bottom:.2rem;
}
.ic-blue  { background:var(--info-bg);    color:var(--info); }
.ic-green { background:var(--success-bg); color:var(--success); }
.ic-gold  { background:var(--accent-light); color:#92400e; }
.ic-red   { background:var(--danger-bg);  color:var(--danger); }
.up   { color:var(--success); }
.down { color:var(--danger); }

/* ── CARDS ── */
.card { background:var(--card); border-radius:12px; border:1px solid var(--border); padding:1.2rem 1.4rem; }
.card-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem; }
.card-title { font-size:1rem; font-weight:700; color:var(--primary); }

/* ── TABLE ── */
.tbl-wrap { overflow-x:auto; }
table { width:100%; border-collapse:collapse; font-size:.88rem; }
th { background:var(--bg); color:var(--muted); font-weight:500; padding:.6rem .9rem; text-align:right; font-size:.8rem; border-bottom:1px solid var(--border); }
td { padding:.7rem .9rem; border-bottom:1px solid var(--border); color:var(--text); vertical-align:middle; }
tr:last-child td { border-bottom:none; }
tr:hover td { background:#fafbfd; }
.badge {
  display:inline-block; padding:2px 10px; border-radius:20px; font-size:.78rem; font-weight:500;
}
.badge-green  { background:var(--success-bg); color:var(--success); }
.badge-red    { background:var(--danger-bg); color:var(--danger); }
.badge-amber  { background:var(--warning-bg); color:var(--warning); }
.badge-blue   { background:var(--info-bg); color:var(--info); }
.badge-gray   { background:#f1f5f9; color:#64748b; }

/* ── BTN ── */
.btn {
  display:inline-flex; align-items:center; gap:.4rem; padding:.5rem 1rem;
  border-radius:8px; border:1px solid var(--border); cursor:pointer;
  font-family:'Tajawal',sans-serif; font-size:.88rem; transition:.15s;
  background:var(--card); color:var(--text);
}
.btn:hover { background:var(--bg); }
.btn-primary { background:var(--primary); color:#fff; border-color:var(--primary); }
.btn-primary:hover { background:var(--primary-light); }
.btn-accent { background:var(--accent); color:#fff; border-color:var(--accent); }

/* ── GRID 2/3 ── */
.grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.grid-3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem; }
@media(max-width:850px){ .grid-2,.grid-3 { grid-template-columns:1fr; } }

/* ── PROGRESS BAR ── */
.prog-bar { background:var(--bg); border-radius:20px; height:7px; overflow:hidden; }
.prog-fill { height:100%; border-radius:20px; transition:width .4s; }

/* ── FORM ── */
.form-group { display:flex; flex-direction:column; gap:.35rem; margin-bottom:.9rem; }
.form-group label { font-size:.83rem; color:var(--muted); font-weight:500; }
.form-group input, .form-group select, .form-group textarea {
  border:1px solid var(--border); border-radius:8px; padding:.55rem .9rem;
  font-family:'Tajawal',sans-serif; font-size:.9rem; color:var(--text);
  outline:none; transition:.15s; background:var(--card);
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
  border-color:var(--primary-light); box-shadow:0 0 0 3px rgba(44,82,130,.1);
}

/* ── ATTENDANCE GRID ── */
.att-grid { display:grid; grid-template-columns:repeat(7,1fr); gap:5px; }
.att-day {
  aspect-ratio:1; border-radius:6px; display:flex; align-items:center;
  justify-content:center; font-size:.78rem; font-weight:500; cursor:default;
}
.att-p  { background:var(--success-bg); color:var(--success); }
.att-a  { background:var(--danger-bg);  color:var(--danger); }
.att-l  { background:var(--warning-bg); color:var(--warning); }
.att-off { background:var(--bg); color:var(--muted); }

/* ── DONUT PLACEHOLDER ── */
.donut-wrap { display:flex; align-items:center; gap:1.5rem; }
.donut-svg { flex-shrink:0; }
.donut-legend { display:flex; flex-direction:column; gap:.5rem; font-size:.85rem; }
.legend-item { display:flex; align-items:center; gap:.5rem; }
.legend-dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }

/* ── TIMELINE ── */
.timeline { display:flex; flex-direction:column; gap:.8rem; }
.tl-item { display:flex; gap:.9rem; align-items:flex-start; }
.tl-dot { width:10px; height:10px; border-radius:50%; margin-top:5px; flex-shrink:0; }
.tl-info h4 { font-size:.88rem; font-weight:500; }
.tl-info p  { font-size:.78rem; color:var(--muted); margin-top:.1rem; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:10px; }
</style>
</head>
<body>

<!-- ═══ SIDEBAR ═══ -->
<aside class="sidebar">
  <div class="sidebar-logo">
    <div class="logo-icon">🏫</div>
    <h2>نظام إدارة المدارس</h2>
    <span>لوحة التحكم الرئيسية</span>
  </div>

  <nav>
    <div class="nav-section">الرئيسية</div>
    <div class="nav-item active" onclick="showPage('dashboard',this)">
      <span class="icon">📊</span> لوحة التحكم
    </div>

    <div class="nav-section">إدارة الطلاب</div>
    <div class="nav-item" onclick="showPage('students',this)">
      <span class="icon">👨‍🎓</span> الطلاب
      <span class="badge">1240</span>
    </div>
    <div class="nav-item" onclick="showPage('attendance',this)">
      <span class="icon">📅</span> الحضور والغياب
    </div>

    <div class="nav-section">أكاديمي</div>
    <div class="nav-item" onclick="showPage('exams',this)">
      <span class="icon">📝</span> الامتحانات والدرجات
    </div>
    <div class="nav-item" onclick="showPage('classes',this)">
      <span class="icon">🏛️</span> الصفوف والمواد
    </div>
    <div class="nav-item" onclick="showPage('teachers',this)">
      <span class="icon">👩‍🏫</span> المدرسون
    </div>

    <div class="nav-section">مالي</div>
    <div class="nav-item" onclick="showPage('fees',this)">
      <span class="icon">💰</span> الأقساط والرسوم
      <span class="badge">12</span>
    </div>

    <div class="nav-section">تقارير</div>
    <div class="nav-item" onclick="showPage('reports',this)">
      <span class="icon">📈</span> التقارير والإحصائيات
    </div>

    <div class="nav-section">النظام</div>
    <div class="nav-item" onclick="showPage('settings',this)">
      <span class="icon">⚙️</span> الإعدادات
    </div>
  </nav>

  <div class="sidebar-footer">
    <div class="avatar">أم</div>
    <div class="info">
      <h4>أ. أحمد محمد</h4>
      <p>مدير المدرسة</p>
    </div>
  </div>
</aside>

<!-- ═══ MAIN ═══ -->
<div class="main">
  <div class="topbar">
    <div class="topbar-title" id="page-title">لوحة التحكم</div>
    <div class="topbar-search">
      <span class="si">🔍</span>
      <input type="text" placeholder="بحث عن طالب، صف، مدرس...">
    </div>
    <div class="topbar-actions">
      <div class="btn-icon" title="الإشعارات">🔔<span class="notif-dot"></span></div>
      <div class="btn-icon" title="الرسائل">✉️</div>
      <div class="btn-icon" title="ملء الشاشة">🖥️</div>
    </div>
  </div>

  <div class="content">

    <!-- ═══════════════ DASHBOARD ═══════════════ -->
    <div class="page active" id="page-dashboard">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="sc-icon ic-blue">👨‍🎓</div>
          <div class="sc-label">إجمالي الطلاب</div>
          <div class="sc-value">1,240</div>
          <div class="sc-sub up">↑ 3.2% عن الفصل الماضي</div>
        </div>
        <div class="stat-card">
          <div class="sc-icon ic-green">✅</div>
          <div class="sc-label">معدل الحضور اليومي</div>
          <div class="sc-value">92.4%</div>
          <div class="sc-sub up">↑ 1.1% عن الأسبوع الماضي</div>
        </div>
        <div class="stat-card">
          <div class="sc-icon ic-gold">💰</div>
          <div class="sc-label">الأقساط المحصلة</div>
          <div class="sc-value">87%</div>
          <div class="sc-sub">12 قسط متأخر</div>
        </div>
        <div class="stat-card">
          <div class="sc-icon ic-red">📝</div>
          <div class="sc-label">امتحانات هذا الشهر</div>
          <div class="sc-value">8</div>
          <div class="sc-sub">3 قادمة خلال أسبوع</div>
        </div>
      </div>

      <div class="grid-2" style="margin-bottom:1rem">
        <!-- Recent Students -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">آخر الطلاب المسجلين</div>
            <button class="btn" onclick="showPage('students',document.querySelector('[onclick*=students]'))">عرض الكل</button>
          </div>
          <div class="tbl-wrap">
            <table>
              <tr><th>الطالب</th><th>الصف</th><th>تاريخ التسجيل</th><th>الحالة</th></tr>
              <tr><td>علي حسن الموسوي</td><td>الخامس أ</td><td>2024/09/01</td><td><span class="badge badge-green">نشط</span></td></tr>
              <tr><td>زينب كريم</td><td>السادس ب</td><td>2024/09/02</td><td><span class="badge badge-green">نشط</span></td></tr>
              <tr><td>محمد جاسم</td><td>الرابع ج</td><td>2024/09/03</td><td><span class="badge badge-amber">معلق</span></td></tr>
              <tr><td>رنا طارق</td><td>الثالث أ</td><td>2024/09/04</td><td><span class="badge badge-green">نشط</span></td></tr>
              <tr><td>كرار علي</td><td>السادس أ</td><td>2024/09/05</td><td><span class="badge badge-green">نشط</span></td></tr>
            </table>
          </div>
        </div>

        <!-- Activity -->
        <div class="card">
          <div class="card-header"><div class="card-title">آخر النشاطات</div></div>
          <div class="timeline">
            <div class="tl-item"><div class="tl-dot" style="background:var(--success)"></div><div class="tl-info"><h4>تسجيل حضور الصف الخامس أ</h4><p>منذ 10 دقائق</p></div></div>
            <div class="tl-item"><div class="tl-dot" style="background:var(--info)"></div><div class="tl-info"><h4>إضافة درجات امتحان الرياضيات</h4><p>منذ 35 دقيقة</p></div></div>
            <div class="tl-item"><div class="tl-dot" style="background:var(--accent)"></div><div class="tl-info"><h4>تحصيل قسط: علي حسن - 150,000 د.ع</h4><p>منذ ساعة</p></div></div>
            <div class="tl-item"><div class="tl-dot" style="background:var(--danger)"></div><div class="tl-info"><h4>تنبيه: 3 طلاب غياب متكرر</h4><p>منذ ساعتين</p></div></div>
            <div class="tl-item"><div class="tl-dot" style="background:var(--primary)"></div><div class="tl-info"><h4>اجتماع أولياء الأمور — الأحد القادم</h4><p>منذ 3 ساعات</p></div></div>
          </div>
        </div>
      </div>

      <div class="grid-3">
        <div class="card">
          <div class="card-header"><div class="card-title">حضور اليوم بالصف</div></div>
          <div style="display:flex;flex-direction:column;gap:.7rem">
            <div><div style="display:flex;justify-content:space-between;font-size:.83rem;margin-bottom:4px"><span>الصف الخامس أ</span><span style="color:var(--success);font-weight:600">95%</span></div><div class="prog-bar"><div class="prog-fill" style="width:95%;background:var(--success)"></div></div></div>
            <div><div style="display:flex;justify-content:space-between;font-size:.83rem;margin-bottom:4px"><span>الصف السادس ب</span><span style="color:var(--success);font-weight:600">88%</span></div><div class="prog-bar"><div class="prog-fill" style="width:88%;background:var(--success)"></div></div></div>
            <div><div style="display:flex;justify-content:space-between;font-size:.83rem;margin-bottom:4px"><span>الصف الرابع ج</span><span style="color:var(--warning);font-weight:600">72%</span></div><div class="prog-bar"><div class="prog-fill" style="width:72%;background:var(--accent)"></div></div></div>
            <div><div style="display:flex;justify-content:space-between;font-size:.83rem;margin-bottom:4px"><span>الصف الثالث أ</span><span style="color:var(--danger);font-weight:600">61%</span></div><div class="prog-bar"><div class="prog-fill" style="width:61%;background:var(--danger)"></div></div></div>
          </div>
        </div>

        <div class="card">
          <div class="card-header"><div class="card-title">توزيع الطلاب</div></div>
          <div class="donut-wrap">
            <svg class="donut-svg" width="100" height="100" viewBox="0 0 36 36">
              <circle cx="18" cy="18" r="15.9" fill="none" stroke="#e2e8f0" stroke-width="3.8"/>
              <circle cx="18" cy="18" r="15.9" fill="none" stroke="#22863a" stroke-width="3.8" stroke-dasharray="58 42" stroke-dashoffset="25" stroke-linecap="round"/>
              <circle cx="18" cy="18" r="15.9" fill="none" stroke="#c9a84c" stroke-width="3.8" stroke-dasharray="26 74" stroke-dashoffset="-33" stroke-linecap="round"/>
              <circle cx="18" cy="18" r="15.9" fill="none" stroke="#e74c3c" stroke-width="3.8" stroke-dasharray="16 84" stroke-dashoffset="-59" stroke-linecap="round"/>
              <text x="18" y="19.5" text-anchor="middle" font-size="5.5" fill="#1a202c" font-weight="bold">1,240</text>
              <text x="18" y="24" text-anchor="middle" font-size="3.2" fill="#64748b">طالب</text>
            </svg>
            <div class="donut-legend">
              <div class="legend-item"><div class="legend-dot" style="background:#22863a"></div><span style="font-size:.8rem">ذكور <strong>718</strong></span></div>
              <div class="legend-item"><div class="legend-dot" style="background:#c9a84c"></div><span style="font-size:.8rem">إناث <strong>322</strong></span></div>
              <div class="legend-item"><div class="legend-dot" style="background:#e74c3c"></div><span style="font-size:.8rem">منتقلون <strong>200</strong></span></div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header"><div class="card-title">الأقساط المتأخرة</div></div>
          <div style="display:flex;flex-direction:column;gap:.7rem">
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:.85rem;padding-bottom:.5rem;border-bottom:1px solid var(--border)"><span>علي الكعبي</span><span class="badge badge-red">180,000 د.ع</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:.85rem;padding-bottom:.5rem;border-bottom:1px solid var(--border)"><span>سارة عبود</span><span class="badge badge-amber">120,000 د.ع</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:.85rem;padding-bottom:.5rem;border-bottom:1px solid var(--border)"><span>حيدر ناصر</span><span class="badge badge-red">220,000 د.ع</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:.85rem"><span>مريم حمد</span><span class="badge badge-amber">90,000 د.ع</span></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════ STUDENTS ═══════════════ -->
    <div class="page" id="page-students">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.2rem">
        <div style="display:flex;gap:.6rem">
          <select style="border:1px solid var(--border);border-radius:8px;padding:.45rem .8rem;font-family:'Tajawal',sans-serif;font-size:.88rem;background:var(--card);color:var(--text);outline:none">
            <option>كل الصفوف</option><option>الثالث</option><option>الرابع</option><option>الخامس</option><option>السادس</option>
          </select>
          <select style="border:1px solid var(--border);border-radius:8px;padding:.45rem .8rem;font-family:'Tajawal',sans-serif;font-size:.88rem;background:var(--card);color:var(--text);outline:none">
            <option>كل الحالات</option><option>نشط</option><option>معلق</option>
          </select>
        </div>
        <button class="btn btn-primary">+ إضافة طالب جديد</button>
      </div>
      <div class="card">
        <div class="tbl-wrap">
          <table>
            <tr><th>#</th><th>اسم الطالب</th><th>الصف</th><th>الجنس</th><th>ولي الأمر</th><th>رقم الهاتف</th><th>معدل الحضور</th><th>المعدل</th><th>الحالة</th><th>إجراءات</th></tr>
            <tr><td>1001</td><td><strong>علي حسن الموسوي</strong></td><td>الخامس أ</td><td>ذكر</td><td>حسن الموسوي</td><td>07701234567</td><td><span style="color:var(--success)">95%</span></td><td>88</td><td><span class="badge badge-green">نشط</span></td><td><button class="btn" style="padding:.3rem .7rem;font-size:.78rem">عرض</button></td></tr>
            <tr><td>1002</td><td><strong>زينب كريم علوان</strong></td><td>السادس ب</td><td>أنثى</td><td>كريم علوان</td><td>07709876543</td><td><span style="color:var(--success)">98%</span></td><td>94</td><td><span class="badge badge-green">نشط</span></td><td><button class="btn" style="padding:.3rem .7rem;font-size:.78rem">عرض</button></td></tr>
            <tr><td>1003</td><td><strong>محمد جاسم ناصر</strong></td><td>الرابع ج</td><td>ذكر</td><td>جاسم ناصر</td><td>07705551122</td><td><span style="color:var(--warning)">71%</span></td><td>63</td><td><span class="badge badge-amber">معلق</span></td><td><button class="btn" style="padding:.3rem .7rem;font-size:.78rem">عرض</button></td></tr>
            <tr><td>1004</td><td><strong>رنا طارق سعيد</strong></td><td>الثالث أ</td><td>أنثى</td><td>طارق سعيد</td><td>07703334455</td><td><span style="color:var(--success)">92%</span></td><td>81</td><td><span class="badge badge-green">نشط</span></td><td><button class="btn" style="padding:.3rem .7rem;font-size:.78rem">عرض</button></td></tr>
            <tr><td>1005</td><td><strong>كرار علي مهدي</strong></td><td>السادس أ</td><td>ذكر</td><td>علي مهدي</td><td>07706667788</td><td><span style="color:var(--success)">89%</span></td><td>77</td><td><span class="badge badge-green">نشط</span></td><td><button class="btn" style="padding:.3rem .7rem;font-size:.78rem">عرض</button></td></tr>
            <tr><td>1006</td><td><strong>نور عباس الحسيني</strong></td><td>الخامس ب</td><td>أنثى</td><td>عباس الحسيني</td><td>07708889900</td><td><span style="color:var(--danger)">58%</span></td><td>52</td><td><span class="badge badge-red">موقف</span></td><td><button class="btn" style="padding:.3rem .7rem;font-size:.78rem">عرض</button></td></tr>
          </table>
        </div>
      </div>
    </div>

    <!-- ═══════════════ ATTENDANCE ═══════════════ -->
    <div class="page" id="page-attendance">
      <div class="grid-2" style="margin-bottom:1rem">
        <div class="card">
          <div class="card-header"><div class="card-title">تسجيل الحضور — اليوم</div></div>
          <div class="form-group"><label>اختر الصف</label>
            <select><option>الخامس أ (30 طالب)</option><option>السادس ب</option><option>الرابع ج</option></select>
          </div>
          <div class="form-group"><label>المادة / الحصة</label>
            <select><option>الرياضيات</option><option>اللغة العربية</option><option>العلوم</option></select>
          </div>
          <div class="tbl-wrap">
            <table>
              <tr><th>الطالب</th><th>حاضر</th><th>غائب</th><th>متأخر</th></tr>
              <tr><td>علي حسن</td><td><input type="radio" name="s1" checked></td><td><input type="radio" name="s1"></td><td><input type="radio" name="s1"></td></tr>
              <tr><td>زينب كريم</td><td><input type="radio" name="s2" checked></td><td><input type="radio" name="s2"></td><td><input type="radio" name="s2"></td></tr>
              <tr><td>محمد جاسم</td><td><input type="radio" name="s3"></td><td><input type="radio" name="s3" checked></td><td><input type="radio" name="s3"></td></tr>
              <tr><td>رنا طارق</td><td><input type="radio" name="s4" checked></td><td><input type="radio" name="s4"></td><td><input type="radio" name="s4"></td></tr>
              <tr><td>كرار علي</td><td><input type="radio" name="s5"></td><td><input type="radio" name="s5"></td><td><input type="radio" name="s5" checked></td></tr>
            </table>
          </div>
          <div style="margin-top:1rem"><button class="btn btn-primary" style="width:100%">💾 حفظ السجل</button></div>
        </div>
        <div class="card">
          <div class="card-header"><div class="card-title">سجل الحضور — مايو 2025</div></div>
          <div style="display:flex;gap:.5rem;margin-bottom:.8rem;font-size:.8rem">
            <span class="badge badge-green">ح حاضر</span>
            <span class="badge badge-red">غ غائب</span>
            <span class="badge badge-amber">ت متأخر</span>
            <span class="badge badge-gray">إج إجازة</span>
          </div>
          <div class="att-grid">
            <div class="att-day att-off">س</div><div class="att-day att-off">أ</div><div class="att-day att-off">ث</div><div class="att-day att-off">ر</div><div class="att-day att-off">خ</div><div class="att-day att-off">ج</div><div class="att-day att-off">س</div>
            <div class="att-day att-p">ح</div><div class="att-day att-p">ح</div><div class="att-day att-p">ح</div><div class="att-day att-p">ح</div><div class="att-day att-p">ح</div><div class="att-day att-off">إج</div><div class="att-day att-off">إج</div>
            <div class="att-day att-p">ح</div><div class="att-day att-a">غ</div><div class="att-day att-p">ح</div><div class="att-day att-p">ح</div><div class="att-day att-l">ت</div><div class="att-day att-off">إج</div><div class="att-day att-off">إج</div>
            <div class="att-day att-p">ح</div><div class="att-day att-p">ح</div><div class="att-day att-p">ح</div><div class="att-day att-a">غ</div><div class="att-day att-p">ح</div><div class="att-day att-off">إج</div><div class="att-day att-off">إج</div>
            <div class="att-day att-p">ح</div><div class="att-day att-p">ح</div><div class="att-day att-l">ت</div><div class="att-day att-p">ح</div><div class="att-day att-p">ح</div>
          </div>
          <div style="margin-top:1rem;display:flex;gap:1rem;font-size:.85rem">
            <span>✅ حاضر: <strong>18</strong></span>
            <span>❌ غائب: <strong>2</strong></span>
            <span>⏰ متأخر: <strong>2</strong></span>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════ EXAMS ═══════════════ -->
    <div class="page" id="page-exams">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.2rem">
        <div style="display:flex;gap:.6rem">
          <select style="border:1px solid var(--border);border-radius:8px;padding:.45rem .8rem;font-family:'Tajawal',sans-serif;font-size:.88rem;background:var(--card);color:var(--text);outline:none"><option>الفصل الدراسي الثاني</option><option>الفصل الأول</option></select>
        </div>
        <button class="btn btn-primary">+ إضافة امتحان</button>
      </div>
      <div class="card" style="margin-bottom:1rem">
        <div class="card-header"><div class="card-title">الامتحانات القادمة</div></div>
        <div class="tbl-wrap">
          <table>
            <tr><th>المادة</th><th>الصف</th><th>التاريخ</th><th>الوقت</th><th>القاعة</th><th>عدد الطلاب</th><th>الحالة</th></tr>
            <tr><td><strong>الرياضيات</strong></td><td>السادس أ+ب</td><td>2025/05/15</td><td>9:00 ص</td><td>قاعة A</td><td>55</td><td><span class="badge badge-blue">قادم</span></td></tr>
            <tr><td><strong>اللغة العربية</strong></td><td>الخامس أ</td><td>2025/05/17</td><td>10:00 ص</td><td>قاعة B</td><td>30</td><td><span class="badge badge-blue">قادم</span></td></tr>
            <tr><td><strong>العلوم</strong></td><td>الرابع ج</td><td>2025/05/20</td><td>9:00 ص</td><td>قاعة A</td><td>28</td><td><span class="badge badge-blue">قادم</span></td></tr>
            <tr><td><strong>التاريخ</strong></td><td>السادس ب</td><td>2025/05/05</td><td>11:00 ص</td><td>قاعة C</td><td>27</td><td><span class="badge badge-green">اكتمل</span></td></tr>
          </table>
        </div>
      </div>
      <div class="card">
        <div class="card-header"><div class="card-title">إدخال الدرجات — رياضيات السادس أ</div></div>
        <div class="tbl-wrap">
          <table>
            <tr><th>الطالب</th><th>درجة النظري /50</th><th>درجة العملي /30</th><th>الواجبات /20</th><th>المجموع /100</th><th>التقدير</th></tr>
            <tr><td>علي حسن</td><td><input type="number" max="50" value="44" style="width:70px;border:1px solid var(--border);border-radius:6px;padding:.3rem .5rem;font-family:'Tajawal',sans-serif;text-align:center"></td><td><input type="number" max="30" value="27" style="width:70px;border:1px solid var(--border);border-radius:6px;padding:.3rem .5rem;font-family:'Tajawal',sans-serif;text-align:center"></td><td><input type="number" max="20" value="18" style="width:70px;border:1px solid var(--border);border-radius:6px;padding:.3rem .5rem;font-family:'Tajawal',sans-serif;text-align:center"></td><td><strong>89</strong></td><td><span class="badge badge-green">A</span></td></tr>
            <tr><td>زينب كريم</td><td><input type="number" max="50" value="48" style="width:70px;border:1px solid var(--border);border-radius:6px;padding:.3rem .5rem;font-family:'Tajawal',sans-serif;text-align:center"></td><td><input type="number" max="30" value="29" style="width:70px;border:1px solid var(--border);border-radius:6px;padding:.3rem .5rem;font-family:'Tajawal',sans-serif;text-align:center"></td><td><input type="number" max="20" value="20" style="width:70px;border:1px solid var(--border);border-radius:6px;padding:.3rem .5rem;font-family:'Tajawal',sans-serif;text-align:center"></td><td><strong>97</strong></td><td><span class="badge badge-green">A+</span></td></tr>
            <tr><td>محمد جاسم</td><td><input type="number" max="50" value="31" style="width:70px;border:1px solid var(--border);border-radius:6px;padding:.3rem .5rem;font-family:'Tajawal',sans-serif;text-align:center"></td><td><input type="number" max="30" value="18" style="width:70px;border:1px solid var(--border);border-radius:6px;padding:.3rem .5rem;font-family:'Tajawal',sans-serif;text-align:center"></td><td><input type="number" max="20" value="12" style="width:70px;border:1px solid var(--border);border-radius:6px;padding:.3rem .5rem;font-family:'Tajawal',sans-serif;text-align:center"></td><td><strong>61</strong></td><td><span class="badge badge-amber">C</span></td></tr>
          </table>
        </div>
        <div style="margin-top:1rem;display:flex;gap:.6rem"><button class="btn btn-primary">💾 حفظ الدرجات</button><button class="btn">📤 تصدير PDF</button></div>
      </div>
    </div>

    <!-- ═══════════════ FEES ═══════════════ -->
    <div class="page" id="page-fees">
      <div class="stats-grid" style="grid-template-columns:repeat(3,1fr)">
        <div class="stat-card"><div class="sc-icon ic-green">💵</div><div class="sc-label">إجمالي المحصل</div><div class="sc-value">87.2M</div><div class="sc-sub up">د.ع هذا الفصل</div></div>
        <div class="stat-card"><div class="sc-icon ic-red">⏳</div><div class="sc-label">المتأخرات</div><div class="sc-value">12.4M</div><div class="sc-sub down">12 طالب</div></div>
        <div class="stat-card"><div class="sc-icon ic-gold">📊</div><div class="sc-label">نسبة التحصيل</div><div class="sc-value">87%</div><div class="sc-sub">من الإجمالي المستهدف</div></div>
      </div>
      <div class="grid-2">
        <div class="card">
          <div class="card-header"><div class="card-title">سجل المدفوعات</div></div>
          <div class="tbl-wrap">
            <table>
              <tr><th>الطالب</th><th>الصف</th><th>المبلغ</th><th>نوع الدفع</th><th>التاريخ</th><th>الحالة</th></tr>
              <tr><td>علي حسن</td><td>الخامس أ</td><td>150,000</td><td>نقدي</td><td>2025/05/01</td><td><span class="badge badge-green">مدفوع</span></td></tr>
              <tr><td>زينب كريم</td><td>السادس ب</td><td>150,000</td><td>بطاقة</td><td>2025/05/02</td><td><span class="badge badge-green">مدفوع</span></td></tr>
              <tr><td>علي الكعبي</td><td>الرابع أ</td><td>180,000</td><td>—</td><td>2025/04/01</td><td><span class="badge badge-red">متأخر</span></td></tr>
              <tr><td>سارة عبود</td><td>الثالث ب</td><td>120,000</td><td>—</td><td>2025/04/01</td><td><span class="badge badge-red">متأخر</span></td></tr>
              <tr><td>كرار علي</td><td>السادس أ</td><td>150,000</td><td>تحويل</td><td>2025/05/05</td><td><span class="badge badge-green">مدفوع</span></td></tr>
            </table>
          </div>
        </div>
        <div class="card">
          <div class="card-header"><div class="card-title">تسجيل دفعة جديدة</div></div>
          <div class="form-group"><label>اسم الطالب</label><input type="text" placeholder="ابحث عن الطالب..."></div>
          <div class="form-group"><label>نوع القسط</label><select><option>القسط الفصلي</option><option>رسوم الأنشطة</option><option>رسوم المواصلات</option><option>رسوم المكتبة</option></select></div>
          <div class="form-group"><label>المبلغ (د.ع)</label><input type="number" placeholder="150,000"></div>
          <div class="form-group"><label>طريقة الدفع</label><select><option>نقدي</option><option>بطاقة بنكية</option><option>تحويل إلكتروني</option></select></div>
          <div class="form-group"><label>ملاحظات</label><textarea rows="2" placeholder="ملاحظات اختيارية..."></textarea></div>
          <div style="display:flex;gap:.6rem"><button class="btn btn-primary" style="flex:1">✅ تسجيل الدفعة</button><button class="btn">🖨️ طباعة وصل</button></div>
        </div>
      </div>
    </div>

    <!-- ═══════════════ REPORTS ═══════════════ -->
    <div class="page" id="page-reports">
      <div class="grid-3" style="margin-bottom:1rem">
        <div class="card" style="text-align:center;cursor:pointer" onclick="alert('جاري إنشاء التقرير...')">
          <div style="font-size:2.5rem;margin-bottom:.5rem">📊</div>
          <div style="font-weight:600;color:var(--primary)">تقرير الحضور الشهري</div>
          <div style="font-size:.82rem;color:var(--muted);margin:.3rem 0 .8rem">إحصائيات الحضور لكل صف</div>
          <button class="btn btn-primary" style="width:100%">📥 تحميل</button>
        </div>
        <div class="card" style="text-align:center;cursor:pointer">
          <div style="font-size:2.5rem;margin-bottom:.5rem">📝</div>
          <div style="font-weight:600;color:var(--primary)">تقرير الدرجات</div>
          <div style="font-size:.82rem;color:var(--muted);margin:.3rem 0 .8rem">نتائج الامتحانات والتقديرات</div>
          <button class="btn btn-primary" style="width:100%">📥 تحميل</button>
        </div>
        <div class="card" style="text-align:center;cursor:pointer">
          <div style="font-size:2.5rem;margin-bottom:.5rem">💰</div>
          <div style="font-weight:600;color:var(--primary)">تقرير الأقساط</div>
          <div style="font-size:.82rem;color:var(--muted);margin:.3rem 0 .8rem">المحصل والمتأخرات المالية</div>
          <button class="btn btn-primary" style="width:100%">📥 تحميل</button>
        </div>
        <div class="card" style="text-align:center;cursor:pointer">
          <div style="font-size:2.5rem;margin-bottom:.5rem">👩‍🏫</div>
          <div style="font-weight:600;color:var(--primary)">تقرير المدرسين</div>
          <div style="font-size:.82rem;color:var(--muted);margin:.3rem 0 .8rem">أداء وحضور الكادر التدريسي</div>
          <button class="btn btn-primary" style="width:100%">📥 تحميل</button>
        </div>
        <div class="card" style="text-align:center;cursor:pointer">
          <div style="font-size:2.5rem;margin-bottom:.5rem">🏆</div>
          <div style="font-weight:600;color:var(--primary)">تقرير المتفوقين</div>
          <div style="font-size:.82rem;color:var(--muted);margin:.3rem 0 .8rem">قائمة الطلاب المتميزين</div>
          <button class="btn btn-primary" style="width:100%">📥 تحميل</button>
        </div>
        <div class="card" style="text-align:center;cursor:pointer">
          <div style="font-size:2.5rem;margin-bottom:.5rem">📋</div>
          <div style="font-weight:600;color:var(--primary)">التقرير الشامل</div>
          <div style="font-size:.82rem;color:var(--muted);margin:.3rem 0 .8rem">تقرير كامل لنهاية الفصل</div>
          <button class="btn btn-accent" style="width:100%">🌟 تحميل</button>
        </div>
      </div>
    </div>

    <!-- ═══════════════ SETTINGS ═══════════════ -->
    <div class="page" id="page-settings">
      <div class="grid-2">
        <div class="card">
          <div class="card-header"><div class="card-title">🏫 معلومات المدرسة</div></div>
          <div class="form-group"><label>اسم المدرسة</label><input type="text" value="مدرسة النخيل الابتدائية"></div>
          <div class="form-group"><label>رقم المدرسة الوطني</label><input type="text" value="IQ-BAS-0042"></div>
          <div class="form-group"><label>العنوان</label><input type="text" value="البصرة، حي الجمهورية"></div>
          <div class="form-group"><label>رقم الهاتف</label><input type="text" value="07701234567"></div>
          <div class="form-group"><label>البريد الإلكتروني</label><input type="text" value="info@school.edu.iq"></div>
          <button class="btn btn-primary">💾 حفظ التغييرات</button>
        </div>
        <div class="card">
          <div class="card-header"><div class="card-title">📅 إعدادات الفصل الدراسي</div></div>
          <div class="form-group"><label>العام الدراسي الحالي</label><select><option>2024 / 2025</option><option>2023 / 2024</option></select></div>
          <div class="form-group"><label>الفصل الدراسي</label><select><option>الفصل الثاني</option><option>الفصل الأول</option></select></div>
          <div class="form-group"><label>تاريخ بدء الفصل</label><input type="date" value="2025-01-05"></div>
          <div class="form-group"><label>تاريخ انتهاء الفصل</label><input type="date" value="2025-05-31"></div>
          <div class="form-group"><label>درجة النجاح (%)</label><input type="number" value="50"></div>
          <button class="btn btn-primary">💾 حفظ التغييرات</button>
        </div>
        <div class="card">
          <div class="card-header"><div class="card-title">🔐 إدارة المستخدمين</div></div>
          <div class="tbl-wrap">
            <table>
              <tr><th>المستخدم</th><th>الدور</th><th>الحالة</th><th>آخر دخول</th></tr>
              <tr><td>أحمد محمد</td><td><span class="badge badge-blue">مدير</span></td><td><span class="badge badge-green">نشط</span></td><td>اليوم 8:00 ص</td></tr>
              <tr><td>فاطمة عبدالله</td><td><span class="badge badge-gray">سكرتيرة</span></td><td><span class="badge badge-green">نشط</span></td><td>اليوم 7:45 ص</td></tr>
              <tr><td>علاء الدين</td><td><span class="badge badge-gray">محاسب</span></td><td><span class="badge badge-green">نشط</span></td><td>أمس</td></tr>
            </table>
          </div>
          <div style="margin-top:.8rem"><button class="btn btn-primary">+ إضافة مستخدم</button></div>
        </div>
        <div class="card">
          <div class="card-header"><div class="card-title">🔔 إعدادات الإشعارات</div></div>
          <div style="display:flex;flex-direction:column;gap:.9rem">
            <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:.8rem;border-bottom:1px solid var(--border)">
              <div><div style="font-weight:500;font-size:.9rem">إشعار الغياب اليومي</div><div style="font-size:.78rem;color:var(--muted)">إرسال تقرير الغياب لولي الأمر</div></div>
              <label style="cursor:pointer"><input type="checkbox" checked> مفعّل</label>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:.8rem;border-bottom:1px solid var(--border)">
              <div><div style="font-weight:500;font-size:.9rem">تذكير الأقساط</div><div style="font-size:.78rem;color:var(--muted)">إشعار الأقساط المتأخرة</div></div>
              <label style="cursor:pointer"><input type="checkbox" checked> مفعّل</label>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <div><div style="font-weight:500;font-size:.9rem">نتائج الامتحانات</div><div style="font-size:.78rem;color:var(--muted)">إرسال النتائج لأولياء الأمور</div></div>
              <label style="cursor:pointer"><input type="checkbox"> مفعّل</label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════ CLASSES ═══════════════ -->
    <div class="page" id="page-classes">
      <div class="grid-3">
        <div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem"><div style="font-weight:700;font-size:1.1rem;color:var(--primary)">الصف الثالث أ</div><span class="badge badge-green">نشط</span></div><div style="font-size:.85rem;color:var(--muted);margin-bottom:.4rem">المشرفة: أ. نور الهاشمي</div><div style="font-size:.85rem;margin-bottom:.8rem">👨‍🎓 28 طالب | 🚪 قاعة 12</div><div class="prog-bar" style="margin-bottom:.4rem"><div class="prog-fill" style="width:94%;background:var(--success)"></div></div><div style="font-size:.78rem;color:var(--muted)">حضور اليوم: 94%</div></div>
        <div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem"><div style="font-weight:700;font-size:1.1rem;color:var(--primary)">الصف الرابع ب</div><span class="badge badge-green">نشط</span></div><div style="font-size:.85rem;color:var(--muted);margin-bottom:.4rem">المشرف: أ. حيدر السعدي</div><div style="font-size:.85rem;margin-bottom:.8rem">👨‍🎓 32 طالب | 🚪 قاعة 8</div><div class="prog-bar" style="margin-bottom:.4rem"><div class="prog-fill" style="width:81%;background:var(--accent)"></div></div><div style="font-size:.78rem;color:var(--muted)">حضور اليوم: 81%</div></div>
        <div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem"><div style="font-weight:700;font-size:1.1rem;color:var(--primary)">الصف الخامس أ</div><span class="badge badge-green">نشط</span></div><div style="font-size:.85rem;color:var(--muted);margin-bottom:.4rem">المشرفة: أ. ميسون علي</div><div style="font-size:.85rem;margin-bottom:.8rem">👨‍🎓 30 طالب | 🚪 قاعة 5</div><div class="prog-bar" style="margin-bottom:.4rem"><div class="prog-fill" style="width:95%;background:var(--success)"></div></div><div style="font-size:.78rem;color:var(--muted)">حضور اليوم: 95%</div></div>
        <div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem"><div style="font-weight:700;font-size:1.1rem;color:var(--primary)">الصف السادس أ</div><span class="badge badge-green">نشط</span></div><div style="font-size:.85rem;color:var(--muted);margin-bottom:.4rem">المشرف: أ. علاء الدين</div><div style="font-size:.85rem;margin-bottom:.8rem">👨‍🎓 27 طالب | 🚪 قاعة 2</div><div class="prog-bar" style="margin-bottom:.4rem"><div class="prog-fill" style="width:89%;background:var(--success)"></div></div><div style="font-size:.78rem;color:var(--muted)">حضور اليوم: 89%</div></div>
        <div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem"><div style="font-weight:700;font-size:1.1rem;color:var(--primary)">الصف السادس ب</div><span class="badge badge-green">نشط</span></div><div style="font-size:.85rem;color:var(--muted);margin-bottom:.4rem">المشرفة: أ. رواء محمد</div><div style="font-size:.85rem;margin-bottom:.8rem">👨‍🎓 29 طالب | 🚪 قاعة 3</div><div class="prog-bar" style="margin-bottom:.4rem"><div class="prog-fill" style="width:72%;background:var(--accent)"></div></div><div style="font-size:.78rem;color:var(--muted)">حضور اليوم: 72%</div></div>
        <div class="card" style="border:2px dashed var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:140px;cursor:pointer" onclick="alert('إضافة صف جديد')"><div style="font-size:2rem;margin-bottom:.5rem;color:var(--muted)">+</div><div style="color:var(--muted);font-size:.9rem">إضافة صف جديد</div></div>
      </div>
    </div>

    <!-- ═══════════════ TEACHERS ═══════════════ -->
    <div class="page" id="page-teachers">
      <div style="display:flex;justify-content:flex-end;margin-bottom:1.2rem"><button class="btn btn-primary">+ إضافة مدرس</button></div>
      <div class="card">
        <div class="tbl-wrap">
          <table>
            <tr><th>المدرس</th><th>التخصص</th><th>الصفوف</th><th>حصص/أسبوع</th><th>معدل الحضور</th><th>الحالة</th></tr>
            <tr><td><div style="display:flex;align-items:center;gap:.6rem"><div class="avatar" style="width:30px;height:30px;font-size:.75rem">نه</div>نور الهاشمي</div></td><td>رياضيات</td><td>الثالث أ، الرابع ب</td><td>24</td><td><span style="color:var(--success)">98%</span></td><td><span class="badge badge-green">نشط</span></td></tr>
            <tr><td><div style="display:flex;align-items:center;gap:.6rem"><div class="avatar" style="width:30px;height:30px;font-size:.75rem">حس</div>حيدر السعدي</div></td><td>لغة عربية</td><td>السادس أ، السادس ب</td><td>20</td><td><span style="color:var(--success)">95%</span></td><td><span class="badge badge-green">نشط</span></td></tr>
            <tr><td><div style="display:flex;align-items:center;gap:.6rem"><div class="avatar" style="width:30px;height:30px;font-size:.75rem">مع</div>ميسون علي</div></td><td>علوم</td><td>الخامس أ، الخامس ب</td><td>18</td><td><span style="color:var(--warning)">79%</span></td><td><span class="badge badge-amber">إجازة</span></td></tr>
            <tr><td><div style="display:flex;align-items:center;gap:.6rem"><div class="avatar" style="width:30px;height:30px;font-size:.75rem">رم</div>رواء محمد</div></td><td>تاريخ وجغرافيا</td><td>السادس ب، الرابع ج</td><td>22</td><td><span style="color:var(--success)">92%</span></td><td><span class="badge badge-green">نشط</span></td></tr>
          </table>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
const titles = {
  dashboard:'لوحة التحكم', students:'الطلاب', attendance:'الحضور والغياب',
  exams:'الامتحانات والدرجات', classes:'الصفوف والمواد', teachers:'المدرسون',
  fees:'الأقساط والرسوم', reports:'التقارير', settings:'الإعدادات'
};
function showPage(id, el){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  document.getElementById('page-'+id).classList.add('active');
  el.classList.add('active');
  document.getElementById('page-title').textContent = titles[id]||id;
  window.scrollTo({top:0,behavior:'smooth'});
}
</script>
</body>
</html>"""