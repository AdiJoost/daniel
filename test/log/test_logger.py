import unittest
from unittest.mock import mock_open, patch
from log.logger import Logger
from log.logLevel import LogLevel

class TestLogger(unittest.TestCase):

    def test_debug_LogLevelLow_logs(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.DEBUG)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.debug("Hello")

        #ASSERT
        mockOpen().write.assert_called_once()

    def test_debug_LogLevelHigh__doesNotLog(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.INFO)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.debug("Hello")

        #ASSERT
        mockOpen().write.assert_not_called()

    @patch("builtins.print")
    def test_debug_chattyLevelLow_prints(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.DEBUG)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.debug("Hello")

        #ASSERT
        mockPrint.assert_called_once()

    @patch("builtins.print")
    def test_debug_chattyLevelHigh_doesNotPrint(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.INFO)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.debug("Hello")

        #ASSERT
        mockPrint.assert_not_called()

    def test_info_LogLevelLow_logs(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.DEBUG)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.info("Hello")

        #ASSERT
        mockOpen().write.assert_called_once()

    def test_info_LogLevelequals_logs(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.INFO)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.info("Hello")

        #ASSERT
        mockOpen().write.assert_called_once()

    def test_info_LogLevelHigh__doesNotLog(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.WARN)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.info("Hello")

        #ASSERT
        mockOpen().write.assert_not_called()

    @patch("builtins.print")
    def test_info_chattyLevelLow_prints(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.DEBUG)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.info("Hello")

        #ASSERT
        mockPrint.assert_called_once()

    @patch("builtins.print")
    def test_info_chattyLevelEqual_prints(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.INFO)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.info("Hello")

        #ASSERT
        mockPrint.assert_called_once()

    @patch("builtins.print")
    def test_info_chattyLevelHigh_doesNotPrint(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.WARN)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.info("Hello")

        #ASSERT
        mockPrint.assert_not_called()

    def test_warn_LogLevelLow_logs(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.INFO)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.warn("Hello")

        #ASSERT
        mockOpen().write.assert_called_once()

    def test_warn_LogLevelEquals_logs(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.WARN)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.warn("Hello")

        #ASSERT
        mockOpen().write.assert_called_once()

    def test_warn_LogLevelHigh__doesNotLog(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.ERROR)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.warn("Hello")

        #ASSERT
        mockOpen().write.assert_not_called()

    @patch("builtins.print")
    def test_warn_chattyLevelLow_prints(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.INFO)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.warn("Hello")

        #ASSERT
        mockPrint.assert_called_once()

    @patch("builtins.print")
    def test_warn_chattyLevelEqual_prints(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.WARN)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.warn("Hello")

        #ASSERT
        mockPrint.assert_called_once()

    @patch("builtins.print")
    def test_warn_chattyLevelHigh_doesNotPrint(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.ERROR)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.warn("Hello")

        #ASSERT
        mockPrint.assert_not_called()

    def test_error_LogLevelLow_logs(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.WARN)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.error("Hello")

        #ASSERT
        mockOpen().write.assert_called_once()

    def test_error_LogLevelEquals_logs(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.ERROR)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.error("Hello")

        #ASSERT
        mockOpen().write.assert_called_once()

    def test_error_LogLevelHigh__doesNotLog(self):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setLogLevel(LogLevel.OFF)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.error("Hello")

        #ASSERT
        mockOpen().write.assert_not_called()

    @patch("builtins.print")
    def test_error_chattyLevelLow_prints(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.WARN)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.error("Hello")

        #ASSERT
        mockPrint.assert_called_once()

    @patch("builtins.print")
    def test_error_chattyLevelEqual_prints(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.ERROR)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.error("Hello")

        #ASSERT
        mockPrint.assert_called_once()

    @patch("builtins.print")
    def test_error_chattyLevelHigh_doesNotPrint(self, mockPrint):
        #ARRANGE
        mockOpen = mock_open()
        Logger.setChattyLevel(LogLevel.OFF)
        logger = Logger()


        #ACT
        with patch("builtins.open", mockOpen):
            logger.error("Hello")

        #ASSERT
        mockPrint.assert_not_called()