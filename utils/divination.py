import random

# 卦象和爻的映射表
reversed_gua_map = {'乾为天': '111111', '天风姤': '111110', '天山遁': '111100', '天地否': '111000', '风地观': '110000', '山地剥': '100000',
     '火地晋': '101000', '火天大有': '101111',
     '兑为泽': '011011', '泽水困': '011010', '泽地萃': '011000', '泽山咸': '', '水山蹇': '010111', '地山谦': '000100', '雷山小过': '001100',
     '雷泽归妹': '001011',
     '离为火': '101101', '火山旅': '101100', '火风鼎': '101110', '火水未济': '101010', '山水蒙': '100010', '风水涣': '110010',
     '天水讼': '111010', '天火同人': '111101',
     '震为雷': '001001', '雷地豫': '001000', '雷水解': '001010', '雷风恒': '001110', '地风升': '000110', '水风井': '010110',
     '泽风大过': '011110', '泽雷随': '011001',
     '巽为风': '110110', '风天小畜': '110111', '风火家人': '110101', '风雷益': '110001', '天雷无妄': '111001', '火雷噬嗑': '101001',
     '山雷颐': '100001', '山风蛊': '100110',
     '坎为水': '010010', '水泽节': '010011', '水雷屯': '010001', '水火既济': '010101', '泽火革': '011101', '雷火丰': '001101',
     '地火明夷': '000101', '地水师': '000010',
     '艮为山': '100100', '山火贲': '100101', '山天大畜': '100111', '山泽损': '100011', '火泽睽': '101011', '天泽履': '111011',
     '风泽中孚': '110011', '风山渐': '110100',
     '坤为地': '000000', '地雷复': '000001', '地泽临': '000011', '地天泰': '000111', '雷天大壮': '001111', '泽天夬': '011111',
     '水天需': '010111', '水地比': '010000'}
gua_map = {v: k for k, v in reversed_gua_map.items()}

import json
with open("/root/banxian/resource/卦名map.json") as f:
    gua_name_map = json.load(f)

def coin_toss():
    return random.choice([2, 3])

def qigua():
    lines = []
    moving_lines = []

    for _ in range(6):
        coins = coin_toss() + coin_toss() + coin_toss()
        if coins == 6:
            lines.append('0')
            moving_lines.append(len(lines))
        elif coins == 9:
            lines.append('1')
            moving_lines.append(len(lines))
        elif coins % 2 == 0:
            lines.append('0')
        else:
            lines.append('1')

    original_hex = ''.join(lines[::-1])
    changed_hex = ''.join(['1' if x == '0' else '0' if x == '1' else x for x in lines][::-1])

    original_gua = gua_map.get(original_hex, '乾为天')
    changed_gua = gua_map.get(changed_hex, '乾为天')

    return {
        '原卦': original_gua,
        '卦名': gua_name_map[original_gua],
        '变卦': changed_gua,
        '变卦名': gua_name_map[changed_gua],
        '动爻': moving_lines,
        '详细': f"卦名: {gua_name_map[original_gua]}, 原卦: {original_gua} ({original_hex}), 变卦名: {gua_name_map[changed_gua]}, 变卦: {changed_gua} ({changed_hex}), 动爻: {', '.join(map(str, moving_lines))}"
    }