import http.server
import socketserver
import threading
import webbrowser

HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>كافيه النخيل</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&family=Lateef:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f9f5ef;
    --card: #ffffff;
    --accent: #c89b3c;
    --accent-2: #2f5d34;
    --text: #2a1c0b;
    --muted: #7c6b58;
    --danger: #b42318;
    --shadow: 0 10px 30px rgba(37, 24, 10, 0.1);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: "Tajawal", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
  }

  .hero {
    min-height: 46vh;
    display: grid;
    place-items: center;
    text-align: center;
    padding: 3rem 1rem;
    color: #fff;
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.2), transparent 40%),
                linear-gradient(135deg, #1f3b22 0%, #2f5d34 45%, #6a4a2a 100%);
  }

  .palm {
    position: absolute;
    bottom: -22px;
    font-size: clamp(3.2rem, 9vw, 5.4rem);
    opacity: 0.26;
    transform-origin: center bottom;
    animation: palmSway 4.2s ease-in-out infinite;
    user-select: none;
    pointer-events: none;
  }

  .palm-left { left: 3%; animation-delay: 0s; }
  .palm-right { right: 3%; animation-delay: 1s; }

  @keyframes palmSway {
    0%, 100% { transform: rotate(-4deg) translateY(0); }
    50% { transform: rotate(4deg) translateY(-6px); }
  }

  .hero h1 {
    font-family: "Lateef", serif;
    font-size: clamp(3rem, 8vw, 6rem);
    line-height: 1;
    color: #f5d281;
  }

  .hero p { color: rgba(255, 255, 255, 0.85); font-size: 1.1rem; }

  .container { max-width: 1150px; margin: 0 auto; padding: 2rem 1rem 4rem; }

  .toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
  }

  .toolbar h2 {
    font-family: "Lateef", serif;
    font-size: 2.4rem;
    color: var(--accent-2);
  }

  .btn {
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    font-size: 0.95rem;
    cursor: pointer;
    transition: transform 0.2s ease, opacity 0.2s ease;
  }

  .btn:hover { transform: translateY(-2px); }
  .btn-primary { background: var(--accent); color: #fff; font-weight: 700; }
  .btn-muted { background: #ece6dd; color: #4e3f30; }
  .btn-danger { background: #fff2f0; color: var(--danger); border: 1px solid #f3c6bf; }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1.2rem;
  }

  .card {
    background: var(--card);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow);
    border: 1px solid #eee5d9;
  }

  .card-top {
    background: linear-gradient(135deg, #efe4d4 0%, #f8f1e7 100%);
    padding: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.6rem;
  }

  .card-image {
    width: 100%;
    height: 170px;
    object-fit: cover;
    display: block;
  }

  .card-body { padding: 1rem 1rem 1.2rem; }
  .card h3 { margin-bottom: 0.35rem; color: #3f2d18; }
  .card p { color: var(--muted); min-height: 50px; font-size: 0.95rem; }

  .meta {
    margin-top: 0.7rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.6rem;
  }

  .tag {
    font-size: 0.82rem;
    color: #44513f;
    background: #edf6ee;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
  }

  .price {
    background: linear-gradient(135deg, var(--accent), #d4af5a);
    color: white;
    border-radius: 999px;
    padding: 0.25rem 0.7rem;
    font-weight: 700;
    font-size: 0.9rem;
  }

  .admin-panel {
    margin: 1.5rem 0 2rem;
    background: #fff;
    border: 1px solid #e8dece;
    border-radius: 16px;
    box-shadow: var(--shadow);
    padding: 1rem;
    display: none;
  }

  .admin-panel.active { display: block; }

  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .panel-header h3 { color: var(--accent-2); }

  .form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.8rem;
    margin-bottom: 0.8rem;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .field label { font-size: 0.85rem; color: #6d5a46; }

  .field input, .field select, .field textarea {
    border: 1px solid #d8ccb9;
    border-radius: 10px;
    padding: 0.6rem 0.7rem;
    font-family: inherit;
    font-size: 0.95rem;
    background: #fffdfa;
  }

  .field textarea { resize: vertical; min-height: 70px; }

  .admin-table-wrap {
    margin-top: 1rem;
    border: 1px solid #eadfcd;
    border-radius: 12px;
    overflow: auto;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    min-width: 640px;
    background: #fff;
  }

  th, td {
    text-align: right;
    padding: 0.65rem;
    border-bottom: 1px solid #f1e7d8;
    font-size: 0.9rem;
  }

  th { background: #fbf6ef; color: #5c4a36; }
  .status { margin-top: 0.6rem; color: var(--accent-2); font-size: 0.92rem; min-height: 1.3rem; }

  footer {
    background: #1f170f;
    color: #c4b6a4;
    text-align: center;
    padding: 1.5rem;
    margin-top: 2rem;
  }

  @media (max-width: 640px) {
    .hero { min-height: 38vh; }
    .toolbar h2 { font-size: 2rem; }
  }
</style>
</head>
<body>
  <header class="hero">
    <span class="palm palm-left">🌴</span>
    <span class="palm palm-right">🌴</span>
    <div>
      <h1>كافيه النخيل</h1>
      <p>واجهة حديثة + لوحة أدمن لإدارة المنتجات والأسعار</p>
    </div>
  </header>

  <main class="container">
    <div class="toolbar">
      <h2>المنيو</h2>
      <button class="btn btn-primary" id="toggleAdminBtn">فتح لوحة الأدمن</button>
    </div>

    <section id="adminPanel" class="admin-panel">
      <div class="panel-header">
        <h3>لوحة الأدمن</h3>
        <button class="btn btn-muted" id="seedBtn">إعادة المنتجات الافتراضية</button>
      </div>

      <form id="productForm">
        <div class="form-grid">
          <div class="field">
            <label for="name">اسم المنتج</label>
            <input id="name" required placeholder="مثال: كورتادو النخيل">
          </div>
          <div class="field">
            <label for="price">السعر (د.ع)</label>
            <input id="price" required type="number" min="0" step="100" placeholder="2500">
          </div>
          <div class="field">
            <label for="category">التصنيف</label>
            <select id="category" required>
              <option value="مشروبات">مشروبات</option>
              <option value="مأكولات">مأكولات</option>
            </select>
          </div>
          <div class="field">
            <label for="emoji">أيقونة</label>
            <input id="emoji" maxlength="2" placeholder="☕">
          </div>
          <div class="field">
            <label for="imageUrl">رابط الصورة</label>
            <input id="imageUrl" type="url" placeholder="https://example.com/item.jpg">
          </div>
          <div class="field">
            <label for="imageFile">أو ارفع صورة من جهازك</label>
            <input id="imageFile" type="file" accept="image/*">
          </div>
          <div class="field" style="grid-column: 1 / -1;">
            <label for="description">الوصف</label>
            <textarea id="description" required placeholder="وصف قصير للمنتج"></textarea>
          </div>
        </div>
        <button class="btn btn-primary" type="submit">إضافة المنتج</button>
      </form>
      <p class="status" id="status"></p>

      <div class="admin-table-wrap">
        <table>
          <thead>
            <tr>
              <th>الاسم</th>
              <th>التصنيف</th>
              <th>السعر</th>
              <th>إجراء</th>
            </tr>
          </thead>
          <tbody id="adminTableBody"></tbody>
        </table>
      </div>
    </section>

    <section class="grid" id="productGrid"></section>
  </main>

  <footer>
    <p>🌴 كافيه النخيل - البصرة، العراق</p>
  </footer>

<script>
  const STORAGE_KEY = "cafe-products-v1";
  const defaultProducts = [
    { id: 1, name: "قهوة النخيل الخاصة", price: 2500, category: "مشروبات", emoji: "☕", description: "خلطة بن عربي مع الهيل." },
    { id: 2, name: "لاتيه التمر", price: 3000, category: "مشروبات", emoji: "🧋", description: "لاتيه كريمي بلمسة تمر بصري." },
    { id: 3, name: "هوت شوكولاتة", price: 2800, category: "مشروبات", emoji: "🍫", description: "شوكولاتة دافئة مع القرفة." },
    { id: 4, name: "كيكة النخيل", price: 2500, category: "مأكولات", emoji: "🍰", description: "كيكة تمر وجوز مع كراميل." },
    { id: 5, name: "كرواسون التمر", price: 2000, category: "مأكولات", emoji: "🥐", description: "كرواسون طازج بحشوة التمر." }
  ];

  const grid = document.getElementById("productGrid");
  const adminPanel = document.getElementById("adminPanel");
  const toggleAdminBtn = document.getElementById("toggleAdminBtn");
  const seedBtn = document.getElementById("seedBtn");
  const form = document.getElementById("productForm");
  const adminTableBody = document.getElementById("adminTableBody");
  const status = document.getElementById("status");
  const imageFileInput = document.getElementById("imageFile");

  function readProducts() {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultProducts));
      return [...defaultProducts];
    }
    try {
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) throw new Error("invalid data");
      return parsed;
    } catch (_) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultProducts));
      return [...defaultProducts];
    }
  }

  function writeProducts(products) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(products));
  }

  function formatPrice(value) {
    return Number(value).toLocaleString("ar-IQ") + " د.ع";
  }

  function fileToDataUrl(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(new Error("image read failed"));
      reader.readAsDataURL(file);
    });
  }

  function renderCards() {
    const products = readProducts();
    grid.innerHTML = "";
    products.forEach((product) => {
      const card = document.createElement("article");
      card.className = "card";
      const visual = product.image
        ? `<img class="card-image" src="${product.image}" alt="${product.name}">`
        : `<div class="card-top">${product.emoji || "☕"}</div>`;
      card.innerHTML = `
        ${visual}
        <div class="card-body">
          <h3>${product.name}</h3>
          <p>${product.description}</p>
          <div class="meta">
            <span class="tag">${product.category}</span>
            <span class="price">${formatPrice(product.price)}</span>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
  }

  function renderAdminTable() {
    const products = readProducts();
    adminTableBody.innerHTML = "";
    products.forEach((product) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${product.name}</td>
        <td>${product.category}</td>
        <td>${formatPrice(product.price)}</td>
        <td><button class="btn btn-danger" data-id="${product.id}">حذف</button></td>
      `;
      adminTableBody.appendChild(row);
    });
  }

  function showStatus(message) {
    status.textContent = message;
    setTimeout(() => { status.textContent = ""; }, 2200);
  }

  function refreshAll() {
    renderCards();
    renderAdminTable();
  }

  toggleAdminBtn.addEventListener("click", () => {
    adminPanel.classList.toggle("active");
    toggleAdminBtn.textContent = adminPanel.classList.contains("active")
      ? "إغلاق لوحة الأدمن"
      : "فتح لوحة الأدمن";
  });

  seedBtn.addEventListener("click", () => {
    writeProducts([...defaultProducts]);
    refreshAll();
    showStatus("تمت إعادة المنتجات الافتراضية.");
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const name = document.getElementById("name").value.trim();
    const price = Number(document.getElementById("price").value);
    const category = document.getElementById("category").value;
    const emoji = document.getElementById("emoji").value.trim() || "☕";
    const imageUrl = document.getElementById("imageUrl").value.trim();
    const description = document.getElementById("description").value.trim();
    const imageFile = imageFileInput.files && imageFileInput.files[0];
    let image = imageUrl;

    if (!name || !description || !price || price < 0) {
      showStatus("تحقق من إدخال الاسم والوصف والسعر بشكل صحيح.");
      return;
    }

    if (imageFile) {
      try {
        image = await fileToDataUrl(imageFile);
      } catch (_) {
        showStatus("تعذر قراءة ملف الصورة.");
        return;
      }
    }

    const products = readProducts();
    const nextId = products.length ? Math.max(...products.map((p) => p.id || 0)) + 1 : 1;
    products.push({ id: nextId, name, price, category, emoji, image, description });
    writeProducts(products);
    form.reset();
    refreshAll();
    showStatus("تمت إضافة المنتج بنجاح.");
  });

  adminTableBody.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) return;
    const id = Number(target.dataset.id);
    const products = readProducts();
    const updated = products.filter((p) => p.id !== id);
    writeProducts(updated);
    refreshAll();
    showStatus("تم حذف المنتج.");
  });

  refreshAll();
</script>
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