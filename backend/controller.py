import json, os

def load_settings():
    with open(os.path.join(os.getcwd(), "data", "settings.json"), "r", encoding='utf-8') as f:
        settings = json.load(f)
    return settings

def save_sattings(new_settings):
    with open(os.path.join(os.getcwd(), "data", "settings.json"), "r", encoding='utf-8') as file:
        elements = json.load(file)
    
    elements.append(new_settings)

    with open(os.path.join(os.getcwd(), "data", "settings.json"), "w", encoding='utf-8') as settings:
        json.dump(elements, settings, indent=4, ensure_ascii=False)

def clear_settings():
    with open(os.path.join(os.getcwd(), "data", "settings.json"), "w", encoding='utf-8') as settings:
        json.dump([], settings, indent=4, ensure_ascii=False)


def save_data(text):
    with open(os.path.join(os.getcwd(), "data", "save.json"), "r", encoding='utf-8') as file:
        elements = json.load(file)

    name = text[:text.find(',')]
    age = text[text.find(',')+2:text.find(',')+4]
    link = 'https://' + text[text.find('vk.com/'):text.find('\n')]
    new_element ={
        "name": name,
        "age": age,
        "url": link
    }
    elements.append(new_element)

    with open(os.path.join(os.getcwd(), "data", "save.json"), "w", encoding='utf-8') as settings:
        json.dump(elements, settings, indent=4, ensure_ascii=False)

def load_data():
    with open(os.path.join(os.getcwd(), "data", "save.json"), "r", encoding='utf-8') as f:
        data = json.load(f)
    return data

def clear_data():
    with open(os.path.join(os.getcwd(), "data", "save.json"), "w", encoding='utf-8') as settings:
        json.dump([], settings, indent=4, ensure_ascii=False)
