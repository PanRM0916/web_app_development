from .db import get_db_connection
import logging

class Ingredient:
    """食材模型，處理 ingredients 資料表的 CRUD 操作"""

    @staticmethod
    def create(data):
        """新增食材記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO ingredients (recipe_id, name, quantity, unit) VALUES (?, ?, ?, ?)",
                (data['recipe_id'], data['name'], data.get('quantity'), data.get('unit'))
            )
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error creating ingredient: {e}")
            raise

    @staticmethod
    def get_by_recipe(recipe_id):
        """取得特定食譜的所有食材"""
        try:
            conn = get_db_connection()
            rows = conn.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (recipe_id,)).fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting ingredients for recipe {recipe_id}: {e}")
            return []

    @staticmethod
    def delete_by_recipe(recipe_id):
        """刪除特定食譜的所有食材"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting ingredients for recipe {recipe_id}: {e}")
            raise

    @staticmethod
    def delete(ingredient_id):
        """刪除單一食材記錄"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM ingredients WHERE id = ?", (ingredient_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting ingredient {ingredient_id}: {e}")
            raise
