# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AnyaIcon(Component):
    """An AnyaIcon component.
An Ant Design Icon component
See https://ant.design/components/icon

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content to be displayed on the button.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS classes to be added to the component.

- icon (string; optional):
    Specifies the icon type.

- nClicks (number; default 0):
    Records the number of times the button has been clicked since
    rendering, default is 0.

- style (dict; optional):
    Inline CSS style."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'anya_dash'
    _type = 'AnyaIcon'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, icon=Component.UNDEFINED, nClicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'icon', 'nClicks', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'icon', 'nClicks', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AnyaIcon, self).__init__(children=children, **args)
