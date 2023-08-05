from setuptools import setup, find_packages

setup(
    name='yolov8-detect',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    author='xingyue',
    author_email='ywb10.8@qq.com',
    description='offer the datasets can tran the new model,offer the model and image can infer the object in the image'
)
