import json
import colorsys
import re
import glob
from os import path


def repl(match):
    hex_rep = match.group(1)
    parsed_hex = [int(hex_rep[index:index + 2], 16) for index in range(6)[::2]]
    hsv = list(colorsys.rgb_to_hsv(*parsed_hex))
    hsv[0] += 0.5
    modified_rgb = colorsys.hsv_to_rgb(*hsv)
    string_rgb = '#' + \
        ''.join(map(lambda x: str(format(round(x), 'x').zfill(2)), modified_rgb))
    return string_rgb


def get_input(prompt, condition):
    while True:
        user_input = input(prompt)
        if condition(user_input):
            return user_input
        print('Sorry. I didn\'t understand.')


parent_options = glob.glob('./parent_themes/*')
[print(f'( {index + 1} ) {path.basename(parent)}')
 for index, parent in enumerate(parent_options)]
parent_theme = parent_options[int(get_input(
    '\n  Choose theme number: ', lambda value: 0 < int(value) <= len(parent_options))) - 1]

parent_brightness = 'vs' + '-dark' * (get_input(
    '\n  Dark or light? (d/l) ', lambda value: value in ['d', 'l']) == 'd')

theme_display_name = input('\n  Theme name: ')
theme_path = './themes/' + theme_display_name.lower().replace(' ', '-') + \
    '-color-theme.json'

with open(parent_theme, 'r') as theme_file:
    theme = theme_file.read()
    generated_theme = re.sub('#([0-9a-fA-F]{6})', repl, theme)
    with open(theme_path, 'w') as generated_file:
        generated_file.write(generated_theme)

with open('./package.json', 'r') as package_json:
    generated_file = json.load(package_json)
    generated_file['contributes']['themes'].append({
        'label': theme_display_name,
        'uiTheme': parent_brightness,
        'path': theme_path
    })
    with open('./package.json', 'w') as generated_package_json:
        json.dump(generated_file, generated_package_json, indent=2)
