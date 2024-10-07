def transform_device_name(device_name):
    # Mappa per i suffissi di Galaxy
    galaxy_suffix_map = {
        "Ultra": "U",
        "Plus": "P",
        "": ""
    }

    # Mappa per i dispositivi GoPro
    gopro_prefix_map = {
        "HERO": "GoPro"
    }

    # Controlla se il nome è di un dispositivo Galaxy
    if "Galaxy" in device_name:
        parts = device_name.split()
        model = parts[1]  # Il modello è sempre il secondo elemento
        suffix = parts[2] if len(parts) > 2 else ""
        suffix_letter = galaxy_suffix_map.get(suffix, "")
        transformed_name = f"{model}{suffix_letter}"
    
    # Controlla se il nome è di un dispositivo GoPro
    elif "HERO" in device_name:
        parts = device_name.split()
        model = parts[1]  # Il numero è sempre il secondo elemento
        transformed_name = f"{gopro_prefix_map['HERO']}{model}"
    
    else:
        transformed_name = device_name  # Restituisce il nome originale se non corrisponde ai modelli

    return transformed_name
