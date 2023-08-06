# Learning python

This is a simple example package. 

just for learning how to build a package.


rm ./dist/*tar.gz
python3 setup.py sdist build
export PATH=$PATH:~/.local/bin
twine upload dist/*

       输入用户名 密码 即可完成上传。




