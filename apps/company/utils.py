def unmask_number(value):
    # return re.sub(r"\D", "", value)
    return "".join(c for c in value if c.isdigit())


def mask_number(dirty_value):
    cleanValue = unmask_number(dirty_value)

    result = ""

    if dirty_value[0] == "7" or dirty_value[0] == "8":
        result = "+7" + cleanValue[1:]
    elif dirty_value[0] != "+" and dirty_value != "":
        result = "+7" + cleanValue
    elif dirty_value[0] == "+":
        result = "+" + cleanValue

    if len(result) > 2 and result.startsWith("+7"):
        result = result[0:2] + " (" + result[2:]

    if len(result) > 7 and result.startsWith("+7"):
        result = result[0:7] + ") " + result[7:]

    if len(result) > 12 and result.startsWith("+7"):
        result = result[0:12] + "-" + result[12:]

    if len(result) > 15 and result.startsWith("+7"):
        result = result[0:15] + "-" + result[15:]

    if result.startsWith("+7"):
        result = result[0:18]
    else:
        result = result[0:16]

    return result
