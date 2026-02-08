# SSD1680 墨水屏驱动

## 使用之前

如果你的屏幕分辨率是 `104x212` ，则可以跳过这一步

**你必须先修改 `epd.py` 的第121行和第126~127行**

**第121行**:

```python
# 将 0C 改为 屏幕宽/8-1 的16进制
self._data(b'\x0C')
```

如，屏幕宽为128，则改为 

```python
# 128/8-1=15，15的16进制为F
self._data(b'\x0F')
```

**第126~127行**：

```python
# 将 00 DB 改为 屏幕高+7 的十六进制
# 这里要注意，如果值超过两位，则后两位写在第一行，前两位写在第二行
# 如，十六进制12FF要写成:
# self._data(b'\xFF')
# self._data(b'\x12')
self._data(b'\xDB')
self._data(b'\x00')
```

如，屏幕高为512，则改为

```python
# 512+7=519，519的16进制为207
self._data(b'\x07')
self._data(b'\x02')
```

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