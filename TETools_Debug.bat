@echo off

pushd TETools

call ..\py_net TETools.py >..\error.log %*

popd

notepad error.log
