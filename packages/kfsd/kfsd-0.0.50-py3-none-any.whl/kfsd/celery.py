from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.attr import AttrUtils
from kfsd.apps.core.utils.system import System
from celery import Celery

config = KubefacetsConfig().getConfig()
celeryConfig = DictUtils.get_by_path(config, "services.general.celery")
celeryInitConfig = DictUtils.get(celeryConfig, "init")
appName = System.getEnv("app")
celeryInitConfig["main"] = appName
celeryInitConfig["task_default_queue"] = "celery.queue." + appName
celeryInitConfig["task_default_exchange"] = "celery.prjs.exchange"
celeryInitConfig["task_default_routing_key"] = "celery.key." + appName

celeryConfigAttr = AttrUtils.format(celeryInitConfig)

app = Celery(appName)
app.conf.update(**celeryInitConfig)
app.autodiscover_tasks()
