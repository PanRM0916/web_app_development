# app/__init__.py
from flask import Flask
import os
from .models.db import init_db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # 基本配置
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models.db import close_db
    app.teardown_appcontext(close_db)

    # 註冊 Blueprint
    from .routes.recipe import recipe_bp
    app.register_blueprint(recipe_bp)

    return app
