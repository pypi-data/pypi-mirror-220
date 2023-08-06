from dash import dcc

full_variant = {"font-family": "Noto Sans", "maxWidth": "400px", "whiteSpace": "pre-line",
                "backgroundColor": "#000000", "borderColor": "#0000c9", "color": "#ffffff", "marginTop": "16px"}


class Tooltip(dcc.Tooltip):
    """A Tooltip component.
    A tooltip with an absolute position.

    Keyword arguments:

        - children (a list of or a singular dash component, string or number; optional):
            The contents of the tooltip.

        - id (string; optional):
            The ID of this component, used to identify dash components in
            callbacks. The ID needs to be unique across all of the components
            in an app.

        - background_color (string; default 'white'):
            Color of the tooltip background, as a CSS color string.

        - bbox (dict; optional):
            The bounding box coordinates of the item to label, in px relative
            to the positioning parent of the Tooltip component.

            `bbox` is a dict with keys:

            - x0 (number; optional)

            - x1 (number; optional)

            - y0 (number; optional)

            - y1 (number; optional)

        - border_color (string; default '#d6d6d6'):
            Color of the tooltip border, as a CSS color string.

        - className (string; default ''):
            The class of the tooltip.

        - direction (a value equal to: 'top', 'right', 'bottom', 'left'; default 'right'):
            The side of the `bbox` on which the tooltip should open.

        - loading_state (dict; optional):
            Object that holds the loading state object coming from
            dash-renderer.

            `loading_state` is a dict with keys:

            - component_name (string; optional):
                Holds the name of the component that is loading.

            - is_loading (boolean; optional):
                Determines if the component is loading or not.

            - prop_name (string; optional):
                Holds which property is loading.

        - loading_text (string; default 'Loading...'):
            The text displayed in the tooltip while loading.

        - show (boolean; default True):
            Whether to show the tooltip.

        - style (dict; optional):
            The style of the tooltip.

        - targetable (boolean; default False):
            Whether the tooltip itself can be targeted by pointer events. For
            tooltips triggered by hover events, typically this should be left
            `False` to avoid the tooltip interfering with those same events.

        - zindex (number; default 1):
            The `z-index` CSS property to assign to the tooltip. Components
            with higher values will be displayed on top of components with
            lower values."""

    def __init__(self, children=None, **tooltip_props):
        # Create a shallow copy of component props if it exists, otherwise create an empty dictionary
        tooltip_props = tooltip_props.copy() if tooltip_props else {}
        # Extract the 'style' property if it exists and remove it from component props
        style = tooltip_props.pop('style', None)
        default_style = {}
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        tooltip_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children,**tooltip_props)


class FullVariant(Tooltip):
    """
    Class representing the 'full_variant' style.

    Style:
        - font-family: Noto Sans
        - maxWidth: 400px
        - whiteSpace: pre-line
        - backgroundColor: #000000
        - borderColor: #0000c9
        - color: #ffffff
        - marginTop: 16px
    """

    def __init__(self, children=None, **tooltip_props):
        tooltip_props['style'] = full_variant
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **tooltip_props)
