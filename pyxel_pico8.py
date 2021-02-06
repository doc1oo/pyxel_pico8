import copy
import math
import random
import dataclasses
import typing
#
import pyxel
# 
_print = print
_map = map

# ----
SCREEN_W = 128
SCREEN_H = 128
PICO8_CART_HEADER_GRAPHICS = "__gfx__"
PICO8_CART_HEADER_LABEL = "__label__"
PICO8_CART_HEADER_TILE_FLAG = "__gff__"
PICO8_CART_HEADER_MAP = "__map__"
PICO8_CART_HEADER_SFX = "__sfx__"
PICO8_CART_HEADER_MUSIC = "__music__"
PICO8_CART_ALL_HEADERS = [PICO8_CART_HEADER_GRAPHICS, PICO8_CART_HEADER_LABEL, PICO8_CART_HEADER_TILE_FLAG, PICO8_CART_HEADER_MAP, PICO8_CART_HEADER_SFX, PICO8_CART_HEADER_MUSIC]

BTN_KEY_MAP = [pyxel.KEY_LEFT,  pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_Z, pyxel.KEY_X, pyxel.KEY_C, pyxel.KEY_ENTER]
BTN_PADKEY_MAP = [pyxel.GAMEPAD_1_LEFT,  pyxel.GAMEPAD_1_RIGHT, pyxel.GAMEPAD_1_UP, pyxel.GAMEPAD_1_DOWN, pyxel.GAMEPAD_1_B, pyxel.GAMEPAD_1_A, pyxel.GAMEPAD_1_X, pyxel.GAMEPAD_1_Y]
PALETTE_LIST = [0x000000, 0x1D2B53, 0x7E2553, 0x008751, 0xAB5236, 0x5F574F, 0xC2C3C7, 0xFFF1E8, 0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436, 0x29ADFF, 0x83769C, 0xFF77A8, 0xFFCCAA]
PALETTE_LIST_BLEND = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    0, 1, 1, 1, 2, 5, 13, 13, 13, 2,  3,  3, 13,  1, 13,  2,
    5, 1, 2, 1, 2, 5, 13, 4, 14, 4,  4,  4, 13, 13, 14,  4,
    5, 1, 1, 3, 5, 5, 13, 6, 10, 10, 11,  3,  3, 13, 10,  6,
    5, 2, 2, 5, 4, 5, 13, 15, 14, 4,  4, 10, 14,  2,  4,  4,
    0, 5, 5, 5, 5, 5, 13, 6, 4, 4,  4,  6,  6,  5,  4,  6,
    5, 13, 13, 13, 13, 13, 6, 6, 13, 14,  6,  3,  6, 13,  6,  6,
    5, 13, 4, 6, 15, 6, 6, 7, 14, 15, 15, 15,  7,  6, 15,  7,
    2, 13, 14, 10, 14, 4, 13, 14, 8, 8,  9, 10, 14, 14, 14, 14,
    5, 2, 4, 10, 4, 4, 14, 15, 8, 9, 10, 10, 11, 14, 14, 15,
    5, 3, 4, 11, 4, 4, 6, 15, 9, 10, 10, 10, 11, 14, 15, 15,
    5, 3, 4, 3, 10, 6, 3, 15, 10, 10, 10, 11, 12, 13, 10, 10,
    13, 13, 13, 3, 14, 6, 6, 7, 14, 11, 11, 12, 12, 13, 13, 11,
    5, 1, 13, 13, 2, 5, 13, 6, 14, 14, 14, 13, 13, 13, 13,  6,
    5, 13, 14, 10, 4, 4, 6, 15, 14, 14, 15, 10, 13, 13, 14, 15,
    5, 2, 4, 6, 4, 6, 6, 7, 14, 15, 15, 10, 11, 6, 15, 15
]

CHAR_DICT = {
    "▮": 16, "■": 17, "□": 18, "⁙": 19, "⁘": 20, "‖": 21, "◀": 22, "▶": 23, "「": 24, "」": 25, "¥": 26, "•": 27, "、": 28, "。": 29, "゛": 30, "゜": 31,
    " ": 32, "!": 33, '"': 34, "#": 35, "$": 36, "%": 37, "&": 38, "'": 39, "(": 40, ")": 41, "*": 42, "+": 43, ",": 44, "-": 45, ".": 46, "/": 47,
    "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57, ":": 58, ";": 59, "<": 60, "=": 61, ">": 62, "?": 63,
    "@": 64, "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74, "K": 75, "L": 76, "M": 77, "N": 78, "O": 79,
    "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84, "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "[": 91, "\\": 92, "]": 93, "^": 94, "_": 95,
    "`": 96, "a": 97, "b": 98, "c": 99, "d": 100, "e": 101, "f": 102, "g": 103, "h": 104, "i": 105, "j": 106, "k": 107, "l": 108, "m": 109, "n": 110, "o": 111,
    "p": 112, "q": 113, "r": 114, "s": 115, "t": 116, "u": 117, "v": 118, "w": 119, "x": 120, "y": 121, "z": 122, "{": 123, "|": 124, "}": 125, "~": 126, "○": 127,
    "█": 128, "▒": 129, "🐱": 130, "⬇": 131, "░": 132, "✽": 133, "●": 134, "♥": 135, "☉": 136, "웃": 137, "⌂": 138, "⬅": 139, "😐": 140, "♪": 141, "🅾": 142, "◆": 143,
    "…": 144, "➡️": 145, "★": 146, "⧗": 147, "⬆": 148, "ˇ": 149, "∧": 150, "❎": 151, "▤": 152, "▥": 153, "あ": 154, "い": 155, "う": 156, "え": 157, "お": 158, "か": 159,
    "き": 160, "く": 161, "け": 162, "こ": 163, "さ": 164, "し": 165, "す": 166, "せ": 167, "そ": 168, "た": 169, "ち": 170, "つ": 171, "て": 172, "と": 173, "な": 174, "に": 175,
    "ぬ": 176, "ね": 177, "の": 178, "は": 179, "ひ": 180, "ふ": 181, "へ": 182, "ほ": 183, "ま": 184, "み": 185, "む": 186, "め": 187, "も": 188, "や": 189, "ゆ": 190, "よ": 191,
    "ら": 192, "り": 193, "る": 194, "れ": 195, "ろ": 196, "わ": 197, "を": 198, "ん": 199, "っ": 200, "ゃ": 201, "ゅ": 202, "ょ": 203, "ア": 204, "イ": 205, "ウ": 206, "エ": 207,
    "オ": 208, "カ": 209, "キ": 210, "ク": 211, "ケ": 212, "コ": 213, "サ": 214, "シ": 215, "ス": 216, "セ": 217, "ソ": 218, "タ": 219, "チ": 220, "ツ": 221, "テ": 222, "ト": 223,
    "ナ": 224, "ニ": 225, "ヌ": 226, "ネ": 227, "ノ": 228, "ハ": 229, "ヒ": 230, "フ": 231, "ヘ": 232, "ホ": 233, "マ": 234, "ミ": 235, "ム": 236, "メ": 237, "モ": 238, "ヤ": 239,
    "ユ": 240, "ヨ": 241, "ラ": 242, "リ": 243, "ル": 244, "レ": 245, "ロ": 246, "ワ": 247, "ヲ": 248, "ン": 249, "ッ": 250, "ャ": 251, "ュ": 252, "ョ": 253, "◜": 254, "◝": 255
}

EX_CHAR_DICT = {
    "ぁ": 256, "ぃ": 257, "ぅ": 258, "ぇ": 259, "ぉ": 260, "ァ": 261, "ィ": 262, "ゥ": 263, "ェ": 264, "ォ": 265,
    "！": 272, "？": 273, "…": 274, "ー": 275, "　": 276
}

HIRAGANA_LIST = [
    "あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ", "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と",
    "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ", "ま", "み", "む", "め", "も", "や", "ゆ", "よ", "ら", "り",
    "る", "れ", "ろ", "わ", "を", "ん", "っ", "ゃ", "ゅ", "ょ", "…", "、", "。", "゛", "゜", "！", '"', "ー", "？",
    "ァ", "ィ", "ゥ", "ェ", "ォ"
]

JP_LETTER_SPLIT_DICT = {
    "が": "か゛", "ぎ": "き゛", "ぐ": "く゛", "げ": "け゛", "ご": "こ゛",
    "ざ": "さ゛", "じ": "し゛", "ず": "す゛", "ぜ": "せ゛", "ぞ": "そ゛",
    "だ": "た゛", "ぢ": "ち゛", "づ": "つ゛", "で": "て゛", "ど": "と゛",
    "ば": "は゛", "び": "ひ゛", "ぶ": "ふ゛", "べ": "へ゛", "ぼ": "ほ゛",
    "ぱ": "は゜", "ぴ": "ひ゜", "ぷ": "ふ゜", "ぺ": "へ゜", "ぽ": "ほ゜",
    "ゔ": "う゛",

    "ガ": "カ゛", "ギ": "キ゛", "グ": "ク゛", "ゲ": "ケ゛", "ゴ": "コ゛",
    "ザ": "サ゛", "ジ": "シ゛", "ズ": "ス゛", "ゼ": "セ゛", "ゾ": "ソ゛",
    "ダ": "タ゛", "ヂ": "チ゛", "ヅ": "ツ゛", "デ": "テ゛", "ド": "ト゛",
    "バ": "ハ゛", "ビ": "ヒ゛", "ブ": "フ゛", "ベ": "ヘ゛", "ボ": "ホ゛",
    "パ": "ハ゜", "ピ": "ヒ゜", "プ": "フ゜", "ペ": "ヘ゜", "ポ": "ホ゜",
    "ヴ": "ウ゛",
}


@dataclasses.dataclass
class Pico8State:
    camera_x: float = 0
    camera_y: float = 0
    fillp: int = 0
    pal_list: typing.List[int] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.pal_list = [i for i in range(16)]


p8st = Pico8State()


class Util:

    def __init__(self):
        pass

    def load(self):
        self.load_chipflag()
        self.load_map()
        self.load_music()
        self.load_sfx()
        self.load_spreadsheet()

    def import_p8cart(self, file_path):
        print("dw2_sfx")
        self.p8cart_file_path = file_path

        try:
            with open(file_path, encoding="utf-8") as f:
                self.p8cart_text = f.read()
        except:
            _print("can't not read pico8 cartridge: %s", file_path)
            return False

        self.p8cart_text_graphics = self._get_p8cart_asset_text(PICO8_CART_HEADER_GRAPHICS)
        self.p8cart_text_label = self._get_p8cart_asset_text(PICO8_CART_HEADER_LABEL)
        self.p8cart_text_tile_flag = self._get_p8cart_asset_text(PICO8_CART_HEADER_TILE_FLAG)
        self.p8cart_text_map = self._get_p8cart_asset_text(PICO8_CART_HEADER_MAP)
        self.p8cart_text_sfx = self._get_p8cart_asset_text(PICO8_CART_HEADER_SFX)
        self.p8cart_text_music = self._get_p8cart_asset_text(PICO8_CART_HEADER_MUSIC)

    def _get_p8cart_asset_text(self, search_header):
        data_list = []

        header_found = False
        for line in self.p8cart_text.splitlines():
            if line == search_header:
                header_found = True
                continue

            if header_found is True:
                if line == "" or line in PICO8_CART_ALL_HEADERS:
                    break
                else:
                    data_list.append(line)
        rtn_str = "\n".join(data_list)
        #_print("_get_p8cart_asset_text()", search_header)
        #_print(rtn_str)
        return rtn_str

    def load_spreadsheet(self):
        pyxel.image(0).load(0, 0, "assets/dw2_.png")
        pyxel.image(1).load(0, 0, "assets/pico8_1oo_font.PNG")

    def load_sfx(self):
        sfx_info_dict_list = []
        key_dict1 = ["c", "d", "d", "d", "e",
                     "f", "f", "g", "g", "a", "a", "b"]
        key_dict2 = ["", "-", "", "#", "", "", "#", "", "#", "", "#", ""]
        tone_dict = ["S", "T", "P", "P", "P", "S", "N", "S",
                     "P", "P", "P", "P", "P", "P", "P", "P", "P"]
        fx_dict = ["N", "S", "V", "V", "N", "F", "V", "V"]
        alignment = 8

        i = 0
        for line in self.p8cart_text_sfx.split("\n"):

            sfx_speed = int(line[2:4], 16)
            sfx_start = int(line[4:6], 16)
            sfx_end = int(line[6:8], 16)

            str_sfx_note_key = ""
            str_sfx_note_waveform = ""
            str_sfx_note_vol = ""
            str_sfx_note_fx = ""

            sfx_info_dict_list.append({"speed": sfx_speed, "loop_start": sfx_start, "loop_end": sfx_end})

            for j in range(32):

                if sfx_end == 0:
                    idx = j*5 + alignment
                else:
                    idx = (j % sfx_end)*5 + alignment

                key_val = int(line[idx: idx+2], 16)
                volume = int(line[idx+3], 16)
                if volume == 0 and key_val <= 0:
                    str_sfx_note_key += "R"
                elif math.floor(key_val/12) <= 4:
                    str_sfx_note_key += key_dict1[key_val % 12] + \
                        key_dict2[key_val % 12] + str(math.floor(key_val/12))
                else:
                    str_sfx_note_key += "R"
                waveform = tone_dict[int(line[idx+2], 16)]
                str_sfx_note_waveform += waveform
                vol = int(line[idx+3])
                volume = str(max(vol - 1 if waveform=="S" else vol, 0))
                str_sfx_note_vol += volume
                str_sfx_note_fx += fx_dict[int(line[idx+4], 16)]

            pyxel.sound(i).set(str_sfx_note_key, str_sfx_note_waveform,
                               str_sfx_note_vol, str_sfx_note_fx, sfx_speed)
            i += 1

        # _print(sfx_info_dict_list)
        return sfx_info_dict_list

    def load_music(self, start_track=0):
        ptn_speed = 120
        m_ch0 = []
        m_ch1 = []
        m_ch2 = []
        m_ch3 = []
        k = start_track
        begin_loop_flag = []
        end_loop_flag = []
        stop_at_end_flag = []
        begin_loop_bar = None
        end_loop_bar = None
        stop_at_end_bar = None
        t = 0
        # 64 line to 64 music
        music_lines = self.p8cart_text_music.split("\n")
        while True:
            line = music_lines[k]

            ptn_setting = int(line[0:2], 16)
            begin_loop = ptn_setting & 1
            end_loop = ptn_setting & 2
            stop_at_end = ptn_setting & 4
            # _print("music_setting",music_setting)

            i = 3
            val0 = int(line[i:i+2], 16)
            val1 = int(line[i+2:i+4], 16)
            val2 = int(line[i+4:i+6], 16)
            val3 = int(line[i+6:i+8], 16)

            # 3 is silent sfx
            m_ch0.append(val0 if val0 < 64 else 3)
            m_ch1.append(val1 if val1 < 64 else 3)
            m_ch2.append(val2 if val2 < 64 else 3)
            m_ch3.append(val3 if val3 < 64 else 3)

            begin_loop_flag.append(k if begin_loop != 0 else None)
            end_loop_flag.append(k if end_loop != 0 else None)
            stop_at_end_flag.append(k if stop_at_end != 0 else None)

            if begin_loop != 0:
                begin_loop_bar = t
            if end_loop != 0:
                end_loop_bar = t
            if stop_at_end != 0:
                stop_at_end_bar = t
            if end_loop != 0 or stop_at_end != 0:
                break

            t += 1
            k += 1

        music_dict = {
            "start_track": start_track,
            "begin_loop_flag": begin_loop_flag,
            "end_loop_flag": end_loop_flag,
            "stop_at_end_flag": stop_at_end_flag,
            "begin_loop_bar": begin_loop_bar,
            "end_loop_bar": end_loop_bar,
            "stop_at_end_bar": stop_at_end_bar,

            "sound_id_list": [m_ch0, m_ch1, m_ch2, m_ch3],
            "bar_length": t+1
        }
        return music_dict

    def load_map(self):
        global mapdata_list_master
        map_val_list = []
        for line in self.p8cart_text_map.split("\n"):
            map_val_list.append([])
            for i in range(128):
                __builtins__.print(line[i*2:i*2+2])
                val = int(line[i*2: i*2+2], 16)
                val = val % 16 + math.floor(val/16)*32
                map_val_list[len(map_val_list)-1].append(val)
        mapdata_list_master = copy.deepcopy(map_val_list)

        self._mapval_to_tilemap(0, mapdata_list_master)
        self._mapval_to_tilemap(1, mapdata_list_master)
        self._mapval_to_tilemap(2, mapdata_list_master)
        self._mapval_to_tilemap(7, mapdata_list_master)

    def _mapval_to_tilemap(self, tmid, mapval_list):
        i = 0
        for line in mapval_list:
            j = 0
            for v in line:
                pyxel.tilemap(tmid).set(j, i, v)
                j += 1
            i += 1

    def load_chipflag(self):
        global chipflag_list, chipflag_list_master
        chipflag_list = []

        i = 0
        for line in self.p8cart_text_tile_flag.split("\n"):
            for j in range(128):
                idx = j*2
                val = int(line[idx: idx+2], 16)
                chipflag_list.append(val)
            i += 1
        chipflag_list_master = copy.deepcopy(chipflag_list)


    # pico8 0.2.x utility functions ==================

    def btnr(n):
        return pyxel.btnr(BTN_KEY_MAP[n]) or pyxel.btnr(BTN_PADKEY_MAP[n])

    def bool(v):
        if v is None or v is False:
            return False
        return True

    # for spr()

    def sprid2xy(spr_id):
        return (spr_id % 16)*8, math.floor(spr_id/16)*8

    def b2i(v):
        return 1 if v else 0

    def b2dir(v):
        return -1 if v else 1

    def b2n(bl, true_num=1, false_num=0):
        return true_num if bl else false_num

    def cyclic(n, mod):
        return (n + mod) % mod

    def rndi(n, start=0):
        return randint(0, n) + start

    def rndi_pn(num, start=0):
        return rndi(num*2, start - num)

    def dump_readchar(c):
        return ord(c) - 48

    def ex_ord(c):
        if c in EX_CHAR_DICT:
            return EX_CHAR_DICT[c]
        elif c in CHAR_DICT:
            return CHAR_DICT[c]
        return None

    # graphics utility -------------------

    def rectfill2(x0, y0, w, h, col=None):
        if col is None:
            col = 0
        pyxel.rect(x0 + p8st.camera_x, y0 + p8st.camera_y, w, h, col)

    def wspr(sn, x, y, flipx=False, flipy=False):
        spr(sn, x, y, 2, 2, flipx, flipy)

    # --  x, y, dest_sz,dest_sz,flipx, flipy

    def sspr2(sn, sz,  x, y, w, h, flipx=False, flipy=False, img_id=0):
        sx, sy = Util.sprid2xy(sn)
        sz *= 8
        Util.p8blts(x, y, Util.b2dir(flipx)*w, Util.b2dir(flipy)*h, img_id,  sx, sy, sz, sz)

    def p8blts(x, y, dw, dh, img, u, v, w, h, colkey=0):
        pimg_get = pyxel.image(img).get
        sign_x = sign(dw)
        sign_y = sign(dh)
        dw = math.floor(abs(dw))
        dh = math.floor(abs(dh))
        rw = w / dw
        rh = h / dh

        start_sx = 0 if sign_x >= 0 else dw
        start_sy = 0 if sign_y >= 0 else dh

        for i in range(dh):
            dest_y = i + y
            cy = dest_y + p8st.camera_y
            sy = v + int(rh * (sign_y*i + start_sy))
            for j in range(dw):
                dest_x = j + x
                cx = dest_x + p8st.camera_x
                if cx >= 0 and cy >= 0 and cx <= 127 and cy <= 127:
                    pset(dest_x, dest_y, pimg_get(u + int(rw * (sign_x*j + start_sx)), sy), colkey)

    def blts(x, y, dw, dh, img, u, v, w, h, colkey=0):
        pimg = pyxel.image(img)
        sign_x = sign(dw)
        sign_y = sign(dh)
        dw = math.floor(abs(dw))
        dh = math.floor(abs(dh))
        rw = w / dw
        rh = h / dh

        for i in range(dh):
            sy = int(rh*i) + v
            for j in range(dw):
                pset(j*sign_x + x,  i*sign_y + y, pimg.get(int(rw*j) + u, sy), colkey)

    def get_pal(idx):
        return p8st.pal_list[idx]

    def get_pal_list():
        return p8st.pal_list

    def spr_blend(spr_id, x, y, w, h, flip_x=False, flip_y=False):
        sx_base, sy = Util.sprid2xy(spr_id)

        for i in range(8):
            dy = y+i

            for j in range(16):
                dx, src_col = flip_x and x+15-j or x+j, pyxel.image(0).get(sx_base+j, sy)

                if src_col != 0:
                    pset(dx, dy, PALETTE_LIST_BLEND[src_col*16 + pyxel.pget(dx, dy)])
            sy += 1

    def rectfill_blend(x, y, w, h, col=0,  col_key=None):

        for i in range(y, y+h):

            for j in range(x, x+w):

                # if col is not col_key:
                src_col = pyxel.pget(j, i)
                pyxel.pset(j, i, PALETTE_LIST_BLEND[col*16 + src_col])

    def fillp_rectfill(x0, y0, x1, y1, col=None, fill_ptn=0xa0a0):
        fillp_list = []
        ptn = fill_ptn
        for i in range(4):
            ptn = math.floor(fill_ptn >> 4*(3-i))
            fillp_list.append([ptn & 8, ptn & 4, ptn & 2, ptn & 1])

        if col is None:
            col = 0

        for i in range(y0, y1+1):
            for j in range(x0, x1+1):
                fx = j % 4  # math.floor(j/4)
                fy = i % 4  # math.floor(i/4)
                # _print("fillp,",fillp_list[fy][fx])
                if fillp_list[fy][fx] == 0:
                    pset(j, i, col)


    def make_cache_spr_free_aspect(sx, sy, ssw, ssh, img_id=0):
        pimg_get = pyxel.image(img_id).get
        src_px_array = [[0] * ssw for i in range(ssh)]

        for i in range(ssh):
            for j in range(ssw):
                src_px_array[i][j] = pimg_get(j+sx, i+sy)

        return src_px_array

    def fast_sspr_list_free_aspect(ssw, ssh, xysz_list, src_px_array, colkey=0):
        ps = pyxel.pset

        # ------------------
        for sp in xysz_list:
            x, y, dsw, dsh = sp
            
            # out of drawing area
            if dsw == 0 or dsh == 0 or  x>=128 or y>=128:
                continue

            # out of drawing area
            dx = int(x + p8st.camera_x)
            dy = int(y + p8st.camera_y)
            if dx+dsw<0 or dy+dsh<0:
                continue

            # drawing ---------
            rate_x = ssw / dsw
            rate_y = ssh / dsh
            dsw = int(dsw)
            dsh = int(dsh)
            src_indexes_x = [int(rate_x * i) for i in range(dsw)]
            src_indexes_y = [int(rate_y * i) for i in range(dsh)]
            
            py = dy
            for si in src_indexes_y:

                if py&127 == py:     # same if py >= 0 and py <=127:

                    line_pixels = src_px_array[si]
                    px = dx

                    for col in [line_pixels[n] for n in src_indexes_x]:
                        if col!=colkey and px&127 == px:
                            ps(px, py, col)
                        elif px >= 128:
                            break
                        px += 1

                elif py >= 128:
                    break
                py += 1


    def make_cache_spr(spr_id, ssz,  img_id=0):
        sx, sy = Util.sprid2xy(spr_id)
        pimg_get = pyxel.image(img_id).get
        src_px_array = [[0] * ssz for i in range(ssz)]

        for i in range(ssz):
            for j in range(ssz):
                src_px_array[i][j] = pimg_get(j+sx, i+sy)

        return src_px_array

    def fast_sspr_list(spr_id, ssz, xysz_list, src_px_array):
        ps = pyxel.pset

        # ------------------
        for sp in xysz_list:
            x, y, dsz = sp
            
            # out of drawing area
            if dsz == 0 or x>=128 or y>=128:
                continue

            # out of drawing area
            dx = int(x + p8st.camera_x)
            dy = int(y + p8st.camera_y)
            if dx+dsz<0 or dy+dsz<0:
                continue

            # drawing ---------
            rate = ssz / dsz
            dsz = int(dsz)
            src_indexes = [int(rate * i) for i in range(dsz)]
            
            py = dy
            for si in src_indexes:

                if py&127 == py:     # same if py >= 0 and py <=127:

                    line_pixels = src_px_array[si]
                    px = dx

                    for col in [line_pixels[n] for n in src_indexes]:
                        if col and px&127 == px:
                            ps(px, py, col)
                        elif px >= 128:
                            break
                        px += 1

                elif py >= 128:
                    break
                py += 1




# Pico8 0.2.x Compatible functions ==========================================

# math ---------------------------------------------

def rnd(n):
    return random.random()*n


def sign(n):
    if n > 0:
        return 1
    elif n == 0:
        return 0
    return -1


def min(n, m):
    if n in [None, False]:
        n = 0
    if m in [None, False]:
        m = 0
    return n if n <= m else m


def mid(minim, n, maxim):
    n = float(n)

    return max(min(n, maxim), minim)


def max(n, m):
    if n in [None, False]:
        n = 0
    if m in [None, False]:
        m = 0
    return n if n >= m else m


def sin(n):
    return - math.sin(n*2*math.pi)


def cos(n):
    return math.cos(n*2*math.pi)


def ord(c):
    if c in CHAR_DICT:
        return CHAR_DICT[c]


# input ---------------------


def btn(n):
    return pyxel.btn(BTN_KEY_MAP[n]) or pyxel.btn(BTN_PADKEY_MAP[n])


def btnp(n, hold=0, period=0):
    return pyxel.btnp(BTN_KEY_MAP[n], hold, period) or  pyxel.btnp(BTN_PADKEY_MAP[n], hold, period)


# map ---------------------------------------

def mget(x, y, tm_id=7):
    if x >= 0 and x <= 127 and y >= 0 and y <= 127:
        tid = pyxel.tilemap(tm_id).get(x, y)
        return math.floor(tid/32)*16 + tid % 16
    return 0


def mset(x, y, val, tm_id=7):
    pyxel.tilemap(tm_id).set(x, y, math.floor(val/16)*32+val % 16)


def fget(tid, bit=None):
    if bit is None:
        return chipflag_list[tid]
    else:
        bitn = 1 << bit
        return (chipflag_list[tid] & bitn) == bitn


# Graphics ---------------------------------

def pal(a=None, b=None):
    if a is None:
        pyxel.pal()
        p8st.pal_list = [i for i in range(16)]
    elif type(a) is list:
        i = 0
        for col in a:
            pyxel.pal(i, int(col))
            p8st.pal_list[i] = int(col)
            i += 1
    else:
        pyxel.pal(a, b)
        p8st.pal_list[a] = b

def palt( a, b):
    pass


def camera(x=None, y=None):
    global p8st
    if x is not None:
        #p8st.cam_float_x, p8st.cam_float_y = -x,-y
        p8st.camera_x, p8st.camera_y = -math.ceil(x), -math.ceil(y)
    else:
        p8st.camera_x, p8st.camera_y = 0, 0

#str, [x,] [y,] [col]


def print(s, x=None, y=None, col=0, colkey=2, font=0, tm_id=1, line_h=8):
    x = x if x is not None else 0
    y = y if y is not None else 0
    px, py = x, y
    fw, fh = 8, 8

    pyxel.pal(7, col)
    for char in s:
        c = None
        if char in EX_CHAR_DICT:
            c = EX_CHAR_DICT[char]
        elif char in CHAR_DICT:
            c = CHAR_DICT[char]
        elif char == "\n":
            px, py = 0, py + line_h

        if c is not None:
            if c >= 0x9a:
                font_dw = 7 if font == 1 else 6
            else:
                font_dw = 4 if c < 0x80 else 8

            sx, sy = Util.sprid2xy(c)
            #_print(str(c) + " " + str(sx) + " " + str(sy))
            pyxel.blt(px + p8st.camera_x, py + p8st.camera_y, tm_id, sx + font*128, sy, fw, fh, colkey)
            px += font_dw
    pyxel.pal()
    return px


def spr(spr, x, y, w=1, h=1, flipx=False, flipy=False):
    sx, sy = Util.sprid2xy(spr)
    pyxel.blt(x + p8st.camera_x, y + p8st.camera_y, 0, sx, sy, Util.b2dir(flipx)*w*8, Util.b2dir(flipy)*h*8, 0)


def sspr(sx, sy, sw, sh,  x, y, dw=None, dh=None, flipx=False, flipy=False,  colkey=-1, tm_id=0):
    sw = Util.b2dir(flipx)*w
    sh = Util.b2dir(flipy)*h
    if dw is not None and dh is not None:
        pyxel.blt(x + p8st.camera_x, y + p8st.camera_y, tm_id, sx, sy, sw, sh, colkey=colkey)
    else:
        Util.blts(x, y, dw, dh, tm_id, sx, sy, sw, sh, colkey=colkey)


def map(celx, cely, x, y, celw, celh, layer=None, tm_id=0, colkey=-1):
    pyxel.bltm(x + p8st.camera_x, y + p8st.camera_y, tm_id, celx, cely, celw, celh, colkey=colkey)
    #pyxel.blt(x + p8st.camera_x, y + p8st.camera_y, 0, celx*8, cely*8, celw*8, celh*8, colkey=colkey)


def circfill(x, y, r=4, col=0):
    pyxel.circ(x + p8st.camera_x, y + p8st.camera_y, r, col)


def clip(x=None, y=None, w=None, h=None):
    if x is None:
        pyxel.clip()
    else:
        pyxel.clip(x, y, w, h)


def rectfill(x0, y0, x1, y1, col=None):
    if col is None:
        col = 0
    pyxel.rect(x0 + p8st.camera_x, y0 + p8st.camera_y, x1-x0+1, y1-y0+1, col)


def fillp(a=None, b=None):
    if a is None:
        pass
    pass


def pset(x, y, col, colkey=0):
    if col != colkey:
        pyxel.pset(x + p8st.camera_x, y + p8st.camera_y, col)
