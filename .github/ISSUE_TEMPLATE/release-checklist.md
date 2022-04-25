---
name: Release checklist
about: prepare for relase
title: Release X.X.X
labels: release
assignees: ''

---

Prepare for release:

- [ ] `git pull`
- [ ] Polish [HISTORY](../../HISTORY.rst)
- [ ] `pre-commit run`
- [ ] `pytest` 
- [ ] `bumpversion minor` or `bumpversion major`
- [ ] `python -m build`

Submit to PyPI:

- [ ] `python -m twine upload dist/*`
- [ ] Submit 🎉