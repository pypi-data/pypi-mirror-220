from django.contrib import admin
from .models import BabelfishProfile
from djangoldp.admin import DjangoLDPAdmin

class BabelfishProfileAdmin(DjangoLDPAdmin):
    list_display = ("user", "babelfish_user_id", "client_id", "client_secret", "organisation_id")
    exclude = (
        "urlid",
        "is_backlink",
        "allow_create_backlink",
    )
    search_fields = ["user", "organisation_id", "babelfish_user_id"]


admin.site.register(BabelfishProfile, BabelfishProfileAdmin)

