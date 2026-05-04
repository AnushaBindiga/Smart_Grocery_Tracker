from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from scrapers.carrefour import scrape_carrefour
from scrapers.auchan import scrape_auchan

def run_carrefour():
    print("Running Carrefour scraper...")
    asyncio.run(scrape_carrefour())

def run_auchan():
    print("Running Auchan scraper...")
    asyncio.run(scrape_auchan())

def run_all_scrapers():
    print("Running all scrapers...")
    run_carrefour()
    run_auchan()
    print("All scrapers done!")

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Run every day at 7am
    scheduler.add_job(
        run_all_scrapers,
        CronTrigger(hour=7, minute=0),
        id='daily_scraper',
        name='Daily promotion scraper',
        replace_existing=True
    )
    
    scheduler.start()
    print("Scheduler started — scrapers will run daily at 7am!")
    return scheduler