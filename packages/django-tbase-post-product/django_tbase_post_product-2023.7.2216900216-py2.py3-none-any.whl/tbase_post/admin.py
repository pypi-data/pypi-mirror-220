from django.contrib import admin
from django.db import models
# Register your models here.
from .models import Post,AmazonSettings
# from markdownx.admin import MarkdownxModelAdmin
# from markdownx.widgets import AdminMarkdownxWidget
from martor.widgets import AdminMartorWidget
from solo.admin import SingletonModelAdmin
from django.utils.safestring import mark_safe
from django.utils.safestring import SafeText
class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title','image_data', 'updated_on','product_name','product_id','youtube_id')
    list_filter = (['updated_on']) # 过滤字段
    search_fields =('title', 'product_name','product_id')  # 设置搜索字段
    ordering = ('-updated_on','product_name','product_id' )
    # formfield_overrides = {
    #     models.TextField: {'widget': AdminMarkdownxWidget},
    # }
    fieldsets = (
            ('产品信息', {
                'fields': ('product_name', 'product_id', 'article_img','image_data',
                            'youtube_id','youtube_player'
                            ),
            }),
            ('seo优化', {
                'fields': ('tags', 'meta_keywords', 'meta_description'),
            }),
            ('内容', {
                'fields': ['content'],
            }),
            ('资料', {
                'fields': ['data'],
            }),
        )

    readonly_fields=('image_data','youtube_player',)

    def image_data(self, obj):
        return mark_safe(f'<img width="100px" class="list_img_article_img" src="{obj.article_img}">')


    def youtube_player(self, obj):
        return SafeText(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{obj.youtube_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>')
 


 
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMartorWidget
        },
    }


admin.site.register(Post, PostAdmin)

class AmazonSettingsAdmin(SingletonModelAdmin):
    # form = ConfigurationForm):
    # form = ConfigurationForm
    # list_display = ('site_title', 'maintenance_mode')
    # 编辑页面字段定制
    fieldsets = [
        ("Base information", {
            'fields': [
                'store_id'
            ]
        }),
       
    ]
    pass
# 注册配置页面
admin.site.register(AmazonSettings, AmazonSettingsAdmin)













# class PostAdmin(MarkdownxModelAdmin):
#     list_display = ('title', 'created_on')
#     pass
# # admin.site.register(Post, PostAdmin)
# admin.site.register(Post, PostAdmin)