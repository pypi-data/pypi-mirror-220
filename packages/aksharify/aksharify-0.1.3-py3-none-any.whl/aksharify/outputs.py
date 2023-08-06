LINK = "https://primepatel.github.io/aksharify/"
SVG_HEADER = '<?xml version="1.0" standalone="no"?><svg width="{}" height="{}" version="1.1" xmlns="http://www.w3.org/2000/svg" style="font-family: {}; font-size:{};"><desc>Aksharify Art</desc><rect width="100%" height="100%" fill="{}"/>'
HTML_HEADER = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Aksharify Art</title></head><body><a href="https://primepatel.github.io/aksharify/" style="text-decoration: none">{}</a></body></html>'


class HTML:
    
    def __init__(self):
        self.title = "Aksharify Art"
        self.link = LINK # not added yet
        self.font_family = "monospace"
        self.font_size = 10
        self.bold = False
        self.file_name = "aksharify"

    def bspan(self, char:str, char_colour:tuple) -> str:
        return f"<span style='color: rgb{char_colour};'><b>{char}</b></span>"
    
    def span(self, char:str, char_colour:tuple) -> str:
        return f"<span style='color: rgb{char_colour};'>{char}</span>"

    def generate_art(self, matrix, image) -> None:
        html_content = f'<p style="font-size: {self.font_size}px; font-family: {self.font_family};">'
        w, h = image.shape[1], image.shape[0] 
        if self.bold == True:
            span = self.bspan
        else:
            span = self.span
        for line_no in range(h):
            for char_no in range(w):
                rgba = image[line_no, char_no]
                r, g, b = rgba[0]*255, rgba[1]*255, rgba[2]*255
                html_content += span(
                    f"&#{ord(matrix[line_no][char_no])};", (r,g,b)
                    )
            html_content += '<br>'
        html_content += "</p>"
        return HTML_HEADER.format(html_content)


class SVG:
    
    def __init__(self):
        self.font_family = "monospace"
        self.font_size = 10
        self.background_color = "#ffffff"
        self.link = LINK # not added yet
        self.bold = False
        self.fill_color = None
        self.file_name = "aksharify"
        self.background_color = "None"
    
    def generate_art(self, matrix, image) -> None:
        H_dis = round((self.font_size*555)/1000, 2)
        V_dis = self.font_size
        w, h = image.shape[1], image.shape[0] 
        width = int(w*H_dis)+41
        height = int(h*V_dis)+41
        file = SVG_HEADER.format(width, height, self.font_family, self.font_size, self.background_color)
        # file += f'<a href="https://primepatel.github.io/aksharify/">'
        file += '<style>text{'
        if self.bold:
            file += 'font-weight: bold;'
        if self.fill_color:
            file += 'fill:' + self.fill_color + ';'
        file += '}</style>'
        if self.fill_color:
            char_func = lambda x, char: f'<tspan x="{x}">{char}</tspan>'
            x, y = 20, 30
            for line_no in range(h):
                file += f'<text x="{x}" y="{y}">'
                for char_no in range(w):
                    file += char_func(x, f"&#{ord(matrix[line_no][char_no])};")
                    x += H_dis
                file += '</text>'
                x = 20
                y += V_dis
            # file += "</a>"
            file += "</svg>"
        else:
            rgb2hex = lambda rgba: '#{:02x}{:02x}{:02x}'.format(int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255))
            char_func = lambda x, char, char_color: f'<tspan x="{x}" fill="{char_color}">{char}</tspan>'
            x, y = 20, 30
            for line_no in range(h):
                file += f'<text x="{x}" y="{y}">'
                for char_no in range(w):
                    file += char_func(x, f"&#{ord(matrix[line_no][char_no])};", rgb2hex(image[line_no, char_no]))
                    x += H_dis
                file += '</text>'
                x = 20
                y += V_dis
            # file += "</a>"
            file += "</svg>"
        return file


class PNG(SVG):
    def __init__(self) -> None:
        super().__init__()
        self.width = None
        self.height = None
        
    def generate_svg(self, matrix, image) -> None:
        return self.generate_art(matrix, image)


class PDF(SVG):
    def __init__(self) -> None:
        super().__init__()
        
    def generate_svg(self, matrix, image) -> None:
        return self.generate_art(matrix, image)
    

class EPS(SVG):
    def __init__(self) -> None:
        super().__init__()
        
    def generate_svg(self, matrix, image) -> None:
        return self.generate_art(matrix, image)