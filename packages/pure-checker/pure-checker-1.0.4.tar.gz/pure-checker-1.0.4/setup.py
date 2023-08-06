from setuptools import setup, Extension


def main():
    setup(
        name="pure-checker",
        version="1.0.4",
        description="A static analysis file format checker.",
        ext_modules=[Extension("pure_py", ["pure_py.c"])],
        include_package_data=True,
        packages=[],
    )


if __name__ == "__main__":
    main()
