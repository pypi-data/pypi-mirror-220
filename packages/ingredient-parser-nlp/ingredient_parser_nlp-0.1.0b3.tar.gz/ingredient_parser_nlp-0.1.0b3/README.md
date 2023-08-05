# Ingredient Parser

The Ingredient Parser package is a Python package for parsing structured information out of recipe ingredient sentences.

![](docs/source/_static/logo.svg)

## Documentation

Documentation on using the package and training the model can be found at https://ingredient-parser.readthedocs.io/en/latest/.

## Quick Start

Install the package using pip

```bash
python -m pip install ingredient-parser-nlp
```

Import the ```parse_ingredient``` function and pass it an ingredient sentence.

```python
>>> from ingredient_parser import parse_ingredient

>>> parse_ingredient("3 pounds pork shoulder, cut into 2-inch chunks")
{'sentence': '3 pounds pork shoulder, cut into 2-inch chunks',
 'quantity': '3',
 'unit': 'pound',
 'name': 'pork shoulder',
 'comment': 'cut into 2-inch chunks',
 'other': ''}

# Output confidence for each label
>>> parse_ingredient("3 pounds pork shoulder, cut into 2-inch chunks", confidence=True)
{'sentence': '3 pounds pork shoulder, cut into 2-inch chunks',
 'quantity': '3',
 'unit': 'pound',
 'name': 'pork shoulder',
 'comment': 'cut into 2-inch chunks',
 'other': '',
 'confidence': {'quantity': 0.9988,
  'unit': 0.9969,
  'name': 0.9698,
  'comment': 0.9992,
  'other': 0}}
```

The returned dictionary has the format

```python
{
    "sentence": str,
    "quantity": str,
    "unit": str,
    "name": str,
    "comment": str,
    "other": str
}
```

## Model accuracy

The model provided in ```ingredient-parser/``` directory has the following accuracy on a test data set of 25% of the total  data used:

```
Sentence-level results:
	Total: 9448
	Correct: 8189
	-> 86.67%

Word-level results:
	Total: 54854
	Correct: 52509
	-> 95.73%
```

## Development

The development dependencies are in the ```requirements-dev.txt``` file.

Note that development includes training the model.

* ```Black``` is used for code formatting.
* ```ruff``` is used for linting. 
* ```pyright``` is used for type static analysis.
* ```pytest``` is used for tests, with ```coverage``` being used for test coverage.

The documentation dependencies are in the ```requirement-doc.txt``` file.
