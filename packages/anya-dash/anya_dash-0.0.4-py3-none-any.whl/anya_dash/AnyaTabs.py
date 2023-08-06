# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AnyaTabs(Component):
    """An AnyaTabs component.
An Ant Design Tag component
See https://ant.design/components/tabs

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Content to display if itemContent is set to False.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- activeKey (string; optional):
    Current TabPane's key.

- centered (boolean; default False):
    Centers tabs.

- childCardBorder (boolean; default True):
    Whether the child card bordy should have borders.

- childCardStyle (dict; default {borderTop: 0}):
    Inline CSS style of the child card body.

- className (string; optional):
    CSS classes to be added to the component.

- defaultActiveKey (string; optional):
    Initial active TabPane's key, if activeKey is not set.

- disabledTabKeys (list of strings; optional):
    Array of keys of tabs to be disabled.

- itemContent (boolean; default False):
    Whether to display children content under each item, defaults to
    False.

- items (list of dicts; optional):
    Tab items.

    `items` is a list of dicts with keys:

    - children (a list of or a singular dash component, string or number; optional)

    - closable (boolean; optional)

    - disabled (boolean; optional)

    - forceRender (boolean; optional)

    - key (string; optional)

    - label (a list of or a singular dash component, string or number; optional)

- size (a value equal to: 'small', 'default', 'large'; default 'small'):
    Preset tab bar size.

- style (dict; optional):
    Inline CSS style.

- tabBarGutter (number; optional):
    The gap between tabs.

- tabPosition (a value equal to: 'top', 'left', 'right', 'bottom'; default 'top'):
    Position of tabs.

- type (a value equal to: 'line', 'card', ' editable-card'; default 'card'):
    Type of the tabs, only card and line types are avaialable at this
    moment.

- wrapperStyle (dict; optional):
    Inline CSS style of the entire wrapper if itemContent is set to
    False."""
    _children_props = ['items[].label', 'items[].children']
    _base_nodes = ['children']
    _namespace = 'anya_dash'
    _type = 'AnyaTabs'
    @_explicitize_args
    def __init__(self, children=None, items=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, type=Component.UNDEFINED, size=Component.UNDEFINED, defaultActiveKey=Component.UNDEFINED, activeKey=Component.UNDEFINED, disabledTabKeys=Component.UNDEFINED, tabPosition=Component.UNDEFINED, centered=Component.UNDEFINED, tabBarGutter=Component.UNDEFINED, itemContent=Component.UNDEFINED, wrapperStyle=Component.UNDEFINED, childCardBorder=Component.UNDEFINED, childCardStyle=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'activeKey', 'centered', 'childCardBorder', 'childCardStyle', 'className', 'defaultActiveKey', 'disabledTabKeys', 'itemContent', 'items', 'size', 'style', 'tabBarGutter', 'tabPosition', 'type', 'wrapperStyle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'activeKey', 'centered', 'childCardBorder', 'childCardStyle', 'className', 'defaultActiveKey', 'disabledTabKeys', 'itemContent', 'items', 'size', 'style', 'tabBarGutter', 'tabPosition', 'type', 'wrapperStyle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AnyaTabs, self).__init__(children=children, **args)
