# Grimmbot Repository

This repository uses `main` as the primary branch. Any new work should branch
from `main` and later merge back into it.

Individual robots are expected to be developed on their own branches. Example
branch names could be:

- `alpha-robot`
- `beta-robot`
- `gamma-robot`

Each robot branch contains its own `setup.exe` installer. To work on a specific
robot, check out its branch and run the installer:

```bash
git checkout <robot-branch>
./setup.exe
```

These branches and the installers are placeholders and may not be available in
this repository yet.
