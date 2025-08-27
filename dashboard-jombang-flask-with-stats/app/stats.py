from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db  # sesuaikan dengan struktur project-mu

bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@bp.route('/volume')
def volume():
    q = text("""
      SELECT DATE(published_at) AS day, COUNT(*) AS cnt
      FROM articles
      WHERE published_at >= CURRENT_DATE - INTERVAL '90 days'
      GROUP BY day
      ORDER BY day;
    """)
    rows = db.session.execute(q).fetchall()
    data = [{'date': str(r[0]), 'count': r[1]} for r in rows]
    return jsonify(data)

@bp.route('/categories')
def categories():
    q = text("""
      SELECT COALESCE(category, 'Tidak diketahui') AS category, COUNT(*) AS cnt
      FROM articles
      WHERE published_at >= CURRENT_DATE - INTERVAL '30 days'
      GROUP BY category
      ORDER BY cnt DESC
      LIMIT 10;
    """)
    rows = db.session.execute(q).fetchall()
    data = [{'category': r[0], 'count': r[1]} for r in rows]
    return jsonify(data)
