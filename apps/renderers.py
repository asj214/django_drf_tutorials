from configs.renderers import BaseRenderer


class UserRenderer(BaseRenderer):
    object_label = 'user'
    pagination_object_label = 'users'
    pagination_count_label = 'count'


class ErrorRenderer(BaseRenderer):
    object_label = 'error'
    pagination_object_label = 'errors'
    pagination_count_label = 'count'