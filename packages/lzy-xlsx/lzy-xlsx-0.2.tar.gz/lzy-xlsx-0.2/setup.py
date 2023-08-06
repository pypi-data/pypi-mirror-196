from setuptools import setup

setup(name='lzy-xlsx',  # 包名

      version='0.2',  # 版本

      author_email='mvli@qq.com',  # 作者邮箱

      py_modules=['xlsx']),  # 上传的文件



# python setup.py sdist  打包
# twine upload dist/*  上传
