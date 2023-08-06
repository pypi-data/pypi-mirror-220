# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SolanaWalletMultiButton(Component):
    """A SolanaWalletMultiButton component.


Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- network (a value equal to: 'devnet', 'mainnet', 'testnet'; default 'mainnet')

- publicKeyState (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_solana_components'
    _type = 'SolanaWalletMultiButton'
    @_explicitize_args
    def __init__(self, network=Component.UNDEFINED, publicKeyState=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'network', 'publicKeyState']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'network', 'publicKeyState']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SolanaWalletMultiButton, self).__init__(**args)
