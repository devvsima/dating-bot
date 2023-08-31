from babel.messages import frontend as babel
from distutils.core import setup

setup(
    name="foo",
    version="1.0",
    cmdclass={
        "extract_messages": babel.extract_messages,
        "init_catalog": babel.init_catalog,
        "update_catalog": babel.update_catalog,
        "compile_catalog": babel.compile_catalog,
    },
)
