from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField


from ..models import Category, Recipe


class CategoryForm(FlaskForm):
    """
    Form for admin to add or edit a category
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RecipeForm(FlaskForm):
    """"
    Form for admin to add or edit a recipe
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
    """
    Form for admin to assign category and recipes to users
    """
    category = QuerySelectField(query_factory=lambda: Category.query.all(),
                                get_label="name")
    recipe = QuerySelectField(query_factory=lambda: Recipe.query.all(),
                                get_label="name")
    submit = SubmitField('Submit')



        
