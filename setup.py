from setuptools import setup, find_packages

setup(
    name="whatsapp-bot-colombiano",
    version="1.0.0",
    description="Bot de WhatsApp con personalidad colombiana",
    author="CodeWithBotinaOficial",
    author_email="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "Flask>=2.3.3",
        "twilio>=8.9.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "requests>=2.31.0",
        "colorlog>=6.7.0",
    ],
)