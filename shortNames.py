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

    gopro_prefix_map = {
        "HERO": "GoPro"
    }

    if "Galaxy" in device_name:
        parts = device_name.split()
        model = parts[1] 
        suffix = parts[2] if len(parts) > 2 else ""
        suffix_letter = galaxy_suffix_map.get(suffix, "")
        transformed_name = f"{model}{suffix_letter}"
  
    elif "HERO" in device_name:
        parts = device_name.split()
        model = parts[1] 
        transformed_name = f"{gopro_prefix_map['HERO']}{model}"
 
    else:
        transformed_name = device_name  # Restituisce il nome originale se non corrisponde ai modelli

    return transformed_name
