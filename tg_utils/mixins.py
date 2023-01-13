import re

from django.contrib.admin import helpers
from django.utils.html import escape
from django.utils.safestring import mark_safe


class OrderingOptionsMixin:
    """
    Mixin for easier implementation of ordering in Django's generic ListView.

    Add `ordering_options` to your subclass and you should be ready to go.
    Note that the user-passed query parameters are validated and you should have ascending as well as descending (with a
    starting minus-sign (-)) listed in the ordering_options.

    Use `{{ view.ordering_query_<field_name> }}` in the template to get the corresponding parameters for a header link.
    """

    ordering_query_param = "order"
    ordering_options = ()
    discard_params = ("page",)

    @staticmethod
    def ordering_to_str(ordering: tuple):
        return mark_safe(",".join(map(escape, ordering)))

    def get_ordering(self):
        requested_ordering = self.request.GET.get(self.ordering_query_param)
        if requested_ordering is not None:
            requested_ordering = tuple(o for o in requested_ordering.split(","))
            if all(map(lambda o: o in self.ordering_options, requested_ordering)):
                return requested_ordering
        return super().get_ordering()

    def __getitem__(self, item):
        current_ordering = tuple(self.get_ordering())
        if item == "ordering_query_current":
            if current_ordering is not None:
                return self.ordering_to_str(current_ordering)
            return ""

        match = re.search("^ordering_query_([_a-zA-Z]+)$", item)
        if match is not None:
            ordering = match.group(1)
            if ordering in self.ordering_options:
                if current_ordering is None or not current_ordering:
                    resulting_ordering = ordering
                else:
                    reverse = ordering == current_ordering[0]
                    ordering_possibilities = (ordering, f"-{ordering}")
                    filtered_ordering = tuple(
                        co
                        for co in current_ordering
                        if co not in ordering_possibilities
                    )
                    resulting_ordering = (
                        ordering if not reverse else f"-{ordering}",
                    ) + filtered_ordering
                query_params = self.request.GET.copy()
                for param in self.discard_params:
                    if param in query_params:
                        del query_params[param]
                query_params[self.ordering_query_param] = self.ordering_to_str(
                    resulting_ordering
                )
                return query_params.urlencode()

        return super()[item]


class ReadOnlyAdminMixin:
    """
    Mixin that makes an admin view read-only to protect a model from changes.
    Makes all fields read-only, removes save buttons, delete, and add permissions.
    """

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """customize add/edit form to remove save / save and continue"""
        extra_context = extra_context or {}
        extra_context["show_save_and_continue"] = False
        extra_context["show_save"] = False
        return super().change_view(request, object_id, extra_context=extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_readonly_fields(self, request, obj=None):
        fields = [field.name for field in obj._meta.fields]
        many_to_many = [field.name for field in obj._meta.many_to_many]
        return list(self.readonly_fields) + fields + many_to_many

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ExtendedActionsMixin:
    """
    Mixin to allow for admin actions that do not require selected model instances.

    This mixin must extend ModelAdmin.
    """

    # actions that can be executed with no items selected on the admin change list.
    # The filtered queryset displayed to the user will be used instead
    extended_actions = []

    def changelist_view(self, request, extra_context=None):
        # if a extended action is called and there's no checkbox selected, select one with
        # invalid id, to get an empty queryset
        if "action" in request.POST and request.POST["action"] in self.extended_actions:
            if not request.POST.getlist(helpers.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                post.update({helpers.ACTION_CHECKBOX_NAME: 0})
                # pylint:disable=protected-access
                request._set_post(post)

        return super().changelist_view(request, extra_context)
