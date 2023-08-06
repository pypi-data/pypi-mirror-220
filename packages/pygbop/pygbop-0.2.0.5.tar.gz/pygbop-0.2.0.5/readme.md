### Geely GBOP Client

request demo:

```python
from pygbop import GbopApiClient, Method, BasicAuth

auth = BasicAuth(access_key='xxxxxxxxxxxxxxxxx', secret_key='xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx')
client = GbopApiClient(auth, base_url='hello.api-dev.test.xxxxx.com')

print('=============GET=============')
params = {
    'params1': '123',
    'params3': ['s', 'w', 'k'],
    'params2': '321',
}
res = client.execute(Method.GET, '/api/v1/hello', params)
print(res.decode('utf-8'))

print('=============POST=============')
data = {'params3': 'testA', 'params4': 'testB'}
res = client.execute(Method.POST, '/api/v1/demo', data=data)
print(res.decode('utf-8'))

print('=============POST2=============')
params = {'params3': 'testA', 'params4': 'testB'}
res = client.execute(Method.POST, '/api/v1/demo', params=params, data=data)
print(res.decode('utf-8'))
```

cloud event push demo:

```python
from pygbop import CloudEventBasicAuth, EventPushClient

auth = CloudEventBasicAuth(producer_group='xxxxxxx',
                           subject='persistent://Information_Technology/xxxx/XXXX_EVENT',
                           secret_token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
event_push_client = EventPushClient(auth=auth, base_url='http://xxxx.dev.xxxxx.com')
data = {
    "message": "hello 喵啪斯"
}
response = event_push_client.push_message(data=data,
                                          source='xx.cmdb',
                                          type_='xx:cmdb:InstanceChanged')
print(response.decode('utf-8'))
```
or
```python
from pygbop import CloudEventBasicAuth, EventPushClient

auth = CloudEventBasicAuth(producer_group='xxxxxxx',
                           subject='persistent://Information_Technology/xxxx/XXXX_EVENT',
                           secret_token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
event_push_client = EventPushClient(auth=auth, base_url='http://xxxx.dev.xxxxx.com')
data = {
    "message": "hello 喵啪斯"
}
response = event_push_client.push(data=data,
                                  source='xx.cmdb',
                                  type_='xx:cmdb:InstanceChanged')
if response.result:
    message_id = response.data
else:
    code = response.code
    fail_message = response.message
```