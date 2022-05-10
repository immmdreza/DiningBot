import logging
from telegram.ext import Updater
from src.db import DB


class GarbageCollector:
    def __init__(self, token = None, admin_ids=set(), log_level='INFO', db: DB = None):
        if token:
            self.updater = Updater(token=token, use_context=True)
            self.dispatcher = self.updater.dispatcher
        self.db = db
        self.admin_ids = admin_ids
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            level={
                'INFO': logging.INFO,
                'DEBUG': logging.DEBUG,
                'ERROR': logging.ERROR,
            }[log_level])  

    def run(self):
        pass
    
    def clear_forget_codes(self):
        self.db.clear_forget_codes()
        logging.info("Forget codes cleared")

    def update_user_records(self):
        forget_codes = self.db.find_forget_code()
        users = {}
        for forget_code in forget_codes:
            users[forget_code['user_id']] = {
                'count': users.get(forget_code['user_id'], {'count': 0})['count'] + 1,
                'username': forget_code['username']
            }
        for user_id in users:
            self.db.update_user_forget_code_counts(users[user_id]['username'], user_id, users[user_id]['count'])
        logging.info("User records updated")