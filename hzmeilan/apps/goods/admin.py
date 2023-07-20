from django.contrib import admin

from . import models
from celery_tasks.html.tasks import generate_static_list_search_html, generate_static_sku_detail_html


class GoodsCategoryAdmin(admin.ModelAdmin):
    """ 商品类别模型站点管理 """

    def save_model(self, request, obj, form, change):
        """
        当点击admin中的保存按钮时会调用次方法
        @param request: 保存时本次请求的对象
        @param obj: 本次要保存的模型对象
        @param form: admin中表单
        @param change: 是否更改 True
        @return:
        """
        obj.save()
        generate_static_list_search_html.delay()

    def delete_model(self, request, obj):
        obj.delete()
        generate_static_list_search_html.delay()


class SKUImageModelAdmin(admin.ModelAdmin):
    """ 商品图片站点管理类 """

    def save_model(self, request, obj, form, change):
        """
        admin保存图片
        @param request: 请求体
        @param obj: 图片模型对象
        @param form:
        @param change:
        @return:
        """
        obj.save()
        sku = obj.sku
        if not sku.default_image:
            sku.default_image = obj.image
            sku.save()
        generate_static_sku_detail_html(sku.id)

    def delete_model(self, request, obj):
        obj.delete()
        sku = obj.sku
        generate_static_sku_detail_html.delay(sku.id)


# Register your models here.
admin.site.register(models.GoodsCategory, GoodsCategoryAdmin)
admin.site.register(models.GoodsChannelGroup)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Brand)
admin.site.register(models.SPU)
admin.site.register(models.SKU)
admin.site.register(models.SKUImage, SKUImageModelAdmin)
admin.site.register(models.SPUSpecification)
admin.site.register(models.SpecificationOption)
admin.site.register(models.SKUSpecification)
admin.site.register(models.GoodsVisitCount)
