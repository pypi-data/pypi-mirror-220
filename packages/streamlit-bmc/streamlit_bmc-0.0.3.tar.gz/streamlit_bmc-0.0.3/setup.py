import setuptools

setuptools.setup(
    name="streamlit_bmc",
    version="0.0.3",
    author="Ember",
    author_email="nguyencaonguyenthuy@gmail.com",
    description="A Streamlit Component for drawing Business Model Canvas",
    long_description="A Streamlit Component for drawing Business Model Canvas",
    long_description_content_type="text/plain",
    url="https://github.com/teq-thuynguyen/streamlit-business_model_canvas",
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
