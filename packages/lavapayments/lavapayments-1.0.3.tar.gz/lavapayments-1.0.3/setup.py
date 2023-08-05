from setuptools import setup

setup(
    name="lavapayments",
    version="1.0.3",
    description="Библиотека для работы с Бизнес API Lava.ru",
    packages=["lavapayments"],
    author_email="dimabykov189@gmail.com",
    zip_safe=False,
    requires=["aiohttp"],
    python_requires=">=3.8",
    long_description_content_type="text/markdown"
)
