import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="syspend",
    version="0.0.2",
    author="town_paddy",
    author_email="town_paddy@yahoo.com",
    description="Recursively search the parent directory and execute sys.path.append on the path where the SYSPEND_ROOT file exists.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/town-paddy/syspend",
    project_urls={
        "website": "https://sites.google.com/view/kumake/english",
        "youtube": "https://www.youtube.com/channel/UCxm0sZwjGff8KdRcymFKIfA",
        "twitter": "https://twitter.com/tweet_paddy",
        "Instagram": "https://www.instagram.com/town_paddy/"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['syspend'],
    python_requires=">=3.6",
)