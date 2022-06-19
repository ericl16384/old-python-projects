def x():
    print("START")
    out = range(10)
    for i in out:
        ans = yield i
        print("x: "+str(ans))

y = x()

try:
    print("test")
    print("y: "+str(y.send(None)))
    while True:
        print("y: "+str(y.send("asdf")))
except StopIteration:
    print("DONE")
