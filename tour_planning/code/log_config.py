import logging

class LogConfig:
    """
    Eine Klasse zum Konfigurieren und Erstellen von Loggern für verschiedene Logdateien.
    """
     
    def __init__(self):
        """
        Initialisiert eine Instanz der LogConfig-Klasse.
        """
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    def setup_logger(self, name, log_file, level=logging.INFO):
        """
        Konfiguriert und erstellt einen Logger für eine spezifizierte Logdatei.

        Args:
            name (str): Der Name des Loggers.
            log_file (str): Der Dateiname der Logdatei, in die die Logeinträge geschrieben werden.
            level (int, optional): Das Level des Loggers (Standard: logging.INFO).

        Returns:
            logging.Logger: Ein konfigurierter Logger für die angegebene Logdatei.
        """
        handler = logging.FileHandler(log_file)
        handler.setFormatter(self.formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger