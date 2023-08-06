# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class LayoutUpdater(Component):
    """A LayoutUpdater component.
LayoutUpdater is a component which updates the annotations of a plotly graph.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- data (list; optional):
    The data to update the graph with, it is an object containing   -
    list containing the annotations   - list with shapes   - list
    updateData.

- gdID (string; required):
    The id of the graph-div whose traces should be updated.  .. Note:
    * if you use multiple graphs; each graph MUST have a unique id;
    otherwise we     cannot guarantee that resampling will work
    correctly.   * LayoutUpdater will determine the html-graph-div by
    performing partial matching     on the \"id\" property (using
    `gdID`) of all divs with classname=\"dash-graph\".     It will
    select the first item of that match list; so if multiple same
    graph-div IDs are used, or one graph-div-ID is a subset of the
    other (partial     matching) there is no guarantee that the
    correct div will be selected.

- initLayout (dict; optional):
    The initial layout of the component."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'layout_updater'
    _type = 'LayoutUpdater'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, gdID=Component.REQUIRED, data=Component.UNDEFINED, initLayout=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'gdID', 'initLayout']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'gdID', 'initLayout']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['gdID']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(LayoutUpdater, self).__init__(**args)
