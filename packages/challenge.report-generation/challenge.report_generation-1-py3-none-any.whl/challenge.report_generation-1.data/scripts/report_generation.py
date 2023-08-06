#!python

import argparse
import logging
from itertools import groupby
from typing import NamedTuple

import dateparser
from traceback import print_exc

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime


DESCRIPTION = (
    "Management tool for trades report generation. Two arguments are mandatory, a --trader_id"
    " and a SQL database URL --. A date in DD/MM/YYYY format can also be provided. "
    "If not given, current date will be taken."
)

# Set up the python logger and create a stream handler for console output
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

Base = declarative_base()


class Trade(Base):
    """
    Database model for the Trade objects
    """

    __tablename__ = "trades"
    id = Column(String(50), primary_key=True)
    price = Column(Integer)
    quantity = Column(Integer)
    direction = Column(String(50))
    delivery_day = Column(Date)
    delivery_hour = Column(Integer)
    trader_id = Column(String(50))
    execution_time = Column(DateTime, default=datetime.datetime.utcnow)


def parse_args():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
    )
    parser.add_argument(
        "--date",
        type=dateparser.parse,
        default=datetime.date.today(),
        help="Date for PnL calculation, if none given, current date will be taken",
    )
    parser.add_argument(
        "--trader-id",
        type=str,
        dest="trader_id",
        help="Trader_id for which PnL is calculated",
        required=True,
    )
    parser.add_argument(
        "--SQL-db-url",
        type=str,
        dest="sql_db_url",
        help="SQL URL for database connection",
        required=True,
    )
    args = parser.parse_args()
    return args


def setup_connection(args):
    """
    Function for initialising the engine and session to allow database connections
    via sqlalchemy from the provided SQL database_url.
    """
    database_url = args.sql_db_url
    engine = create_engine(database_url)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    return engine, session


def process(session, args):
    """
    Function which prints out the generated data report.
    """
    license_report = TradesReportingCommand(
        session, date=args.date, trader_id=args.trader_id
    )
    license_report.provide_report()


class TradesReportingCommand:
    def __init__(self, session, date, trader_id):
        self._session = session
        self._date = date
        self._trader_id = trader_id
        self._trades_raw = None
        self._grouped_trades = None
        self._report = []

    def provide_report(self):
        self._check_date_validity()
        self._get_trades()
        if self._trades_raw:
            self._group_data()
            self._process_data()
        self._display_data()

    def _check_date_validity(self):
        if not isinstance(self._date, datetime.date):
            try:
                self._date = dateparser.parse(self._date)
            except Exception:
                logger.error(
                    f"The provided date is invalid. Please provide date in format DD/MM/YYYY"
                )
                raise

    def _get_trades(self):
        try:
            query = (
                self._session.query(Trade)
                .filter(Trade.trader_id == self._trader_id)
                .filter(Trade.delivery_day == self._date)
                .order_by(Trade.delivery_hour)
            )
            self._trades_raw = query.all()
        except AttributeError as e:
            logger.error(
                f"There was an error when fetching the trades from the database, {e}"
            )
            raise
        except OperationalError as e:
            logger.error(
                f"There was an error when connecting to the given database url, {e}"
            )
            raise

    def _group_data(self):
        # The queried trades are grouped per delivery hour
        self._grouped_trades = groupby(
            sorted(self._trades_raw, key=lambda x: x.delivery_hour),
            key=lambda x: x.delivery_hour,
        )

    def _process_data(self):
        self._report.append(
            f"The report data for the given date {str(self._date)} is: \n"
        )
        for delivery_hour, group in self._grouped_trades:
            # The group iterator needs to be stored as a list, because it shares the underlying iterable with groupby().
            # Because the source is shared, when the groupby() object is advanced, the previous group is no longer
            # visible.
            grouped_list = list(group)

            # First, a list of trade tuples is generated, one for each direction
            trade_buy_tuples = calculate_trade_tuples_list(grouped_list, "buy")
            trade_sell_tuples = calculate_trade_tuples_list(grouped_list, "sell")

            # With the previously created list of trades, the total MW quantities and PnL per direction is calculated
            total_buy_quantity = calculate_mw_quantity_from_trade_tuple(
                trade_buy_tuples
            )
            total_buy_pnl = calculate_pnl_from_trade_tuple(trade_buy_tuples)

            total_sell_quantity = calculate_mw_quantity_from_trade_tuple(
                trade_sell_tuples
            )
            total_sell_pnl = calculate_pnl_from_trade_tuple(trade_sell_tuples)

            # The pnl is defined as the difference between the income made selling energy
            # and the cost made buying it for a given hour.
            total_pnl = total_sell_pnl - total_buy_pnl

            # The number of trades can be calculated as the number of trades stored
            # in the trades list, for both directions
            number_of_trades = len(trade_buy_tuples) + len(trade_sell_tuples)

            # Finally, the calculated values are added into the report
            self._report.append(
                f"Hour: {str(delivery_hour)}-{str(delivery_hour+1)}, "
                f"Number of Trades: {str(number_of_trades)}, "
                f"total BUY [MW]: {str(total_buy_quantity)}, "
                f"total SELL [MW]: {str(total_sell_quantity)}, "
                f"PnL [Eur]: {str(total_pnl)} \n"
            )

    def _display_data(self):
        if not self._trades_raw:
            logger.info(
                f"There is no trade activity for the given trader {self._trader_id} for the date {self._date}"
            )
        else:
            logger.info("".join(self._report))


class TradeTuple(NamedTuple):
    quantity: int
    price: int


def calculate_trade_tuples_list(grouped_list_trades, direction: str) -> list:
    """
    For a given direction, it returns a list of all trades, transforming each trade as a NamedTuple,
    with the quantity and price attributes.
    """
    return [
        TradeTuple(quantity=trade.quantity, price=trade.price)
        for trade in grouped_list_trades
        if trade.direction == direction
    ]


def calculate_mw_quantity_from_trade_tuple(trade_tuples: list) -> int:
    """
    From a list of TradeTuple objects, it sums the quantity of all trades.
    """
    return sum(trade_tuple.quantity for trade_tuple in trade_tuples)


def calculate_pnl_from_trade_tuple(trade_tuples: list) -> int:
    """
    From a list of TradeTuple objects, it calculates the sum of PnL of the trades.
    The trade_tuple.price is given in eurocent/MWh, however the desired output of the report is in Euro,
    therefore the division by 100 is necessary.
    """
    return sum(
        trade_tuple.quantity * int(trade_tuple.price) / 100
        for trade_tuple in trade_tuples
    )


def main(args=None):
    try:
        if args is None:
            args = parse_args()
        engine, session = setup_connection(args)
        try:
            process(session, args)
        except Exception:
            raise
    except Exception as e:
        logger.error(
            "An unexpected error occurred:\n{}: {}".format(e.__class__.__name__, e)
        )
        print_exc()
    finally:
        if "session" in globals():
            logger.debug(f"Closing the database connection.")
            session.close()
            engine.dispose()


if __name__ == "__main__":
    main()
