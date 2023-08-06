from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="chatting-with-pdfs",
    version="0.0.12",
    description="Load a PDF file and ask questions via llama_index and GPT.",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Morne",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "bson >= 0.5.10",
        "openai >= 0.27.6",
        "langchain >= 0.0.160",
        "setuptools >= 67.8.0",
        "llama-index >= 0.6.7",
        "PyPDF2 >= 3.0.1"
    ],
    extras_require={
        "dev": ["pytest>=7.4.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
