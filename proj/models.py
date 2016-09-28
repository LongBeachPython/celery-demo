from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

class AsciiTask(Model):
    class Meta:
        table_name = 'dynamodb-ascii-tasks'
        host = "http://localhost:8000"
    task_id = UnicodeAttribute(hash_key=True)
    ascii_text = UnicodeAttribute()