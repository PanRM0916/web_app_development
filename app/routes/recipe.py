from flask import Blueprint, render_template, request, redirect, url_for, flash
import random

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    食譜列表首頁
    支援關鍵字搜尋 (?q=...) 與分類篩選 (?category=...)
    """
    pass

@recipe_bp.route('/recipe/random')
def random_recipe():
    """
    隨機推薦功能
    隨機挑選一個食譜並重導向至其詳情頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>')
def detail(id):
    """
    食譜詳情頁面
    顯示單一食譜的完整資訊，包含食材份量換算
    """
    pass

@recipe_bp.route('/recipe/new', methods=['GET', 'POST'])
def create():
    """
    新增食譜
    GET: 顯示空白表單
    POST: 接收表單資料並儲存
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    編輯食譜頁面
    顯示帶有原有資料的編輯表單
    """
    pass

@recipe_bp.route('/recipe/<int:id>/update', methods=['POST'])
def update(id):
    """
    更新食譜動作
    接收編輯後的表單資料並更新資料庫
    """
    pass

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除食譜動作
    刪除食譜及其關聯資料
    """
    pass
