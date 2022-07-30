n = nuke.thisNode()
k = nuke.thisKnob()

with n:
    linear = nuke.toNode("toLinear")
    other = nuke.toNode("toOther")
    cConstant = nuke.toNode("ColorConstant")
    cSwitch = nuke.toNode("cSwitch")

#=======================================================================function
def numCorrect_1(numbers):
    if isinstance(numbers, list):
        for number in numbers:
            if number < 0:
                numbers[numbers.index(number)] = 0
            elif number > 1:
                numbers[numbers.index(number)] = 1

    else:
        if numbers < 0:
            numbers = 0
        elif numbers > 1:
            numbers = 1

    return numbers

def numCorrect_255(r, g, b):
    numbers = [r, g, b]

    for value in numbers:
        if value < 0:
            numbers[numbers.index(value)] = 0
        elif value > 255:
            numbers[numbers.index(value)] = 255
        else:
            numbers[numbers.index(value)] = int(round(value))

    return numbers[0], numbers[1], numbers[2]

def check_hex(hex, num):
    alphanumber = list("0123456789ABCDEFabcdef")
    str0x = ["0x", "0X"]
    strff = ["FF", "ff", "fF", "Ff"]

    if num == 0:
        if hex == "":
            return "blank"
        elif hex[:2] in str0x and hex[-2:] in strff and len(hex) <= 10 and hex[2:].isalnum():
            for i in hex[2:]:
                if i not in alphanumber:
                    return False
        else:
            return False

    if num == 1:
        if hex == "":
            return "blank"
        elif hex[0] == "#" and len(hex) == 7 and hex[1:].isalnum():
            for i in hex[1:]:
                if i not in alphanumber:
                    return False
        else:
            return False

def check_integer(check_int):
    if check_int == "":
        return "blank"

    elif check_int.count(".") == 1:
        if check_int.split(".")[1] == "0":
            check_int = check_int.split(".")[0]
            if check_int.isdigit():
                if int(check_int) >= 255 and int(check_int) <= int('0xFFFFFFFF', 16):
                    return True

    elif check_int.isdigit():
        if int(check_int) >= 255 and int(check_int) <= int('0xFFFFFFFF', 16):
            return True

def float2Hex(r, g, b):
    r = int(round(r*255))
    g = int(round(g*255))
    b = int(round(b*255))
    return hex(int(("0x" + "{:02x}{:02x}{:02x}".format(r, g, b) + "ff"), 16))

def rgb2Hex(r, g, b):
    r = int(round(r))
    g = int(round(g))
    b = int(round(b))
    return "#" + "{:02x}{:02x}{:02x}".format(r, g, b)

def o_hex2Int(n, sHex):
    n['o_r_cChip'].setValue(int("0x" + sHex[1:3] + "0000ff", 16))
    n['o_g_cChip'].setValue(int("0x" + sHex[3:5] + "00ff", 16))
    n['o_b_cChip'].setValue(int("0x" + sHex[5:7] + "ff", 16))

def num2Multiple(numbers):
    if isinstance(numbers, list):
        numbers.append(1.0)
    else:
        numbers = [numbers, numbers, numbers, 1.0]

    return numbers

def sglOrMultiple(n, r, g, b):
    if n['w_float'].singleValue() and (r==g and r==b and g==b):
        return r
    else:
        return r, g, b

def convCase(case, num, f):
    if f == 0:
        case = str(case)[:num] + str(case)[num:].upper()
    else:
        case = str(case)[:num] + str(case)[num:].lower()

    return case

def check_link_tile(n):
    if n['link_tile_color'].getValue() == False:
        n['linkSymbol'].setEnabled(False)
        n['tile_color'].setValue(int(n['w_cChip'].getValue()))
        n['current_tile_color'].setLabel("tile_color ")
        n['current_tile_color'].setValue(str(int(n['w_cChip'].getValue())))
    else:
        n['linkSymbol'].setEnabled(True)
        n['tile_color'].setValue(int(n['o_cChip'].getValue()))
        n['current_tile_color'].setLabel("tile_color ")
        n['current_tile_color'].setValue(str(int(n['o_cChip'].getValue())))

def set_python_example(n):
    python_example = "nuke.selectedNode()['tile_color'].setValue({})".format(n['w_int'].getValue())
    n['w_python_example'].setValue(python_example)

def set_html_example(n):
    html_example1 = "<span style='color:{}".format(n['o_hex'].getValue())
    html_example2 = "'>{}</span>".format(n['o_text_test'].getValue())
    html_example = html_example1 + html_example2
    n['o_html_example'].setValue(html_example)

    if n['o_text_test'].getValue() == "":
        n['o_html_display'].setValue("<span style='font-size:20px'>&nbsp;</span>")
    else:
        html_display1 = "; font-size:20px"
        html_display = html_example1 + html_display1 + html_example2
        n['o_html_display'].setValue(html_display)

#===============================================================linear and other
def linear2other(cConstant, fRGB, cSwitch, other, n, w_int, check=True):
    cConstant['color'].setValue(num2Multiple(fRGB))
    cSwitch['which'].setValue(0)

    o_r = int(round(other.sample('red', 0, 0)*255))
    o_g = int(round(other.sample('green', 0, 0)*255))
    o_b = int(round(other.sample('blue', 0, 0)*255))
    o_hex = rgb2Hex(o_r, o_g, o_b)

    n['o_r'].setValue(o_r)
    n['o_g'].setValue(o_g)
    n['o_b'].setValue(o_b)
    n['o_hex'].setValue(convCase(o_hex, 1, n['o_hex_case'].getValue()))
    n['o_errorMsg'].setValue(" ")
    n['o_cChip'].setValue(int("0x" + o_hex[1:] + "ff", 16))
    o_hex2Int(n, o_hex)

    if check == True:
        check_link_tile(n)

    set_python_example(n)
    set_html_example(n)

    if n['w_hex_case'].enabled() == False:
        n['w_hex_case'].setEnabled(True)

    n['o_text_test'].setEnabled(True)
    if n['o_hex_case'].enabled() == False:
        n['o_hex_case'].setEnabled(True)

def other2Linear(cConstant, o_r, o_g, o_b, cSwitch, linear, n, o_hex, check=True):
    cConstant['color'].setValue([o_r/255, o_g/255, o_b/255, 1.0])
    cSwitch['which'].setValue(1)

    fR = linear.sample('red', 0, 0)
    fG = linear.sample('green', 0, 0)
    fB = linear.sample('blue', 0, 0)
    w_hex = float2Hex(fR, fG, fB)
    w_int = int(w_hex, 16)

    n['w_float'].setValue(sglOrMultiple(n, fR, fG, fB))
    n['w_hex'].setValue(convCase(w_hex, 2, n['w_hex_case'].getValue()))
    n['w_int'].setValue(str(w_int))
    n['w_errorMsg'].setValue(" ")
    n['w_cChip'].setValue(w_int)

    if check == True:
        check_link_tile(n)

    set_python_example(n)
    set_html_example(n)

    if n['w_hex_case'].enabled() == False:
        n['w_hex_case'].setEnabled(True)

    n['o_text_test'].setEnabled(True)
    if n['o_hex_case'].enabled() == False:
        n['o_hex_case'].setEnabled(True)

#==================================================================working space
#==================================================================working space
#==================================================================working space
if k.name() == "w_float":
    #=========working space
    fRGB = numCorrect_1(n['w_float'].getValue())
    n['w_float'].setValue(fRGB)

    if n['w_float'].singleValue():
        fR, fG, fB = fRGB, fRGB, fRGB
    else:
        fR, fG, fB = fRGB[0], fRGB[1], fRGB[2]

    w_hex = float2Hex(fR, fG, fB)
    w_int = int(w_hex, 16)

    n['w_hex'].setValue(convCase(w_hex, 2, n['w_hex_case'].getValue()))
    n['w_int'].setValue(str(w_int))
    n['w_errorMsg'].setValue(" ")
    n['w_cChip'].setValue(w_int)

    #=========other space
    linear2other(cConstant, fRGB, cSwitch, other, n, w_int)

elif k.name() == "w_hex":
    if check_hex(n['w_hex'].getValue(), 1) == "blank":
        w_errorMsg = "<span style='color:#FFE500'>The value can't be blank.</span>"
        n['w_errorMsg'].setValue(w_errorMsg)
        n['w_hex_case'].setEnabled(False)

    elif check_hex(n['w_hex'].getValue(), 0) == False:
        msg1 = "<span style='color:#FFE500'>The&nbsp;&nbsp;</span>"
        msg2 = str(n['w_hex'].getValue())
        msg3 = "<span style='color:#FFE500'>&nbsp;&nbsp;is invalid.</span>"
        w_errorMsg = msg1 + msg2 + msg3
        n['w_errorMsg'].setValue(w_errorMsg)
        n['w_hex_case'].setEnabled(False)

    else:
        #=========working space
        w_hex = hex(int(n['w_hex'].getValue(), 16))
        n['w_hex'].setValue(convCase(w_hex, 2, n['w_hex_case'].getValue()))
        w_hex_10 = "{:#010x}".format(int(n['w_hex'].getValue(), 16))

        fR = int(w_hex_10[2:4], 16)/255
        fG = int(w_hex_10[4:6], 16)/255
        fB = int(w_hex_10[6:8], 16)/255
        fRGB = [fR, fG, fB]
        w_int = int(n['w_hex'].getValue(), 16)

        n['w_float'].setValue(sglOrMultiple(n, fR, fG, fB))
        n['w_int'].setValue(str(w_int))
        n['w_errorMsg'].setValue(" ")
        n['w_cChip'].setValue(w_int)

        #=========other space
        linear2other(cConstant, fRGB, cSwitch, other, n, w_int)

elif k.name() == "w_int":
    if check_integer(n['w_int'].getValue()) == True:
        #=========working space
        w_int = int(float(n['w_int'].getValue()))
        n['w_int'].setValue(str(w_int))

        w_hex_10 = "{:#010x}".format(w_int)
        fR = int(w_hex_10[2:4], 16)/255
        fG = int(w_hex_10[4:6], 16)/255
        fB = int(w_hex_10[6:8], 16)/255
        fRGB = [fR, fG, fB]
        w_hex = hex(w_int)

        n['w_float'].setValue(sglOrMultiple(n, fR, fG, fB))
        n['w_hex'].setValue(convCase(w_hex, 2, n['w_hex_case'].getValue()))
        n['w_errorMsg'].setValue(" ")
        n['w_cChip'].setValue(w_int)

        #=========other space
        linear2other(cConstant, fRGB, cSwitch, other, n, w_int)

    elif check_integer(n['w_int'].getValue()) == "blank":
        w_errorMsg = "<span style='color:#FFE500'>The value can't be blank.</span>"
        n['w_errorMsg'].setValue(w_errorMsg)

    else:
        msg1 = "<span style='color:#FFE500'>The&nbsp;&nbsp;</span>"
        msg2 = n['w_int'].getValue()
        msg3 = "<span style='color:#FFE500'>&nbsp;&nbsp;is invalid.</span>"
        w_errorMsg = msg1 + msg2 + msg3
        n['w_errorMsg'].setValue(w_errorMsg)

elif k.name() == "w_cChip":
    #=========working space
    w_int = int(n['w_cChip'].getValue())

    w_hex_10 = "{:#010x}".format(w_int)
    fR = int(w_hex_10[2:4], 16)/255
    fG = int(w_hex_10[4:6], 16)/255
    fB = int(w_hex_10[6:8], 16)/255
    fRGB = [fR, fG, fB]
    w_hex = hex(w_int)

    n['w_float'].setValue(sglOrMultiple(n, fR, fG, fB))
    n['w_hex'].setValue(convCase(w_hex, 2, n['w_hex_case'].getValue()))
    n['w_int'].setValue(str(w_int))
    n['w_errorMsg'].setValue(" ")

    #=========other space
    linear2other(cConstant, fRGB, cSwitch, other, n, w_int)

#=====================================================================tile_color
elif k.name() == "tile_color":
    value_int = int(n['tile_color'].getValue())

    n['current_tile_color'].setLabel("tile_color ")
    n['current_tile_color'].setValue(str(value_int))

    if n['link_tile_color'].getValue() == False:
        #=========working space
        w_int = value_int
        w_hex_10 = "{:#010x}".format(w_int)
        fR = int(w_hex_10[2:4], 16)/255
        fG = int(w_hex_10[4:6], 16)/255
        fB = int(w_hex_10[6:8], 16)/255
        fRGB = [fR, fG, fB]
        w_hex = hex(w_int)

        n['w_float'].setValue(sglOrMultiple(n, fR, fG, fB))
        n['w_hex'].setValue(convCase(w_hex, 2, n['w_hex_case'].getValue()))
        n['w_int'].setValue(str(w_int))
        n['w_errorMsg'].setValue(" ")
        n['w_cChip'].setValue(w_int)

        #=========other space
        linear2other(cConstant, fRGB, cSwitch, other, n, w_int, False)

    else:
        #=========other space
        o_hex = "#" + "{:08x}".format(value_int)[:6]
        o_r = int(o_hex[1:3], 16)
        o_g = int(o_hex[3:5], 16)
        o_b = int(o_hex[5:7], 16)

        n['o_r'].setValue(o_r)
        n['o_g'].setValue(o_g)
        n['o_b'].setValue(o_b)
        n['o_hex'].setValue(convCase(o_hex, 1, n['o_hex_case'].getValue()))
        n['o_errorMsg'].setValue(" ")
        n['o_cChip'].setValue(value_int)
        o_hex2Int(n, o_hex)

        #=========working space
        other2Linear(cConstant, o_r, o_g, o_b, cSwitch, linear, n, o_hex, False)

elif k.name() == "current_tile_color":
    if check_integer(n['current_tile_color'].getValue()) == True:
        value_int = int(float(n['current_tile_color'].getValue()))
        
        n['current_tile_color'].setValue(str(value_int))
        n['current_tile_color'].setLabel("tile_color ")
        n['tile_color'].setValue(value_int)

        if n['link_tile_color'].getValue() == False:
            #=========working space
            w_int = value_int
            w_hex_10 = "{:#010x}".format(w_int)
            fR = int(w_hex_10[2:4], 16)/255
            fG = int(w_hex_10[4:6], 16)/255
            fB = int(w_hex_10[6:8], 16)/255
            fRGB = [fR, fG, fB]
            w_hex = hex(w_int)

            n['w_float'].setValue(sglOrMultiple(n, fR, fG, fB))
            n['w_hex'].setValue(convCase(w_hex, 2, n['w_hex_case'].getValue()))
            n['w_int'].setValue(str(w_int))
            n['w_errorMsg'].setValue(" ")
            n['w_cChip'].setValue(w_int)

            #=========other space
            linear2other(cConstant, fRGB, cSwitch, other, n, w_int, False)

        else:
            #=========other space
            o_hex = "#" + "{:08x}".format(value_int)[:6]
            o_r = int(o_hex[1:3], 16)
            o_g = int(o_hex[3:5], 16)
            o_b = int(o_hex[5:7], 16)

            n['o_r'].setValue(o_r)
            n['o_g'].setValue(o_g)
            n['o_b'].setValue(o_b)
            n['o_hex'].setValue(convCase(o_hex, 1, n['o_hex_case'].getValue()))
            n['o_errorMsg'].setValue(" ")
            n['o_cChip'].setValue(value_int)
            o_hex2Int(n, o_hex)

            #=========working space
            other2Linear(cConstant, o_r, o_g, o_b, cSwitch, linear, n, o_hex, False)

    elif check_integer(n['current_tile_color'].getValue()) == "blank":
        w_errorMsg = "<span style='color:#FFE500'>Blank </span>"
        n['current_tile_color'].setLabel(w_errorMsg)

    else:
        w_errorMsg = "<span style='color:#FFE500'>Invalid </span>"
        n['current_tile_color'].setLabel(w_errorMsg)

#====================================================================other space
#====================================================================other space
#====================================================================other space
elif k.name() in ['o_r', 'o_g', 'o_b']:
    #=========other space
    o_r, o_g, o_b = n['o_r'].getValue(), n['o_g'].getValue(), n['o_b'].getValue()
    o_r, o_g, o_b = numCorrect_255(o_r, o_g, o_b)
    o_hex = rgb2Hex(o_r, o_g, o_b)

    n['o_r'].setValue(o_r)
    n['o_g'].setValue(o_g)
    n['o_b'].setValue(o_b)
    n['o_hex'].setValue(convCase(o_hex, 1, n['o_hex_case'].getValue()))
    n['o_errorMsg'].setValue(" ")
    n['o_cChip'].setValue(int("0x" + o_hex[1:] + "ff", 16))
    o_hex2Int(n, o_hex)

    #=========working space
    other2Linear(cConstant, o_r, o_g, o_b, cSwitch, linear, n, o_hex)

elif k.name() == "o_hex":
    if check_hex(n['o_hex'].getValue(), 1) == "blank":
        errorMsg = "<span style='color:#FFE500'>The value can't be blank.</span>"
        n['o_errorMsg'].setValue(errorMsg)
        n['o_text_test'].setEnabled(False)
        n['o_hex_case'].setEnabled(False)

    elif check_hex(n['o_hex'].getValue(), 1) == False:
        msg1 = "<span style='color:#FFE500'>The&nbsp;&nbsp;</span>"
        msg2 = str(n['o_hex'].getValue())
        msg3 = "<span style='color:#FFE500'>&nbsp;&nbsp;is invalid.</span>"
        o_errorMsg = msg1 + msg2 + msg3
        n['o_errorMsg'].setValue(o_errorMsg)
        n['o_text_test'].setEnabled(False)
        n['o_hex_case'].setEnabled(False)

    else:
        #=========other space
        n['o_hex'].setValue(convCase(n['o_hex'].getValue(), 1, n['o_hex_case'].getValue()))
        o_hex = n['o_hex'].getValue()

        o_r = int(o_hex[1:3], 16)
        o_g = int(o_hex[3:5], 16)
        o_b = int(o_hex[5:7], 16)

        n['o_r'].setValue(o_r)
        n['o_g'].setValue(o_g)
        n['o_b'].setValue(o_b)
        n['o_errorMsg'].setValue(" ")
        n['o_cChip'].setValue(int("0x" + o_hex[1:] + "ff", 16))
        o_hex2Int(n, o_hex)

        #=========working space
        other2Linear(cConstant, o_r, o_g, o_b, cSwitch, linear, n, o_hex)

elif k.name() == "o_cChip":
    #=========other space
    o_hex = "#" + "{:08x}".format(int(n['o_cChip'].getValue()))[:6]

    o_r = int(o_hex[1:3], 16)
    o_g = int(o_hex[3:5], 16)
    o_b = int(o_hex[5:7], 16)

    n['o_r'].setValue(o_r)
    n['o_g'].setValue(o_g)
    n['o_b'].setValue(o_b)
    n['o_hex'].setValue(convCase(o_hex, 1, n['o_hex_case'].getValue()))
    n['o_errorMsg'].setValue(" ")
    o_hex2Int(n, o_hex)

    #=========working space
    other2Linear(cConstant, o_r, o_g, o_b, cSwitch, linear, n, o_hex)

#===================================================================other action
elif k.name() == "link_tile_color":
    check_link_tile(n)

elif k.name() == "w_hex_case":
    n['w_hex'].setValue(convCase(n['w_hex'].getValue(), 2, k.getValue()))

elif k.name() == "o_hex_case":
    n['o_hex'].setValue(convCase(n['o_hex'].getValue(), 1, k.getValue()))
    set_html_example(n)

elif k.name() == "o_text_test":
    set_html_example(n)
