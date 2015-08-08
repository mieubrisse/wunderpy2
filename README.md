## Installation
**TODO** Actually put this package on pip :|
```
pip install wunderpy2
```

## Design
This library is a thin one, meaning:

1. Only the bare minimum of error-checking to pass [the Wunderlist API specifications](https://developer.wunderlist.com/documentation) is performed (e.g. there's no checking whether a task's title is empty, even though the Wunderlist web client enforces nonempty titles)
2. There aren't any 'convenience' functions (e.g. get a list by its name)
These choices were made intentionally, so as to give developers full control and not to get mired in implementation specifics of fancy things.
