import setuptools

setuptools.setup(
    name="ImgTextClipboard-python",  # 库的名字
    version='0.1.3',  # 库的版本号，后续更新的时候只需要改版本号就行
    author="LanluZ",  # 你的你的名字
    description="Convenient to operate clipboard related images by oneself",  # 介绍
    long_description_content_type="text/markdown",
    url='https://github.com/LanluZ/ImgTextClipboard-python',
    packages=setuptools.find_packages(),
    install_requires=[
        "pywin32>=306",
        "Pillow>=10.0.0",
        "image>=1.5.33",
        "pyperclip>=1.8.2"
    ],
    keywords=['image', 'copy', 'paste', 'windows', 'clipboard'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
# 注意：没有注释的地方不要改
