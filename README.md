# `lf-exa-icons`

A script to match `lf`'s icons to `exa`'s icons.

This script pulls the [`exa`](https://github.com/ogham/exa) source code then parses it to extract icons for every availble extension. It then prints a statement with the same form as the instructions found in the `lf`  wiki [here](https://github.com/gokcehan/lf/wiki/Icons) which declares the `LF_ICONS` variable with the proper formatting when sourced. This script is definitely prone to breaking as it relies on the current formatting of `exa`'s source code to function properly, however due to the way extension matching is implemented in `exa`, there's no way for me to extract it nicely even if this were written in rust.

## Usage

Clone the repository and `cd` into it:

```bash
git clone https://github.com/mtoohey31/lf-exa-icons
cd lf-exa-icons
```

Run the script once without writing it to ensure the output matches the expected format:

```bash
python3 lf_exa_icons.py
```

Then run it for real:

```bash
python3 lf_exa_icons.py > ~/.config/lf/icons
```

Add the following line to your shell's config file (e.g.: `~/.bashrc`, `~/.zshrc`, `~/.config/fish/config.fish`):

```bash
source ~/.config/lf/icons
```

This statement should work in `bash`, `zsh`, and `fish`, it hasn't been tested in other shells though. If this doesn't work for you (the sourcing specifically, open issues on this repo for other problems), see the `lf` wiki [here](https://github.com/gokcehan/lf/wiki/Icons).
