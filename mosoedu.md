

### 使用说明

1. python环境
```sh
which python
pip uninstall ora2
pip install --no-deps git+https://github.com/jerrybox/edx-ora2.git@mosoH2 -i https://pypi.doubanio.com/simple/
```


2. mosoedu 用到的配置参数
- 配置参数接口
```sh
vim /edx/app/edxapp/edx-platform/cms/envs/aws.py +/AUTH_TOKENS
vim /edx/app/edxapp/edx-platform/lms/envs/aws.py +/AUTH_TOKENS

###############################aliyunoss#######################
OSS_ACCESS_KEY_ID = AUTH_TOKENS.get('OSS_ACCESS_KEY_ID', '<AccessKeyId>')
OSS_ACCESS_KEY_SECRET = AUTH_TOKENS.get('OSS_ACCESS_KEY_SECRET', '<AccessKeySecret>')
OSS_ENDPOINT = ENV_TOKENS.get('OSS_ENDPOINT', '<endpoint>')

ORA2_FILEUPLOAD_BACKEND = ENV_TOKENS.get("ORA2_FILEUPLOAD_BACKEND")
```

- 配置文件
```sh
vim /edx/app/edxapp/cms.env.json
vim /edx/app/edxapp/lms.env.json
+ "ORA2_FILEUPLOAD_BACKEND": "aliyunoss",
+ "FILE_UPLOAD_STORAGE_BUCKET_NAME": "edxapp-edxuploads",

vim /edx/app/edxapp/cms.auth.json
vim /edx/app/edxapp/lms.auth.json
OSS_ACCESS_KEY_ID = AUTH_TOKENS.get('OSS_ACCESS_KEY_ID', '<AccessKeyId>')
OSS_ACCESS_KEY_SECRET = AUTH_TOKENS.get('OSS_ACCESS_KEY_SECRET', '<AccessKeySecret>')
OSS_ENDPOINT = ENV_TOKENS.get('OSS_ENDPOINT', '<endpoint>')
```

