import httpx
import argparse
import json
import urllib
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import Mapping
from sys import stderr
from pathlib import Path
import packaging.version
import time


def app_version():
    import importlib.metadata
    return importlib.metadata.version(__package__
                                      or __name__).removesuffix('+editable')


APP_VERSION = app_version()


def retry(times: int, delay_secs: int):
    def decorator(func):
        def warpper(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(
                        f'error: retry().exception thrown {e} when attempting to run {func}({args}&{kwargs}), attempt {attempt} of {times}',file=stderr)
                    attempt += 1
                    time.sleep(delay_secs)
            return func(*args, **kwargs)
        return warpper
    return decorator

def nvl(*values):
    for v in values:
        if v is not None:
            return v
    return None


@dataclass
class ExtensionInfo:
    name: str
    version: str
    publisher: str

    @property
    def file_url(self):
        prefix = 'https://marketplace.visualstudio.com/_apis/public/gallery/publishers'
        url = f'{prefix}/{self.publisher}/vsextensions/{self.name}/{self.version}/vspackage'
        return url


class ExtensionMan:

    def __init__(self, full_name: str, output_file: Path, tls_verify: bool):
        self.tls_verify: bool = tls_verify
        self.full_name = full_name
        self.output_file = output_file

    def __download(self, url: str) -> bytes:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'}
        data = bytearray()
        with httpx.stream('GET',
                          url=url,
                          headers=headers,
                          verify=self.tls_verify,
                          follow_redirects=True) as rsp:
            if rsp.status_code !=200:
                return None
            for chunk in rsp.iter_bytes():
                data.extend(chunk)
            return bytes(data)

    def __get_page(self) -> str:
        url = f'https://marketplace.visualstudio.com/items?itemName={urllib.parse.quote(self.full_name)}'
        content = self.__download(url=url)
        return content.decode('utf-8')

    def ext_info(self) -> ExtensionInfo:
        html = self.__get_page()
        soup = BeautifulSoup(html, 'html.parser')
        s = soup.find('script', {'class': 'jiContent'})
        jons_data = s.text
        info = json.loads(jons_data)
        publisher = info['Resources']['PublisherName']
        name = info['Resources']['ExtensionName']
        version = info['Resources']['Version']
        return ExtensionInfo(name=name, version=version, publisher=publisher)

    @retry(times=10,delay_secs=10)
    def download(self, ext: ExtensionInfo):
        data = self.__download(ext.file_url)
        if not data:
            raise RuntimeError('download error.')
        with open(file=self.output_file, mode='wb') as f:
            f.write(data)


def init_args():
    """
    init args
    :return:
    """
    parser = argparse.ArgumentParser(
        prog=f'vsc-ed',
        description='Vidual studio code extension downloader',
        epilog='download and query')
    parser.add_argument('action', choices=['query', 'download'], help='Action')
    parser.add_argument('-n', help='extension name', required=True)
    parser.add_argument('-v', help='extension version check', required=False)
    parser.add_argument('-o', help='file name', required=False)
    parser.add_argument('--disable-tls-verify',
                        action='store_false',
                        help='disable TLS check',
                        required=False)
    parser.add_argument('--version',
                        action='version',
                        version=f'%(prog)s {APP_VERSION}')
    args = parser.parse_args()
    return args


def main():
    args = init_args()
    op = args.action
    ext_full_name = args.n
    ext_version = args.v
    disable_tls_verify = args.disable_tls_verify
    output_file = Path(nvl(args.o, f'{ext_full_name}.vsix'))
    ext_man = ExtensionMan(full_name=ext_full_name,
                           output_file=output_file,
                           tls_verify=not disable_tls_verify)
    ext_info = ext_man.ext_info()
    ext_json = json.dumps(asdict(ext_info))
    current_version = packaging.version.parse(ext_info.version)
    if not ext_version or (ext_version and
                           current_version > packaging.version.parse(ext_version)):
        if op == 'download':
            ext_man.download(ext_info)
    if op == 'query':
        print(ext_json)


if __name__ == '__main__':
    main()