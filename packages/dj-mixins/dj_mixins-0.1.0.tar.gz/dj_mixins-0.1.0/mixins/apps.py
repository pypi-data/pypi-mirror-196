""" App Configuration """


from django.apps import AppConfig


class MixinsConfig(AppConfig):
    """ Configuration for mixins """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mixins'
