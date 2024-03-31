from django.contrib import admin

from .models import Pet, Category, Tags, Auction, Bid

admin.site.register(Pet)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Auction)
admin.site.register(Bid)