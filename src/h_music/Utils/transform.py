def _MM_TO_MIN(mm):
    mm = float(mm)
    hm = str(int(round(mm, 2) * 100 % 100))
    hm = "0" + hm if len(hm) == 1 else hm
    m, s = divmod(int(float(mm)), 60)
    h, m = divmod(m, 60)
    return "%s:%s.%s" % (str(m), str(s), str(hm))


def _MIN_TO_MM(min):
    "2:20"
    min, s = str(min).split(":")
    return int(min) * 60 + int(s)

def _MIN_TO_MS(min):
    "2:20.11"
    min, s = str(min).split(":")
    s,ms = str(s).split(".")
    return int(min) * 60 + int(s)+float(ms) / 100


def _STR_TO_FILE_NAME_(title):
    error_set = ['/', '\\', ':', '*', '?', '"', '|', '<', '>']
    for c in error_set:
        title = str(title).replace(c,"")
    return title
