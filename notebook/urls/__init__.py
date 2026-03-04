from .notebook_urls import urlpatterns as notebook_urls
from .notebook_fields_urls import urlpatterns as notebook_fields_urls
from .notebook_data_urls import urlpatterns as notebook_data_urls

urlpatterns = notebook_urls + notebook_fields_urls + notebook_data_urls
