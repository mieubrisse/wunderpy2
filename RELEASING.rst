Releasing
=========

Because I always forget how to do this for Python modules:

1. Merge code changes into develop
2. Use `gitflow-pp <https://github.com/mieubrisse/dotfiles/blob/master/bash/utils/gitflow-pp.sh>`_ script to run :code:`gitflow-pp.sh release start`
3. Update HISTORY.rst with version I'm releasing with
4. Use `bumpversion <https://github.com/peritus/bumpversion>`_ to run :code:`bumpversion (major|minor|patch)` which will increment the version in all appropriate files
5. 
