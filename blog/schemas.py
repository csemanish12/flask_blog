from flask_marshmallow import Schema
from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy import ModelSchema
from blog.models import Post


class PostSchema(ModelSchema):
    class Meta:
        include_fk = True
        model = Post

    title = fields.Str(required=True)
    content = fields.Str(required=True)


class PostPlainSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
