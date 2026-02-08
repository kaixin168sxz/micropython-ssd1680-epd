from machine import Pin, SPI
from epd import EPD

# 定义引脚
miso = Pin(5)
mosi = Pin(6)
sck = Pin(4)
cs = Pin(2)
dc = Pin(1)
rst = Pin(3)
busy = Pin(0)
spi = SPI(1, baudrate=2000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)

# 初始化对象
epd = EPD(104, 212, spi, cs, dc, rst, busy)
epd.rotation = 3

epd.init_full()  # 初始化（全局刷新模式）
epd.fill(1)      # 填充白色
epd.rect(32, 88, 32, 32, 0)     # 显示方块
epd.text('B', 0, 0, 0, size=2)         # 显示文字
epd.show_full()     # 全局刷新

epd.init_part()  # 初始化（局部刷新模式）
for i in range(100, 0, -1):
    epd.fill_rect(0, 0, 64, 64, 1)  # 清空部分区域（绘制实心白色方块）
    epd.text(str(i), 0, 0, 0, size=3)       # 显示文字
    epd.show_part(0, 0, 64, 64)     # 局部刷新

# 休眠
epd.sleep()