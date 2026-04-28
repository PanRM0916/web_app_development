from .db import get_db_connection

class Ingredient:
    @staticmethod
    def create(recipe_id, name, quantity, unit):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO ingredients (recipe_id, name, quantity, unit) VALUES (?, ?, ?, ?)",
            (recipe_id, name, quantity, unit)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_recipe(recipe_id):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (recipe_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def delete_by_recipe(recipe_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        conn.commit()
        conn.close()
