import django

from django.contrib.admin.options import InlineModelAdmin
from django.forms.models import BaseInlineFormSet


# Select correct has_add_permission signature based on Django version
if django.VERSION >= (2, 1):
    class ReadOnlyAddAdminMixin:
        def has_add_permission(self, request, obj):
            return False

else:
    class ReadOnlyAddAdminMixin:
        def has_add_permission(self, request):
            return False


class AutoMediaFormSet(BaseInlineFormSet):
    @property
    def media(self):
        return self.empty_form.media


class StaticModelAdmin(ReadOnlyAddAdminMixin, InlineModelAdmin):
    """ Displays inline models as read-only.
    """

    extra = 0
    max_num = 0
    formset = AutoMediaFormSet

    exclude = ('created_by', 'created_at', 'closed_by', 'closed_at', 'updated_at', )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        base = list(super().get_readonly_fields(request, obj) or [])

        return [x.name for x in self.model._meta.fields] + base


class StaticStackedInlineModelAdmin(StaticModelAdmin):
    template = 'admin/edit_inline/no_obj_head/stacked.html'


class StaticTabularInlineModelAdmin(StaticModelAdmin):
    template = 'admin/edit_inline/no_obj_head/tabular.html'
