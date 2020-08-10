@echo off

pushd FlexTools

call ..\py_net TETools.py >..\error.log %*

popd

notepad error.log
