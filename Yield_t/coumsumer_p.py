#coding:utf-8

"""
pi@raspberrypi:~/git/master/Study/Yield_t $ python coumsumer_p.py


[PRODUCER]Produce 1....
[CONSUMER] Consuming 1 ....
200 OK

[PRODUCEr]Comsumer return 200 OK...
[PRODUCER]Produce 2....
[CONSUMER] Consuming 2 ....
200 OK

[PRODUCEr]Comsumer return 200 OK...
[PRODUCER]Produce 3....
[CONSUMER] Consuming 3 ....
200 OK

[PRODUCEr]Comsumer return 200 OK...
[PRODUCER]Produce 4....
[CONSUMER] Consuming 4 ....
200 OK

[PRODUCEr]Comsumer return 200 OK...
[PRODUCER]Produce 5....
[CONSUMER] Consuming 5 ....
200 OK

[PRODUCEr]Comsumer return 200 OK...
********************************************
step1. run generate consumer and wait at 'n = yield r'
step2. producer to run and run to 'r = c.send(n)', resume generate and replace 'yield r' with 'value of n'
step3. consumer run and loop to "n = yield r" wait
step4. return producer run to the next loop till "r = c.send(n)", repeat step 1~4, till 'n < 5', loop end.
"""
def consumer():
    r = ""
    while True:
        print("\033[32m%s\033[0m\n" % r)
        n = yield r
        if not n:
            return
        print("[CONSUMER] Consuming %s ...." % n)
        r = "200 OK"

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print("[PRODUCER]Produce %s...." % n)
        r = c.send(n)
        print("[PRODUCEr]Comsumer return %s..." % r)
    c.close()

if __name__ == "__main__":
    c = consumer()
    produce(c)
