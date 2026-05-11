"""
تطبيق Flask — كوفي النخيل: قائمة، طلبات حسب رقم الطاولة، لوحة مدير.
تشغيل محلي: flask --app app run
إنتاج: gunicorn -w 2 -b 127.0.0.1:8000 app:app

بيئة الإنتاج: عيّن SECRET_KEY و CAFE_ADMIN_PASSWORD (لا تعتمد على القيم الافتراضية).
"""

from __future__ import annotations

import os
import sqlite3
import uuid
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any

from flask import (
    Flask,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

# --- إعدادات ---
ALLOWED_IMAGE_EXT = frozenset({"png", "jpg", "jpeg", "webp"})
MAX_UPLOAD_BYTES = 2 * 1024 * 1024
TABLE_MIN, TABLE_MAX = 1, 99
ORDER_STATUSES = ("pending", "preparing", "ready", "done")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        path = Path(current_app.instance_path) / "cafe.db"
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


def close_db(_: Any = None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS menu_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_ar TEXT NOT NULL,
            price REAL NOT NULL,
            image_path TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS cafe_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            note TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS order_line (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL REFERENCES cafe_order(id) ON DELETE CASCADE,
            menu_item_id INTEGER NOT NULL REFERENCES menu_item(id),
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            UNIQUE(order_id, menu_item_id)
        );
        """
    )
    cur = db.execute("SELECT COUNT(*) AS c FROM menu_item")
    if cur.fetchone()["c"] == 0:
        defaults = [
            ("قهوة عربية", 12.0, "/static/img/placeholder.svg", 1),
            ("كابتشينو", 18.0, "/static/img/placeholder.svg", 2),
            ("لاتيه", 20.0, "/static/img/placeholder.svg", 3),
            ("شاي كرك", 14.0, "/static/img/placeholder.svg", 4),
            ("عصير برتقال طازج", 16.0, "/static/img/placeholder.svg", 5),
            ("موكا", 22.0, "/static/img/placeholder.svg", 6),
        ]
        db.executemany(
            "INSERT INTO menu_item (name_ar, price, image_path, sort_order) VALUES (?,?,?,?)",
            defaults,
        )
    db.commit()


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def create_app() -> Flask:
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="templates",
        static_folder="static",
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "dev-only-change-in-production"
    app.config["ADMIN_PASSWORD"] = os.environ.get("CAFE_ADMIN_PASSWORD") or "admin"

    app.teardown_appcontext(close_db)

    @app.before_request
    def _ensure_db() -> None:
        if request.endpoint == "static":
            return
        init_db()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/")
    def index():
        db = get_db()
        items = db.execute(
            "SELECT id, name_ar, price, image_path FROM menu_item ORDER BY sort_order, id"
        ).fetchall()
        return render_template("index.html", items=items)

    @app.post("/order")
    def place_order():
        if not request.is_json:
            return {"ok": False, "error": "JSON مطلوب"}, 400
        data = request.get_json(silent=True) or {}
        try:
            table = int(data.get("table_number"))
        except (TypeError, ValueError):
            return {"ok": False, "error": "رقم الطاولة غير صالح"}, 400
        if table < TABLE_MIN or table > TABLE_MAX:
            return {"ok": False, "error": f"رقم الطاولة يجب أن يكون بين {TABLE_MIN} و {TABLE_MAX}"}, 400
        raw_items = data.get("items")
        if not isinstance(raw_items, list) or not raw_items:
            return {"ok": False, "error": "السلة فارغة"}, 400
        note = (data.get("note") or "").strip()
        if len(note) > 500:
            note = note[:500]

        lines: list[tuple[int, int, float]] = []
        db = get_db()
        for entry in raw_items:
            if not isinstance(entry, dict):
                continue
            try:
                mid = int(entry.get("menu_item_id"))
                qty = int(entry.get("quantity", 0))
            except (TypeError, ValueError):
                continue
            if qty <= 0:
                continue
            row = db.execute(
                "SELECT id, price FROM menu_item WHERE id = ?", (mid,)
            ).fetchone()
            if row is None:
                continue
            lines.append((mid, qty, float(row["price"])))
        if not lines:
            return {"ok": False, "error": "لا توجد عناصر صالحة في الطلب"}, 400

        db.execute("BEGIN")
        try:
            cur = db.execute(
                "INSERT INTO cafe_order (table_number, created_at, status, note) VALUES (?,?,?,?)",
                (table, _utc_now_iso(), "pending", note),
            )
            oid = cur.lastrowid
            for mid, qty, price in lines:
                db.execute(
                    """
                    INSERT INTO order_line (order_id, menu_item_id, quantity, unit_price)
                    VALUES (?,?,?,?)
                    ON CONFLICT(order_id, menu_item_id) DO UPDATE SET
                      quantity = order_line.quantity + excluded.quantity
                    """,
                    (oid, mid, qty, price),
                )
            db.commit()
        except Exception:
            db.rollback()
            return {"ok": False, "error": "تعذر حفظ الطلب"}, 500

        return {"ok": True, "order_id": oid}

    @app.get("/order/done/<int:order_id>")
    def order_done(order_id: int):
        return render_template("order_success.html", order_id=order_id)

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if session.get("admin"):
            return redirect(url_for("admin_dashboard"))
        nxt = (request.args.get("next") or "").strip()
        if request.method == "POST":
            pwd = (request.form.get("password") or "").strip()
            nxt = (request.form.get("next") or request.args.get("next") or "").strip()
            if pwd == app.config["ADMIN_PASSWORD"]:
                session["admin"] = True
                if nxt.startswith("/") and not nxt.startswith("//"):
                    return redirect(nxt)
                return redirect(url_for("admin_dashboard"))
            flash("كلمة المرور غير صحيحة", "error")
        return render_template("admin_login.html", next_url=nxt)

    @app.get("/admin/logout")
    def admin_logout():
        session.pop("admin", None)
        return redirect(url_for("index"))

    @app.get("/admin")
    @admin_required
    def admin_dashboard():
        db = get_db()
        orders = db.execute(
            """
            SELECT o.id, o.table_number, o.created_at, o.status, o.note,
                   GROUP_CONCAT(m.name_ar || ' × ' || l.quantity, '، ') AS summary
            FROM cafe_order o
            JOIN order_line l ON l.order_id = o.id
            JOIN menu_item m ON m.id = l.menu_item_id
            GROUP BY o.id
            ORDER BY o.created_at DESC
            LIMIT 200
            """
        ).fetchall()
        menu = db.execute(
            "SELECT id, name_ar, price, image_path FROM menu_item ORDER BY sort_order, id"
        ).fetchall()
        return render_template("admin_dashboard.html", orders=orders, menu=menu)

    @app.post("/admin/orders/<int:order_id>/status")
    @admin_required
    def admin_order_status(order_id: int):
        status = (request.form.get("status") or "").strip()
        if status not in ORDER_STATUSES:
            flash("حالة غير صالحة", "error")
            return redirect(url_for("admin_dashboard"))
        db = get_db()
        db.execute("UPDATE cafe_order SET status = ? WHERE id = ?", (status, order_id))
        db.commit()
        return redirect(url_for("admin_dashboard"))

    @app.post("/admin/menu/<int:item_id>/image")
    @admin_required
    def admin_menu_image(item_id: int):
        f = request.files.get("image")
        if not f or not f.filename:
            flash("لم يُرفع ملف", "error")
            return redirect(url_for("admin_dashboard"))
        ext = (Path(f.filename).suffix or "").lower().lstrip(".")
        if ext not in ALLOWED_IMAGE_EXT:
            flash("الامتداد غير مسموح (png, jpg, jpeg, webp)", "error")
            return redirect(url_for("admin_dashboard"))
        f.stream.seek(0, os.SEEK_END)
        size = f.stream.tell()
        f.stream.seek(0)
        if size > MAX_UPLOAD_BYTES:
            flash("حجم الملف كبير جداً (الحد 2 ميجابايت)", "error")
            return redirect(url_for("admin_dashboard"))

        uploads = Path(app.root_path) / "static" / "uploads"
        uploads.mkdir(parents=True, exist_ok=True)
        fname = f"{item_id}_{uuid.uuid4().hex[:10]}.{ext}"
        safe = secure_filename(fname)
        if not safe:
            safe = f"{uuid.uuid4().hex}.{ext}"
        dest = uploads / safe
        f.save(dest)

        rel = f"/static/uploads/{safe}"
        db = get_db()
        row = db.execute("SELECT id FROM menu_item WHERE id = ?", (item_id,)).fetchone()
        if row is None:
            abort(404)
        db.execute("UPDATE menu_item SET image_path = ? WHERE id = ?", (rel, item_id))
        db.commit()
        flash("تم تحديث الصورة", "ok")
        return redirect(url_for("admin_dashboard"))

    return app


app = create_app()

if __name__ == "__main__":
    import threading
    import webbrowser

    host, port = "127.0.0.1", 5000
    url = f"http://{host}:{port}/"

    def _open_browser() -> None:
        webbrowser.open(url)

    threading.Timer(0.8, _open_browser).start()
    print(f"كوفي النخيل — افتح المتصفح على {url} (أو انتظر فتحه تلقائياً)")
    print("للإيقاف: Ctrl+C")
    app.run(host=host, port=port, debug=True, use_reloader=False)
