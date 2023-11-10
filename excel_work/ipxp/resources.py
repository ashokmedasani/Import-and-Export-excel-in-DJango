from import_export import resources
from .models import person

class personResources(resources.ModelResource):
    class meta:
        model = person