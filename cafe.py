import http.server
import socketserver
import webbrowser
import threading
import os

HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>كافيه النخيل</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&family=Lateef:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --sand: #f2e8d5;
    --gold: #c9a84c;
    --brown: #5c3d1e;
    --date: #8b4513;
    --palm: #2d5a27;
    --cream: #fdf6e3;
    --dark: #1a0f00;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--cream);
    color: var(--dark);
    font-family: 'Tajawal', sans-serif;
    overflow-x: hidden;
  }

  /* ===== HERO ===== */
  .hero {
    position: relative;
    min-height: 100vh;
    background: linear-gradient(160deg, #1a2e0a 0%, #2d5a27 40%, #8b6914 80%, #5c3d1e 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  /* Stars / noise overlay */
  .hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
  }

  /* Sun glow */
  .sun {
    position: absolute;
    bottom: -80px;
    left: 50%;
    transform: translateX(-50%);
    width: 320px;
    height: 320px;
    border-radius: 50%;
    background: radial-gradient(circle, #f9d423 0%, #c9a84c 40%, transparent 75%);
    opacity: 0.35;
    filter: blur(18px);
    animation: pulse 4s ease-in-out infinite;
  }

  @keyframes pulse {
    0%,100% { transform: translateX(-50%) scale(1); opacity: .35; }
    50%      { transform: translateX(-50%) scale(1.08); opacity: .5; }
  }

  /* ---- Palm trees ---- */
  .palms {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }

  .palm {
    position: absolute;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .trunk {
    width: 18px;
    border-radius: 9px;
    background: linear-gradient(to right, #4a2c0a, #7a4f20, #4a2c0a);
    transform-origin: bottom center;
    animation: sway 5s ease-in-out infinite;
  }

  .fronds {
    position: relative;
    animation: sway 5s ease-in-out infinite;
  }

  .frond {
    position: absolute;
    width: 90px;
    height: 14px;
    background: linear-gradient(90deg, #2d5a27, #4a8c3f, #1a3a15);
    border-radius: 50% 90% 50% 0;
    transform-origin: left center;
  }

  @keyframes sway {
    0%,100% { transform: rotate(0deg); }
    25%      { transform: rotate(2deg); }
    75%      { transform: rotate(-2deg); }
  }

  /* Left palm */
  .palm-left  { left: 3%;  }
  .palm-right { right: 3%; }
  .palm-mid-l { left: 15%; }
  .palm-mid-r { right: 15%; }

  /* ---- Logo / Title ---- */
  .brand {
    position: relative;
    z-index: 10;
    text-align: center;
    padding: 2rem;
  }

  .brand-icon {
    font-size: 4rem;
    display: block;
    margin-bottom: .5rem;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,.5));
    animation: floatIcon 3s ease-in-out infinite;
  }

  @keyframes floatIcon {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-10px); }
  }

  .brand h1 {
    font-family: 'Lateef', serif;
    font-size: clamp(3rem, 8vw, 6rem);
    color: var(--gold);
    text-shadow: 0 2px 20px rgba(0,0,0,.6);
    letter-spacing: .05em;
    line-height: 1;
  }

  .brand p {
    font-size: 1.2rem;
    color: rgba(255,255,255,.75);
    margin-top: .5rem;
    font-weight: 300;
  }

  .scroll-hint {
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    color: rgba(255,255,255,.5);
    font-size: .85rem;
    animation: bounce 2s ease infinite;
    z-index: 10;
  }

  @keyframes bounce {
    0%,100% { transform: translateX(-50%) translateY(0); }
    50%      { transform: translateX(-50%) translateY(8px); }
  }

  /* ===== SECTIONS ===== */
  section { padding: 5rem 2rem; max-width: 1100px; margin: 0 auto; }

  .section-title {
    font-family: 'Lateef', serif;
    font-size: 2.8rem;
    color: var(--brown);
    text-align: center;
    margin-bottom: .3rem;
  }

  .divider {
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--palm));
    margin: .5rem auto 3rem;
    border-radius: 2px;
  }

  /* ===== MENU GRID ===== */
  .menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
  }

  .card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 6px 30px rgba(92,61,30,.12);
    transition: transform .3s, box-shadow .3s;
    cursor: default;
  }

  .card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(92,61,30,.2);
  }

  .card-img {
    height: 160px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 5rem;
    background: linear-gradient(135deg, var(--sand), #e8d5b0);
  }

  .card-body { padding: 1.2rem 1.4rem 1.5rem; }

  .card-body h3 {
    font-size: 1.25rem;
    color: var(--brown);
    font-weight: 700;
  }

  .card-body p {
    font-size: .9rem;
    color: #7a6550;
    margin: .4rem 0 .8rem;
    line-height: 1.6;
  }

  .price {
    display: inline-block;
    background: linear-gradient(135deg, var(--gold), #e8b84b);
    color: white;
    padding: .3rem .9rem;
    border-radius: 30px;
    font-weight: 700;
    font-size: .9rem;
  }

  /* ===== ABOUT ===== */
  .about-wrap {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
  }

  @media(max-width:700px){ .about-wrap { grid-template-columns: 1fr; gap: 2rem; } }

  .about-art {
    height: 340px;
    border-radius: 24px;
    background: linear-gradient(135deg, #2d5a27 0%, #4a8c3f 50%, #c9a84c 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 9rem;
    box-shadow: 0 12px 40px rgba(45,90,39,.3);
  }

  .about-text h2 {
    font-family: 'Lateef', serif;
    font-size: 2.2rem;
    color: var(--brown);
    margin-bottom: 1rem;
  }

  .about-text p {
    font-size: 1.05rem;
    color: #5c4030;
    line-height: 2;
  }

  /* ===== HOURS ===== */
  .hours-bg {
    background: linear-gradient(135deg, #1a2e0a, #2d5a27);
    color: white;
    border-radius: 28px;
    padding: 3rem 2rem;
    text-align: center;
  }

  .hours-bg .section-title { color: var(--gold); }
  .hours-bg .divider { background: linear-gradient(90deg, var(--gold), #fff); }

  .hours-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
  }

  .hour-item {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(201,168,76,.3);
    border-radius: 16px;
    padding: 1.2rem;
  }

  .hour-item .day { font-size: .85rem; color: rgba(255,255,255,.6); }
  .hour-item .time { font-size: 1.2rem; font-weight: 700; color: var(--gold); margin-top: .3rem; }

  /* ===== FOOTER ===== */
  footer {
    background: var(--dark);
    color: rgba(255,255,255,.5);
    text-align: center;
    padding: 2rem;
    font-size: .9rem;
  }

  footer span { color: var(--gold); }
</style>
</head>
<body>

<!-- ========= HERO ========= -->
<div class="hero">
  <div class="sun"></div>

  <!-- Palm Trees -->
  <div class="palms">
    <!-- Left big -->
    <div class="palm palm-left" style="left:2%">
      <div class="fronds" style="position:relative;width:10px;height:80px">
        <div class="frond" style="transform:rotate(-40deg);top:0;right:-30px;width:110px"></div>
        <div class="frond" style="transform:rotate(-15deg);top:10px;right:-20px;width:100px;opacity:.9"></div>
        <div class="frond" style="transform:rotate(10deg);top:15px;right:-10px;width:90px;opacity:.8"></div>
        <div class="frond" style="transform:rotate(30deg);top:20px;right:0px;width:85px;opacity:.7"></div>
        <div class="frond" style="transform:rotate(55deg);top:25px;right:5px;width:75px;opacity:.6"></div>
        <div class="frond" style="transform:rotate(-65deg);top:5px;right:-35px;width:80px;opacity:.7"></div>
      </div>
      <div class="trunk" style="height:220px;animation-delay:.4s"></div>
    </div>

    <!-- Right big -->
    <div class="palm palm-right" style="right:2%">
      <div class="fronds" style="position:relative;width:10px;height:80px;animation-delay:.8s">
        <div class="frond" style="transform:rotate(-40deg) scaleX(-1);top:0;left:-30px;width:110px"></div>
        <div class="frond" style="transform:rotate(-15deg) scaleX(-1);top:10px;left:-20px;width:100px;opacity:.9"></div>
        <div class="frond" style="transform:rotate(10deg) scaleX(-1);top:15px;left:-10px;width:90px;opacity:.8"></div>
        <div class="frond" style="transform:rotate(30deg) scaleX(-1);top:20px;left:0px;width:85px;opacity:.7"></div>
        <div class="frond" style="transform:rotate(55deg) scaleX(-1);top:25px;left:5px;width:75px;opacity:.6"></div>
      </div>
      <div class="trunk" style="height:200px;animation-delay:.2s"></div>
    </div>

    <!-- Mid left -->
    <div class="palm palm-mid-l" style="left:12%">
      <div class="fronds" style="position:relative;width:10px;height:60px;animation-delay:1s">
        <div class="frond" style="transform:rotate(-35deg);top:0;right:-25px;width:80px"></div>
        <div class="frond" style="transform:rotate(10deg);top:15px;right:-10px;width:70px;opacity:.85"></div>
        <div class="frond" style="transform:rotate(45deg);top:20px;right:0;width:65px;opacity:.7"></div>
        <div class="frond" style="transform:rotate(-60deg);top:5px;right:-30px;width:60px;opacity:.7"></div>
      </div>
      <div class="trunk" style="height:150px;animation-delay:.6s"></div>
    </div>

    <!-- Mid right -->
    <div class="palm palm-mid-r" style="right:12%">
      <div class="fronds" style="position:relative;width:10px;height:60px;animation-delay:1.5s">
        <div class="frond" style="transform:rotate(-35deg) scaleX(-1);top:0;left:-25px;width:80px"></div>
        <div class="frond" style="transform:rotate(10deg) scaleX(-1);top:15px;left:-10px;width:70px;opacity:.85"></div>
        <div class="frond" style="transform:rotate(45deg) scaleX(-1);top:20px;left:0;width:65px;opacity:.7"></div>
      </div>
      <div class="trunk" style="height:170px;animation-delay:1s"></div>
    </div>
  </div>

  <!-- Brand -->
  <div class="brand">
    <span class="brand-icon">🌴</span>
    <h1>كافيه النخيل</h1>
    <p>حيث تلتقي أصالة البصرة بعطر القهوة</p>
  </div>

  <div class="scroll-hint">▼ اكتشف القائمة</div>
</div>

<!-- ========= MENU ========= -->
<section>
  <h2 class="section-title">☕ قائمة المشروبات</h2>
  <div class="divider"></div>
  <div class="menu-grid">

    <div class="card">
      <div class="card-img">☕</div>
      <div class="card-body">
        <h3>قهوة النخيل الخاصة</h3>
        <p>خلطتنا السرية من البن العربي مع عطر الهيل والزعفران</p>
        <span class="price">2,500 د.ع</span>
      </div>
    </div>

    <div class="card">
      <div class="card-img">🧋</div>
      <div class="card-body">
        <h3>لاتيه التمر والكراميل</h3>
        <p>لاتيه ناعم بنكهة التمر البصري الأصيل وصوص الكراميل</p>
        <span class="price">3,000 د.ع</span>
      </div>
    </div>

    <div class="card">
      <div class="card-img">🍵</div>
      <div class="card-body">
        <h3>شاي الورد والهيل</h3>
        <p>شاي عربي معطر بماء الورد وبذور الهيل الأخضر</p>
        <span class="price">2,000 د.ع</span>
      </div>
    </div>

    <div class="card">
      <div class="card-img">🥤</div>
      <div class="card-body">
        <h3>فرابيه النخيل</h3>
        <p>مزيج مثلج من القهوة والتمر والقشطة الطازجة</p>
        <span class="price">3,500 د.ع</span>
      </div>
    </div>

    <div class="card">
      <div class="card-img">🫖</div>
      <div class="card-body">
        <h3>ماتشا صحراوي</h3>
        <p>ماتشا بريميوم مع حليب جوز الهند ولمسة من العسل</p>
        <span class="price">3,200 د.ع</span>
      </div>
    </div>

    <div class="card">
      <div class="card-img">🍫</div>
      <div class="card-body">
        <h3>هوت شوكولاتة الرمال</h3>
        <p>شوكولاتة داكنة دافئة مع قرفة ورشة ملح البحر</p>
        <span class="price">2,800 د.ع</span>
      </div>
    </div>

  </div>
</section>

<!-- ========= FOOD ========= -->
<section>
  <h2 class="section-title">🥐 المأكولات</h2>
  <div class="divider"></div>
  <div class="menu-grid">

    <div class="card">
      <div class="card-img">🥐</div>
      <div class="card-body">
        <h3>كرواسون التمر والجبن</h3>
        <p>كرواسون طازج محشو بعجينة التمر والجبن الكريمي</p>
        <span class="price">2,000 د.ع</span>
      </div>
    </div>

    <div class="card">
      <div class="card-img">🍰</div>
      <div class="card-body">
        <h3>كيكة النخيل</h3>
        <p>كيكة إسفنجية بنكهة التمر والجوز مع صوص الكراميل</p>
        <span class="price">2,500 د.ع</span>
      </div>
    </div>

    <div class="card">
      <div class="card-img">🥪</div>
      <div class="card-body">
        <h3>ساندويش الدجاج المشوي</h3>
        <p>خبز محلي مع دجاج متبل وخضار طازجة وصوص النعناع</p>
        <span class="price">3,500 د.ع</span>
      </div>
    </div>

  </div>
</section>

<!-- ========= ABOUT ========= -->
<section>
  <div class="about-wrap">
    <div class="about-art">🌴</div>
    <div class="about-text">
      <h2>قصتنا</h2>
      <p>
        وُلد كافيه النخيل من وسط نخيل البصرة الشامخة، حيث قررنا أن نجمع بين
        أصالة القهوة العربية وبهجة المكان الجميل. كل كوب نقدمه يحمل حبًا حقيقيًا
        ولمسة من تراب هذه الأرض الطيبة. نستخدم أجود أنواع البن المختار يدويًا،
        ونحرص على أن تكون تجربتك معنا لحظة راحة حقيقية.
      </p>
    </div>
  </div>
</section>

<!-- ========= HOURS ========= -->
<section>
  <div class="hours-bg">
    <h2 class="section-title">🕐 أوقات العمل</h2>
    <div class="divider"></div>
    <div class="hours-grid">
      <div class="hour-item">
        <div class="day">السبت – الأربعاء</div>
        <div class="time">7:00 ص – 12:00 م</div>
      </div>
      <div class="hour-item">
        <div class="day">الخميس</div>
        <div class="time">7:00 ص – 1:00 ص</div>
      </div>
      <div class="hour-item">
        <div class="day">الجمعة</div>
        <div class="time">12:00 م – 1:00 ص</div>
      </div>
      <div class="hour-item">
        <div class="day">التوصيل</div>
        <div class="time">متاح طوال اليوم</div>
      </div>
    </div>
  </div>
</section>

<!-- ========= FOOTER ========= -->
<footer>
  <p>🌴 <span>كافيه النخيل</span> — البصرة، العراق</p>
  <p style="margin-top:.5rem">📞 07700000000 &nbsp;|&nbsp; 📍 شارع النخيل، البصرة</p>
</footer>

</body>
</html>"""

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))
    def log_message(self, format, *args):
        pass  # تعطيل الطباعة في الكونسول

def open_browser():
    import time
    time.sleep(0.8)
    webbrowser.open(f"http://localhost:{PORT}")

print("=" * 45)
print("   🌴 كافيه النخيل — جاري التشغيل...")
print(f"   🌐 http://localhost:{PORT}")
print("   اضغط Ctrl+C للإيقاف")
print("=" * 45)

threading.Thread(target=open_browser, daemon=True).start()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n   ✅ تم إيقاف السيرفر. إلى اللقاء! 🌴")