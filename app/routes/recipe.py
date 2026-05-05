from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.step import Step
from app.models.tag import Tag
import random

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    食譜列表首頁
    支援關鍵字搜尋 (?q=...) 與分類篩選 (?category=...)
    """
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    
    if query:
        recipes = Recipe.search(query)
    else:
        recipes = Recipe.get_all()
        
    if category:
        recipes = [r for r in recipes if r['category'] == category]
        
    return render_template('index.html', recipes=recipes, q=query, category=category)

@recipe_bp.route('/recipe/random')
def random_recipe():
    """
    隨機推薦功能
    隨機挑選一個食譜並重導向至其詳情頁
    """
    recipes = Recipe.get_all()
    if not recipes:
        flash("目前沒有任何食譜，請先新增一筆！", "warning")
        return redirect(url_for('recipe.index'))
    
    random_id = random.choice(recipes)['id']
    return redirect(url_for('recipe.detail', id=random_id))

@recipe_bp.route('/recipe/<int:id>')
def detail(id):
    """
    食譜詳情頁面
    顯示單一食譜的完整資訊，包含食材份量換算
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("找不到該食譜！", "danger")
        return redirect(url_for('recipe.index'))
        
    ingredients = Ingredient.get_by_recipe(id)
    steps = Step.get_by_recipe(id)
    tags = Tag.get_by_recipe(id)
    
    return render_template('detail.html', recipe=recipe, ingredients=ingredients, steps=steps, tags=tags)

@recipe_bp.route('/recipe/new', methods=['GET', 'POST'])
def create():
    """
    新增食譜
    GET: 顯示空白表單
    POST: 接收表單資料並儲存
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        total_time = request.form.get('total_time')
        servings = request.form.get('servings', 2)
        
        # 驗證
        if not title or not category:
            flash("標題與分類為必填項目！", "danger")
            return render_template('recipe_form.html', recipe=None)
            
        try:
            # 1. 建立食譜
            recipe_id = Recipe.create({
                'title': title,
                'category': category,
                'total_time': total_time,
                'servings': servings
            })
            
            # 2. 處理食材
            names = request.form.getlist('ingredient_name[]')
            quantities = request.form.getlist('ingredient_quantity[]')
            units = request.form.getlist('ingredient_unit[]')
            for name, quantity, unit in zip(names, quantities, units):
                if name.strip():
                    Ingredient.create({
                        'recipe_id': recipe_id,
                        'name': name.strip(),
                        'quantity': quantity if quantity else None,
                        'unit': unit.strip()
                    })
            
            # 3. 處理步驟
            step_descriptions = request.form.getlist('step_description[]')
            for i, desc in enumerate(step_descriptions):
                if desc.strip():
                    Step.create({
                        'recipe_id': recipe_id,
                        'step_number': i + 1,
                        'description': desc.strip()
                    })
            
            # 4. 處理標籤
            tags_input = request.form.get('tags', '').replace('，', ',').split(',')
            for tag_name in tags_input:
                tag_name = tag_name.strip()
                if tag_name:
                    tag_id = Tag.get_or_create(tag_name)
                    Tag.link_to_recipe(recipe_id, tag_id)
            
            flash("食譜建立成功！", "success")
            return redirect(url_for('recipe.detail', id=recipe_id))
            
        except Exception as e:
            flash(f"建立失敗：{str(e)}", "danger")
            return render_template('recipe_form.html', recipe=None)

    return render_template('recipe_form.html', recipe=None)

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    編輯食譜頁面
    顯示帶有原有資料的編輯表單
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("找不到該食譜！", "danger")
        return redirect(url_for('recipe.index'))
        
    ingredients = Ingredient.get_by_recipe(id)
    steps = Step.get_by_recipe(id)
    tags = Tag.get_by_recipe(id)
    tags_str = ', '.join([t['name'] for t in tags])
    
    return render_template('recipe_form.html', recipe=recipe, ingredients=ingredients, steps=steps, tags_str=tags_str)

@recipe_bp.route('/recipe/<int:id>/update', methods=['POST'])
def update(id):
    """
    更新食譜動作
    接收編輯後的表單資料並更新資料庫
    """
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip()
    total_time = request.form.get('total_time')
    servings = request.form.get('servings')
    
    if not title or not category:
        flash("標題與分類為必填項目！", "danger")
        return redirect(url_for('recipe.edit', id=id))
        
    try:
        # 1. 更新食譜主表
        Recipe.update(id, {
            'title': title,
            'category': category,
            'total_time': total_time,
            'servings': servings
        })
        
        # 2. 重新處理食材 (先刪後加)
        Ingredient.delete_by_recipe(id)
        names = request.form.getlist('ingredient_name[]')
        quantities = request.form.getlist('ingredient_quantity[]')
        units = request.form.getlist('ingredient_unit[]')
        for name, quantity, unit in zip(names, quantities, units):
            if name.strip():
                Ingredient.create({
                    'recipe_id': id,
                    'name': name.strip(),
                    'quantity': quantity if quantity else None,
                    'unit': unit.strip()
                })
        
        # 3. 重新處理步驟 (先刪後加)
        Step.delete_by_recipe(id)
        step_descriptions = request.form.getlist('step_description[]')
        for i, desc in enumerate(step_descriptions):
            if desc.strip():
                Step.create({
                    'recipe_id': id,
                    'step_number': i + 1,
                    'description': desc.strip()
                })
        
        # 4. 重新處理標籤 (先斷開關聯後重新建立)
        Tag.unlink_from_recipe(id)
        tags_input = request.form.get('tags', '').replace('，', ',').split(',')
        for tag_name in tags_input:
            tag_name = tag_name.strip()
            if tag_name:
                tag_id = Tag.get_or_create(tag_name)
                Tag.link_to_recipe(id, tag_id)
        
        flash("食譜更新成功！", "success")
        return redirect(url_for('recipe.detail', id=id))
        
    except Exception as e:
        flash(f"更新失敗：{str(e)}", "danger")
        return redirect(url_for('recipe.edit', id=id))

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除食譜動作
    刪除食譜及其關聯資料
    """
    try:
        # 由於 SQLite 有設定 ON DELETE CASCADE，我們只需刪除 recipes 表記錄
        # 但為了保險起見，我們手動清理或依賴 Model 邏輯
        Recipe.delete(id)
        flash("食譜已刪除！", "success")
    except Exception as e:
        flash(f"刪除失敗：{str(e)}", "danger")
        
    return redirect(url_for('recipe.index'))
