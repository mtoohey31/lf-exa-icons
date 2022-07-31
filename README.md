# `lf-exa-icons`

A script to match `lf`'s icons to `exa`'s icons.

This script first detects the version of `exa` that is installed, then pulls the corresponding `exa` source code and parses it using [`py-tree-sitter`](https://github.com/tree-sitter/py-tree-sitter/) to extract icons for every available extension. It then prints a statement of the same form as that in the instructions found in the `lf` wiki [here](https://github.com/gokcehan/lf/wiki/Icons) which declares the `LF_ICONS` variable with the proper formatting when sourced. This script may break since it relies on being able to parse the `exa` source code correctly, however it should be able to handle minor changes since it is implemented with `tree-sitter` instead of simple string parsing. Also, note that there may still be a few minor icon differences, mainly for folders or files with specific names, since `exa` uses some more advanced icon assignment logic that relies on more than just extensions, which `lf` does not support.

## Usage

### Fetching Release

Use the following for curl:

```bash
curl -sSL https://raw.githubusercontent.com/mtoohey31/lf-exa-icons/main/scripts/install.sh | sh
```

Or the following to use wget:

```bash
wget -qO - https://raw.githubusercontent.com/mtoohey31/lf-exa-icons/main/scripts/install.sh | sh
```

Finally, follow the instructions under [Sourcing](#sourcing).

### Building

Clone the repository, `cd` into it, and fetch the necessary submodules:

```bash
git clone https://github.com/mtoohey31/lf-exa-icons
cd lf-exa-icons
git submodule update --init
```

Install the required python packages:

```bash
pip3 install -r requirements.txt
```

Run the script once without writing it to ensure the output matches the expected format:

```bash
python3 lf_exa_icons/main.py
```

Then run it for real:

```bash
python3 lf_exa_icons/main.py > ~/.config/lf/icons
```

Finally, follow the instructions under [Sourcing](#sourcing).

### Sourcing

Add the following line to your shell's config file (e.g.: `~/.bashrc`, `~/.zshrc`, `~/.config/fish/config.fish`):

```bash
source ~/.config/lf/icons
```

This statement should work in `bash`, `zsh`, and `fish` and allow `lf` to recognize the custom icons, it hasn't been tested in other shells though.
