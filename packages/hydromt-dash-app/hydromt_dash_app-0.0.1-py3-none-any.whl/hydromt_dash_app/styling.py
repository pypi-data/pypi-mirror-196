def button_style(**kwargs):
    style_dict = {
        # "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgb(0 0 0 / 19%)"
        "backgroundColor": "#080C80",
        "borderColor": "#080C80",
    }
    if kwargs:
        style_dict.update(kwargs)
    return style_dict


def SIDEBAR_STYLE(**kwargs):
    style_dict = {
        "display": "flex",
        "width": "100%",
        "margin": "2rem",
        "padding": "1rem 1rem",
        "background-color": "#f0f2f4",
        "height": "85vh",
        "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgb(0 0 0 / 19%)",
        "justifyContent": "center",
        "alignItems": "center",
    }
    style_dict.update(kwargs)
    return style_dict


def center_align():
    return {"display": "block", "margin": "5px auto", "textAlign": "center"}


def sidebar_input_style(**kwargs):
    style_dict = {"margin": " 0.2rem 0rem 1rem"}
    style_dict.update(kwargs)
    return style_dict


def sidebar_row_button_style(**kwargs):
    style_dict = {
        "width": "60%",
        "justifyContent": "center",
        "display": "flex",
        "margin": "auto",
    }
    style_dict.update(kwargs)
    return style_dict
