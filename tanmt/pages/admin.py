import nested_admin
from admin_ordering.admin import OrderableAdmin
from components.admin import (
    AbstractEditorialAdmin,
    AbstractEmbedAdmin,
    AbstractImageAdmin,
    AbstractImageWithTextAdmin,
    AbstractQuoteAdmin,
    AbstractTableAdmin,
)

from tanmt.admin import tanmt_admin

from .models import (
    Component,
    Editorial,
    Embed,
    Image,
    ImageWithText,
    Page,
    Quote,
    Table,
)


class EditorialAdmin(AbstractEditorialAdmin):
    model = Editorial


class EmbedAdmin(AbstractEmbedAdmin):
    model = Embed


class ImageAdmin(AbstractImageAdmin):
    model = Image


class ImageWithTextAdmin(AbstractImageWithTextAdmin):
    model = ImageWithText


class QuoteAdmin(AbstractQuoteAdmin):
    model = Quote


class TableAdmin(AbstractTableAdmin):
    model = Table


class ComponentAdmin(nested_admin.NestedStackedInline):
    model = Component
    extra = 0
    inlines = [
        EditorialAdmin,
        EmbedAdmin,
        ImageAdmin,
        ImageWithTextAdmin,
        QuoteAdmin,
        TableAdmin,
    ]
    # disable drag/drop sorting, in order for the ordering value to work
    # when using the following var, the order set in the admin is ignored
    # sortable_field_name = 'order'


class PageAdmin(nested_admin.NestedModelAdmin):
    list_display = [
        'title',
        'slug',
        'display_in_header',
        'display_in_footer',
    ]
    search_fields = ['title']
    ordering = ['slug']
    inlines = [ComponentAdmin]

    # if adding, hide readonly fixture detail field
    def get_readonly_fields(self, request, obj):
        return [] if obj is None else ['slug']

    # if adding, hide slug select field
    def get_exclude(self, request, obj):
        return ['author'] if obj is None else ['author', 'slug']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

    # base PageAdmin form doesn't contain files,
    # so doesn't register as requring multipart support (`has_file_field`)
    # this fix ensures `enctype="multipart/form-data"` is added to HTML form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.is_multipart = lambda n: True
        return form


class TopLevelPageOrderingAdmin(OrderableAdmin, nested_admin.NestedModelAdmin):
    list_display = [
        'title',
        'display_in_header',
        'display_in_footer',
        'order',
    ]
    list_editable = ('order', )
    list_display_links = None
    ordering_field = 'order'
    readonly_fields = ('order', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TopLevelPage(Page):

    class Meta:
        proxy = True
        verbose_name_plural = "Reorder pages for header/footer menus"


tanmt_admin.register(Page, PageAdmin)
tanmt_admin.register(TopLevelPage, TopLevelPageOrderingAdmin)
