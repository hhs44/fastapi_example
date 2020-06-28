def pagenation(record, url, currage, count: int):
    nextnum = int(count // 1) if (currage + 1) >= count else currage + 1
    prenum = 1 if (currage - 1) == 0 else currage - 1
    nexturl = url + f"page={nextnum}"
    preurl = url + f"page={prenum}"
    if currage == 0:
        currage = 1
    if currage >= count:
        currage = count
    latest = {
        'count': count,
        'currpage': currage,
        'nexturl': nexturl,
        'preurl': preurl,
        "records": record,
    }
    return latest
