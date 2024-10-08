from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import QtWidgets

from ..engine import (
    PaperEngine,
    APP_NAME,
)


class PaperManager(QtWidgets.QWidget):
    """"""

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        """"""
        super().__init__()

        self.main_engine: MainEngine = main_engine
        self.event_engine: EventEngine = event_engine

        self.paper_engine: PaperEngine = main_engine.get_engine(APP_NAME)

        self.init_ui()

    def init_ui(self) -> None:
        """"""
        self.setWindowTitle("Paper Trading")
        self.setFixedHeight(200)
        self.setFixedWidth(500)

        interval_spin: QtWidgets.QSpinBox = QtWidgets.QSpinBox()
        interval_spin.setMinimum(1)
        interval_spin.setValue(self.paper_engine.timer_interval)
        interval_spin.setSuffix(" seconds")
        interval_spin.valueChanged.connect(self.paper_engine.set_timer_interval)

        slippage_spin: QtWidgets.QSpinBox = QtWidgets.QSpinBox()
        slippage_spin.setMinimum(0)
        slippage_spin.setValue(self.paper_engine.trade_slippage)
        slippage_spin.setSuffix(" ticks")
        slippage_spin.valueChanged.connect(self.paper_engine.set_trade_slippage)

        instant_check: QtWidgets.QCheckBox = QtWidgets.QCheckBox()
        instant_check.setChecked(self.paper_engine.instant_trade)
        instant_check.stateChanged.connect(self.paper_engine.set_instant_trade)

        clear_button: QtWidgets.QPushButton = QtWidgets.QPushButton(
            "Liquidate all positions"
        )
        clear_button.clicked.connect(self.paper_engine.clear_position)
        clear_button.setFixedHeight(clear_button.sizeHint().height() * 2)

        form: QtWidgets.QFormLayout = QtWidgets.QFormLayout()
        form.addRow("Market and stop orders and turnover slippage", slippage_spin)
        form.addRow(
            "Calculation of the frequency of simulation trading position profit and loss",
            interval_spin,
        )
        form.addRow(
            "Order immediately after the use of the current market summarization",
            instant_check,
        )
        form.addRow(clear_button)

        vbox: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(form)
        vbox.addStretch()
        self.setLayout(vbox)
