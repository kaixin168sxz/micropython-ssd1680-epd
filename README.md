# SSD1680 墨水屏驱动

## 使用

**`EPD` 继承自 `framebuf.Framebuffer` （或 `adafruit_framebuf.Framebuffer`）**

**所以，可以直接调用`EPD`绘制，无需额外的 `Framebuffer` （如`EPD.rect` `EPD.text` 等）**

示例代码见 `test.py`

## 旋转屏幕

*一般来说，`framebuf.Framebuffer` （`micropython` 内置）就足以处理显示内容 （`buffer`）*

**如果使用`framebuf.Framebuffer`，请将`epd.py`中的第19行取消注释，并注释 20~21 行**

---

*但是，如果你需要**旋转屏幕**，那就可以使用 `adafruit_framebuf.Framebuffer`*

**如果使用`adafruit_framebuf.Framebuffer`，请将`epd.py`中的第 20~21 行取消注释，并注释 19 行**

在使用 `adafruit_framebuf.Framebuffer` 时，可以通过 `EPD.rotation` 来修改方向 (值为0-3之内的整数)，如：

```python
...
epd = EPD(w, h, spi, cs, dc, rst, busy)
epd.rotation = 0
# epd.rotation = 1
# epd.rotation = 2
# epd.rotation = 3
...
```

## 局部刷新问题

**局部刷新出现问题，一般来说是`LUT`表导致的**

可通过修改`LUT`表来解决问题，可参考[文章](https://blog.csdn.net/weixin_53556090/article/details/146292375)