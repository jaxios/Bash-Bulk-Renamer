import re

def transform_device_name(device_name):
    """Shortens certains devices names

    Args:
        device_name (str): Name of the device

    Returns:
        str: shortened name
    """
    galaxy_suffix_map = {
        "Ultra": "U",
        "Plus": "P",
        "": ""
    }

    if device_name == "SM-G975F":
        return "S10P"

    if "Galaxy" in device_name:
        parts = device_name.split()
        model = parts[1] 
        suffix = parts[2] if len(parts) > 2 else ""
        suffix_letter = galaxy_suffix_map.get(suffix, "")
        transformed_name = f"{model}{suffix_letter}"
  
    elif "HERO" in device_name:
        parts = device_name.split()
        model = re.sub("[^0-9]", "", parts[0])
        transformed_name = f"GoPro{model}"
 
    else:
        transformed_name = device_name

    return transformed_name
