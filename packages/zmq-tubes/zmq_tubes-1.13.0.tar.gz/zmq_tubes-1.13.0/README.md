[![PyPI](https://img.shields.io/pypi/v/zmq_tubes?color=green&style=plastic)](https://pypi.org/project/zmq-tubes/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zmq_tubes?style=plastic)
![License](https://img.shields.io/github/license/calcite/zmq_tubes?style=plastic)
# ZMQ Tubes

ZMQ Tubes is a managing system for ZMQ communication. 
It can manage many ZMQ sockets by one interface. 
The whole system is hierarchical, based on topics 
(look at [MQTT topics](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/)).

## Classes
- **TubeMessage** - This class represents a request/response message. 
  Some types of tubes require a response in this format.
- **Tube** - This class wraps a ZMQ socket. 
  It represents a connection between client and server.
- **TubeMonitor** - The class can sniff of the ZMQTube communication.
- **TubeNode** - This represents an application interface for communication via tubes.


## Asyncio / Threading
The library support bot method. Asyncio from Python 3.7.

```python
from zmq_tubes import TubeNode, Tube            # Asyncio classes
from zmq_tubes.threads import TubeNode, Tube    # Threads classes
```


## Usage:

### Node definitions in yml file 
We can define all tubes for one TubeNode by yml file. 

```yaml
# test.yml
tubes:
  - name: Client REQ
    addr:  ipc:///tmp/req.pipe    
    tube_type: REQ
    topics:
      - foo/#
      - +/bar
  
  - name: Client PUB
    addr:  ipc:///tmp/pub.pipe    
    tube_type: PUB
    topics:
      - foo/pub/#

  - name: Server ROUTER
    addr:  ipc:///tmp/router.pipe    
    tube_type: ROUTER
    server: yes
    sockopts:
      LINGER: 0
    topics:
      - server/#
```

```python
import asyncio
import yaml
from zmq_tubes import TubeNode, TubeMessage


async def handler(request: TubeMessage):
  print(request.payload)
  return request.create_response('response')


async def run():
  with open('test.yml', 'r+') as fd:
    schema = yaml.safe_load(fd)
  node = TubeNode(schema=schema)
  node.register_handler('server/#', handler)
  async with node:
      await node.publish('foo/pub/test', 'message 1')
      print(await node.request('foo/xxx', 'message 2'))

asyncio.run(run())
```




### Request / Response
This is a simple scenario, the server processes the requests serially.
#### Server:

```python
from zmq_tubes import Tube, TubeNode, TubeMessage


async def handler(request: TubeMessage):
  print(request.payload)
  return 'answer'
  # or return request.create_response('response')


tube = Tube(
  name='Server',
  addr='ipc:///tmp/req_resp.pipe',
  server=True,
  tube_type='REP'
)

node = TubeNode()
node.register_tube(tube, 'test/#')
node.register_handler('test/#', handler)
await node.start()

# output: 'question'
```

#### Client:

```python
from zmq_tubes import Tube, TubeNode

tube = Tube(
  name='Client',
  addr='ipc:///tmp/req_resp.pipe',
  tube_type='REQ'
)

node = TubeNode()
node.register_tube(tube, 'test/#')
response = await node.request('test/xxx', 'question')
print(response.payload)
# output: 'answer'
```




### Subscribe / Publisher
#### Server:

```python
from zmq_tubes import Tube, TubeNode, TubeMessage


async def handler(request: TubeMessage):
  print(request.payload)


tube = Tube(
  name='Server',
  addr='ipc:///tmp/sub_pub.pipe',
  server=True,
  tube_type='SUB'
)

node = TubeNode()
node.register_tube(tube, 'test/#')
node.register_handler('test/#', handler)
await node.start()
# output: 'message'
```

#### Client:

```python
from zmq_tubes import Tube, TubeNode

tube = Tube(
  name='Client',
  addr='ipc:///tmp/sub_pub.pipe',
  tube_type='PUB'
)
# In the case of publishing, the first message is very often
# lost. The workaround is to connect the tube manually as soon as possible.
tube.connect()

node = TubeNode()
node.register_tube(tube, 'test/#')
node.publish('test/xxx', 'message')        
```




### Request / Router
The server is asynchronous. It means it is able to process 
more requests at the same time.

#### Server:

```python
import asyncio
from zmq_tubes import Tube, TubeNode, TubeMessage


async def handler(request: TubeMessage):
  print(request.payload)
  if request.payload == 'wait':
    await asyncio.sleep(10)
  return request.create_response(request.payload)


tube = Tube(
  name='Server',
  addr='ipc:///tmp/req_router.pipe',
  server=True,
  tube_type='ROUTER'
)

node = TubeNode()
node.register_tube(tube, 'test/#')
node.register_handler('test/#', handler)
await node.start()
# output: 'wait'
# output: 'message'
```

#### Client:

```python
import asyncio
from zmq_tubes import Tube, TubeNode

tube = Tube(
  name='Client',
  addr='ipc:///tmp/req_router.pipe',
  tube_type='REQ'
)


async def task(node, text):
  print(await node.request('test/xxx', text))


node = TubeNode()
node.register_tube(tube, 'test/#')
asyncio.create_task(task(node, 'wait'))
asyncio.create_task(task(node, 'message'))
# output: 'message'
# output: 'wait'
```




### Dealer / Response
The client is asynchronous. It means it is able to send 
more requests at the same time.

#### Server:

```python
from zmq_tubes import Tube, TubeNode, TubeMessage


async def handler(request: TubeMessage):
  print(request.payload)
  return 'response'
  # or return requset.create_response('response')


tube = Tube(
  name='Server',
  addr='ipc:///tmp/dealer_resp.pipe',
  server=True,
  tube_type='REP'
)

node = TubeNode()
node.register_tube(tube, 'test/#')
node.register_handler('test/#', handler)
await node.start()
# output: 'message'
```

#### Client:

```python
from zmq_tubes import Tube, TubeNode, TubeMessage

tube = Tube(
  name='Client',
  addr='ipc:///tmp/dealer_resp.pipe',
  tube_type='DEALER'
)


async def handler(response: TubeMessage):
  print(response.payload)


node = TubeNode()
node.register_tube(tube, 'test/#')
node.register_handler('test/#', handler)

await node.send('test/xxx', 'message')

# output: 'response'
```



### Dealer / Router
The client and server are asynchronous. It means it is able to send and process 
more requests/responses at the same time.

#### Server:

```python
import asyncio
from zmq_tubes import Tube, TubeNode, TubeMessage


async def handler(request: TubeMessage):
  print(request.payload)
  if request.payload == 'wait':
    await asyncio.sleep(10)
  return request.create_response(request.payload)


tube = Tube(
  name='Server',
  addr='ipc:///tmp/dealer_router.pipe',
  server=True,
  tube_type='ROUTER'
)

node = TubeNode()
node.register_tube(tube, 'test/#')
node.register_handler('test/#', handler)
await node.start()
# output: 'wait'
# output: 'message'
```

#### Client:

```python
from zmq_tubes import Tube, TubeNode, TubeMessage

tube = Tube(
  name='Client',
  addr='ipc:///tmp/dealer_router.pipe',
  tube_type='DEALER'
)


async def handler(response: TubeMessage):
  print(response.payload)


node = TubeNode()
node.register_tube(tube, 'test/#')
node.register_handler('test/#', handler)

await node.send('test/xxx', 'wait')
await node.send('test/xxx', 'message')

# output: 'message'
# output: 'wait'
```



### Dealer / Dealer
The client and server are asynchronous. It means it is able to send and process 
more requests/responses at the same time.

#### Server:

```python
from zmq_tubes import Tube, TubeNode, TubeMessage

tube = Tube(
  name='Server',
  addr='ipc:///tmp/dealer_dealer.pipe',
  server=True,
  tube_type='DEALER'
)


async def handler(response: TubeMessage):
  print(response.payload)


node = TubeNode()
node.register_tube(tube, 'test/#')
node.register_handler('test/#', handler)

await node.send('test/xxx', 'message from server')
# output: 'message from client'
```

#### Client:

```python
from zmq_tubes import Tube, TubeNode, TubeMessage

tube = Tube(
  name='Client',
  addr='ipc:///tmp/dealer_dealer.pipe',
  tube_type='DEALER'
)


async def handler(response: TubeMessage):
  print(response.payload)


node = TubeNode()
node.register_tube(tube, 'test/#')
node.register_handler('test/#', handler)

await node.send('test/xxx', 'message from client')
# output: 'message from server'
```


## Debugging / Monitoring
We can assign a monitor socket to our zmq tubes. By this monitor socket, we can sniff zmq communication or get a zmq tube
configuration. 
```yaml
tubes:
  - name: ServerRouter
    addr:  ipc:///tmp/router.pipe
    monitor: ipc:///tmp/test.monitor 
    tube_type: ROUTER
    server: yes    
    topics:
      - foo/#       
```
This is example of a yaml definition. We can use the same monitor socket for more tubes in the same tubeNode.
When we add the monitor attribute to our tube definition, the application automatically create a new socket monitor: 
`/tmp/test.monitor`. Your application works as a server side. The logs are sent to the socket only for the time, when the monitoring
tool is running.

### Monitoring tool

After enabling of the monitoring in the application, we can use the monitoring tool for sniff. 

```shell
# get the server tube configuration
> zmqtube-monitor get_schema ipc:///tmp/display.monitor
    tubes:
      - addr: ipc:///tmp/router.pipe
        monitor: ipc:///tmp/test.monitor 
        name: ServerRouter
        server: 'yes'
        tube_type: ROUTER

# the log tube communication. Logs will be saved to dump.rec as well. 
> zmqtube-monitor logs -d ./dump.rec ipc:///tmp/display.monitor
 0.28026580810546875 ServerRouter < foo/test Request
 0.0901789665222168 ServerRouter > foo/test Response

# The format of output
# <relative time> <tube name> <direction> <topic> <message>` 
```

### Simulation of the client side
When we have a dump file (e.g. `dump.rec`), we can simulate the communication with our app.
The first step is prepare the mock client schema file.
For this, We can get the tube node configuration from our application and after that edit it. 
```shell
> zmqtube-monitor get_schema ipc:///tmp/display.monitor > mock_schema.yaml
> vim mock_schema.yaml
...   
# Now, we have to update the file mock_schema.yaml. 
# We change configuration to the mock client configuration. 
# The names of the tubes must be the same as are in your app. 
# We can remove monitoring attribute and change server and 
# tube_type attributes. In this mock file, the topics are not 
# required, they are ignored. 

> cat mock_schema.yaml
tubes:
- addr: ipc:///tmp/router.pipe
  name: ServerRouter
  tube_type: REQ
```

Now, we can start the simulation of the client communication.
```shell
> zmqtube-monitor simulate mock_schema.yaml dump.rec
```
If the response of our app is not the same as tool expects (the response saved in dump file), then 
the monitoring tool warns us.  
We can modify speed of the simulation by the parameter `--speed`.

In the default configuration, is  the simulation run the same
speed as original communication (parameter `--speed=1`). 

| Speed | description |
| :-: | :- |
| 0 | no blocking simulation |
| 0.5 | twice faster than original |
| 1 | original speed |
| 2 | twice slower than original |


### Example of programming declaration of the monitoring.
```python
import zmq
from zmq_tubes.threads import Tube, TubeNode, TubeMessage, TubeMonitor


def handler(request: TubeMessage):
  print(request.payload)
  return request.create_response('response')

resp_tube = Tube(
  name='REP',
  addr='ipc:///tmp/rep.pipe',
  server='yes',
  tube_type=zmq.REP
)

req_tube = Tube(
  name='REQ',
  addr='ipc:///tmp/rep.pipe',  
  tube_type=zmq.REQ
)

node = TubeNode()
node.register_tube(resp_tube, f"foo/#")
node.register_tube(req_tube, f"foo/#")
node.register_handler(f"foo/#", handler)

node.register_monitor(resp_tube, TubeMonitor(addr='ipc:///tmp/test.monitor'))
  
with node:
    print(node.request('foo/xxx', 'message 2'))

```
