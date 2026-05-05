from .db import get_db_connection
import logging

class Step:
    """步驟模型，處理 steps 資料表的 CRUD 操作"""

    @staticmethod
    def create(data):
        """新增步驟記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO steps (recipe_id, step_number, description) VALUES (?, ?, ?)",
                (data['recipe_id'], data['step_number'], data['description'])
            )
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error creating step: {e}")
            raise

    @staticmethod
    def get_by_recipe(recipe_id):
        """取得特定食譜的所有步驟"""
        try:
            conn = get_db_connection()
            rows = conn.execute(
                "SELECT * FROM steps WHERE recipe_id = ? ORDER BY step_number ASC",
                (recipe_id,)
            ).fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting steps for recipe {recipe_id}: {e}")
            return []

    @staticmethod
    def delete_by_recipe(recipe_id):
        """刪除特定食譜的所有步驟"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM steps WHERE recipe_id = ?", (recipe_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting steps for recipe {recipe_id}: {e}")
            raise
            
    @staticmethod
    def delete(step_id):
        """刪除單一步驟記錄"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM steps WHERE id = ?", (step_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting step {step_id}: {e}")
            raise
