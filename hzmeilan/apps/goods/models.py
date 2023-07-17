from django.db import models
from utils.models import BaseModels

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class GoodsCategory(BaseModels):
    """商品类别"""
    name = models.CharField(max_length=10, verbose_name='名称', help_text='名称')
    parent = models.ForeignKey('self', related_name='subs', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='父类别', help_text='父类别')

    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsChannelGroup(BaseModels):
    """商品频道组"""
    name = models.CharField(max_length=20, verbose_name='频道组名', help_text='频道组名')

    class Meta:
        db_table = 'tb_channel_group'
        verbose_name = '商品频道组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsChannel(BaseModels):
    """商品频道"""
    group = models.ForeignKey(GoodsChannelGroup, on_delete=models.CASCADE, verbose_name='频道组名', help_text='频道组名')
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='顶级商品类别', help_text='顶级商品类别')
    url = models.CharField(max_length=50, verbose_name='频道页面链接', help_text='频道页面链接')
    sequence = models.IntegerField(verbose_name='组内顺序', help_text='组内顺序')

    class Meta:
        db_table = 'tb_goods_channel'
        verbose_name = '商品频道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name


class Brand(BaseModels):
    """品牌"""
    name = models.CharField(max_length=20, verbose_name='名称', help_text='名称')
    logo = models.ImageField(verbose_name='Logo图片', help_text='Logo图片')
    first_letter = models.CharField(max_length=1, verbose_name='品牌首字母', help_text='品牌首字母')

    class Meta:
        db_table = 'tb_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SPU(BaseModels):
    """商品SPU"""
    name = models.CharField(max_length=50, verbose_name='名称', help_text='名称')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='品牌', help_text='品牌')
    category1 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat1_spu', verbose_name='一级类别',
                                  help_text='一级类别')
    category2 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat2_spu', verbose_name='二级类别',
                                  help_text='二级类别')
    category3 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='cat3_spu', verbose_name='三级类别',
                                  help_text='三级类别')
    sales = models.IntegerField(default=0, verbose_name='销量', help_text='销量')
    comments = models.IntegerField(default=0, verbose_name='评价数', help_text='评价数')
    # desc_detail = models.TextField(default='', verbose_name='详细介绍')  # 只能写文本内容
    # desc_pack = models.TextField(default='', verbose_name='包装信息')
    # desc_service = models.TextField(default='', verbose_name='售后服务')
    desc_detail = RichTextUploadingField(default='', verbose_name='详细介绍', help_text='详细介绍')  # 富文本编辑器
    desc_pack = RichTextField(default='', verbose_name='包装信息', help_text='包装信息')  # 这个方式不能上传图片
    desc_service = RichTextUploadingField(default='', verbose_name='售后服务', help_text='售后服务')

    class Meta:
        db_table = 'tb_spu'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SKU(BaseModels):
    """商品SKU"""
    name = models.CharField(max_length=50, verbose_name='名称', help_text='名称')
    caption = models.CharField(max_length=100, verbose_name='副标题', help_text='副标题')
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, verbose_name='商品', help_text='商品')
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, verbose_name='从属类别', help_text='从属类别')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价', help_text='单价')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='进价', help_text='进价')
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='市场价', help_text='市场价')
    stock = models.IntegerField(default=0, verbose_name='库存', help_text='库存')
    sales = models.IntegerField(default=0, verbose_name='销量', help_text='销量')
    comments = models.IntegerField(default=0, verbose_name='评价数', help_text='评价数')
    is_launched = models.BooleanField(default=True, verbose_name='是否上架销售', help_text='是否上架销售')
    default_image = models.ImageField(max_length=200, default='', null=True, blank=True, verbose_name='默认图片',
                                      help_text='默认图片')

    class Meta:
        db_table = 'tb_sku'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class SKUImage(BaseModels):
    """SKU图片"""
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='sku', help_text='sku')
    image = models.ImageField(verbose_name='图片', help_text='图片')

    class Meta:
        db_table = 'tb_sku_image'
        verbose_name = 'SKU图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.sku.name, self.id)


class SPUSpecification(BaseModels):
    """商品SPU规格"""
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, related_name='specs', verbose_name='商品SPU',
                            help_text='商品SPU')
    name = models.CharField(max_length=20, verbose_name='规格名称', help_text='规格名称')

    class Meta:
        db_table = 'tb_spu_specification'
        verbose_name = '商品SPU规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.spu.name, self.name)


class SpecificationOption(BaseModels):
    """规格选项"""
    spec = models.ForeignKey(SPUSpecification, related_name='options', on_delete=models.CASCADE, verbose_name='规格',
                             help_text='规格')
    value = models.CharField(max_length=20, verbose_name='选项值', help_text='选项值')

    class Meta:
        db_table = 'tb_specification_option'
        verbose_name = '规格选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s - %s' % (self.spec, self.value)


class SKUSpecification(BaseModels):
    """SKU具体规格"""
    sku = models.ForeignKey(SKU, related_name='specs', on_delete=models.CASCADE, verbose_name='sku', help_text='sku')
    spec = models.ForeignKey(SPUSpecification, on_delete=models.PROTECT, verbose_name='规格名称', help_text='规格名称')
    option = models.ForeignKey(SpecificationOption, on_delete=models.PROTECT, verbose_name='规格值', help_text='规格值')

    class Meta:
        db_table = 'tb_sku_specification'
        verbose_name = 'SKU规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s - %s' % (self.sku, self.spec.name, self.option.value)


"""
问题：
    工程没有执行迁移。 数据库中已经有响应的表了
"""


class GoodsVisitCount(BaseModels):
    """统计分类商品访问量模型类"""
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品分类', help_text='商品分类')
    count = models.IntegerField(verbose_name='访问量', default=0, help_text='访问量')
    date = models.DateField(auto_now_add=True, verbose_name='统计日期', help_text='统计日期')

    class Meta:
        db_table = 'tb_goods_visit'
        verbose_name = '统计分类商品访问量'
        verbose_name_plural = verbose_name
