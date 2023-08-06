import tqdm     # 打印进度条
import requests
from io import BytesIO
def format_file_size(bites: int):
    bites = int(bites)
    kb = bites / 1024
    if kb < 1:
        return f"{bites} b"

    mb = kb / 1024
    if mb < 1:
        return f"{round(kb, 2)} Kb"

    gb = mb / 1024
    if gb < 1:
        return f"{round(mb, 2)} Mb"

    tb = gb / 1024
    if tb < 1:
        return f"{round(gb, 2)} Gb"
    return f"{round(tb, 2)} Tb"


link = "www.baidu.com"
# 流下载
file_res = requests.get(link, stream=True, timeout=(20, 120))
# 总大小
dl_content_length = int(file_res.headers["Content-Length"])
dl_content_type = file_res.headers["Content-Type"]

note_str = f"no cache found, downloading: [ {link} ], size: {format_file_size(dl_content_length)}"
bio_file = BytesIO()
tq_content_length = int(dl_content_length / 1024 + 0.5)
for chunk in tqdm.tqdm(desc=note_str,                               # 前缀
                       iterable=file_res.iter_content(1024),        # 每次下载1M
                       total=tq_content_length,
                       unit="k"):
    bio_file.write(chunk)
bio_file.seek(0)
bio_file.close()