
import random
from PIL import Image,ImageDraw,ImageFont,ImageFilter

_letter_cases = 'abcdefghjkmnpqrstuvwxy'
_upper_cases = _letter_cases.upper()
_numbers = ''.join(map(str,range(0,10)))

init_chars = ''.join((_letter_cases,_upper_cases,_numbers),)

def create_validate_code(size=(120,30),chars=init_chars,
                         img_type='GIF',mode='RGB',
                         bg_color = (255,255,255),
                         fg_color = (0,0,255),font_size=18,
                         font_type='Monaco.ttf',length=4,
                         draw_lines=True,n_line=(1,2),
                         draw_points=True,point_chance=2):

    width,heigth = size
    '''创建图形'''
    img = Image.new(mode,size,bg_color)
    '''创建画笔'''
    draw = ImageDraw.Draw(img)

    def get_chars():
        """生成给定长度的字符串，返回列表格式"""
        return random.sample(chars,length)

    def create_lines():
        '''绘制干扰线'''
        line_num = random.randint(*n_line) #干扰线条数

        for i in range(line_num):
            begin = (random.randint(0,size[0]),random.randint(0,size[1]))
            end = (random.randint(0,size[0]),random.randint(0,size[1]))
            draw.line([begin,end],fill=(0,0,0))

    def create_points():
        '''绘制干扰点'''
        chance = min(100,max(0,int(point_chance)))

        for w in range(width):
            for h in range(heigth):
                tmp = random.randint(1,100)
                if tmp > 100 -chance:
                    draw.point((w,h),fill=(0,0,0))


    def create_strs():
        '''绘制验证码字符'''
        c_chars = get_chars()
        '''每个字符前后以空格隔开'''
        strs = ' %s ' % ' '.join(c_chars)
        font = ImageFont.truetype(font_type,font_size)
        font_width,font_height = font.getsize(strs)

        draw.text(((width- font_width)/3,(heigth - font_height)/3),strs,font=font,fill=fg_color)
        return ''.join(c_chars)

    if draw_lines:
        create_lines()

    if draw_points:
        create_points()

    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    return img, strs


