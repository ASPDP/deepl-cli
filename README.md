# deepl-cli

[![Release Package](
  <https://github.com/eggplants/deepl-cli/workflows/Release%20Package/badge.svg>
  )](
  <https://github.com/eggplants/deepl-cli/actions/workflows/release.yml>
) [![PyPI version](
  <https://badge.fury.io/py/deepl-cli.svg>
  )](
  <https://badge.fury.io/py/deepl-cli>
)

[![Code Coverage](
  <https://qlty.sh/badges/bafc68a7-d3c7-4f3f-b09b-b86739801231/test_coverage.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/deepl-cli>
) [![Test](
  <https://github.com/eggplants/deepl-cli/actions/workflows/test.yml/badge.svg>
  )](
  <https://github.com/eggplants/deepl-cli/actions/workflows/test.yml>
)

[![Maintainability](
  <https://qlty.sh/badges/bafc68a7-d3c7-4f3f-b09b-b86739801231/maintainability.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/deepl-cli>
) [![pre-commit.ci status](
  <https://results.pre-commit.ci/badge/github/eggplants/deepl-cli/master.svg>
  )](
  <https://results.pre-commit.ci/latest/github/eggplants/deepl-cli/master>
)

![image](https://user-images.githubusercontent.com/42153744/159145088-752decf7-8736-44c3-86aa-37fd0cee83df.png)

- [DeepL Translator](https://www.deepl.com/translator) CLI using [playwright-python](https://github.com/microsoft/playwright-python)

Note: *This project works without DeepL API key. With DeepL API, use [DeepLcom/deepl-python](https://github.com/DeepLcom/deepl-python)*

## Install

```bash
pip install deepl-cli
```

## Usage

### CLI

```bash
deepl -F en -T ja -s <<<'This tool is useful for me.'
# このツールは私にとって便利だ。
deepl -F ja -T en -s <<<'このツールは私にとって便利だ。'
# This tool is useful for me.

curl https://example.com | sed -nr '/^<body>/,/<\/body>/s/<[^>]+>//gp' | tr -d \\n > txt
deepl -f txt -F en -T ja
# 例文ドメイン このドメインは、文書の例文に使用するためのものです。事前の調整や許可を得ることなく、このドメインを文献で使用することができます。   詳細はこちら
```

### HTTP Server

You can also run deepl-cli as an HTTP server:

```bash
# Start server on default port 3001
deepl --server

# Start server on custom host/port  
deepl --server --host 0.0.0.0 --port 8080
```

The server provides a REST API endpoint for translation:

**Endpoint**: `GET /api/translate`

**Parameters**:
- `engine` - Translation engine (always uses DeepL)
- `from` - Source language code (e.g., `en`, `ru`, `ja`)
- `to` - Target language code
- `text` - Text to translate (URL encoded)

**Example**:
```bash
curl "http://127.0.0.1:3001/api/translate?engine=deepl&from=en&to=ru&text=hello%20world"
```

**Response**:
```json
{
  "engine": "deepl",
  "detected": "",
  "translated-text": "привет мир",
  "source_language": "en", 
  "target_language": "ru"
}
```

#### Windows

The server commands work identically on Windows. You can run them in Command Prompt or PowerShell:

**Command Prompt:**

```cmd
REM Start server on default port 3001
deepl --server

REM Start server on custom host/port
deepl --server --host 0.0.0.0 --port 8080
```

**PowerShell:**

```powershell
# Start server on default port 3001
deepl --server

# Start server on custom host/port
deepl --server --host 0.0.0.0 --port 8080
```

**Testing the API on Windows:**

Using PowerShell (recommended):

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:3001/api/translate?engine=deepl&from=en&to=ru&text=hello%20world"
```

Using curl (if available):

```cmd
curl "http://127.0.0.1:3001/api/translate?engine=deepl&from=en&to=ru&text=hello%20world"
```

```shellsession
$ deepl -h
usage: deepl [-h] (-f PATH | -s | --server) [-F FR] [-T TO] [--host HOST] [--port PORT] [-t MS] [-v] [-V]

DeepL Translator CLI without API Key

options:
  -h, --help            show this help message and exit
  -f PATH, --file PATH  source text file to translate (default: None)
  -s, --stdin           read source text from stdin (default: False)
  --server              run as HTTP server (default: False)
  -F FR, --fr FR        input language (not required for server mode) (default: None)
  -T TO, --to TO        output language (not required for server mode) (default: None)
  --host HOST           server host (default: 127.0.0.1) (default: 127.0.0.1)
  --port PORT           server port (default: 3001) (default: 3001)
  -t MS, --timeout MS   timeout interval (default: 5000)
  -v, --verbose         make output verbose (default: False)
  -V, --version         show program's version number and exit

valid languages of `-F` / --fr`:
{'cs', 'fr', 'ru', 'hu', 'zh', 'da', 'nl', 'es', 'lv', 'nb', 'de', 'ko', 'it', 'pt', 'pl', 'et', 'ar', 'el', 'en', 'id', 'sv', 'ro', 'ja', 'uk', 'bg', 'sk', 'fi', 'tr', 'sl', 'lt'}

valid languages of `-T` / `--to`:
{'cs', 'fr', 'ru', 'hu', 'zh', 'da', 'nl', 'en-gb', 'es', 'lv', 'nb', 'de', 'ko', 'it', 'pt', 'zh-hans', 'pl', 'et', 'pt-br', 'ar', 'el', 'en', 'id', 'sv', 'ro', 'ja', 'uk', 'bg', 'en-us', 'sk', 'zh-hant', 'pt-pt', 'fi', 'tr', 'sl', 'lt'}
```

### Package

```python
from deepl import DeepLCLI

deepl = DeepLCLI("en", "ja")
deepl.translate("hello") #=> "こんにちわ"
```

If you use with asyncio, Use `DeepLCLI.translate_async`. See [examples/async.py](https://github.com/eggplants/deepl-cli/blob/master/examples/async.py).

## License

MIT
