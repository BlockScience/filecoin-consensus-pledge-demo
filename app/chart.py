from abc import ABC, abstractclassmethod

import plotly.express as px
import streamlit as st

from utils import load_constants


C = CONSTANTS = load_constants()


class PlotlyChart(ABC):
    def __init__(self, chart, use_container_width=True):
        self.chart = st.plotly_chart(
            chart, use_container_width=use_container_width)

    @abstractclassmethod
    def build(cls):
        raise NotImplementedError

    @staticmethod
    def compose_x_domain(num_steps):
        return (
            C["days_after_launch"] / C["days_per_year"],
            (C["days_after_launch"] + num_steps *
             C["days_per_step"]) / C["days_per_year"],
        )


class NetworkPowerPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        chart = px.line(
            df,
            x="years_passed",
            y=["power_rb", "baseline"],
            title="RB Network Power vs. Time",
            labels={
                "years_passed": "Year",
                "value": "Raw Bytes Network Power (RB PiB)",
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(0, 50_000),
            log_y=True,
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        return cls(chart)


class QAPowerPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        chart = px.line(
            df,
            x="years_passed",
            y='power_qa',
            title="QA Power vs. Time",
            labels={
                "years_passed": "Year",
                "power_qa": "QA Network Power (QA PiB)",
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(0, 150_000),
            log_y=True,
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        return cls(chart)

        return cls(chart)


class EffectiveNetworkTimePlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        chart = px.line(
            df,
            x="years_passed",
            y="effective_network_time",
            color="scenario",
            title="Effective Network Time vs. Time",
            labels={
                "years_passed": "Year",
                "effective_network_time": "Effective Network Time (Years)",
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(2.5, 4.5),
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        return cls(chart)


class RewardPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        fig_df = df.melt(id_vars=['years_passed'], value_vars=['daily_simple_reward', 'daily_baseline_reward'])
        chart = px.line(
            fig_df,
            x="years_passed",
            y="value",
            color='variable',
            title="Reward vs. Time",
            labels={
                "years_passed": "Year",
                "value": "Daily FIL",
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(60_000, 100_0000),
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        chart.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5))
        return cls(chart)
    
class RewardPerPowerPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        fig_df = df.melt(id_vars=['years_passed'], value_vars=['daily_reward_per_rbp', 'daily_reward_per_qap'])
        chart = px.line(
            fig_df,
            x="years_passed",
            y="value",
            color='variable',
            title="Reward per PiB vs. Time",
            labels={
                "years_passed": "Year",
                "value": "Daily FIL per PiB",
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(60_000, 100_0000),
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        chart.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5))
        return cls(chart)


class TokenDistributionPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        chart = px.line(
            df,
            x="years_passed",
            y=["fil_circulating",
               'fil_locked'],
            title="Token Distribution - Circulating vs Locked",
            line_dash='scenario',
            labels={
                "years_passed": "Year",
                "value": "FIL"
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(0, 500_000_000),
            # log_y=True,
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        chart.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5))
        return cls(chart)


class TokenLockedDistributionPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        chart = px.line(
            df,
            x="years_passed",
            y=["fil_collateral", "fil_locked_reward"],
            title="Locked Token Distribution - Collateral vs Locked Rewards",
            line_dash='scenario',
            labels={
                "years_passed": "Year",
                "value": "FIL"
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(0, 150_000_000),
            # log_y=True,
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        chart.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5))
        return cls(chart)


class CriticalCostPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        chart = px.line(
            df,
            x="years_passed",
            y="critical_cost",
            title="Critical Cost",
            line_dash='scenario',
            labels={
                "years_passed": "Year",
                "critical_cost": "FIL"
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(0, 40_000_000),
            # log_y=True,
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        chart.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5))
        return cls(chart)


class CirculatingSurplusPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        chart = px.line(
            df,
            x="years_passed",
            y="circulating_surplus",
            title="Circulating Surplus",
            line_dash='scenario',
            labels={
                "years_passed": "Year",
                'circulating_surplus': "Excess Circulating Supply vs Critical Cost"
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(5, 5000),
            log_y=True
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        chart.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5))
        return cls(chart)


class CirculatingSupplyPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):
        chart = px.line(
            df,
            x="years_passed",
            y=["circulating_supply", 'locked_supply'],
            title="Circulating and Locked Supply",
            line_dash='scenario',
            labels={
                "years_passed": "Year",
                "value": "% of Available FIL"
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(0, 1),
        )
        chart.update_yaxes(tickformat=".0%")
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        chart.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5))
        return cls(chart)


class OnboardingCollateralPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):

        fig_df = df.melt(id_vars=['years_passed', 'scenario'],
                         value_vars=['initial_pledge_per_new_qa_power',
                                     'storage_pledge_per_new_qa_power',
                                     'consensus_pledge_per_new_qa_power',
                                    ])

        chart = px.line(
            fig_df,
            x="years_passed",
            y="value",
            color='variable',
            line_dash='scenario',
            title="Initial Pledge per QA-PiB",
            labels={
                "years_passed": "Year",
                "value": "FIL per QA-PiB"
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(0, 8_000),
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        chart.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5))
        return cls(chart)


class RBOnboardingCollateralPlotlyChart(PlotlyChart):
    @classmethod
    def build(cls, df, num_steps, vline):

        fig_df = df.melt(id_vars=['years_passed', 'scenario'],
                         value_vars=['initial_pledge_per_new_rb_power',
                                     'storage_pledge_per_new_rb_power',
                                     'consensus_pledge_per_new_rb_power'
                                    ])

        chart = px.line(
            fig_df,
            x="years_passed",
            y="value",
            color='variable',
            line_dash='scenario',
            title="Initial Pledge per RB-PiB",
            labels={
                "years_passed": "Year",
                "value": "FIL per RB-PiB"
            },
            # range_x=cls.compose_x_domain(num_steps),
            #range_y=(0, 8_000),
        )
        for k, v in vline.items():
            chart.add_vline(v, line_dash="dot",   annotation_text=k)
        chart.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5))
        return cls(chart)
