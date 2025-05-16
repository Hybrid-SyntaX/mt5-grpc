import logging
from typing import Literal


def auto_map(source_obj, dest_type: type, map_direction: Literal['left','right','both'] = 'left', manual:dict=None):
    if manual is None:
        manual = {}
    dest_obj = dest_type()

    source_public_attr = list(filter(lambda x: not x.startswith('_'), dir(source_obj)))
    destination_public_attr = list(filter(lambda x: not x.startswith('_'), dir(dest_obj)))
    match map_direction:
        case 'left':
            public_attr = source_public_attr
        case 'right':
            public_attr = destination_public_attr
        case 'join':
            public_attr = list(set(source_public_attr).intersection(destination_public_attr))
        case _:
            public_attr = list(set(source_public_attr).intersection(destination_public_attr))

    for attr_name in public_attr:
        try:
            attr_value = getattr(source_obj, attr_name)# if hasattr(source_obj,attr_name) else None
            if hasattr(dest_obj, attr_name) and attr_value is not None:
                if attr_name in manual:
                    manual[attr_name](dest_obj,attr_value)
                else:
                    setattr_typed(dest_obj, attr_name, attr_value)
        except Exception as e:
            logging.error(f'Error occurred during mapping {attr_name}, {attr_value}: {e}')

    return dest_obj

def setattr_typed(dest_obj, attr_name, attr_value):
    # Get current attribute to infer type
    current_value = getattr(dest_obj, attr_name, None)
    if current_value is not None:
        expected_type = type(current_value)
        try:
            casted_value = expected_type(attr_value)
        except Exception as e:
            raise ValueError(f"Failed to cast {attr_value} to {expected_type}: {e}")
    else:
        # If attribute doesn't exist or is None, fallback to setting directly
        casted_value = attr_value

    setattr(dest_obj, attr_name, casted_value)
