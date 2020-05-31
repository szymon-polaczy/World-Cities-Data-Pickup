def clear_string(element):
    element = element.replace("\n", '')
    element = element.replace("•", '')
    element = element.replace("\xa0", ' ')
    element = element.replace("/", '')
    element = element.replace("—", '')
    element = element.replace("(", '')
    element = element.replace(")", '')
    element = element.replace(":", '')
    element = element.replace("↗", '')
    element = element.replace("\ufeff", '')
    element = element.strip()

    return element