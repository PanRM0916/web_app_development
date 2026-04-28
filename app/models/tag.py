from .db import get_db_connection

class Tag:
    @staticmethod
    def get_or_create(name):
        conn = get_db_connection()
        row = conn.execute("SELECT id FROM tags WHERE name = ?", (name,)).fetchone()
        if row:
            tag_id = row['id']
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tags (name) VALUES (?)", (name,))
            tag_id = cursor.lastrowid
            conn.commit()
        conn.close()
        return tag_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM tags").fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def link_to_recipe(recipe_id, tag_id):
        conn = get_db_connection()
        conn.execute(
            "INSERT OR IGNORE INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)",
            (recipe_id, tag_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_recipe(recipe_id):
        conn = get_db_connection()
        rows = conn.execute(
            """
            SELECT t.* FROM tags t
            JOIN recipe_tags rt ON t.id = rt.tag_id
            WHERE rt.recipe_id = ?
            """,
            (recipe_id,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def unlink_from_recipe(recipe_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM recipe_tags WHERE recipe_id = ?", (recipe_id,))
        conn.commit()
        conn.close()
