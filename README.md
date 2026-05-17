# 👑 Crusader Queens

> *In a world where queens lead crusades and empresses forge dynasties, history bends to the will of women.*

A **Crusader Kings III** total gender-swap overhaul mod. Crusader Queens flips the default gender dynamics of the entire game — female rulers are the norm, matrilineal succession is standard, and the world's faiths and cultures are built around women in power.

[![Validate Mod Structure](https://github.com/YOUR_USERNAME/crusader_queens/actions/workflows/validate.yml/badge.svg)](https://github.com/YOUR_USERNAME/crusader_queens/actions/workflows/validate.yml)
![CK3 Version](https://img.shields.io/badge/CK3-1.12.*-darkred)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✨ Features

| Area | What Changes |
|---|---|
| **Succession** | Female-first succession is the default across all cultures |
| **Marriage** | Matrilineal marriage is the standard contract type |
| **Titles** | King→Queen, Duke→Duchess, Emperor→Empress (and vice versa for men) |
| **Pronouns** | He/Him/His ↔ She/Her throughout all event text |
| **Religion** | All faiths default to female clergy and female rulers as orthodox |
| **Family** | Father/Son/Brother ↔ Mother/Daughter/Sister in all flavor text |
| **Court** | All court positions open to women by default |
| **Innovations** | Patriarchal succession requires a cultural unlock (not the default) |

---

## 📥 Installation

### Steam Workshop *(recommended)*
> Workshop link coming soon — subscribe and it installs automatically.

### Manual Installation
1. Download the latest release `.zip` from [Releases](https://github.com/YOUR_USERNAME/crusader_queens/releases)
2. Extract to your CK3 mod folder:
   - **Windows:** `%USERPROFILE%\Documents\Paradox Interactive\Crusader Kings III\mod\`
   - **Mac:** `~/Documents/Paradox Interactive/Crusader Kings III/mod/`
   - **Linux:** `~/.local/share/Paradox Interactive/Crusader Kings III/mod/`
3. Launch CK3, open the **Mod Manager**, and enable **Crusader Queens**

---

## 🔧 Compatibility

- **CK3 version:** `1.12.*`
- **Save game safe?** No — start a new game after enabling
- **Ironman compatible?** No (modded achievements are disabled by Paradox)
- **DLC required?** None — works with base game; enhanced with Royal Court, Fate of Iberia, etc.

### Known Conflicts
| Mod | Status | Notes |
|---|---|---|
| Any mod that edits `succession_laws.txt` | ⚠️ Likely conflict | Load order matters — put Crusader Queens last |
| Any mod that edits religion gender doctrines | ⚠️ Likely conflict | Check load order |
| Cosmetic / portrait mods | ✅ Compatible | No overlap |
| Event story mods (Sinful, etc.) | 🔍 Untested | Pronoun swaps may not apply to their custom events |

---

## 🛠 For Developers / Contributors

### Repository Structure

```
crusader_queens/
├── .github/workflows/      # CI validation (brace checks, encoding, etc.)
├── common/
│   ├── culture/innovations/    cq_innovations.txt      — matrilineal tradition & patriarchy lock
│   ├── laws/                   cq_succession_laws.txt  — female-first succession defaults
│   ├── religion/religions/     cq_religion_patches.txt — faith gender doctrine overrides
│   └── game_rules/             cq_game_rules.txt       — world-gen defaults
├── localization/english/       cq_titles_l_english.yml — title & pronoun swaps
├── tools/
│   └── swap_localization.py    — batch-processes vanilla .yml files
├── descriptor.mod
└── README.md
```

### Generating Localization Patches from Vanilla

The `tools/swap_localization.py` script automates swapping gendered language across all vanilla CK3 localization files. Point it at your CK3 install:

```bash
python3 tools/swap_localization.py \
  --vanilla "C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/localization/english" \
  --output  "./localization/english/vanilla_patched"
```

Use `--dry-run` to preview changes without writing files.

### Contributing

Contributions very welcome! High-priority areas:

- [ ] **Localization coverage** — run the swap script and spot-check output for unnatural phrasing
- [ ] **Event text review** — some vanilla events have hard-coded gender language that needs manual fixes
- [ ] **Non-English localization** — French, German, Spanish, Russian, etc. all need equivalents of `swap_localization.py`
- [ ] **Portrait overrides** — ensure female portraits appear where male portraits did in vanilla ruler slots
- [ ] **Compatibility patches** — patches for popular mods (AGOT, EPE, Sinful, etc.)

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a PR.

---

## 📜 License

[MIT](LICENSE) — free to use, modify, and redistribute. Credit appreciated but not required.

---

## 🙏 Credits

- Paradox Interactive for Crusader Kings III
- The CK3 modding community for documentation at [ck3.paradoxwikis.com](https://ck3.paradoxwikis.com)
- Contributors: *you could be here!*
