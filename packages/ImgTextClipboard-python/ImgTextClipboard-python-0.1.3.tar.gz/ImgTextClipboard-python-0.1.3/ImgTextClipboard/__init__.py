import pyperclip
import win32clipboard

from PIL import ImageGrab
from io import BytesIO


def copyTextFormClipboard():
    """
    从剪贴板读取文本
    :return: String
    """
    return pyperclip.paste()


def copyImgFormClipboard():
    """
    从剪贴板读取Image图片
    :return: Image
    """
    return ImageGrab.grabclipboard()


def pasteImgToClipboard(image):
    """
    将一张Image图片写入Windows剪贴板中
    :param image:Image 图片
    :return:
    """

    # 剪贴板操作
    def sendMsgToClip(type_data, msg):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(type_data, msg)
        win32clipboard.CloseClipboard()

    output = BytesIO()
    image.save(output, 'BMP')

    # 去除BMP图片14字节的header
    data = output.getvalue()[14:]

    # DIB: 设备无关位图(device-independent bitmap)
    sendMsgToClip(win32clipboard.CF_DIB, data)

    output.close()


def pasteTextToClipboard(text):
    """
    写入字符串到剪贴板
    :param text:
    :return:
    """
    pyperclip.copy(text)
