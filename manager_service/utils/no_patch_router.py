from rest_framework.routers import DefaultRouter


class NoPatchRouter(DefaultRouter):
    """
    Router class that disables the PATCH method.
    """

    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)

        if 'patch' in bound_methods.keys():
            del bound_methods['patch']

        return bound_methods
