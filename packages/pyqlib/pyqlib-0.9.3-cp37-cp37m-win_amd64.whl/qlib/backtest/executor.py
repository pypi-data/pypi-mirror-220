from __future__ import annotations

import copy
from abc import abstractmethod
from collections import defaultdict
from types import GeneratorType
from typing import Any, Dict, Generator, List, Tuple, Union, cast

import pandas as pd

from qlib.backtest.account import Account
from qlib.backtest.position import BasePosition
from qlib.log import get_module_logger

from ..strategy.base import BaseStrategy
from ..utils import init_instance_by_config
from .decision import BaseTradeDecision, Order
from .exchange import Exchange
from .utils import CommonInfrastructure, LevelInfrastructure, TradeCalendarManager, get_start_end_idx


class BaseExecutor:
    """Base executor for trading"""

    def __init__(
        self,
        time_per_step: str,
        start_time: Union[str, pd.Timestamp] = None,
        end_time: Union[str, pd.Timestamp] = None,
        indicator_config: dict = {},
        generate_portfolio_metrics: bool = False,
        verbose: bool = False,
        track_data: bool = False,
        trade_exchange: Exchange | None = None,
        common_infra: CommonInfrastructure | None = None,
        settle_type: str = BasePosition.ST_NO,
        **kwargs: Any,
    ) -> None:
        """
        Parameters
        ----------
        time_per_step : str
            trade time per trading step, used for generate the trade calendar
        show_indicator: bool, optional
            whether to show indicators, :
            - 'pa', the price advantage
            - 'pos', the positive rate
            - 'ffr', the fulfill rate
        indicator_config: dict, optional
            config for calculating trade indicator, including the following fields:
            - 'show_indicator': whether to show indicators, optional, default by False. The indicators includes
                - 'pa', the price advantage
                - 'pos', the positive rate
                - 'ffr', the fulfill rate
            - 'pa_config': config for calculating price advantage(pa), optional
                - 'base_price': the based price than which the trading price is advanced, Optional, default by 'twap'
                    - If 'base_price' is 'twap', the based price is the time weighted average price
                    - If 'base_price' is 'vwap', the based price is the volume weighted average price
                - 'weight_method': weighted method when calculating total trading pa by different orders' pa in each
                    step, optional, default by 'mean'
                    - If 'weight_method' is 'mean', calculating mean value of different orders' pa
                    - If 'weight_method' is 'amount_weighted', calculating amount weighted average value of different
                        orders' pa
                    - If 'weight_method' is 'value_weighted', calculating value weighted average value of different
                        orders' pa
            - 'ffr_config': config for calculating fulfill rate(ffr), optional
                - 'weight_method': weighted method when calculating total trading ffr by different orders' ffr in each
                    step, optional, default by 'mean'
                    - If 'weight_method' is 'mean', calculating mean value of different orders' ffr
                    - If 'weight_method' is 'amount_weighted', calculating amount weighted average value of different
                        orders' ffr
                    - If 'weight_method' is 'value_weighted', calculating value weighted average value of different
                        orders' ffr
            Example:
                {
                    'show_indicator': True,
                    'pa_config': {
                        "agg": "twap",  # "vwap"
                        "price": "$close", # default to use deal price of the exchange
                    },
                    'ffr_config':{
                        'weight_method': 'value_weighted',
                    }
                }
        generate_portfolio_metrics : bool, optional
            whether to generate portfolio_metrics, by default False
        verbose : bool, optional
            whether to print trading info, by default False
        track_data : bool, optional
            whether to generate trade_decision, will be used when training rl agent
            - If `self.track_data` is true, when making data for training, the input `trade_decision` of `execute` will
                be generated by `collect_data`
            - Else,  `trade_decision` will not be generated

        trade_exchange : Exchange
            exchange that provides market info, used to generate portfolio_metrics
            - If generate_portfolio_metrics is None, trade_exchange will be ignored
            - Else If `trade_exchange` is None, self.trade_exchange will be set with common_infra

        common_infra : CommonInfrastructure, optional:
            common infrastructure for backtesting, may including:
            - trade_account : Account, optional
                trade account for trading
            - trade_exchange : Exchange, optional
                exchange that provides market info

        settle_type : str
            Please refer to the docs of BasePosition.settle_start
        """
        self.time_per_step = time_per_step
        self.indicator_config = indicator_config
        self.generate_portfolio_metrics = generate_portfolio_metrics
        self.verbose = verbose
        self.track_data = track_data
        self._trade_exchange = trade_exchange
        self.level_infra = LevelInfrastructure()
        self.level_infra.reset_infra(common_infra=common_infra, executor=self)
        self._settle_type = settle_type
        self.reset(start_time=start_time, end_time=end_time, common_infra=common_infra)
        if common_infra is None:
            get_module_logger("BaseExecutor").warning(f"`common_infra` is not set for {self}")

        # record deal order amount in one day
        self.dealt_order_amount: Dict[str, float] = defaultdict(float)
        self.deal_day = None

    def reset_common_infra(self, common_infra: CommonInfrastructure, copy_trade_account: bool = False) -> None:
        """
        reset infrastructure for trading
            - reset trade_account
        """
        if not hasattr(self, "common_infra"):
            self.common_infra = common_infra
        else:
            self.common_infra.update(common_infra)

        self.level_infra.reset_infra(common_infra=self.common_infra)

        if common_infra.has("trade_account"):
            # NOTE: there is a trick in the code.
            # shallow copy is used instead of deepcopy.
            # 1. So positions are shared
            # 2. Others are not shared, so each level has it own metrics (portfolio and trading metrics)
            self.trade_account: Account = (
                copy.copy(common_infra.get("trade_account"))
                if copy_trade_account
                else common_infra.get("trade_account")
            )
            self.trade_account.reset(freq=self.time_per_step, port_metr_enabled=self.generate_portfolio_metrics)

    @property
    def trade_exchange(self) -> Exchange:
        """get trade exchange in a prioritized order"""
        return getattr(self, "_trade_exchange", None) or self.common_infra.get("trade_exchange")

    @property
    def trade_calendar(self) -> TradeCalendarManager:
        """
        Though trade calendar can be accessed from multiple sources, but managing in a centralized way will make the
        code easier
        """
        return self.level_infra.get("trade_calendar")

    def reset(self, common_infra: CommonInfrastructure | None = None, **kwargs: Any) -> None:
        """
        - reset `start_time` and `end_time`, used in trade calendar
        - reset `common_infra`, used to reset `trade_account`, `trade_exchange`, .etc
        """

        if "start_time" in kwargs or "end_time" in kwargs:
            start_time = kwargs.get("start_time")
            end_time = kwargs.get("end_time")
            self.level_infra.reset_cal(freq=self.time_per_step, start_time=start_time, end_time=end_time)
        if common_infra is not None:
            self.reset_common_infra(common_infra)

    def get_level_infra(self) -> LevelInfrastructure:
        return self.level_infra

    def finished(self) -> bool:
        return self.trade_calendar.finished()

    def execute(self, trade_decision: BaseTradeDecision, level: int = 0) -> List[object]:
        """execute the trade decision and return the executed result

        NOTE: this function is never used directly in the framework. Should we delete it?

        Parameters
        ----------
        trade_decision : BaseTradeDecision

        level : int
            the level of current executor

        Returns
        ----------
        execute_result : List[object]
            the executed result for trade decision
        """
        return_value: dict = {}
        for _decision in self.collect_data(trade_decision, return_value=return_value, level=level):
            pass
        return cast(list, return_value.get("execute_result"))

    @abstractmethod
    def _collect_data(
        self,
        trade_decision: BaseTradeDecision,
        level: int = 0,
    ) -> Union[Generator[Any, Any, Tuple[List[object], dict]], Tuple[List[object], dict]]:
        """
        Please refer to the doc of collect_data
        The only difference between `_collect_data` and `collect_data` is that some common steps are moved into
        collect_data

        Parameters
        ----------
        Please refer to the doc of collect_data


        Returns
        -------
        Tuple[List[object], dict]:
            (<the executed result for trade decision>, <the extra kwargs for `self.trade_account.update_bar_end`>)
        """

    def collect_data(
        self,
        trade_decision: BaseTradeDecision,
        return_value: dict | None = None,
        level: int = 0,
    ) -> Generator[Any, Any, List[object]]:
        """Generator for collecting the trade decision data for rl training

        his function will make a step forward

        Parameters
        ----------
        trade_decision : BaseTradeDecision

        level : int
            the level of current executor. 0 indicates the top level

        return_value : dict
            the mem address to return the value
            e.g.  {"return_value": <the executed result>}

        Returns
        ----------
        execute_result : List[object]
            the executed result for trade decision.
            ** NOTE!!!! **:
            1) This is necessary,  The return value of generator will be used in NestedExecutor
            2) Please note the executed results are not merged.

        Yields
        -------
        object
            trade decision
        """

        if self.track_data:
            yield trade_decision

        atomic = not issubclass(self.__class__, NestedExecutor)  # issubclass(A, A) is True

        if atomic and trade_decision.get_range_limit(default_value=None) is not None:
            raise ValueError("atomic executor doesn't support specify `range_limit`")

        if self._settle_type != BasePosition.ST_NO:
            self.trade_account.current_position.settle_start(self._settle_type)

        obj = self._collect_data(trade_decision=trade_decision, level=level)

        if isinstance(obj, GeneratorType):
            yield_res = yield from obj
            assert isinstance(yield_res, tuple) and len(yield_res) == 2
            res, kwargs = yield_res
        else:
            # Some concrete executor don't have inner decisions
            res, kwargs = obj

        trade_start_time, trade_end_time = self.trade_calendar.get_step_time()
        # Account will not be changed in this function
        self.trade_account.update_bar_end(
            trade_start_time,
            trade_end_time,
            self.trade_exchange,
            atomic=atomic,
            outer_trade_decision=trade_decision,
            indicator_config=self.indicator_config,
            **kwargs,
        )

        self.trade_calendar.step()

        if self._settle_type != BasePosition.ST_NO:
            self.trade_account.current_position.settle_commit()

        if return_value is not None:
            return_value.update({"execute_result": res})

        return res

    def get_all_executors(self) -> List[BaseExecutor]:
        """get all executors"""
        return [self]


class NestedExecutor(BaseExecutor):
    """
    Nested Executor with inner strategy and executor
    - At each time `execute` is called, it will call the inner strategy and executor to execute the `trade_decision`
        in a higher frequency env.
    """

    def __init__(
        self,
        time_per_step: str,
        inner_executor: Union[BaseExecutor, dict],
        inner_strategy: Union[BaseStrategy, dict],
        start_time: Union[str, pd.Timestamp] = None,
        end_time: Union[str, pd.Timestamp] = None,
        indicator_config: dict = {},
        generate_portfolio_metrics: bool = False,
        verbose: bool = False,
        track_data: bool = False,
        skip_empty_decision: bool = True,
        align_range_limit: bool = True,
        common_infra: CommonInfrastructure | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Parameters
        ----------
        inner_executor : BaseExecutor
            trading env in each trading bar.
        inner_strategy : BaseStrategy
            trading strategy in each trading bar
        skip_empty_decision: bool
            Will the executor skip call inner loop when the decision is empty.
            It should be False in following cases
            - The decisions may be updated by steps
            - The inner executor may not follow the decisions from the outer strategy
        align_range_limit: bool
            force to align the trade_range decision
            It is only for nested executor, because range_limit is given by outer strategy
        """
        self.inner_executor: BaseExecutor = init_instance_by_config(
            inner_executor,
            common_infra=common_infra,
            accept_types=BaseExecutor,
        )
        self.inner_strategy: BaseStrategy = init_instance_by_config(
            inner_strategy,
            common_infra=common_infra,
            accept_types=BaseStrategy,
        )

        self._skip_empty_decision = skip_empty_decision
        self._align_range_limit = align_range_limit

        super(NestedExecutor, self).__init__(
            time_per_step=time_per_step,
            start_time=start_time,
            end_time=end_time,
            indicator_config=indicator_config,
            generate_portfolio_metrics=generate_portfolio_metrics,
            verbose=verbose,
            track_data=track_data,
            common_infra=common_infra,
            **kwargs,
        )

    def reset_common_infra(self, common_infra: CommonInfrastructure, copy_trade_account: bool = False) -> None:
        """
        reset infrastructure for trading
            - reset inner_strategy and inner_executor common infra
        """
        # NOTE: please refer to the docs of BaseExecutor.reset_common_infra for the meaning of `copy_trade_account`

        # The first level follow the `copy_trade_account` from the upper level
        super(NestedExecutor, self).reset_common_infra(common_infra, copy_trade_account=copy_trade_account)

        # The lower level have to copy the trade_account
        self.inner_executor.reset_common_infra(common_infra, copy_trade_account=True)
        self.inner_strategy.reset_common_infra(common_infra)

    def _init_sub_trading(self, trade_decision: BaseTradeDecision) -> None:
        trade_start_time, trade_end_time = self.trade_calendar.get_step_time()
        self.inner_executor.reset(start_time=trade_start_time, end_time=trade_end_time)
        sub_level_infra = self.inner_executor.get_level_infra()
        self.level_infra.set_sub_level_infra(sub_level_infra)
        self.inner_strategy.reset(level_infra=sub_level_infra, outer_trade_decision=trade_decision)

    def _update_trade_decision(self, trade_decision: BaseTradeDecision) -> BaseTradeDecision:
        # outer strategy have chance to update decision each iterator
        updated_trade_decision = trade_decision.update(self.inner_executor.trade_calendar)
        if updated_trade_decision is not None:  # TODO: always is None for now?
            trade_decision = updated_trade_decision
            # NEW UPDATE
            # create a hook for inner strategy to update outer decision
            trade_decision = self.inner_strategy.alter_outer_trade_decision(trade_decision)
        return trade_decision

    def _collect_data(
        self,
        trade_decision: BaseTradeDecision,
        level: int = 0,
    ) -> Generator[Any, Any, Tuple[List[object], dict]]:
        execute_result = []
        inner_order_indicators = []
        decision_list = []
        # NOTE:
        # - this is necessary to calculating the steps in sub level
        # - more detailed information will be set into trade decision
        self._init_sub_trading(trade_decision)

        _inner_execute_result = None
        while not self.inner_executor.finished():
            trade_decision = self._update_trade_decision(trade_decision)

            if trade_decision.empty() and self._skip_empty_decision:
                # give one chance for outer strategy to update the strategy
                # - For updating some information in the sub executor (the strategy have no knowledge of the inner
                #   executor when generating the decision)
                break

            sub_cal: TradeCalendarManager = self.inner_executor.trade_calendar

            # NOTE: make sure get_start_end_idx is after `self._update_trade_decision`
            start_idx, end_idx = get_start_end_idx(sub_cal, trade_decision)
            if not self._align_range_limit or start_idx <= sub_cal.get_trade_step() <= end_idx:
                # if force align the range limit, skip the steps outside the decision range limit

                res = self.inner_strategy.generate_trade_decision(_inner_execute_result)

                # NOTE: !!!!!
                # the two lines below is for a special case in RL
                # To solve the conflicts below
                # - Normally, user will create a strategy and embed it into Qlib's executor and simulator interaction
                #   loop For a _nested qlib example_, (Qlib Strategy) <=> (Qlib Executor[(inner Qlib Strategy) <=>
                #   (inner Qlib Executor)])
                # - However, RL-based framework has it's own script to run the loop
                #   For an _RL learning example_, (RL Policy) <=> (RL Env[(inner Qlib Executor)])
                # To make it possible to run  _nested qlib example_ and _RL learning example_ together, the solution
                # below is proposed
                # - The entry script follow the example of  _RL learning example_ to be compatible with all kinds of
                #   RL Framework
                # - Each step of (RL Env) will make (inner Qlib Executor) one step forward
                #     - (inner Qlib Strategy) is a proxy strategy, it will give the program control right to (RL Env)
                #       by `yield from` and wait for the action from the policy
                # So the two lines below is the implementation of yielding control rights
                if isinstance(res, GeneratorType):
                    res = yield from res

                _inner_trade_decision: BaseTradeDecision = res

                trade_decision.mod_inner_decision(_inner_trade_decision)  # propagate part of decision information

                # NOTE sub_cal.get_step_time() must be called before collect_data in case of step shifting
                decision_list.append((_inner_trade_decision, *sub_cal.get_step_time()))

                # NOTE: Trade Calendar will step forward in the follow line
                _inner_execute_result = yield from self.inner_executor.collect_data(
                    trade_decision=_inner_trade_decision,
                    level=level + 1,
                )
                assert isinstance(_inner_execute_result, list)
                self.post_inner_exe_step(_inner_execute_result)
                execute_result.extend(_inner_execute_result)

                inner_order_indicators.append(
                    self.inner_executor.trade_account.get_trade_indicator().get_order_indicator(raw=True),
                )
            else:
                # do nothing and just step forward
                sub_cal.step()

        # Let inner strategy know that the outer level execution is done.
        self.inner_strategy.post_upper_level_exe_step()

        return execute_result, {"inner_order_indicators": inner_order_indicators, "decision_list": decision_list}

    def post_inner_exe_step(self, inner_exe_res: List[object]) -> None:
        """
        A hook for doing sth after each step of inner strategy

        Parameters
        ----------
        inner_exe_res :
            the execution result of inner task
        """
        self.inner_strategy.post_exe_step(inner_exe_res)

    def get_all_executors(self) -> List[BaseExecutor]:
        """get all executors, including self and inner_executor.get_all_executors()"""
        return [self, *self.inner_executor.get_all_executors()]


def _retrieve_orders_from_decision(trade_decision: BaseTradeDecision) -> List[Order]:
    """
    IDE-friendly helper function.
    """
    decisions = trade_decision.get_decision()
    orders: List[Order] = []
    for decision in decisions:
        assert isinstance(decision, Order)
        orders.append(decision)
    return orders


class SimulatorExecutor(BaseExecutor):
    """Executor that simulate the true market"""

    # TODO: TT_SERIAL & TT_PARAL will be replaced by feature fix_pos now.
    # Please remove them in the future.

    # available trade_types
    TT_SERIAL = "serial"
    # The orders will be executed serially in a sequence
    # In each trading step, it is possible that users sell instruments first and use the money to buy new instruments
    TT_PARAL = "parallel"
    # The orders will be executed in parallel
    # In each trading step, if users try to sell instruments first and buy new instruments with money, failure will
    # occur

    def __init__(
        self,
        time_per_step: str,
        start_time: Union[str, pd.Timestamp] = None,
        end_time: Union[str, pd.Timestamp] = None,
        indicator_config: dict = {},
        generate_portfolio_metrics: bool = False,
        verbose: bool = False,
        track_data: bool = False,
        common_infra: CommonInfrastructure | None = None,
        trade_type: str = TT_SERIAL,
        **kwargs: Any,
    ) -> None:
        """
        Parameters
        ----------
        trade_type: str
            please refer to the doc of `TT_SERIAL` & `TT_PARAL`
        """
        super(SimulatorExecutor, self).__init__(
            time_per_step=time_per_step,
            start_time=start_time,
            end_time=end_time,
            indicator_config=indicator_config,
            generate_portfolio_metrics=generate_portfolio_metrics,
            verbose=verbose,
            track_data=track_data,
            common_infra=common_infra,
            **kwargs,
        )

        self.trade_type = trade_type

    def _get_order_iterator(self, trade_decision: BaseTradeDecision) -> List[Order]:
        """

        Parameters
        ----------
        trade_decision : BaseTradeDecision
            the trade decision given by the strategy

        Returns
        -------
        List[Order]:
            get a list orders according to `self.trade_type`
        """
        orders = _retrieve_orders_from_decision(trade_decision)

        if self.trade_type == self.TT_SERIAL:
            # Orders will be traded in a parallel way
            order_it = orders
        elif self.trade_type == self.TT_PARAL:
            # NOTE: !!!!!!!
            # Assumption: there will not be orders in different trading direction in a single step of a strategy !!!!
            # The parallel trading failure will be caused only by the conflicts of money
            # Therefore, make the buying go first will make sure the conflicts happen.
            # It equals to parallel trading after sorting the order by direction
            order_it = sorted(orders, key=lambda order: -order.direction)
        else:
            raise NotImplementedError(f"This type of input is not supported")
        return order_it

    def _collect_data(self, trade_decision: BaseTradeDecision, level: int = 0) -> Tuple[List[object], dict]:
        trade_start_time, _ = self.trade_calendar.get_step_time()
        execute_result: list = []

        for order in self._get_order_iterator(trade_decision):
            # Each time we move into a new date, clear `self.dealt_order_amount` since it only maintains intraday
            # information.
            now_deal_day = self.trade_calendar.get_step_time()[0].floor(freq="D")
            if self.deal_day is None or now_deal_day > self.deal_day:
                self.dealt_order_amount = defaultdict(float)
                self.deal_day = now_deal_day

            # execute the order.
            # NOTE: The trade_account will be changed in this function
            trade_val, trade_cost, trade_price = self.trade_exchange.deal_order(
                order,
                trade_account=self.trade_account,
                dealt_order_amount=self.dealt_order_amount,
            )
            execute_result.append((order, trade_val, trade_cost, trade_price))

            self.dealt_order_amount[order.stock_id] += order.deal_amount

            if self.verbose:
                print(
                    "[I {:%Y-%m-%d %H:%M:%S}]: {} {}, price {:.2f}, amount {}, deal_amount {}, factor {}, "
                    "value {:.2f}, cash {:.2f}.".format(
                        trade_start_time,
                        "sell" if order.direction == Order.SELL else "buy",
                        order.stock_id,
                        trade_price,
                        order.amount,
                        order.deal_amount,
                        order.factor,
                        trade_val,
                        self.trade_account.get_cash(),
                    ),
                )
        return execute_result, {"trade_info": execute_result}
