from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.GoodsCategory)
admin.site.register(models.GoodsChannelGroup)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Brand)
admin.site.register(models.SPU)
admin.site.register(models.SKU)
admin.site.register(models.SKUImage)
admin.site.register(models.SPUSpecification)
admin.site.register(models.SpecificationOption)
admin.site.register(models.SKUSpecification)
admin.site.register(models.GoodsVisitCount)
