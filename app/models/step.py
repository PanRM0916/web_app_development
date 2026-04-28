from .db import get_db_connection

class Step:
    @staticmethod
    def create(recipe_id, step_number, description):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO steps (recipe_id, step_number, description) VALUES (?, ?, ?)",
            (recipe_id, step_number, description)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_recipe(recipe_id):
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT * FROM steps WHERE recipe_id = ? ORDER BY step_number ASC",
            (recipe_id,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def delete_by_recipe(recipe_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM steps WHERE recipe_id = ?", (recipe_id,))
        conn.commit()
        conn.close()
