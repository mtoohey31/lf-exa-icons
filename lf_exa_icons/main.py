import subprocess
import re
import os
import argparse as ap
from tree_sitter import Language, Parser, Node
import requests


RS_LANGUAGE = Language('build/tree-sitter-rust.so', 'rust')


def get_exa_version() -> str | None:
    """Determine the currently installed exa version."""
    try:
        output = subprocess.check_output(['exa', '--version']).decode('utf8')
        if re.findall(r'\[\+git\]', output):
            return None
        else:
            return re.findall(r'v\d+\.\d+\.\d+', output)[0]
    except FileNotFoundError:
        raise OSError('exa was not found on the path')


def fetch_source(version: str | None = None) -> bytes:
    """Fetch the current exa source file from GitHub."""
    if version is None:
        version = get_exa_version()
    if version is None:
        return requests.get(
            'https://raw.githubusercontent.com/ogham/exa/master/src/output/icons.rs'
        ).content
    else:
        potential_shas = [tag['commit']['sha'] for tag in requests.get(
            "https://api.github.com/repos/ogham/exa/tags").json()
            if tag['name'] == version]
        if len(potential_shas) == 0:
            raise ValueError(
                'The detected exa version does not match any GitHub release tags')
        elif len(potential_shas) > 1:
            raise ValueError(
                'The detected exa version matches multiple GitHub release tags')
        else:
            source_sha = potential_shas[0]
            return requests.get(
                f'https://raw.githubusercontent.com/ogham/exa/{source_sha}/src/output/icons.rs'
            ).content


def parse_source(source: bytes) -> tuple[dict[str, str], str, str]:
    """Parse the exa source code and return a tuple containing a mapping of
    extensions to icons, the default file icon, and the default directory icon."""
    parser = Parser()
    parser.set_language(RS_LANGUAGE)
    tree = parser.parse(source)

    extension_match_block_query = RS_LANGUAGE.query("""
(match_expression
  value: (call_expression
                 function: (field_expression value: (identifier) @fx
                                                  (#match? @fx "^ext$")
                                           field: (field_identifier) @fi
                                                  (#match? @fi "^as_str$")
                           )
         )
  body: (match_block) @match_block
)
""")
    directory_match_block_query = RS_LANGUAGE.query("""
(match_expression
  value: (call_expression
                 function: (field_expression
                             value: (field_expression
                                      value: (identifier) @i
                                             (#match? @i "^file$")
                                      field: (field_identifier) @fi1
                                             (#match? @fi1 "^name$")
                                    )
                             field: (field_identifier) @fi2
                                    (#match? @fi2 "^as_str$")
                           )
         )
  body: (match_block) @match_block
)
""")

    extension_match_blocks = [match[0] for match in extension_match_block_query.captures(
        tree.root_node) if match[1] == 'match_block']
    directory_match_blocks = [match[0] for match in directory_match_block_query.captures(
        tree.root_node) if match[1] == 'match_block']

    if len(extension_match_blocks) == 1 and len(directory_match_blocks) == 1:
        return (*parse_match_block(extension_match_blocks[0], source),
                parse_match_block(directory_match_blocks[0], source)[1])
    elif len(extension_match_blocks) == 1:
        directory_char_literal_query = RS_LANGUAGE.query("""
(if_expression
  condition: (call_expression
               function: (field_expression value: (identifier) @fx
                                                  (#match? @fx "^file$")
                                           field: (field_identifier) @fi
                                                  (#match? @fi "^is_directory$")
                         )
             )
  consequence: (block (char_literal) @directory_icon )
)
""")
        directory_char_literals = [match[0] for match in directory_char_literal_query.captures(
            tree.root_node) if match[1] == 'directory_icon']
        if len(directory_char_literals) == 1:
            return (*parse_match_block(extension_match_blocks[0], source),
                    parse_icon(get_node_string(directory_char_literals[0],
                                               source)))

    raise ValueError('Source file did not contain supported syntax')


def parse_match_block(match_block: Node, source: bytes) -> tuple[dict[str, str], str]:
    """Parse the provide match block node and return a tuple containing a
    mapping of values to icons, and the default icon."""
    match_and_char_query = RS_LANGUAGE.query("""
(match_pattern) @match_pattern
(char_literal) @char_literal
""")

    i = 0
    icon_dict = {}
    matches = match_and_char_query.captures(match_block)
    while i < len(matches):
        extension = get_node_string(matches[i][0], source).strip('"\'')
        icon = parse_icon(get_node_string(matches[i + 1][0], source))
        if extension != '_':
            icon_dict[extension] = icon
        else:
            default_icon = icon
        i += 2
    return (icon_dict, default_icon)


def parse_icon(icon_str: str) -> str:
    """Return a string containing the icon, given its string literal
    representation in Rust code."""
    return chr(int(re.sub(r'((\'|")\\u{)|(}(\'|"))', '', icon_str), 16))


def get_node_string(node: Node, source: bytes) -> str:
    """Given a tree_sitter Node, return the literal"""
    source_lst = source.decode('utf8').split('\n')
    start_y, start_x = node.start_point
    end_y, end_x = node.end_point
    lines = source_lst[start_y:end_y + 1]
    if len(lines) == 1:
        return lines[0][start_x:end_x]
    elif len(lines) == 2:
        return lines[0][start_x:] + lines[1][:end_x]
    else:
        return lines[0][start_x:] + '\n' + '\n'.join(lines[1:-2]) + '\n' + \
            lines[-1][:end_x]


def format_icons(icons: tuple[dict[str, str], str, str]) -> str:
    """Return icons in formatted string suitable for sourcing and use by `lf`."""
    icons_dict = icons[0]
    _, file, folder = icons
    special_declaration_map = {'ln': '\uf481', 'or': '\uf481', 'tw': folder,
                               'ow': folder, 'st': folder, 'di': folder,
                               'pi': file, 'so': file, 'bd': file, 'cd': file,
                               'su': file, 'sg': file, 'ex': file, 'fi': file}
    if os.name == 'nt' or "LF_EXA_ICONS_WINDOWS" in os.environ:
        declarations = ':'.join(
            [f'{key}={special_declaration_map[key]}' for key in special_declaration_map] +
            [f'*.{ext}={icons_dict[ext]}:*.{ext.upper()}={icons_dict[ext]}' for ext in icons_dict])
        return f'set LF_ICONS="{declarations}"'
    else:
        declarations = ':\\\n'.join(
            [f'{key}={special_declaration_map[key]}' for key in special_declaration_map] +
            [f'*.{ext}={icons_dict[ext]}:\\\n*.{ext.upper()}={icons_dict[ext]}' for ext in icons_dict])
        return f'export LF_ICONS="{declarations}"'


def main():
    p = ap.ArgumentParser(prog="lf-exa-icons")
    p.add_argument("source", nargs='?')
    args = p.parse_args()
    if args.source is None:
        source = fetch_source()
    else:
        f = open(args.source, mode='rb')
        source = f.read()
        f.close()

    icons = parse_source(source)
    print(format_icons(icons))


if __name__ == '__main__':
    main()
