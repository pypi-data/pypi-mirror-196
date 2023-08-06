# Python代码组件化

## kili-common-storage

1. 本组件用上传文件到对象存储服务器、拼接文件路径。
2. 如何更新本组件
    - 更新kili_common_storage的代码
    - 更新setup.py里kili-common-storage的version和install_requires
    - 打包和上传
    ```sh
    # 打包
    MODULE=kili-common-storag python3 setup.py sdist bdist_wheel
    # 上传到https://pypi.org/
    python3 -m twine upload dist/kili_common_storage-<版本号>* --skip-existing --verbose
    ```
3. 如何在代码中使用
    - 安装
    ```sh
    # 如果使用清华源或者腾讯源, 在更新版本后需要一段时间才能拉取到最新版本
    # 清华源 https://pypi.tuna.tsinghua.edu.cn/simple/kili-common-storage/
    # 腾讯源 http://mirrors.cloud.tencent.com/pypi/simple/kili-common-storage/
    pip install kili-common-storage 
    ```
    - 使用
    ```python
    from kili_common_storage import ObjectStorage
    object_storage = ObjectStorage(
        <nacos-config>, <def_common_struct(thrift)>, <def_exceptions(thrift)>)
    ```
