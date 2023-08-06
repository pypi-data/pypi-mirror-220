
# Eriparse
![is_still_valid_workflow](https://github.com/ncgl-git/eriparse/actions/workflows/is_still_valid.yaml/badge.svg)

*HTML parsing logic for `https://www.erieri.com/cost-of-living-calculator`. Was written to help my wife and I better understand the differences between potential cities for her fellowship.*


#### Notes
Be aware that website frontend can change _whenver_, so, rely on the build badge above for is_still_valid to know whether the website HTML has changed.


## Usage

Intended to be called like: 
```
wget -q https://www.erieri.com/cost-of-living/united-states/illinois/chicago -O - | pipenv run python eriparse/main.py >> chicago.json
```

Or, if you'd like to integrate it into your Python code,  `>>> pip install eriparse`
```
from eriparse import parse
```