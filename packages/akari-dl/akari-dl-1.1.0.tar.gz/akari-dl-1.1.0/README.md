# akari-dl

A lightweight and open-source anime downloading CLI.

1. [akari-dl](#akari-dl)
   1. [About](#about)
   2. [Installation](#installation)
      1. [pypi/pip](#pypipip)
      2. [Build](#build)
   3. [Usage](#usage)
   4. [Arguments](#arguments)
      1. [Positional](#positional)
      2. [Optional](#optional)
   5. [Supported Websites](#supported-websites)
   6. [Known Limitations](#known-limitations)
      1. [Video Downloaded in Bad Resolution or Wrong Format](#video-downloaded-in-bad-resolution-or-wrong-format)
   7. [Disclaimer](#disclaimer)

## About

akari-dl downloads anime video files from direct download websites based on user configuration to avoid more annoying downloading methods like torrenting and manually downloading.

## Installation

Granted you have Python 3.10+

### pypi/pip

```bash
pip install -U akari-dl
```

### Build

1. `git clone https://github.com/keisanng/akari-dl.git`
2. `cd akari-dl`
3. [Activate virtual environment](https://python.land/virtual-environments/virtualenv#Python_venv_activation)
4. `py -m venv .venv`
5. `pip install requests-html`
6. `python setup.py sdist`
7. `pip install .` (or path to akari-dl if you're not in it anymore)

## Usage

User:

```bash
akari-dl tokyoinsider "hidamari sketch" path/to/output
```

Developer:

```bash
py -m akari_dl tokyoinsider "hidamari sketch" path/to/output
```

In your output path, akari-dl will create a folder where all the desired anime episodes will be.

## Arguments

### Positional

1. `website`
   - Specify the name of what website to direct-download anime from (see [supported websites](https://github.com/keisanng/akari-dl#supported-websites).)
2. `anime`
   - Specify what anime to download by title (in [Romaji](https://en.wikipedia.org/wiki/Romanization_of_Japanese).)
3. `output`
   - Specify path to output downloaded video files to.

### Optional

- **Help**
  - `-h`; `--help`
- **Version**
  - `-v`; `--version`
  - Print the current version of akari-dl.
- **Episodes**
  - `-e`; `--episodes`
  - Specify the amount of episodes to download (downloads all if not specified) [NOT YET IMPLEMENTED.]
- **Specials**
  - `s`; `--specials`
  - Enable downloading of special episodes (only works with websites that list the specials on the same page as the episodes.)

## Supported Websites

1. [<img src="https://www.tokyoinsider.com/favicon.ico" style="width: 24px;"/> Tokyoinsider](https://www.tokyoinsider.com)
2. [<img src="https://chauthanh.info/favicon.ico" style="width: 24px;" /> ChauThanh](https://chaunthanh.info)

[*Request a **ddl** site here.*](https://github.com/keisanng/akari-dl/issues)

## Known Limitations

### Video Downloaded in Bad Resolution or Wrong Format

As of now, akari-dl will scrape the first link in the markup of the anime's page for video file. In the near future there will be options to download for file format or resolution specifically - just not now.

## Disclaimer

> The core aim of this project is to co-relate automation and efficiency to extract what is provided to a user on the internet. All content available through the project is hosted by external non-affiliated sources. All content served through this project is publicly accessible. If your site is listed in this project, the code is pretty much public. Take necessary measures to counter the exploits used to extract content in your site.

*Applicable excerpt from <https://github.com/justfoolingaround/animdl/blob/master/disclaimer.md>.*
