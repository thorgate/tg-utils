def annotate_admin_method(**kwargs):
    """
    A decorator for method-based fields and actions of ModelAdmin classes.

    Usage:

    ::

        class CustomAdmin(admin.ModelAdmin):
            def do_something(self, obj):
                # ...

            do_something.short_description = _('Do Something')
            do_something.admin_order_field = 'name'

    Can be replaced with:

    ::

        class CustomAdmin(admin.ModelAdmin):

        @annotate_admin_method(short_description=_('Do Something'), admin_order_field='name')
        def do_something(self, obj):
            # ...
    """

    def wrapped(f):
        for attr_name, attr_value in kwargs.items():
            setattr(f, attr_name, attr_value)
        return f

    return wrapped
