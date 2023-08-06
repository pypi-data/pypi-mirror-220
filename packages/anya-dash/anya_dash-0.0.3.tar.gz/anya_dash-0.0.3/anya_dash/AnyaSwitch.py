# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AnyaSwitch(Component):
    """An AnyaSwitch component.
An Ant Design Swith component
See https://ant.design/components/switch

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- checked (boolean; optional):
    Determine whether the Switch is checked.

- checkedChildren (a list of or a singular dash component, string or number; optional):
    The content to be shown when the state is checked.

- className (string; optional):
    CSS classes to be added to the component.

- disabled (boolean; default False):
    Whether to disable the switch component.

- loading (boolean; default False):
    Loading state of switch.

- persisted_props (list of a value equal to: 'checked's; default ['checked']):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (boolean | string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- size (a value equal to: 'default', 'small'; default 'default'):
    The size of the Switch, options: default small.

- style (dict; optional):
    Inline CSS style.

- unCheckedChildren (a list of or a singular dash component, string or number; optional):
    The content to be shown when the state is unchecked."""
    _children_props = ['checkedChildren', 'unCheckedChildren']
    _base_nodes = ['checkedChildren', 'unCheckedChildren', 'children']
    _namespace = 'anya_dash'
    _type = 'AnyaSwitch'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, disabled=Component.UNDEFINED, checked=Component.UNDEFINED, checkedChildren=Component.UNDEFINED, unCheckedChildren=Component.UNDEFINED, size=Component.UNDEFINED, loading=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'checked', 'checkedChildren', 'className', 'disabled', 'loading', 'persisted_props', 'persistence', 'persistence_type', 'size', 'style', 'unCheckedChildren']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'checked', 'checkedChildren', 'className', 'disabled', 'loading', 'persisted_props', 'persistence', 'persistence_type', 'size', 'style', 'unCheckedChildren']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AnyaSwitch, self).__init__(**args)
