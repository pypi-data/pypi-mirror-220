# nice_logging

Simple logging library that has colored and timestamped output by default. Can be used as a drop-in replacement.

## Installation

```pip install nice_logging```

(Or just grab the .py file)

## Usage

```python
import nice_logging
nice_logging.basicConfig(level=nice_logging.DEBUG)
logger = nice_logging.getLogger(__name__)
logger.info("Hello")
```
```
2023-07-23 11:27:33,571 [INFO ] [__main__] Hello
```

Or:

```python
import nice_logging as logging
```
