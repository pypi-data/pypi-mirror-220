from setuptools import setup, find_packages

setup(
    name='dyc_package',
    version='1.0.1',  # 替换为您的版本号
    description='Description of your package',
    author='dyc',
    author_email='your@email.com',
    packages=find_packages(),
    install_requires=[
        # 列出您的包依赖的其他Python包
        # 例如：'requests', 'numpy', 等等
    ],
)