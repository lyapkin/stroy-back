from core.celery import app
from .watermark import watermark_img


@app.task(bind=True)
def watermark_img_task(self, path):
    try:
        watermark_img(path)
    except Exception as e:
        raise self.retry(exc=e, countdown=2 * 60, max_retries=3)
