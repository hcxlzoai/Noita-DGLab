import asyncio
from math import ceil
import re
import qrcode
import websockets
import hjson
from pydglab_ws import (
    StrengthData,
    Channel,
    StrengthOperationType,
    RetCode,
    DGLabWSServer,
)

PULSE_DATA = {
    # '呼吸': [
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 5, 10, 20)),
    #     ((10, 10, 10, 10), (20, 25, 30, 40)), ((10, 10, 10, 10), (40, 45, 50, 60)),
    #     ((10, 10, 10, 10), (60, 65, 70, 80)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((0, 0, 0, 0), (0, 0, 0, 0)), ((0, 0, 0, 0), (0, 0, 0, 0)), ((0, 0, 0, 0), (0, 0, 0, 0))
    # ],
    # '潮汐': [
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 4, 8, 17)),
    #     ((10, 10, 10, 10), (17, 21, 25, 33)), ((10, 10, 10, 10), (50, 50, 50, 50)),
    #     ((10, 10, 10, 10), (50, 54, 58, 67)), ((10, 10, 10, 10), (67, 71, 75, 83)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 98, 96, 92)),
    #     ((10, 10, 10, 10), (92, 90, 88, 84)), ((10, 10, 10, 10), (84, 82, 80, 76)),
    #     ((10, 10, 10, 10), (68, 68, 68, 68))
    # ],
    # "连击": [
    #     ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (100, 92, 84, 67)),
    #     ((10, 10, 10, 10), (67, 58, 50, 33)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 0, 0, 1)),
    #     ((10, 10, 10, 10), (2, 2, 2, 2)),
    # ],
    # '快速按捏': [
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((0, 0, 0, 0), (0, 0, 0, 0))
    # ],
    # '按捏渐强': [
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (29, 29, 29, 29)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (52, 52, 52, 52)),
    #     ((10, 10, 10, 10), (2, 2, 2, 2)), ((10, 10, 10, 10), (73, 73, 73, 73)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (87, 87, 87, 87)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0))
    # ],
    # '心跳节奏': [
    #     ((110, 110, 110, 110), (100, 100, 100, 100)), ((110, 110, 110, 110), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (75, 75, 75, 75)),
    #     ((10, 10, 10, 10), (75, 77, 79, 83)), ((10, 10, 10, 10), (83, 85, 88, 92)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 0, 0, 0))
    # ],
    "压缩": [
        ((25, 25, 24, 24), (100, 100, 100, 100)),
        ((24, 23, 23, 23), (100, 100, 100, 100)),
        ((22, 22, 22, 21), (100, 100, 100, 100)),
        ((21, 21, 20, 20), (100, 100, 100, 100)),
        ((20, 19, 19, 19), (100, 100, 100, 100)),
        ((18, 18, 18, 17), (100, 100, 100, 100)),
        ((17, 16, 16, 16), (100, 100, 100, 100)),
        ((15, 15, 15, 14), (100, 100, 100, 100)),
        ((14, 14, 13, 13), (100, 100, 100, 100)),
        ((13, 12, 12, 12), (100, 100, 100, 100)),
        ((11, 11, 11, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)),
    ],
    # '节奏步伐': [
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 5, 10, 20)),
    #     ((10, 10, 10, 10), (20, 25, 30, 40)), ((10, 10, 10, 10), (40, 45, 50, 60)),
    #     ((10, 10, 10, 10), (60, 65, 70, 80)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 6, 12, 25)),
    #     ((10, 10, 10, 10), (25, 31, 38, 50)), ((10, 10, 10, 10), (50, 56, 62, 75)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 8, 16, 33)), ((10, 10, 10, 10), (33, 42, 50, 67)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 12, 25, 50)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (100, 100, 100, 100))
    # ],
    # '颗粒摩擦': [
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (0, 0, 0, 0))
    # ],
    # '渐变弹跳': [
    #     ((10, 10, 10, 10), (1, 1, 1, 1)), ((10, 10, 10, 10), (1, 9, 18, 34)),
    #     ((10, 10, 10, 10), (34, 42, 50, 67)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((0, 0, 0, 0), (0, 0, 0, 0)), ((0, 0, 0, 0), (0, 0, 0, 0))
    # ],
    # '波浪涟漪': [
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 12, 25, 50)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (73, 73, 73, 73))
    # ],
    # '雨水冲刷': [
    #     ((10, 10, 10, 10), (34, 34, 34, 34)), ((10, 10, 10, 10), (34, 42, 50, 67)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((0, 0, 0, 0), (0, 0, 0, 0)),
    #     ((0, 0, 0, 0), (0, 0, 0, 0))
    # ],
    # '变速敲击': [
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((110, 110, 110, 110), (100, 100, 100, 100)),
    #     ((110, 110, 110, 110), (100, 100, 100, 100)), ((110, 110, 110, 110), (100, 100, 100, 100)),
    #     ((110, 110, 110, 110), (100, 100, 100, 100)), ((0, 0, 0, 0), (0, 0, 0, 0))
    # ],
    # "信号灯": [
    #     ((197, 197, 197, 197), (100, 100, 100, 100)),
    #     ((197, 197, 197, 197), (100, 100, 100, 100)),
    #     ((197, 197, 197, 197), (100, 100, 100, 100)),
    #     ((197, 197, 197, 197), (100, 100, 100, 100)),
    # ((10, 10, 10, 10), (0, 0, 0, 0)),
    # ((10, 10, 10, 10), (0, 8, 16, 33)),
    # ((10, 10, 10, 10), (33, 42, 50, 67)),
    # ((10, 10, 10, 10), (100, 100, 100, 100)),
    # ],
    # '挑逗1': [
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 6, 12, 25)),
    #     ((10, 10, 10, 10), (25, 31, 38, 50)), ((10, 10, 10, 10), (50, 56, 62, 75)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100))
    # ],
    # '挑逗2': [
    #     ((10, 10, 10, 10), (1, 1, 1, 1)), ((10, 10, 10, 10), (1, 4, 6, 12)),
    #     ((10, 10, 10, 10), (12, 15, 18, 23)), ((10, 10, 10, 10), (23, 26, 28, 34)),
    #     ((10, 10, 10, 10), (34, 37, 40, 45)), ((10, 10, 10, 10), (45, 48, 50, 56)),
    #     ((10, 10, 10, 10), (56, 59, 62, 67)), ((10, 10, 10, 10), (67, 70, 72, 78)),
    #     ((10, 10, 10, 10), (78, 81, 84, 89)), ((10, 10, 10, 10), (100, 100, 100, 100)),
    #     ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (0, 0, 0, 0)),
    #     ((0, 0, 0, 0), (0, 0, 0, 0))
    # ]
}

last_hp: float = 0
last_percent: float = 0


async def set_percent_yx(hp, max_hp):
    global last_percent, last_hp
    if last_hp == hp:
        return

    print("HP:", hp)
    dmg = last_hp - hp
    last_hp = hp
    if dmg > 0:
        last_percent = percent_min + (dmg / dmg_maximum) * (1 - percent_min)
    else:
        return

    t = time_minimum + (time_maximum - time_minimum) * last_percent
    await asyncio.sleep(t)

    last_percent = 0


async def set_percent_orig(hp, max_hp):
    global last_percent, last_hp
    if last_hp != hp:
        if last_hp > hp:
            dmg = last_hp - hp
            last_percent = (
                0.82 if dmg < 10 else 0.89 if dmg < 20 else 0.95 if dmg < 30 else 1
            )
        else:
            percent = 0
        print("HP:", hp)
        last_hp = hp
    else:
        return

    if last_percent == 0.89:
        await asyncio.sleep(1)
    elif last_percent == 0.95:
        await asyncio.sleep(1.5)
    elif last_percent == 1:
        await asyncio.sleep(3)
    else:
        await asyncio.sleep(0.5)

    last_percent = 0


class WebSocketClient:

    def __init__(self, n=0, url="ws://127.0.0.1:9777", token="-jsOdyLDVJK9GPisgo8oU"):
        self.n = n
        self.url = url
        self.token = token
        self.websocket = None
        self.err_cnt = 0

    async def connect(self):
        """连接到WebSocket服务器"""
        while True:
            try:
                self.websocket = await websockets.connect(self.url)
                print(f"已连接: {self.url}")
                global last_hp
                last_hp = 0

                auth_message = f'AUTH "{self.token}"'
                await self.websocket.send(auth_message)
                self.err_cnt = 0

                return True

            except ConnectionRefusedError as e:
                if self.err_cnt % 100 == 0:
                    print(f"cheatgui未运行，连接失败 {self.err_cnt}")
                self.err_cnt += 1
                continue
            except Exception as e:
                print(f"连接错误: {e}")
                return False

    async def send_messages(self):
        """发送消息到服务器"""
        message = "get_health()"
        while True:
            try:
                if last_percent == 0:
                    await self.websocket.send(message)
                await asyncio.sleep(0.1)  # 控制发送频率

            except asyncio.CancelledError:
                break
            except Exception as e:
                await asyncio.sleep(1)
                continue


    async def receive_messages(self):
        """接收服务器消息"""

        def extract_double(data_str):
            match = re.search(r'"([0-9.]+)", "([0-9.]+)"', data_str)
            a, b = float(match.group(1)) * 25, float(match.group(2)) * 25
            return a, b

        while True:
            try:
                async for message in self.websocket:
                    if not message.startswith("RES>"):
                        continue
                    hp, max_hp = extract_double(message)
                    await set_percent_yx(hp, max_hp)
                    # print(f"Received: {hp}, {max_hp}")

            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                # print(f"\n接收错误: {e}")
                pass

    async def test(self):
        if self.n == 0:
            return
        while True:
            global hp
            if hp < 1_0000:
                hp = 1000_0000
            hp -= self.n
            await asyncio.sleep(3)

    async def run(self):
        """运行客户端"""
        await self.test()

        if not await self.connect():
            return

        send_task = asyncio.create_task(self.send_messages())
        receive_task = asyncio.create_task(self.receive_messages())

        try:
            done, pending = await asyncio.wait(
                [send_task, receive_task], return_when=asyncio.FIRST_COMPLETED
            )
        finally:
            for task in [send_task, receive_task]:
                if not task.done():
                    task.cancel()

            # 关闭连接
            if self.websocket:
                await self.websocket.close()

            print("连接被关闭")


class DG_LAB:
    def __init__(self):
        self.client = None
        self.a_limit = self.b_limit = 0
        self.percent = 0
        self.url = None

    def print_qrcode(self):
        """输出二维码到终端界面"""
        qr = qrcode.QRCode()
        qr.add_data(self.url)
        qr.print_ascii(invert=True)

    async def DG_recv_limit(self):
        async for data in self.client.data_generator():
            if isinstance(data, StrengthData):
                self.a_limit = data.a_limit
                self.b_limit = data.b_limit
                # print(f'上限：{data.a_limit}  {data.b_limit}')
            elif data == RetCode.CLIENT_DISCONNECTED:
                print("App 已断开连接，你可以尝试重新扫码进行连接绑定")
                self.print_qrcode()
                await self.client.rebind()
                print("重新绑定成功")
            await asyncio.sleep(0)

    async def DG_send_strength(self):
        pulse_data_iterator = iter(PULSE_DATA.values())
        pulse_data_current = next(pulse_data_iterator, None)
        if not pulse_data_current:
            pulse_data_iterator = iter(PULSE_DATA.values())
        while True:
            try:
                if self.percent == last_percent:
                    await asyncio.sleep(0)
                    continue
                await self.client.set_strength(
                    Channel.A,
                    StrengthOperationType.SET_TO,
                    round(self.a_limit * last_percent),
                )
                await self.client.set_strength(
                    Channel.B,
                    StrengthOperationType.SET_TO,
                    round(self.b_limit * last_percent),
                )
                self.percent = last_percent
                # print(f'{self.percent}  强度：{round(self.a_limit * latest_percent)}')

                await self.client.add_pulses(Channel.A, *(pulse_data_current * 3))
            except Exception:
                pass

    async def run(self):
        server = await DGLabWSServer("0.0.0.0", 5678, 60).__aenter__()
        self.client = client = server.new_local_client()

        self.url = client.get_qrcode(f"ws://{config['ip']}:5678")
        print("请用 DG-Lab App 扫描二维码以连接")
        print(self.url)
        self.print_qrcode()

        await client.bind()
        print(f"已与 App {client.target_id} 成功绑定")

        send_task = asyncio.create_task(self.DG_send_strength())
        receive_task = asyncio.create_task(self.DG_recv_limit())

        try:
            done, pending = await asyncio.wait(
                [send_task, receive_task], return_when=asyncio.FIRST_COMPLETED
            )
        finally:
            for task in [send_task, receive_task]:
                if not task.done():
                    task.cancel()

            print("DG-LAB连接关闭")


async def Get_health_ws():
    while True:
        client = WebSocketClient(0)
        await client.run()


async def DG_LAB_run():
    while True:
        dg = DG_LAB()
        await dg.run()


if __name__ == "__main__":
    try:
        with open("config.hjson", "r", encoding="utf-8") as f:
            config = hjson.load(f)
            dmg_maximum = config["damage_maximum"]
            percent_min = config["percent_minimum"]
            time_minimum = config["time_minimum"]
            time_maximum = config["time_maximum"]
            print("配置文件已加载, 若有修改请按CTRL+C重启程序")
    except Exception as e:
        print("配置文件加载失败，是否在同一个文件夹下?")

    async def run():
        await asyncio.gather(DG_LAB_run(), Get_health_ws())

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("程序已退出")
