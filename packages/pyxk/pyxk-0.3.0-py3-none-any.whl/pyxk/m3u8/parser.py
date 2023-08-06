from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
shlex = LazyLoader("shlex", globals())
shutil = LazyLoader("shutil", globals())
asyncio = LazyLoader("asyncio", globals())
warnings = LazyLoader("warnings", globals())
threading = LazyLoader("threading", globals())
subprocess = LazyLoader("subprocess", globals())

m3u8 = LazyLoader("m3u8", globals())
aiohttp = LazyLoader("aiohttp", globals())
aiofiles = LazyLoader("aiofiles", globals())
panel = LazyLoader("panel", globals(), "rich.panel")
console = LazyLoader("console", globals(), "rich.console")
columns = LazyLoader("columns", globals(), "rich.columns")
progress = LazyLoader("progress", globals(), "rich.progress")

aes = LazyLoader("aes", globals(), "pyxk.aes")
utils = LazyLoader("utils", globals(), "pyxk.utils")
requests = LazyLoader("requests", globals(), "pyxk.requests")



class M3U8Init:
    """M3U8 解析器初始化类"""
    default_video_name = "index.mp4"
    default_aiohttp_limit = 8

    def __init__(
        self,
        video_path=None,
        *,
        rerequest=None,
        delete_m3u8file=None,
        reserve_segments=None
    ):
        """M3U8 INIT
        :params: video_path: 视频保存路径
        :params: rerequest: 重新请求 m3u8 文件(default: False)
        :params: delete_m3u8file: 下载完成后删除 m3u8 文件(default: False)
        :params: reserve_segments: 下载完成后保留 segments 文件(default: False)
        """
        self._video_path = os.path.abspath(video_path) if video_path else os.getcwd()
        self._rerequest  = False
        self._delete_m3u8file  = False
        self._reserve_segments = False
        self._video_name = self.default_video_name
        self._session = requests.Session()
        self._console = console.Console()
        self._limit = self.default_aiohttp_limit
        self._initialization_attr(rerequest, delete_m3u8file, reserve_segments)

    def _initialization_attr(self, rerequest, delete_m3u8file, reserve_segments):
        if rerequest is not None:
            self._rerequest = bool(rerequest)
        if delete_m3u8file is not None:
            self._delete_m3u8file = bool(delete_m3u8file)
        if reserve_segments is not None:
            self._reserve_segments = bool(reserve_segments)

    @property
    def video_path(self):
        """m3u8视频文件夹路径"""
        return self._video_path

    @video_path.setter
    def video_path(self, path):
        self._video_path = os.path.abspath(path)

    @property
    def video_name(self):
        """m3u8视频文件名称"""
        return self._video_name

    @video_name.setter
    def video_name(self, name):
        video = os.path.join(self.video_path, name or self.default_video_name)
        video = "-".join(video.split())
        video = utils.rename_file(video, suffix="mp4")[0]
        self._video_path, self._video_name = os.path.split(video)

    @property
    def _m3u8file_path(self):
        """m3u8 textfile 保存路径"""
        m3u8file_path = "." + self.video_name.removesuffix(".mp4") + "_m3u8file"
        return os.path.join(self.video_path, m3u8file_path)

    @property
    def limit(self):
        """异步请求连接limit"""
        return self._limit

    @limit.setter
    def limit(self, value):
        if (
            not isinstance(value, int)
            or value <= 0
        ):
            value = self.default_aiohttp_limit
        self._limit = value


class M3U8(M3U8Init):
    """M3U8解析器"""

    def _m3u8_secret(self, uri, file, **kwargs):
        """获取 m3u8 密钥 - 本地获取 或 请求网络资源"""
        file = os.path.join(self._m3u8file_path, utils.hash256(file)) + ".key"
        # 1.获取本地文件
        if not self._rerequest and os.path.isfile(file):
            with open(file=file, mode="rb") as fileobj:
                content = fileobj.read()
        # 2.获取网络资源
        else:
            kwargs.setdefault("method", "GET")
            content = self._session.request(url=uri, **kwargs).content
        return content


    def _sava_secret(self, file, content):
        """保存 m3u8 密钥"""
        file = os.path.join(self._m3u8file_path, utils.hash256(file)) + ".key"

        if not os.path.isfile(file) or self._rerequest:
            with utils.open(file=file, mode="wb") as fileobj:
                fileobj.write(content)


    def _m3u8_content(self, uri, file, **kwargs):
        """获取m3u8内容 - 本地获取 或 请求网络资源"""
        file = os.path.join(self._m3u8file_path, utils.hash256(file)) + ".m3u8"
        # 1.获取本地文件
        if not self._rerequest and os.path.isfile(file):
            with open(file=file, encoding="utf-8") as fileobj:
                content = fileobj.read()
        # 2.获取网络资源
        else:
            kwargs.setdefault("method", "GET")
            content = self._session.request(url=uri, **kwargs).text
        return content


    def _sava_m3u8file(self, file, content, encoding="utf-8"):
        """保存 m3u8 文件"""
        file = os.path.join(self._m3u8file_path, utils.hash256(file)) + ".m3u8"

        if not os.path.isfile(file) or self._rerequest:
            with utils.open(file=file, mode="w", encoding=encoding) as fileobj:
                fileobj.write(content)


    def load_m3u8_uri(
        self,
        uri,
        video=None,
        *,
        probe=False,
        rerequest=None,
        delete_m3u8file=None,
        reserve_segments=None,
        **kwargs
    ):
        """解析 m3u8 网络链接"""
        self.video_name = video
        self._initialization_attr(
            rerequest=rerequest,
            delete_m3u8file=delete_m3u8file,
            reserve_segments=reserve_segments
        )
        # content
        content = self._m3u8_content(uri=uri, file=uri, **kwargs)
        return self.load_m3u8_con(
            content=content,
            uri=uri,
            video=self.video_name,
            probe=probe,
            rerequest=rerequest,
            delete_m3u8file=delete_m3u8file,
            reserve_segments=reserve_segments,
            **kwargs
        )


    def load_m3u8_con(
        self,
        content,
        uri=None,
        video=None,
        *,
        probe=False,
        rerequest=None,
        delete_m3u8file=None,
        reserve_segments=None,
        **kwargs
    ):
        """解析 m3u8 文本"""
        self.video_name = video
        self._initialization_attr(
            rerequest=rerequest,
            delete_m3u8file=delete_m3u8file,
            reserve_segments=reserve_segments
        )
        # content
        if not content.startswith("#EXTM3U"):
            m3u8file = os.path.abspath(content)
            if os.path.isfile(m3u8file):
                with open(m3u8file, encoding="utf-8") as fileobj:
                    content = fileobj.read()

        # 开始解析 m3u8
        m3u8_parser = _M3U8Parser(m3u8_instance=self)
        m3u8_parser.start_parsing(content=content, base_uri=uri, **kwargs)
        if not m3u8_parser.segments:
            return

        # 探测 不下载
        if not probe:
            # 开始异步下载
            m3u8_downloader = _M3U8Downloader(m3u8_instance=self, m3u8_parser=m3u8_parser)
            m3u8_downloader.start_downlaod()

            # 合并segments
            merge_result = self.__segments_merging(m3u8_downloader.store)
            if merge_result:
                # 删除segments
                if not reserve_segments:
                    shutil.rmtree(m3u8_downloader.store)

        # 删除 m3u8 文件
        if self._delete_m3u8file:
            for file in os.walk(self._m3u8file_path).__next__()[-1]:
                os.remove(os.path.join(self._m3u8file_path, file))
        if (
            os.path.isdir(self._m3u8file_path)
            and not os.listdir(self._m3u8file_path)
        ):
            os.rmdir(self._m3u8file_path)


    def __segments_merging(self, store):
        """使用ffmpeg合并segments"""
        files = os.walk(store).__next__()[-1]
        # 对files进行排序
        def sorted_files(file):
            file = file.rsplit(".", 1)[0]
            if file.isdigit():
                file = int(file)
            return hash(file)
        files = sorted(files, key=sorted_files)

        # 生成filelists文件
        filelists, filesize = os.path.join(self._m3u8file_path, "filelist.txt"), 0
        with open(filelists, "w", encoding="utf-8") as fileobj:
            for file in files:
                file = os.path.join(store, file)
                fileobj.write(f"file '{file}'\n")
                filesize += os.path.getsize(file) - 16400

        # ffmpeg合并代码
        video = os.path.join(self.video_path, self.video_name)
        merge_code = shlex.split(
            f"ffmpeg -loglevel quiet -f concat -safe 0 -i {filelists} -c copy {video} -y"
        )
        merge_complete = False

        # 合并函数
        def merge():
            try:
                subprocess.run(args=merge_code, check=True)
                os.remove(filelists)
            except FileNotFoundError as error:
                reason = getattr(error, "filename", None)
                if reason != "ffmpeg":
                    raise
                warnings.warn("没有ffmpeg, 调用失败")
            finally:
                nonlocal merge_complete
                merge_complete = True

        # 合并进度条函数
        def merge_progress():
            last_filesize = 0
            get_filesize = lambda file: os.path.getsize(file) if os.path.isfile(file) else 0
            # 进度条
            with progress.Progress(
                *(
                    progress.SpinnerColumn("line"),
                    progress.DownloadColumn(),
                    progress.BarColumn(finished_style="green"),
                    progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                    progress.TimeElapsedColumn()
                ),
                console=self._console,
                transient=True
            ) as progressing:

                progress_task = progressing.add_task(description=None,total=filesize)
                while True:
                    current_filesize = get_filesize(video)
                    progressing.update(progress_task, advance=current_filesize-last_filesize)
                    last_filesize = current_filesize
                    # 控制进度条退出
                    if merge_complete:
                        progressing.update(progress_task, advance=abs(filesize-last_filesize))
                        break

        task1 = threading.Thread(target=merge)
        task2 = threading.Thread(target=merge_progress)
        task1.start()
        task2.start()
        task1.join()
        task2.join()
        return os.path.isfile(video)


class _M3U8Downloader:
    """异步下载 segments"""
    default_timeout_total = 2 * 60

    def __init__(self, m3u8_instance, m3u8_parser):
        self.m3u8   = m3u8_instance
        self.parser = m3u8_parser
        self.store  = os.path.join(self.m3u8._m3u8file_path, "segments")
        # m3u8 解密器
        self.cipher = {
            index: aes.Cryptor(**keys["cipher"])
            for index, keys in self.parser.m3u8_keys.items()
        }
        self.progressing = None
        self.progress_task = None


    def start_downlaod(self):
        """开始异步下载"""
        os.makedirs(self.store, exist_ok=True)
        # 进度条
        with progress.Progress(
            *(
                progress.SpinnerColumn("line"),
                progress.TextColumn("[progress.description]{task.completed}/{task.total}"),
                progress.BarColumn(finished_style="green"),
                progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                progress.TimeElapsedColumn()
            ),
            console=self.m3u8._console,
        ) as self.progressing:
            self.progress_task = self.progressing.add_task(
                description=None,
                total=len(self.parser.segments)
            )
            asyncio.run(self.downloader())


    async def downloader(self):
        """下载管理器"""
        connector = aiohttp.TCPConnector(limit=self.m3u8.limit)
        timeout = aiohttp.ClientTimeout(total=self.default_timeout_total)
        headers = utils.default_headers()

        # 开启异步连接池
        async with aiohttp.ClientSession(
            connector=connector, timeout=timeout, headers=headers
        ) as session:
            # 创建异步任务
            tasks = [
                self.request(session, segment["uri"], index, segment["key"])
                for index, segment in self.parser.segments.items()
            ]
            await asyncio.gather(*tasks)


    async def request(self, session, url, file, key=None):
        """请求 和 保存 segments"""
        file = os.path.join(self.store, str(file)) + ".ts"
        if not os.path.isfile(file) or os.path.getsize(file) == 0:
            content = await self.send(session, url)
            # 解密 segments
            if self.cipher and key is not None:
                content = self.cipher[key].decrypt(content)
            # 保存 segment
            async with aiofiles.open(file, "wb") as fileobj:
                await fileobj.write(content)
        # 更新进度条
        self.progressing.update(self.progress_task, advance=1)


    @staticmethod
    async def send(session, url):
        """获取segment内容"""
        while True:
            try:
                async with session.get(url=url) as response:
                    # 异常状态码捕获
                    if 403 <= response.status <= 410:
                        raise aiohttp.InvalidURL(
                            f"invalid url:{str(response.url)!r}, status_code: {response.status!r}"
                        )
                    # 重试部分请求
                    if response.status != 200:
                        await asyncio.sleep(1)
                        continue
                    content = await response.content.read()
                    return content

            # 请求超时 重试
            except asyncio.exceptions.TimeoutError:
                await asyncio.sleep(1)

            # 连接错误 重试
            except (
                aiohttp.client_exceptions.ClientOSError,
                aiohttp.client_exceptions.ClientPayloadError,
                aiohttp.client_exceptions.ClientConnectorError,
            ):
                # warnings.warn(
                #     "请检查网络是否正常 !"
                # )
                await asyncio.sleep(2)

            # 服务器拒绝连接
            except aiohttp.client_exceptions.ServerDisconnectedError:
                # warnings.warn(
                #     "服务器拒绝连接 !"
                # )
                await asyncio.sleep(2)


class _M3U8Parser:
    """使用模块 m3u8(pip install m3u8) 进行解析"""

    def __init__(self, m3u8_instance):
        self.m3u8 = m3u8_instance
        self.m3u8obj = None
        self.m3u8_urls = []
        self.m3u8_keys = None
        self.segments = None
        self.playtime = None
        self._request = {}

    @property
    def base_uri(self):
        """base_uri"""
        if self.m3u8_urls:
            return self.m3u8_urls[-1]
        return None


    def start_parsing(self, content, base_uri, **kwargs):
        """开始解析m3u8"""
        self.m3u8_urls.append(base_uri)
        self.m3u8obj = m3u8.loads(content=content, uri=self.base_uri)
        self._request = kwargs
        # playlists
        self.parse_playlists()
        # m3u8 keys
        self.parse_m3u8_keys()
        # segments
        self.parse_segments()
        # display
        self.display()


    def parse_playlists(self):
        """解析 m3u8 播放列表"""
        if not self.m3u8obj.is_variant:
            return None

        # 获取带宽最大的 playlist 链接
        def sort_playlists(playlist):
            playlist.uri = playlist.absolute_uri
            return playlist.stream_info.bandwidth
        playlist_uri = sorted(self.m3u8obj.playlists, key=sort_playlists)[-1].uri

        # 保存文件
        if self.base_uri:
            self.m3u8._sava_m3u8file(file=self.base_uri, content=self.m3u8obj.dumps())

        # 获取新的 playlist 数据
        self.m3u8_urls.append(playlist_uri)
        content = self.m3u8._m3u8_content(uri=self.base_uri, file=self.base_uri, **self._request)
        self.m3u8obj = m3u8.loads(content=content, uri=self.base_uri)
        return self.parse_playlists()


    def parse_m3u8_keys(self):
        """解析 m3u8 keys"""
        m3u8_keys = dict(enumerate([key for key in self.m3u8obj.keys if key]))

        for index, key in m3u8_keys.copy().items():
            key.uri = key.absolute_uri
            # 获取密钥
            secret = self.m3u8._m3u8_secret(uri=key.uri, file=key.uri, **self._request)
            # 保存key
            self.m3u8._sava_secret(file=key.uri, content=secret)

            m3u8_keys[index] = {
                "cipher": {
                    "key": secret,
                    "iv": key.iv.removeprefix("0x")[:16] if key.iv else secret[:16],
                },
                "uri": key.uri,
                "method": key.method
            }
        self.m3u8_keys = m3u8_keys


    def parse_segments(self):
        """解析 m3u8 片段"""
        segments ,playtime = {}, 0

        for index, segment in enumerate(self.m3u8obj.segments):
            playtime += segment.duration
            segment.uri, segment_key = segment.absolute_uri, None
            # segment key 解析
            if segment.key and self.m3u8_keys:
                for keyindex, key in self.m3u8_keys.items():
                    if (
                        segment.key.absolute_uri == key["uri"]
                        and segment.key.method == key["method"]
                    ):
                        segment_key = keyindex
            # 收集 segment
            segments[index] = {"uri": segment.uri, "key": segment_key}

        # 保存 m3u8 到本地
        if self.base_uri and segments:
            self.m3u8._sava_m3u8file(file=self.base_uri, content=self.m3u8obj.dumps())
        self.segments, self.playtime = segments, playtime


    def display(self):
        """展示 m3u8 解析结果"""
        display = [
            # f"URI: {self.base_uri}",
            f"Video Name: [magenta]{self.m3u8.video_name}[/]",
            f"Video Path: {self.m3u8.video_path}",
            f"PlayTime: {utils.human_playtime_pr(self.playtime)}",
            f"Maximum: {len(self.segments)}",
            f"Encryption: {bool(self.m3u8_keys)}",
            f"Limit: {self.m3u8.limit}"
        ]
        display = [f"{i+1} {x}" for i, x in enumerate(display)]
        display.append(
            "[green b]Parsing success ![/]" if self.segments \
            else "[red b]Parsing failure ![/]"
        )
        self.m3u8._console.print(
            panel.Panel(columns.Columns(display), title="M3U8 Parsed", border_style="yellow")
        )
