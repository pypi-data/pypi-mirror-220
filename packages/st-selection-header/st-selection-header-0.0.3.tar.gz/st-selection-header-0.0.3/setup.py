import setuptools

setuptools.setup(
    name="st-selection-header",
    version="0.0.3",
    author="Elliot Glas",
    author_email="elliot.glas@viscando.com",
    description="Panel for changing data",
    long_description="Panel for changing data",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
