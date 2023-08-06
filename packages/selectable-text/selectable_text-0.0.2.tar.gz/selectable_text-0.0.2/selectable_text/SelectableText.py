# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SelectableText(Component):
    """A SelectableText component.


Keyword arguments:

- id (string; optional)

- selected_text (string; optional)

- selection_end (number; optional)

- selection_start (number; optional)

- text (string; required)

- width (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'selectable_text'
    _type = 'SelectableText'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, text=Component.REQUIRED, selected_text=Component.UNDEFINED, selection_start=Component.UNDEFINED, selection_end=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'selected_text', 'selection_end', 'selection_start', 'text', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'selected_text', 'selection_end', 'selection_start', 'text', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['text']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(SelectableText, self).__init__(**args)
