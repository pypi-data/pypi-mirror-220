from setuptools import setup, find_packages
 
setup(
    name='singlefactortest',#包名
    version='1.2',#版本
    description="单因子的测试（日级别and分钟级别）",#包简介
    long_description=open('README.md').read(),#读取文件中介绍包的详细内容
    include_package_data=True,#是否允许上传资源文件
    author='IDEA_Wenzhi',#作者
    author_email='1259429314@qq.com',#作者邮件
    maintainer='IDEA_Wenzhi',#维护者
    maintainer_email='1259429314@qq.com',#维护者邮件
    license='MIT License',#协议
    url='https://github.com/Masteryeda',#github或者自己的网站地址
    packages=find_packages(),#包的目录
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
     'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',#设置编写时的python版本
],
    python_requires='>=3.7',#设置python版本要求
    install_requires=['pandas',
                      "numpy",
                      "statsmodels",
                      "matplotlib",
                      "seaborn",
                      "scipy",
                      "baostock"],#安装所需要的库
    py_modules=['singlefactortest']
    )
    
