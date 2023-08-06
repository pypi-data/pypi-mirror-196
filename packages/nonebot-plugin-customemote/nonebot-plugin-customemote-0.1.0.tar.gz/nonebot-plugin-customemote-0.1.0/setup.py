from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nonebot-plugin-customemote",
    version="0.1.0",
    author="DMCSWCG",
    description="A plugin based on NoneBot2, send text to call your set emotes.",
    long_description=long_description,
    license='MIT License',
    long_description_content_type="text/markdown",
    url="https://github.com/DMCSWCG/nonebot-plugin-customemote/",
    project_urls={
        "Bug Tracker": "https://github.com/DMCSWCG/nonebot-plugin-customemote/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["nonebot_plugin_customemote"],
    python_requires=">=3.7",
    install_requires=[
        "nonebot2 >=2.0.0rc1",
        "nonebot-adapter-onebot >= 2.0.0rc1",
        "aiofiles",
        "pydantic",
        "httpx",
        "ujson"
    ]
)