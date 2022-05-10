import logger
from sql_client import SqlClient
from fidelity_splits import FidelitySplits as Fidelity
from benzinga_splits import BenzingaSplits as Benzinga
from nasdaq_splits import NasdaqSplits as Nasdaq

log = logger.logger

__version__ = 1.1
__author__ = 'Jamith Nimantha'

if __name__ == "__main__":
    try:
        sql = SqlClient()
        log.info("Script started")
        if sql.initialize():
            log.info("Deleting all rows where announcement date < Today – 6 Months")
            if sql.delete_old_data():
                log.info("Deleting all rows Completed!")
            # Fidelity(sql)()
            # Benzinga(sql)()
            Nasdaq(sql)()


        else:
            log.critical("failed to establish connection with database.")
    except Exception as e:
        log.error(e)
    finally:
        if sql.connected:
            sql.close()
        log.info("Script ended")
