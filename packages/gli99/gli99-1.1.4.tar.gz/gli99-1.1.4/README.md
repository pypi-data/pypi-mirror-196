## Installation

Run the following to install:

```python
pip install gli99
```

## Usage

```python
from gli99.tools import GifScraper

gs = GifScraper(browser="firefox")
gs.load(query="brazil",amount=5)
gs.download("D:/GifsFolder/")
```

currently supported browsers:

* Edge
* Chrome
* Firefox
```python
from gli99.tools import GifScraper

gs = GifScraper(browser="firefox")
gs.load(query="brazil",amount=5)
gs.download("D:/GifsFolder/")
```

currently supported browsers:

* Edge
* Chrome
* Firefox

![1678407792246](image/README/1678407792246.png)