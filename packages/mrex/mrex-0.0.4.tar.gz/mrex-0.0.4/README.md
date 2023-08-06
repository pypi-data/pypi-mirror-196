# Magic Regex

Read and write regular expressions easily.

```python
import mrex

# Find
id_re = mrex.exactly("id: ").and_(mrex.DIGITS.group_as("id"))
id_str = id_re.find("id: 12345").group("id")
# id_str == "12345"

# Split
words = mrex.NON_CHARS.split("It's just a flesh wound...")
# words == ["It", "s", "just", "a", "flesh", "wound", ""]
```

# Installation

```bash
pip install mrex
```

#  Development

* Download source
* Install development dependencies: `flit install -s --deps develop`
* Format code: `black .`
* Run tests: `pytest`
* Bump version in [src/mrex/\_\_init\_\_.py](src/mrex/__init__.py)
* Build package: `flit build`
* Deploy: `flit publish`

# Thanks

Project influenced by [magic-regexp](https://github.com/danielroe/magic-regexp).
