WINDOW_TITLE = "ElectriPy"
HEIGHT = 750
WIDTH = 750
RESIZABLE = True
FPS = 40
DEFAULT_FORCE_VECTOR_SCALE_FACTOR = 22e32
DEFAULT_EF_VECTOR_SCALE_FACTOR = 2e14
DEFAULT_EF_BRIGHTNESS = 105
DEFAULT_SPACE_BETWEEN_EF_VECTORS = 20
MINIMUM_FORCE_VECTOR_NORM = 10
MINIMUM_ELECTRIC_FIELD_VECTOR_NORM = 15

KEYS = {
    "clear_screen": "r",
    "show_vector_components": "space",
    "show_electric_forces_vectors": "f",
    "show_electric_field_at_mouse_position": "m",
    "show_electric_field": "e",
    "increment_electric_field_brightness": "+",
    "decrement_electric_field_brightness": "-",
    "remove_last_charge_added": "z",
    "add_last_charge_removed": "y",
}

# Text settings:
CHARGES_SIGN_FONT = "Arial"
PROTON_SIGN_FONT_SIZE = 23
ELECTRON_SIGN_FONT_SIZE = 35
VECTOR_COMPONENTS_FONT = "Arial"
VECTOR_COMPONENTS_FONT_SIZE = 13
