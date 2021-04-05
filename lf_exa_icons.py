import requests


def fetch() -> str:
    """Fetch the exa source file."""
    try:
        return requests.get("https://raw.githubusercontent.com/ogham/exa/005a174e60be96e8d8b30a2aa62d12b9cea8a62d/src/output/icons.rs").content.decode('utf-8')
    except:
        raise IOError


def parse_file_icons(source: str) -> tuple[dict[str, str], str, str]:
    """Return a dictionary that maps file extensions to their icons."""
    ext_so_far = {}
    source_iter = iter(source.split('\n'))

    while next(source_iter).strip() != 'match file.name.as_str() {':
        pass
    curr_line = next(source_iter)
    while curr_line.strip()[0] != '_':
        curr_line = next(source_iter)
    folder = curr_line.strip()[-1]
    while next(source_iter).strip() != 'match ext.as_str() {':
        pass
    curr_line = next(source_iter)
    while curr_line.strip()[0] != '_':
        quot_index = curr_line.strip()[1:].index('"')
        ext = curr_line.strip()[1:quot_index + 1]
        icon = curr_line.strip()[-1]
        ext_so_far[ext] = icon
        curr_line = next(source_iter)
    file = curr_line.strip()[-1]
    return (ext_so_far, file, folder)


def format_icons(icons: tuple[dict[str, str], str, str]) -> str:
    """Return icons in formatted string."""
    icons_dict = icons[0]
    _, file, folder = icons
    special_declaration_map = {'ln': '\uf481', 'or': '\uf481', 'tw': folder, 'ow': folder, 'st': folder, 'di': folder,
                               'pi': file, 'so': file, 'bd': file, 'cd': file, 'su': file, 'sg': file, 'ex': file, 'fi': file}
    special_declarations = '\n'.join(
        [f'{key}={special_declaration_map[key]}:\\' for key in special_declaration_map])
    icon_declarations = '\n'.join(
        [f'*.{ext}={icons_dict[ext]}:\\' for ext in icons_dict])
    return f'export LF_ICONS="\\\n{special_declarations}\n{icon_declarations}\n"'


def main() -> None:
    """Main process."""
    source = fetch()
    icons = parse_file_icons(source)
    print(format_icons(icons))


if __name__ == '__main__':
    main()
