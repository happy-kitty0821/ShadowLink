
import os
from datetime import date
from django.conf import settings
from authentication_app import  models as authModel

def ensure_daily_log_model_entry():
    log_date = date.today()
    filename = f"{log_date}-logs.log"
    filepath = os.path.join(settings.LOGS_ROOT, filename)

    #entry creation if it does not exists
    if not authModel.SystemLogRecord.objects.filter(date=log_date).exists():
        authModel.SystemLogRecord.objects.create(date=log_date, log_file_path=filepath)
