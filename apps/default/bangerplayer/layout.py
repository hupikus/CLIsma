from type.colors import Colors

min_canvas_width = 3

def arrange_layout(self, toggle_files, height, width):
    if self.toggle_files:
        pos = min(round(width *  0.3), min_canvas_width)

        self.file_list.width = pos
        self.main_canvas.x = pos

        self.main_canvas.width = width - pos
    else:
        self.file_list.width = 0
        self.main_canvas.x = 0

        self.main_canvas.width = width

    self.file_list.height = height
    self.main_canvas.height = height
