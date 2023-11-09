from sqladmin import ModelView
from .models import QueryModel


class QueryAdmin(ModelView, model=QueryModel):
    column_list = [
        QueryModel.cadastre_num,
        QueryModel.answer,
        QueryModel.created_at
    ]
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True
    name = "Запрос"
    name_plural = "Запросы"

    column_searchable_list = [QueryModel.cadastre_num]
    column_sortable_list = [QueryModel.cadastre_num]
