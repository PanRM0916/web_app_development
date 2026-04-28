from .db import get_db_connection

class Recipe:
    def __init__(self, id=None, title=None, category=None, total_time=None, servings=2, created_at=None):
        self.id = id
        self.title = title
        self.category = category
        self.total_time = total_time
        self.servings = servings
        self.created_at = created_at

    @staticmethod
    def create(title, category, total_time=None, servings=2):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO recipes (title, category, total_time, servings) VALUES (?, ?, ?, ?)",
            (title, category, total_time, servings)
        )
        recipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return recipe_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM recipes ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(recipe_id, title, category, total_time, servings):
        conn = get_db_connection()
        conn.execute(
            "UPDATE recipes SET title = ?, category = ?, total_time = ?, servings = ? WHERE id = ?",
            (title, category, total_time, servings, recipe_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search(keyword):
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT * FROM recipes WHERE title LIKE ? OR category LIKE ? ORDER BY created_at DESC",
            (f'%{keyword}%', f'%{keyword}%')
        )
        conn.close()
        return [dict(row) for row in rows]
