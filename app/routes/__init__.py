from .recipe import recipe_bp

def init_app(app):
    """註冊所有 Blueprint"""
    app.register_blueprint(recipe_bp)
