import IPython.display as ipd
from io import BytesIO
from cairosvg import svg2png, svg2pdf, svg2eps
from .outputs import SVG

class AksharArt:
    
    def __init__(self, image, dist) -> None:
        self.image = image
        self.dist = dist
    
    def set_dim(self, width:int=None, height:int=None):
        self.image.set_dim(width, height)
        
    def aksharify(self, show=False) -> None:
        self.matrix = []
        
        for x in range(self.image.bwimg.shape[0]):
            line = []
            for y in range(self.image.bwimg.shape[1]):
                line.append(self.dist.char_dict[int(self.image.bwimg[x, y]*255)])
            self.matrix.append(line)
        
        if show:
            svg = SVG()
            svg.background_color = "#ffffff"
            svg.bold = False
            svg.fill_color = "#000000"
            art = svg.generate_art(self.matrix, self.image.image)
            ipd.display(ipd.SVG(art))
    
    def replace_char(self, char:str, x:int, y:int)-> None:
        if x<self.image.w and y<self.image.h:
            self.matrix[y][x] = char
        else:
            raise IndexError

    def replace_chars(self, chars:str, x:int, y:int) -> None:
        x, y = abs(x), abs(y)
        if x>self.image.w or y>self.image.h:
            raise IndexError
        if self.image.w - x >= len(chars):
            for i in range(x, x + len(chars)):
                self.replace_char(chars[i-x], i, y)
        else:
            self.replace_chars(chars[:self.image.w-x], x, y)
            self.replace_chars(chars[self.image.w-x:], 0, y+1)

    def txt_output(self, fname:str) -> None:
        text = ""
        for line_no in range(self.image.bwimg.shape[0]):
            text += "".join(self.matrix[line_no]) + "\n"
        with open(fname + ".txt", "w") as file:
            file.write(text)

    def svg_output(self, config):
        svg = config
        with open(svg.file_name + ".svg", "w", encoding="utf-8-sig") as file:
            file.write(svg.generate_art(self.matrix, self.image.image))
    
    def png_output(self, config):
        png = config
        svg = png.generate_svg(self.matrix, self.image.image)
        if png.height == None and png.width != None:
            return svg2png(bytestring=svg, write_to=png.file_name+".png", output_width=png.width)
        elif png.width == None and png.height != None:
            return svg2png(bytestring=svg, write_to=png.file_name+".png", output_height=png.height)
        elif png.height == None and png.width == None:
            return svg2png(bytestring=svg, write_to=png.file_name+".png")
        else:
            return svg2png(bytestring=svg, write_to=png.file_name+".png", output_height=png.height, output_width=png.width)

    def pdf_output(self, config):
        pdf = config
        svg = pdf.generate_svg(self.matrix, self.image.image)
        svg_io = BytesIO(svg.encode('utf-8-sig'))
        svg2pdf(file_obj=svg_io, write_to=config.file_name + ".pdf")
    
    def eps_output(self, config):
        eps = config
        svg = eps.generate_svg(self.matrix, self.image.image)
        svg_io = BytesIO(svg.encode('utf-8'))
        svg2eps(file_obj=svg_io, write_to=eps.file_name + ".eps")
    
    def html_output(self, config):
        html = config
        with open(html.file_name + ".html", "w", encoding="utf-8") as file:
            file.write(html.generate_art(self.matrix, self.image.image))

