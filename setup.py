from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent.resolve()
REQ_FOLDER = ROOT / "requirements"


def get_requirements(path: Path):
    return [
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


install_requires = get_requirements(REQ_FOLDER/"base.txt")

extras_require = {}
for file in REQ_FOLDER.glob("extra-*.txt"):
    extras_require[file.stem[len("extra-"):]] = get_requirements(file)


def extras_combined(*extra_names):
    return list(
        {
            req
            for name, reqs in extras_require.items()
            if not extra_names or name in extra_names
            for req in reqs
        }
    )


extras_require["dev"] = extras_combined()
python_requires = ">=3.8"

setup(
    name="grimmbot",
    version="0.1.0",
    packages=find_packages(include=["cogs", "cogs.*"]),
    py_modules=["grimm_bot", "bloom_bot", "curse_bot", "goon_bot"],
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires=python_requires,
)
