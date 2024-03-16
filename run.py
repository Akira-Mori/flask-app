from waitress import serve
from app import app  # app.py から Flask アプリケーションをインポート

serve(app, host='0.0.0.0', port=8080)  # 適切なホストとポートでサーブ