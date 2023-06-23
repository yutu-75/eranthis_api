# flask, 对外网关

#### 启动方式

```shell
cd backend/scheduler/
python run_proto_gen.py

# change this line 5 in scheduler_pb2_grpc.py
import scheduler_pb2 as scheduler__pb2
# to
from . import scheduler_pb2 as scheduler__pb2

cd backend/gateway/
# Copy 'eth.ini.example' to 'eth.ini' and modify it.
gunicorn -c gateway/gunicorn.py gateway.app:app
```
