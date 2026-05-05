from .db import get_db_connection
import logging

class Tag:
    """標籤模型，處理 tags 與 recipe_tags 資料表的操作"""

    @staticmethod
    def get_or_create(name):
        """取得現有標籤或建立新標籤"""
        try:
            conn = get_db_connection()
            row = conn.execute("SELECT id FROM tags WHERE name = ?", (name,)).fetchone()
            if row:
                return row['id']
            else:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tags (name) VALUES (?)", (name,))
                tag_id = cursor.lastrowid
                conn.commit()
                return tag_id
        except Exception as e:
            logging.error(f"Error in get_or_create tag: {e}")
            raise

    @staticmethod
    def get_all():
        """取得所有標籤"""
        try:
            conn = get_db_connection()
            rows = conn.execute("SELECT * FROM tags").fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting all tags: {e}")
            return []

    @staticmethod
    def link_to_recipe(recipe_id, tag_id):
        """建立食譜與標籤的關聯"""
        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT OR IGNORE INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)",
                (recipe_id, tag_id)
            )
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error linking tag {tag_id} to recipe {recipe_id}: {e}")
            raise

    @staticmethod
    def get_by_recipe(recipe_id):
        """取得特定食譜的所有標籤"""
        try:
            conn = get_db_connection()
            rows = conn.execute(
                """
                SELECT t.* FROM tags t
                JOIN recipe_tags rt ON t.id = rt.tag_id
                WHERE rt.recipe_id = ?
                """,
                (recipe_id,)
            ).fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting tags for recipe {recipe_id}: {e}")
            return []
    
    @staticmethod
    def unlink_from_recipe(recipe_id):
        """移除特定食譜的所有標籤關聯"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM recipe_tags WHERE recipe_id = ?", (recipe_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error unlinking tags from recipe {recipe_id}: {e}")
            raise
            
    @staticmethod
    def delete(tag_id):
        """刪除標籤（這也會因為 ON DELETE CASCADE 移除關聯）"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting tag {tag_id}: {e}")
            raise
