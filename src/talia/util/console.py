import datetime


def log(info):
    stamp = datetime.datetime.now()\
        .strftime("%Y/%m/%d %H:%M:%S")
    print(f"{stamp} | {info}")

    with open("log.txt", "a") as log_f:
        log_f.write(f"{stamp} | {info}")