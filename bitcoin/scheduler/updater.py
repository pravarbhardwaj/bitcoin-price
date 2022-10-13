from apscheduler.schedulers.background import BackgroundScheduler
from bitcoin.views import BitcoinViewSet

def start():
    scheduler = BackgroundScheduler()
    bitcoin = BitcoinViewSet()
    scheduler.add_job(bitcoin.save_bitcoin_data, "interval", seconds=30, id="bitcoin_001", replace_existing=True)
    scheduler.start()