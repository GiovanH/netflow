from numpy import uint32

t = uint32
bad = t(0)
# bad = t(np.nan)


def utos(ipnum):
    return ".".join([str(n) for n in (ipnum).tobytes()])

# np.uint8:  0.00055
# int:       0.00026
# nosum:     0.00025


def stou(ipstr):
    # if ipstr == "":
    #     return bad
    try:
        iptu = [int(m) for m in ipstr.split(".")]
        # Convert
        return t(
            sum(
                [
                    iptu[i] * 256**i  # 2**(8 * i)
                    for i in range(0, 4)
                ]
            )
            # iptu[0] + (iptu[1] * 256) + (iptu[2] * 65536) + (iptu[3] * 16777216)
        )
    except (ValueError, IndexError):
        # print("GIVEN BAD IP ADDRESS \"{}\" ({}, {})".format(ipstr, type(ipstr), ipstr == ""))
        return bad


def tests():
    ipstrs = [
        ("", False,),
        ("0.0.0.0", True,),
        ("1.2.3.4", True,),
        ("192.168.1.1", True,),
        ("4.4.4.4", True,),
        ("004.004.004.004", False,),
        ("255.255.255.255", True,),
        ("255.255.255.256", False,),
        ("256.256.256.256", False,),
        ("42", False,)
    ]
    for (ipstr, shdeq) in ipstrs:
        num = stou(ipstr)
        print("{} {} => {} => {}".format(
            (ipstr == utos(num)) == shdeq,
            ipstr,
            num,
            utos(num)
        )
        )


if __name__ == "__main__":
    tests()
