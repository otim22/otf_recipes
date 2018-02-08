from flask import flash, redirect, render_template, url_for, abort
from flask_login import login_required, current_user

from . import admin
from forms import CategoryForm, RecipeForm, UserAssignForm
from .. import db
from ..models import Category, Recipe, User


def check_admin():
    if not current_user.is_admin:
        """
        Prevent non-admins from accessing the page
        """
        abort(403)


@admin.route('/categories', methods=['GET', 'POST'])
@login_required
def list_categories():
    """
    List all departments
    """
    check_admin()

    categories = Category.query.all()

    return render_template('admin/categories/categories.html',
                           categories=categories, title="Categories")


@admin.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """
    Add a categories to the database
    """
    check_admin()

    add_category = True

    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data,
                            description=form.description.data)
        try:
            db.session.add(category)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case category name already exists
            flash('Error: category name already exists.')

        return redirect(url_for('admin.list_categories'))

    # redirect to categories page
    return render_template('admin/categories/category.html',
                           action="Add", add_category=add_category,
                           form=form, title="Add Category")


@admin.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    """
    Edit a category
    """
    check_admin()
    
    add_category = False
    
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data,
        category.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the categories page
        return redirect(url_for('admin.list_categories'))

    form.description.data = category.description
    form.name.data = category.name
    return render_template('admin/categories/category.html', action="Edit",
                           add_category=add_category, form=form,
                           category=category, title="Edit Category")


@admin.route('/categories/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_category(id):
    """
    Delete a category from the database
    """
    check_admin()

    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the categories page
    return redirect(url_for('admin.list_categories'))

    return render_template(title="Delete Category")


@admin.route('/recipes', methods=['GET', 'POST'])
@login_required
def list_recipes():
    """
    List all recipes
    """
    check_admin()
    
    recipes = Recipe.query.all()
    
    return render_template('admin/recipes/recipes.html', recipes=recipes,
                           title="Recipes")


@admin.route('/recipes/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    """
    Adds a recipe to the database
    """
    check_admin()

    add_recipe = True

    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(name=form.name.data,
                        description=form.description.data)
        try: 
            db.session.add(recipe)
            db.session.commit()
            flash('You have successfully added a new recipe.')
        except:
            flash('Error: category name already exists.')

        # redirect to the recipes page
        return redirect(url_for('admin.list_recipes'))

    # load recipe template
    return render_template('admin/recipes/recipe.html', add_recipe=add_recipe,
                           form=form, title='Add Recipe')


@admin.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    """
    Adds a recipe
    """
    check_admin()

    add_recipe = False

    recipe = Recipe.query.get_or_404(id)
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the recipe.')

        # redirect to the recipes page
        return redirect(url_for('admin.list_recipes'))

    form.description.data = recipe.description
    form.name.data = recipe.name
    return render_template('admin/recipes/recipe.html', add_recipe=add_recipe,
                           form=form, title="Edit Recipe")


@admin.route('/recipes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_recipe(id):
    """
    Deletes a recipe
    """
    check_admin()

    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    flash('You have successfully deleted the department.')

    return redirect(url_for('admin.list_recipes'))

    return render_template(title='Delete Recipe')


@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html', users=users,
                           title="Users")


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign a category and a recipe to an user
    """
    check_admin()

    user = User.query.get_or_404(id)

    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.category = form.category.data
        user.recipe = form.recipe.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a department and recipe.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html', user=user,
                           form=form, title='Assign User')








