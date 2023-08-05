#!/usr/bin/env python

from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="rscad",
    version="0.0.2",
    description="rusty cad utils",
    author="Glenn",
    author_email="gward@python.net",
    rust_extensions=[
        RustExtension(
            "rscad.boolean.rboolean",
            binding=Binding.PyO3,
            path="./boolean/Cargo.toml",
        ),
        RustExtension(
            "rscad.concave.rconcave",
            binding=Binding.PyO3,
            path="./concave/Cargo.toml",
        ),
        RustExtension(
            "rscad.draft.rdraft",
            binding=Binding.PyO3,
            path="./draft/Cargo.toml",
        ),
        RustExtension(
            "rscad.hello.rhello",
            binding=Binding.PyO3,
            path="./hello/Cargo.toml",
        ),
    ],
    packages=[
        "rscad.hello",
        "rscad.boolean",
    ],
    # tell setup that the root python source is inside py folder
    package_dir={
        "rscad.hello": "hello/py",
        "rscad.boolean": "boolean",
    },
    install_requires=["pyvista", "numpy"],
    # entry_points={
    #     "console_scripts": ["greet=hello:greet"],
    # },
    zip_safe=False,
)
