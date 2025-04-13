def L2_color_luminance(a, b):  # Lenght between 2 points
    """
    Calcula una combinación de distancia euclidiana en el espacio de color y distancia Manhattan
    """
    color_distance = np.sqrt(np.sum((a - b) ** 2)) #L2
    luminance_distance = abs(np.mean(a) - np.mean(b)) #L1
    return color_distance + luminance_distance