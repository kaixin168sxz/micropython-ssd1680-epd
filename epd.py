"""
Driver for ssd1680 epd.
"""

"""
A driver to drive ssd1680 epd in microython.
Last edited: 2026.2.8

MIT License
Copyright (c) 2017 Waveshare
Copyright (c) 2018 Mike Causer
Copyright (c) 2026 kaixin168sxz
"""

from time import sleep_ms
import ustruct

# framebuf or adafruit_framebuf
# from framebuf import FrameBuffer, MONO_HMSB      # framebuf
from adafruit_framebuf import FrameBuffer, MHMSB   # adafruit_framebuf
MONO_HMSB = MHMSB

class EPD(FrameBuffer):
    # LUT表（定义局部刷新的行为）
    # https://blog.csdn.net/weixin_53556090/article/details/146292375
    LUT_PARTIAL_UPDATE = bytearray([
        0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x40, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00,
        0x04, 0x00, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00,
    ])

    def __init__(self, w, h, spi, cs, dc, rst, busy):
        self.buffer = bytearray(w * h // 8)
        super().__init__(self.buffer, w, h, MONO_HMSB)
        self.fill(1)
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = w
        self.height = h

    def _command(self, command, data=None):
        """
        Send command to epd.
        """
        self.dc(0)
        self.cs(0)
        # print("command=", command)
        try:
            self.spi.write(bytearray([command]))
        except:
            self.spi.write(command)
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        """
        Send data to epd.
        """
        self.cs(0)
        self.dc(1)
        self.spi.write(data)
        self.cs(1)

    def set_memory_area(self, x_start, y_start, x_end, y_end):
        self._command(b'\x44')
        self._data(bytearray([(x_start >> 3) & 0xFF]))
        self._data(bytearray([(x_end >> 3) & 0xFF]))
        self._command(b'\x45', ustruct.pack("<HH", y_start, y_end))

    def set_memory_pointer(self, x, y):
        self._command(b'\x4E')
        self._data(bytearray([(x >> 3) & 0xFF]))
        self._command(b'\x4F', ustruct.pack("<H", y))
        self.wait_until_idle()

    def wait_until_idle(self):
        # 1 -> BUSY
        # 0 -> FREE
        while self.busy.value() == 1:
            sleep_ms(10)

    def reset(self):
        self.rst(0)
        sleep_ms(10)
        self.rst(1)
        sleep_ms(10)

    def init_full(self):
        self.reset()
        self.wait_until_idle()
        self._command(b'\x12')
        self.wait_until_idle()

        self._command(b'\x01')  # Driver output control
        self._data(b'\x27')
        self._data(b'\x01')
        self._data(b'\x00')

        self._command(b'\x11')  # data entry mode
        self._data(b'\x03')  # 这里影响内容镜像

        self._command(b'\x44')  # set Ram-X address start/end position
        self._data(b'\x00')  # X起始点为0（1个字节）
        self._data(b'\x0C')  # X终止点为（1个字节）0x0F-->(15+1)*8=128

        self._command(b'\x45')  # set Ram-Y address start/end position
        self._data(b'\x00')  # Y设置起始点为 0（2个字节）
        self._data(b'\x00')
        self._data(b'\xDB')  # 终止点为（2个字节）：0x0127-->(295+1)=296
        self._data(b'\x00')

        self._command(b'\x3C')  # BorderWavefrom
        self._data(b'\x05')

        self._command(b'\x21')  # Display update control
        self._data(b'\x00')
        self._data(b'\x80')

        self._command(b'\x18')  # Read built-in temperature sensor
        self._data(b'\x80')

        self._command(b'\x4E')  # set RAM x address count to 0
        self._data(b'\x00')
        self._command(b'\x4F')  # set RAM y address count to 0X199
        self._data(b'\x27')
        self._data(b'\x01')
        self.wait_until_idle()

        # set FULL_LUT (可省略)
        # self.set_lut(self.LUT_FULL_UPDATE)
        # self.wait_until_idle()

    def show_full(self):
        self.set_memory_pointer(0, 0)
        self._command(b'\x24')
        self._data(self.buffer)

        self._command(b'\x22')  # Display Update Control
        self._data(b'\xF7')
        self._command(b'\x20')  # Activate Display Update Sequence
        self.wait_until_idle()

    def init_part(self):
        self.wait_until_idle()

        # set LUT
        self._command(b'\x32')
        self._data(self.LUT_PARTIAL_UPDATE)

        self._command(b'\x3C')
        self._data(b'\x05')

        self._command(b'\x22')  # Display Update Control 2
        self._data(b'\xCF')
        self._command(b'\x20')  # Master Activation
        self.wait_until_idle()

    @staticmethod
    def get_sub_buffer(fb, x, y, w, h):
        sub_buffer = bytearray(w * h // 8)
        sub_fb = FrameBuffer(sub_buffer, w, h, MONO_HMSB)

        for row in range(0, h):
            for col in range(0, w):
                sub_fb.pixel(col, row, fb.pixel(x + col, y + row)) # 复制数据 (fb -> sub_fb)

        return sub_buffer

    def show_part(self, x, y, w, h):
        x = x & 0xF8    # 保证x坐标为8的倍数
        w = w & 0xF8    # 保证w宽度为8的倍数
        x_end = self.width - 1 if x + w >= self.width else x + w - 1
        y_end = self.height - 1 if y + h >= self.height else y + h - 1

        self.set_memory_area(x, y, x_end, y_end)
        self.set_memory_pointer(x, y)

        # 0x24寄存器控制黑/白
        self._command(b'\x24', self.get_sub_buffer(self, x, y, w, h))
        # 0x26寄存器控制第三色 (如红) （单色屏可省略）
        # self._command(b'\x26', self.get_sub_buffer(self, x, y, w, h))

        self._command(b'\x22')
        # 0xCF: Enable clock signal -> Enable Analog -> Display with DISPLAY Mode 2 -> Disable Analog -> Disable OSC
        # （见ssd1680规格书 P26）
        self._data(b'\xCF')
        self._command(b'\x20')
        self.wait_until_idle()

    def sleep(self):
        self._command(0x10)
        self.wait_until_idle()