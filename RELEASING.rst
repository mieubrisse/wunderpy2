Releasing
=========

Because I always forget how to do this for Python modules:

1. Merge code changes into develop
2. Use `gitflow-pp <https://github.com/mieubrisse/dotfiles/blob/master/bash/utils/gitflow-pp.sh>`_ script to run :code:`gitflow-pp.sh release start` and specify the appropriate version to be released
3. Update HISTORY.rst with the version to be released (and release notes, if not already done)
4. Update setup.py with the version to be released
5. Run :code:`gitflow-pp.sh release finish`
6. Verify that the git branching model looks sane
7. Run :code:`gitflow-pp.sh push`
