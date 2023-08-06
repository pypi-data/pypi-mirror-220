from setuptools import find_packages, setup

setup(
    name="foundation-model-package",
    version="0.0.3",
    description="Package for the foundation model tool for prompt flow",
    packages=find_packages(),
    entry_points={
        "package_tools": ["foundation_model = foundation_model_pkg.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)
