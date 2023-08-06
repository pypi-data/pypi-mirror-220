import dash_bootstrap_components as dbc

button_small = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                "flex-direction": "row", "justify-content": "center", "align-item": "center",
                "padding": "7px 16px", "gap": "8px", "position": "relative", "width": "103px",
                "height": "32px", "background": "#003FE2", "border-radius": "1px",
                "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                "color": "#FFFFFF", "border": "none"}

button_medium = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                 "flex-direction": "row", "justify-content": "center", "align-item": "center",
                 "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "119px",
                 "height": "48px", "background": "#003FE2", "border-radius": "1px",
                 "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                 "color": "#FFFFFF", "border": "none"}

button_large = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                "flex-direction": "row", "justify-content": "center", "align-item": "center",
                "padding": "16px 32px", "gap": "12px", "position": "relative", "width": "153px",
                "height": "56px", "background": "#003FE2", "border-radius": "1px",
                "font-weight": "700", "font-size": "17px", "line-height": "24px", "letter-spacing": "-0.5px",
                "color": "#FFFFFF", "border": "none"}

button_xss_icon = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                   "flex-direction": "row", "justify-content": "center", "align-item": "center",
                   "padding": "10px", "position": "relative", "width": "40px",
                   "height": "40px", "background": "#003FE2", "border-radius": "1px",
                   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                   "color": "#FFFFFF", "border": "none"}

button_primary = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                  "flex-direction": "row", "justify-content": "center", "align-item": "center",
                  "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                  "height": "48px", "background": "#003FE2", "border-radius": "1px",
                  "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                  "color": "#FFFFFF", "border": "none"}

button_secondary = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                    "flex-direction": "row", "justify-content": "center", "align-item": "center",
                    "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                    "height": "48px", "background": "#ffffff", "border-radius": "1px",
                    "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                    "color": "#003FE2", "border": "1px solid #003FE2"}

button_tertiary = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                   "flex-direction": "row", "justify-content": "center", "align-item": "center",
                   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                   "height": "48px", "background": "#66BFFF", "border-radius": "1px",
                   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                   "color": "#FFFFFF", "border": "none"}

button_transparent = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                      "flex-direction": "row", "justify-content": "center", "align-item": "center",
                      "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                      "height": "48px", "background": "transparent", "border-radius": "1px",
                      "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                      "color": "#003FE2", "border": "none"}

button_warning = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                  "flex-direction": "row", "justify-content": "center", "align-item": "center",
                  "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                  "height": "48px", "background": "#E84C4E", "border-radius": "1px",
                  "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                  "color": "#FFFFFF", "border": "none"}

button_floating = {"background-color": "#003FE2", "font-family": "NOTO SANS", "display": "flex",
                   "flex-direction": "row", "justify-content": "center", "align-item": "center",
                   "padding": "15px 24px", "gap": "8px", "position": "relative", "width": "95px",
                   "height": "48px", "background": "#003FE2", "border-radius": "91px",
                   "font-weight": "700", "font-size": "14px", "line-height": "18px", "letter-spacing": "-0.5px",
                   "color": "#FFFFFF", "border": "none"}


class Button(dbc.Button):
    """A Button component.
    A component for creating Bootstrap buttons with different style options. The
    Button component can act as a HTML button, link (<a>) or can be used like a
    dash_core_components style `Link` for navigating between pages of a Dash app.

    Use the `n_clicks` prop to trigger callbacks when the button has been
    clicked.

    Keyword arguments:

        - children (a list of or a singular dash component, string or number; optional):
            The children of this component.

        - id (string; optional):
            The ID of this component, used to identify dash components in
            callbacks. The ID needs to be unique across all of the components
            in an app.

        - active (boolean; optional):
            Whether button is in active state. Default: False.

        - className (string; optional):
            **DEPRECATED** Use `class_name` instead.  Often used with CSS to
            style elements with common properties.

        - class_name (string; optional):
            Often used with CSS to style elements with common properties.

        - color (string; optional):
            Button color, options: primary, secondary, success, info, warning,
            danger, link. Default: primary.

        - disabled (boolean; optional):
            Disable button (make unclickable). Default: False.

        - download (string; optional):
            Indicates that the hyperlink is to be used for downloading a
            resource.

        - external_link (boolean; optional):
            If True, the browser will treat this as an external link, forcing
            a page refresh at the new location. If False, this just changes
            the location without triggering a page refresh. Use this if you
            are observing dcc.Location, for instance. Defaults to True for
            absolute URLs and False otherwise.

        - href (string; optional):
            Pass a URL (relative or absolute) to make the menu entry a link.

        - key (string; optional):
            A unique identifier for the component, used to improve performance
            by React.js while rendering components See
            https://reactjs.org/docs/lists-and-keys.html for more info.

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

        - n_clicks (number; default 0):
            An integer that represents the number of times that this element
            has been clicked on.

        - n_clicks_timestamp (number; default -1):
            Use of *_timestamp props has been deprecated in Dash in favour of
            dash.callback_context. See \"How do I determine which Input has
            changed?\" in the Dash FAQs https://dash.plot.ly/faqs.  An integer
            that represents the time (in ms since 1970) at which n_clicks
            changed. This can be used to tell which button was changed most
            recently.

        - name (string; optional):
            The name of the button, submitted as a pair with the button’s
            value as part of the form data.

        - outline (boolean; optional):
            Set outline button style, which removes background images and
            colors for a lightweight style.

        - rel (string; optional):
            Set the rel attribute when Button is being used as a Link.

        - size (string; optional):
            Button size, options: 'lg', 'md', 'sm'.

        - style (dict; optional):
            Defines CSS styles which will override styles previously set.

        - target (string; optional):
            Target attribute to pass on to link if using Button as an external
            link.

        - title (string; optional):
            Sets the title attribute of the underlying HTML button.

        - type (a value equal to: 'button', 'reset', 'submit'; optional):
            The default behavior of the button. Possible values are:
            \"button\", \"reset\", \"submit\". If left unspecified the default
            depends on usage: for buttons associated with a form (e.g. a
            dbc.Button inside a dbc.Form) the default is \"submit\". Otherwise
            the default is \"button\".

        - value (string; optional):
            Defines the value associated with the button’s name when it’s
            submitted with the form data. This value is passed to the server
            in params when the form is submitted."""

    def __init__(self, children=None, **button_props):
        # Create a shallow copy of component props if it exists, otherwise create an empty dictionary
        button_props = button_props.copy() if button_props else {}
        # Extract the 'style' property if it exists and remove it from component props
        style = button_props.pop('style', None)
        default_style = {}
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonSmall(Button):
    """
    Class representing the 'button_small' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 7px 16px
        - gap: 8px
        - position: relative
        - width: 103px
        - height: 32px
        - background: #003FE2
        - border-radius: 1px
        - font-weight: 700
        - font-size: 14px
        - line-height: 18px
        - letter-spacing: -0.5px
        - color: #FFFFFF
        - border: none
    """

    def __init__(self, children=None, **button_props):
        # Create a shallow copy of component props if it exists, otherwise create an empty dictionary
        button_props = button_props.copy() if button_props else {}
        # Extract the 'style' property if it exists and remove it from component props
        style = button_props.pop('style', None)
        default_style = button_small
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonMedium(Button):
    """
    Class representing the 'button_medium' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 15px 24px
        - gap: 8px
        - position: relative
        - width: 119px
        - height: 48px
        - background: #003FE2
        - border-radius: 1px
        - font-weight: 700
        - font-size: 14px
        - line-height: 18px
        - letter-spacing: -0.5px
        - color: #FFFFFF
        - border: none
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_medium
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonLarge(Button):
    """
    Class representing the 'button_large' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 16px 32px
        - gap: 12px
        - position: relative
        - width: 153px
        - height: 56px
        - background: #003FE2
        - border-radius: 1px
        - font-weight: 700
        - font-size: 17px
        - line-height: 24px
        - letter-spacing: -0.5px
        - color: #FFFFFF
        - border: none
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_large
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonXssIcon(Button):
    """
    Class representing the 'button_xss_icon' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 15px 24px
        - gap: 8px
        - position: relative
        - width: 119px
        - height: 48px
        - background: #003FE2
        - border-radius: 1px
        - font-weight: 700
        - font-size: 14px
        - line-height: 18px
        - letter-spacing: -0.5px
        - color: #FFFFFF
        - border: none
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_xss_icon
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonPrimary(Button):
    """
    Class representing the 'button_primary' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 15px 24px
        - gap: 8px
        - position: relative
        - width: 119px
        - height: 48px
        - background: #003FE2
        - border-radius: 1px
        - font-weight: 700
        - font-size: 14px
        - line-height: 18px
        - letter-spacing: -0.5px
        - color: #FFFFFF
        - border: none
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_primary
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonSecondary(Button):
    """
    Class representing the 'button_secondary' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 15px 24px
        - gap: 8px
        - position: relative
        - width: 95px
        - height: 48px
        - background: #ffffff
        - border-radius: 1px
        - font-weight: 700
        - font-size: 14px
        - line-height: 18px
        - letter-spacing: -0.5px
        - color: #003FE2
        - border: 1px solid #003FE2
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_secondary
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonTertiary(Button):
    """
    Class representing the 'button_tertiary' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 15px 24px
        - gap: 8px
        - position: relative
        - width: 95px
        - height: 48px
        - background: #66BFFF
        - border-radius: 1px
        - font-weight: 700
        - font-size: 14px
        - line-height: 18px
        - letter-spacing: -0.5px
        - color: #FFFFFF
        - border: none
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_tertiary
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonTransparent(Button):
    """
    Class representing the 'button_transparent' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 15px 24px
        - gap: 8px
        - position: relative
        - width: 95px
        - height: 48px
        - background: transparent
        - border-radius: 1px
        - font-weight: 700
        - font-size: 14px
        - line-height: 18px
        - letter-spacing: -0.5px
        - color: #003FE2
        - border: none
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_transparent
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonWarning(Button):
    """
    Class representing the 'button_warning' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 15px 24px
        - gap: 8px
        - position: relative
        - width: 95px
        - height: 48px
        - background: #E84C4E
        - border-radius: 1px
        - font-weight: 700
        - font-size: 14px
        - line-height: 18px
        - letter-spacing: -0.5px
        - color: #FFFFFF
        - border: none
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_warning
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)


class ButtonFloating(Button):
    """
    Class representing the 'button_floating' style.

    Style:
        - background-color: #003FE2
        - font-family: NOTO SANS
        - display: flex
        - flex-direction: row
        - justify-content: center
        - align-item: center
        - padding: 15px 24px
        - gap: 8px
        - position: relative
        - width: 95px
        - height: 48px
        - background: #003FE2
        - border-radius: 91px
        - font-weight: 700
        - font-size: 14px
        - line-height: 18px
        - letter-spacing: -0.5px
        - color: #FFFFFF
        - border: none
    """

    def __init__(self, children=None, **button_props):
        button_props = button_props.copy() if button_props else {}
        style = button_props.pop('style', None)
        default_style = button_floating
        # If style is not None, update the default_style dictionary with the contents of the style dictionary
        if style is not None:
            default_style.update(style)
        button_props['style'] = default_style
        # Call the __init__ method of the parent class with the children and component props arguments
        super().__init__(children=children, **button_props)
