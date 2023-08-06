# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SolanaWalletMultiButton(Component):
    """A SolanaWalletMultiButton component.


Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- network (a value equal to: 'devnet', 'mainnet', 'testnet'; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_solana_components'
    _type = 'SolanaWalletMultiButton'
    @_explicitize_args
    def __init__(self, network=Component.REQUIRED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'network']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'network']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['network']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(SolanaWalletMultiButton, self).__init__(**args)
