from io import BytesIO
from minio import Minio

# from BaseColor.base_colors import hyellow, hred
# from Tools import MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME
import logging

logger = logging.getLogger("django")

"""
Minio: http://docs.minio.org.cn/docs/master/python-client-quickstart-guide
适用于与Amazon S3兼容的云存储的MinIO Python Library Slack
MinIO Python Client SDK提供简单的API来访问任何与Amazon S3兼容的对象存储服务。
本文我们将学习如何安装MinIO client SDK，并运行一个python的示例程序。对于完整的API以及示例，请参考Python Client API Reference。
本文假设你已经有一个可运行的 Python开发环境。
使用pip安装
pip install minio
使用源码安装
git clone https://github.com/minio/minio-py
cd minio-py
python setup.py install
"""

def printer(name, text, *args):
    log_ext = ' '.join([str(x) for x in args]) if args else ''
    log_str = f"[{hyellow(name)}] {text} {log_ext}"
    print(log_str)


class MinioOpt:
    """Minio操作类"""

    def __init__(self, host, port, access_key, secret_key, bucket_name=None, **kwargs):
        # 连接minio
        self.minioClient = Minio(f"{host}:{port}", access_key=access_key, secret_key=secret_key, secure=False)

        # 初始化桶，不存在就创建
        self.bucket_name = bucket_name.strip()
        self._init_bucket()

    def _init_bucket(self):
        if self.bucket_name:
            try:
                if not self.minioClient.bucket_exists(self.bucket_name):
                    self.minioClient.make_bucket(self.bucket_name, location="cn-north-1")
            except Exception as IBE:
                printer(
                    "MINIO-init",
                    f"Error in checking minio bucket: {hyellow(self.bucket_name)}  -->{hred(IBE)}"
                )
                return False
            return True

    def save_file(self, file_name, path):
        """
        将文件上传到文件系统
        bucket: 存储桶
        file_name: 上传文件的名称：1.jpg
        path: 文件路径：/tmp/1.jpg

        return: etag: 对象的etag值。
        """
        try:
            etag = self.minioClient.fput_object(self.bucket_name, file_name, path)
        except Exception as err:
            return False, str(err), None

        return True, "", etag

    def save_data(self, object_name, data, length, content_type="application/octet-stream", metadata=None):
        """
        将文件对象上传到文件系统
        bucket: 存储桶
        object_name: 对象名
        data: io.RawIOBase, 任何实现了io.RawIOBase的python对象。
        length: 对象的总长度。
        content_type: 对象的Content type。
        path: 文件路径：/tmp/1.jpg
        metadata: dict, 其它元数据

        return: etag: 对象的etag值。

        外层使用姿势：
            bucket = 'my_bucket'
            object_name = 'my_object'
            minio_ins = MinioStorage()
            with open('my-testfile', 'rb') as file_data:
                file_stat = os.stat('my-testfile')
                minio_ins.save_data(bucket, object_name, file_data, file_stat.st_size)
        """


        try:
            etag = self.minioClient.put_object(self.bucket_name, object_name, data, length)
            return 0, "", etag
        except Exception as err:
            return False, str(err), None

    def save_bytes(self, file_name, file_bytes, content_type=None, metadata=None):
        if isinstance(file_bytes, str):
            file_bytes = file_bytes.encode()
        file_length = len(file_bytes)
        io = BytesIO(file_bytes)
        io.seek(0)
        return self.save_data(object_name=file_name, data=io, length=file_length, content_type=content_type, metadata=metadata)

    def get_file_object(self, file_name):
        """
        获取文件对象
        bucket: 存储桶
        file_name: 上传文件的名称：1.jpg
        """
        try:
            file_object = self.minioClient.get_object(self.bucket_name, file_name, request_headers=None)
            return 0, "", file_object
        except Exception as err:
            return False, str(err), None

    def load_file(self, file_name, file_path):
        """
        下载并将文件保存到本地
        bucket: 存储桶
        file_name: 上传文件的名称：1.jpg
        file_path: 要存储的本地文件路径：/tmp/1.jpg
        注意：本API支持的最大文件大小是5GB
        返回文件对象
        """
        try:
            file_object = self.minioClient.fget_object(self.bucket_name, file_name, file_path)
        except Exception as err:
            return -1, str(err), None

        return 0, "", file_object

    def remove_file(self, file_name):
        """
        删除存储文件
        bucket: 存储桶
        file_name: 上传文件的名称：1.jpg
        """
        try:
            self.minioClient.remove_object(self.bucket_name, file_name)
        except Exception as err:
            return -1, str(err)

        return 0, ""

    def remove_incomplete_file(self, file_name):
        """
        删除一个未完整上传的文件
        bucket: 存储桶
        file_name: 上传文件的名称：1.jpg
        """
        try:
            self.minioClient.remove_incomplete_upload(self.bucket_name, file_name)
        except Exception as err:
            return -1, str(err)
        return 0, ""


minio_html = MinioOpt(MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME)

if __name__ == '__main__':
    test_minio = minio_html
    # test_minio = MinioOpt(
    #     host="10.96.128.45",
    #     port=9000,
    #     access_key="admin",
    #     secret_key="root123456",
    #     bucket_name="html-bucket"
    # )

    # test_sta, test_err, test_tag = test_minio.save_file(
    #     file_name=""".env""",
    #     path="./../../conf/.env"
    # )
    # test_post_sta, test_post_err, test_post_tag = test_minio.save_bytes(
    #     file_name="""a.txt""",
    #     file_bytes="123ahwdgalibwliaubhwfliuabwfliybaliyf"
    # )
    # print("test_post_sta:", test_post_sta)
    # print("test_post_err:", test_post_err)
    # print("test_post_tag:", test_post_tag[0])

    test_sta, test_err, test_tag = test_minio.get_file_object(
        "a.txt",
    )
    with open('my-testfile', 'wb') as file_data:
        for d in test_tag.stream(32 * 1024):
            file_data.write(d)

