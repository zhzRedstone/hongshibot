import io

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import require
from nonebot.params import State, CommandArg
from PIL import Image

#按照XZhouQD/nonebot-plugin-help要求的帮助及用法
# 若此文本不存在，将显示包的__doc__
__help_plugin_name__ = "render" 
__des__ = 'nonebot_plugin_htmlrender的示例插件，支持代码高亮，LaTeX'
__cmd__ = '''
Markdown转图片：
md2pic
<md文本>
纯文本转图片：text2pic <文本>
'''.strip()
# __short_cmd__ = 'md2pic,text2pic'
__example__ = '''
md2pic
# 随机一图
![随机一图](https://iw233.cn/api/Random.php)
-----
text2pic 文本传图片
'''.strip()

__usage__ = f'{__des__}\nUsage:\n{__cmd__}\n\nExample:\n{__example__}'

# 纯文本转图片
text2pic = on_command("text2pic")
text_to_pic = require("nonebot_plugin_htmlrender").text_to_pic


@text2pic.handle()
async def _text2pic(bot: Bot, event: MessageEvent, arg: Message=CommandArg()):
    arg=arg.extract_plain_text()
    msg = str(arg)

    # css_path 可选
    # from pathlib import Path
    # pic = await text_to_pic(
    #     text=msg, css_path=str(Path(__file__).parent / "templates" / "markdown.css")
    # )

    pic = await text_to_pic(text=msg)
    a = Image.open(io.BytesIO(pic))
    a.save("text2pic.png", format="PNG")
    await text2pic.finish(MessageSegment.image(pic))


# 加载本地 html 方法
html2pic = on_command("html2pic")
new_page = require("nonebot_plugin_htmlrender").get_new_page


@html2pic.handle()
async def _html2pic(bot: Bot, event: MessageEvent):
    from pathlib import Path

    # html 可使用本地资源
    async with new_page(viewport={"width": 300, "height": 300}) as page:
        await page.goto(
            "file://" + (str(Path(__file__).parent / "html2pic.html")),
            wait_until="networkidle",
        )
        pic = await page.screenshot(full_page=True, path="./html2pic.png")

    await html2pic.finish(MessageSegment.image(pic))


# 使用 template2pic 加载模板
template2pic = on_command("template2pic")
template_to_pic = require("nonebot_plugin_htmlrender").template_to_pic


@template2pic.handle()
async def _template2pic(bot: Bot, event: MessageEvent):
    from pathlib import Path

    text_list = ["1", "2", "3", "4"]
    template_path = str(Path(__file__).parent / "templates")
    template_name = "text.html"
    # 设置模板
    # 模板中本地资源地址需要相对于 base_url 或使用绝对路径
    pic = await template_to_pic(
        template_path=template_path,
        template_name=template_name,
        templates={"text_list": text_list},
        pages={
            "viewport": {"width": 600, "height": 300},
            "base_url": f"file://{template_path}",
        },
        wait=2,
    )

    a = Image.open(io.BytesIO(pic))
    a.save("template2pic.png", format="PNG")

    await template2pic.finish(MessageSegment.image(pic))


# 使用 md2pic
md2pic = on_command("md2pic")
md_to_pic = require("nonebot_plugin_htmlrender").md_to_pic


@md2pic.handle()
async def _md2pic(bot: Bot, event: MessageEvent, arg: Message=CommandArg()):
    from pathlib import Path

    # 如果是直接获取消息内容 需要 unescape
    from nonebot.adapters.cqhttp import unescape
    arg = arg.extract_plain_text()
    msg = unescape(str(arg))

    # css_path 可选
    # pic = await md_to_pic(
    #     md=msg, css_path=str(Path(__file__).parent / "templates" / "markdown.css")
    # )

    pic = await md_to_pic(md=msg)

    a = Image.open(io.BytesIO(pic))
    a.save("md2pic.png", format="PNG")

    await md2pic.finish(MessageSegment.image(pic))