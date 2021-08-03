import random
import redis
import time
import asyncio
import aioredis 
r = redis.Redis(host='localhost', port=6380, db=0)
import json

def createTicket():
    ticket = "T" + ''.join(random.choice('0123456789ABCDEFGH') for i in range(16))
    print(ticket)
    if r.get(ticket) is None:
        r.set(ticket, 'reserved')
        return ticket
    else:
        ticket = createTicket()
        return ticket

def deleteTicket(ticket):
    ticket = ticket
    if r.get(ticket) !=  b'reserved':
        r.delete(ticket)
        return True
    else:
        return False

# async def getTicketOutput(ticket):
#     await asyncio.sleep(1)
#     redis = await aioredis.create_redis(
#         'redis://localhost:6380')
#     print(redis)
#     print(ticket)
#     while True:
#         if await redis.get(ticket) == b'reserved':
#             await asyncio.sleep(1)
#             print(await redis.get(ticket))
#         else:
#             break

#     output = json.loads(r.get(ticket))
#     redis.close()
#     return output

def getTicketOutput(ticket):
    print(ticket)
    i = 0
    while True:
        i+=1
        if r.get(ticket) == b'reserved':
            print(r.get(ticket))
            time.sleep(0.01)
        else:
            break
        if i==10: #max attempts
            return None
            

    output = json.loads(r.get(ticket))
    return output