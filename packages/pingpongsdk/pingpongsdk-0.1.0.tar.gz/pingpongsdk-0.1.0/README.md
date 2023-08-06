# PingPong Python SDK

## Example


```python
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.deployments.model import CreateDeployment
from src import PingPong


_API_KEY = os.getenv("X_MEDIAMAGIC_KEY")


if __name__ == '__main__':
    pingpong = PingPong(_API_KEY)

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
