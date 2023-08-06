path_image = ''
path_templ = ''

n_items: int = 6
n_types: int = 0
n_types_max: int = 4
n_items_recognition: int = 0

white_part_param: float = 0.65

cell_size: int = 200
calc_size: int = 100
cell_width: int = cell_size
cell_height: int = cell_size

caption_height: int = 45
x_caption_pos: int = cell_width // 2 - 8
y_caption_pos: int = 33
space: int = 9

show_caption: bool = True
color_background: int = 224
color_border: int = 64
color_caption_enable = (0, 38, 255)
color_caption_disable = (224, 224, 224)
font_scale = 1.0

size_dft: int = 2048
lp_param: int = 4
size_roi: int = size_dft // lp_param
size_roi_half: int = size_roi // 2
X0: int = size_roi_half
Y0: int = size_roi_half

n_peaks: int = 13
angle_min: float = 20
angle_max: float = 120
angle_ratio_threshold: float = 2.5

time_self_study = ''
time_recognition = ''

dir_self_study = 'DATA_SELF_STUDY'
dir_recognition = 'DATA_RECOGNITION'
dir_results = 'RESULTS'
