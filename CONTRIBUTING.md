# Contributing to Crusader Queens

Thanks for your interest in contributing! Here's how to get involved.

## Ways to Help

### 🌍 Localization Review
The `swap_localization.py` script handles most pronoun/title swaps automatically,
but CK3 has thousands of event strings and some will come out awkward or wrong.

If you spot unnatural phrasing in-game:
1. Note the exact text you saw
2. Find it in `localization/english/` (or `vanilla_patched/`)
3. Open a PR with the fix, or file an Issue with the original + suggested text

### 🌐 Non-English Localization
The swap script only handles English today. If you speak French, German, Spanish,
Russian, Korean, Simplified Chinese, or any other CK3 language, we'd love a
language-specific swap table. See `tools/swap_localization.py` — the `SWAP_PAIRS`
table is the main thing to translate.

### 🔧 Compatibility Patches
Popular mods (AGOT, EPE, Sinful, etc.) add their own localization and succession
rules. Compatibility patches go in `compatibility/` (create the folder) and should
be clearly named: `compatibility/agot_patch/`.

### 🐛 Bug Reports
File an Issue with:
- Your CK3 version
- Your mod load order
- What you expected vs. what happened
- A save file if possible

## Pull Request Process

1. Fork the repo and create a branch: `git checkout -b fix/my-fix`
2. Make your changes
3. Run the GitHub Actions checks locally if you can:
   ```bash
   # Check for BOM encoding on new .yml files
   python3 -c "
   from pathlib import Path
   for f in Path('localization').rglob('*.yml'):
       raw = f.read_bytes()
       assert raw.startswith(b'\xef\xbb\xbf'), f'{f} missing BOM!'
   print('All good!')
   "
   ```
4. Submit a PR with a clear description of what changed and why

## Code Style

- `.txt` files: 1 tab indent, opening `{` on the same line as the key
- `.yml` files: must be UTF-8 with BOM (`\xef\xbb\xbf`), 1-space indent
- Python: follow PEP 8, type hints appreciated but not required

## Questions?

Open a Discussion on GitHub or find us on the CK3 Modding Discord.
