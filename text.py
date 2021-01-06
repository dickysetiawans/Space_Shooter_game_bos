'''Text'''
def text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	tampilan.blit(img, (x, y))

def draw_text():
	level_label = text50.render("Level: 5", 1, (putih))
	tampilan.blit(level_label, (panjang - level_label.get_width() - 10, 10))
def text_bos():
	bos_label = text30.render("Bos Enemy", 1, (putih))
	tampilan.blit(bos_label, (10, 10))