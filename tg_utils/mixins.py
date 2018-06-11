import re

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
    ordering_query_param = 'order'
    ordering_options = ()
    discard_params = ('page',)

    @staticmethod
    def ordering_to_str(ordering: tuple):
        return mark_safe(','.join(map(escape, ordering)))

    def get_ordering(self):
        requested_ordering = self.request.GET.get(self.ordering_query_param)
        if requested_ordering is not None:
            requested_ordering = tuple(o for o in requested_ordering.split(','))
            if all(map(lambda o: o in self.ordering_options, requested_ordering)):
                return requested_ordering
        return super().get_ordering()

    def __getitem__(self, item):
        current_ordering = tuple(self.get_ordering())
        if item == 'ordering_query_current':
            if current_ordering is not None:
                return self.ordering_to_str(current_ordering)
            return ''

        match = re.search('^ordering_query_([_a-zA-Z]+)$', item)
        if match is not None:
            ordering = match.group(1)
            if ordering in self.ordering_options:
                if current_ordering is None or not current_ordering:
                    resulting_ordering = ordering
                else:
                    reverse = ordering == current_ordering[0]
                    ordering_possibilities = (ordering, '-{}'.format(ordering))
                    filtered_ordering = tuple(co for co in current_ordering if co not in ordering_possibilities)
                    resulting_ordering = (ordering if not reverse else '-{}'.format(ordering),) + filtered_ordering
                query_params = self.request.GET.copy()
                for param in self.discard_params:
                    if param in query_params:
                        del query_params[param]
                query_params[self.ordering_query_param] = self.ordering_to_str(resulting_ordering)
                return query_params.urlencode()

        return super()[item]
