# jocassid-commons

## Overview
Miscellaneous utility code written in Python.  Modules within this library 
include:

* `accumulator_dict` - Contains AccumulatorDict, a dict object where values 
are sets or lists.  Assigning a value to a key (i.e. 
`accumulator_dict['key'] = value`) will automatically add/append the 
value to the list (creating a set or list if the key doesn't exist) 
* `dirf` - Contains the `dirf` function a wrapper around the built-in 
`dir` function that adds filtering capabilities.
* `json` - Contains the `json_get` method for extracting data from within
nested lists and dicts such as those returned from a JSON api.

## Changelog

### 0.0.4
* Added `dirf` module
### 0.0.5
* Added `accumulator_dict` module.
