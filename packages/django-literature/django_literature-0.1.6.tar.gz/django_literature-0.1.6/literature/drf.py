from typing import Any, Dict

from drf_auto_endpoint.endpoints import Endpoint
from drf_auto_endpoint.router import router


class DataTableMixin:
    endpoint: Dict[str, Any] = {}

    class Media:
        css = {"all": ("vendor/DataTables/datatables.min.css",)}
        # js = (
        #     "vendor/DataTables/datatables.min.js",
        #     "literature/js/datatablesHyperlink.js",
        #     "literature/js/admin/change_list.js",

        # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_endpoint()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["datatables_fields"] = self.get_dt_fields()
        return super().changelist_view(request, extra_context=extra_context)

    def register_endpoint(self):
        return router.register(endpoint=Endpoint(model=self.model, **self.endpoint), url="admin")

    def get_dt_fields(self):
        return []
