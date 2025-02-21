import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
from scheduler import run_scheduler

class SchedulerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SchedulerService"
    _svc_display_name_ = "Scheduler Service"
    _svc_description_ = "Service to run the scheduler as a background process."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger('[SchedulerService]')
        handler = logging.FileHandler('scheduler_service.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def SvcStop(self):
        self.logger.info('Service is stopping...')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.logger.info('Service is starting...')
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        run_scheduler()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SchedulerService)