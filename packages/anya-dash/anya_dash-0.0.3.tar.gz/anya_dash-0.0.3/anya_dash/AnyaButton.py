# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AnyaButton(Component):
    """An AnyaButton component.
An Ant Design Button component
See https://ant.design/components/button

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content to be displayed on the button.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    CSS classes to be added to the component.

- danger (boolean; default False):
    Set the danger status of button.

- debounceWait (number; default 200):
    Used to set the debounce waiting duration (in milliseconds) for
    n_clicks listener update; default is 0.

- disabled (boolean; default False):
    Setting whether the button should be rendered as a disabled state,
    default is False.

- href (string; optional):
    href if the button is set to a link.

- info (boolean; optional):
    if the button is an info button (blue).

- n_clicks (number; default 0):
    Recording the number of times the button has been clicked since
    rendering, default is 0.

- pink (boolean; optional):
    if the button is in pink.

- shape (a value equal to: 'circle', 'round'; optional):
    Setting the shape of the button (circle: circle, round: rounded
    rectangle; default is not set, i.e., normal rectangle).

- size (a value equal to: 'small', 'middle', 'large'; default 'small'):
    Setting the size of the button, available options are 'small',
    'middle', and 'large'; default is 'middle'.

- style (dict; optional):
    Inline CSS style.

- success (boolean; default False):
    Set the success status of button, green.

- target (string; default '_blank'):
    target of the link, e.g., \"_blank\".

- type (a value equal to: 'primary', 'ghost', 'dashed', 'link', 'text', 'default'; default 'primary'):
    Setting the overall style of the button (optional options are
    primary, ghost dashed, link, text, default; default is default)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'anya_dash'
    _type = 'AnyaButton'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, type=Component.UNDEFINED, danger=Component.UNDEFINED, success=Component.UNDEFINED, pink=Component.UNDEFINED, info=Component.UNDEFINED, href=Component.UNDEFINED, target=Component.UNDEFINED, disabled=Component.UNDEFINED, shape=Component.UNDEFINED, size=Component.UNDEFINED, n_clicks=Component.UNDEFINED, debounceWait=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'danger', 'debounceWait', 'disabled', 'href', 'info', 'n_clicks', 'pink', 'shape', 'size', 'style', 'success', 'target', 'type']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'danger', 'debounceWait', 'disabled', 'href', 'info', 'n_clicks', 'pink', 'shape', 'size', 'style', 'success', 'target', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AnyaButton, self).__init__(children=children, **args)
