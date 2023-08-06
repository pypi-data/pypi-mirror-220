from setuptools import setup

packages = [
    "lavapayments",
    "lavapayments.client",
    "lavapayments.exceptions",
    "lavapayments.types"
]

setup(
    name="lavapayments",
    version="1.0.5",
    description="Библиотека для работы с Бизнес API Lava.ru",
    packages=packages,
    author_email="dimabykov189@gmail.com",
    zip_safe=False,
    requires=["aiohttp"],
    python_requires=">=3.8",
    long_description_content_type="text/markdown"
)
