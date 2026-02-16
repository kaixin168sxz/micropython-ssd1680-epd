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

epd.init_full()
epd.fill(1)
epd.fill_rect(0, 0, 40, 16, 0)
epd.text('ABC', 0, 0, 1, size=2)
epd.show_full()

epd.init_part()
epd.text('ABC', 0, 24, 0, size=2)
epd.show_part(0, 24, 40, 16)

# 休眠
epd.sleep()