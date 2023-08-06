# PingPong Python SDK

## Example


```python
import os

from pingpongsdk import PingPong
from pingpongsdk.deployments.model import CreateDeployment


if __name__ == '__main__':
    pingpong = PingPong(api_key='<your-pingpong-api-key>')

    model = pingpong.models.get_by_id(id='4954c9fd-7fc2-4d4c-a036-f23f7605fa69')

    try:
        deployment = pingpong.deployments.create(deployment=CreateDeployment(
            name="example-deployment",
            model_id=model.id,
            args={
                'input_image_file': 'https://cdn.mediamagic.dev/media/eb341446-be53-11ed-b4a8-66139910f724.jpg',
            }
        ))

        print(model.name)
        print(deployment.job.results)
    except Exception as e:
        print(e)
```
