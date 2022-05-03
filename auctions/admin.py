from django.contrib import admin

from .models import User, Listings, Categories, Bids, Comments, Pictures

# Register your models here.

admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Categories)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Pictures)
