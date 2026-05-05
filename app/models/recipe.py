from .db import get_db_connection
import logging

class Recipe:
    """食譜模型，處理 recipes 資料表的 CRUD 操作"""

    @staticmethod
    def create(data):
        """
        新增一筆食譜記錄
        :param data: 包含 title, category, total_time, servings 的字典
        :return: 新增記錄的 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO recipes (title, category, total_time, servings) VALUES (?, ?, ?, ?)",
                (data['title'], data['category'], data.get('total_time'), data.get('servings', 2))
            )
            recipe_id = cursor.lastrowid
            conn.commit()
            return recipe_id
        except Exception as e:
            logging.error(f"Error creating recipe: {e}")
            raise

    @staticmethod
    def get_all():
        """取得所有食譜記錄"""
        try:
            conn = get_db_connection()
            rows = conn.execute("SELECT * FROM recipes ORDER BY created_at DESC").fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error getting all recipes: {e}")
            return []

    @staticmethod
    def get_by_id(recipe_id):
        """取得單筆食譜記錄"""
        try:
            conn = get_db_connection()
            row = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
            return dict(row) if row else None
        except Exception as e:
            logging.error(f"Error getting recipe by id {recipe_id}: {e}")
            return None

    @staticmethod
    def update(recipe_id, data):
        """更新食譜記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE recipes SET title = ?, category = ?, total_time = ?, servings = ? WHERE id = ?",
                (data['title'], data['category'], data.get('total_time'), data.get('servings'), recipe_id)
            )
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error updating recipe {recipe_id}: {e}")
            raise

    @staticmethod
    def delete(recipe_id):
        """刪除食譜記錄"""
        try:
            conn = get_db_connection()
            conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting recipe {recipe_id}: {e}")
            raise

    @staticmethod
    def search(keyword):
        """搜尋食譜"""
        try:
            conn = get_db_connection()
            rows = conn.execute(
                "SELECT * FROM recipes WHERE title LIKE ? OR category LIKE ? ORDER BY created_at DESC",
                (f'%{keyword}%', f'%{keyword}%')
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error searching recipes: {keyword}: {e}")
            return []
