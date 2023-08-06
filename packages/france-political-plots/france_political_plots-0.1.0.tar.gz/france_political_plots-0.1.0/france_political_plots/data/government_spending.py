import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import eurostat as eust
import numpy as np

from typing import Self, Dict, List, Any, Literal, Union

DEFAULTS=['FR', 'DE', 'ES', 'DK', 'NO', 'IT']


def add_layout(fig: go.Figure, width: int = 500, height: int = 500):
    return fig.update_layout(autosize=True, margin=dict(
            pad=4
        ))

class GovernmentSpending:
    def __new__(cls) -> Self:
        cls.data = eust.get_data("GOV_10A_MAIN")
        cols = cls.data[0]
        rows = cls.data[1:]

        _df = pd.DataFrame(rows, columns=cols)
        df = _df[(_df.unit == 'MIO_EUR') & (_df.sector == 'S13')]\
            .drop(columns=['freq', 'na_item', 'sector', 'unit'])\
            .rename(columns={'geo\TIME_PERIOD':'code'})\
            .melt(id_vars='code', var_name='year', value_name='spending')
        
        df.year = pd.to_datetime(df.year)
        cls.codes = pd.read_csv("https://gist.githubusercontent.com/arnos-stuff/4cdd8c4ba2cda5060a8864a29272d90a/raw/88359a24fcd3e9a6d2c5aca3cd05e7b292d2b4af/Full_Items_List_EN.txt", sep='\t')
        url_geo = cls.codes.loc[cls.codes.Code == 'GEO', 'Specific tsv download url'].values.tolist().pop()

        cls.geos = pd.read_csv(url_geo, sep='\t', header=None)
        cls.df = pd.merge(df, cls.geos, left_on='code', right_on=0).rename(columns={0:'code_copy',1:'country'}).drop(columns='code_copy')
        cls.simple = cls.df.fillna(0).groupby(['code', 'country', 'year']).sum().reset_index()
        cls.example = None
        return cls
        
    @classmethod
    def examples(
        cls,
        examples:List[str] | None = None,
        start_year:int = 2000
        ) -> pd.DataFrame:
        if not examples:
            examples = DEFAULTS
        cls.example = cls.simple[(cls.simple.code.isin(['FR', 'DE', 'ES', 'DK', 'NO', 'IT'])) & (cls.simple.year > pd.to_datetime(f"{start_year}-01-01"))].copy()
        cls.example = cls.example[['code', 'country', 'year', 'spending']].groupby(['code', 'country', 'year',]).sum().reset_index()
        years = cls.example.year.unique().tolist()
        for country in cls.example.country.unique():
            ex_filter =  cls.example[cls.example.country == country].copy()
            gap = ex_filter.sort_values('year').spending.diff(periods=-1)
            cls.example.loc[cls.example.country == country, 'yearly_delta'] = gap.copy()
            cls.example.loc[cls.example.country == country, 'yearly_gap'] = gap.copy() / ex_filter.spending
            
        cls.example['year_lag'] = (pd.to_datetime('01-01-2023') - cls.example.year).dt.total_seconds() / 60 / 60 / 24 / 365
        cls.example['opacity'] = 1 - 0.5*(cls.example.year_lag -  cls.example.year_lag.min() ) / (cls.example.year_lag.max() - cls.example.year_lag.min())
        cls.example.spending *= 10**6
        return cls.example
    
    @classmethod
    def add_lfi_melenchon(cls):
        year_max = cls.example[
            (~cls.example.spending.isna()) &
            (cls.example.country == 'France')
            ]\
            .year.max()
        ref = cls.example[
            (cls.example.country == 'France') & 
            (cls.example.year < year_max) &
            (~cls.example.spending.isna())
            ].copy()
        ref_row = ref.sort_values('year').iloc[-1].copy()
        ref_spending = ref_row.spending
        ref_year = ref_row.year
        
        target_row = ref.sort_values('year').iloc[-2].copy()
        target_spending = target_row.spending
        target_year = target_row.year
        slope = (target_spending - ref_spending)/((target_year - ref_year).total_seconds() / 60 / 60 / 24 / 365 )
        gap = np.abs(target_spending - ref_spending)
        lfis = [
            ref.iloc[[-1]].copy() for _ in range(5)
            ]
        for i,l in enumerate(lfis):
            l.year = pd.to_datetime(f"{2022 + i}-01-01")
            l.spending += slope * i + gap
            l.country = 'France (LFI 2022)'
            l.yearly_delta += 250*10**9
            l.yearly_gap = (l.yearly_delta - l.spending)/l.spending
            l.spending += l.yearly_delta
        
        ex_lfis = pd.concat([cls.example, *lfis], axis=0)
        
        return ex_lfis
   
    @classmethod
    def spending_change(
        cls,
        kind: Union[Literal['scatter'], Literal['line'], Literal['bar']] = 'scatter',
        width: int = 500,
        height: int = 500,
        ) -> List[go.Figure]:
        if cls.example is None:
            cls.examples()
        if kind == 'scatter':
            before = px.scatter(
                cls.example, x='yearly_delta', y='yearly_gap',
                color='country', marginal_x='violin', marginal_y='violin',
                template='plotly_white', opacity=cls.example.opacity,
                size=[1 for _ in cls.example.index], size_max=15,
                log_x=True, log_y=True
                )
            ex_lfi = cls.add_lfi_melenchon()
            after = px.scatter(
                ex_lfi, x='yearly_delta', y='yearly_gap',
                color='country', marginal_x='violin', marginal_y='violin',
                template='plotly_white', opacity=cls.example.opacity, size=[1 for _ in ex_lfi.index[:-1]]+[3], size_max=15,
                log_x=True, log_y=True
                )
            
        if kind == 'line':
            cls.example = cls.example.sort_values('year')
            before = px.scatter(
                cls.example, x='year', y='spending',
                color='country',
                template='plotly_white',
                trendline='lowess',
                trendline_options=dict(frac=0.2)
                )
            ex_lfi = cls.add_lfi_melenchon()
            ex_lfi = ex_lfi.sort_values('year')
            after = px.scatter(
                ex_lfi, x='year', y='spending',
                color='country',
                template='plotly_white',
                trendline='lowess',
                trendline_options=dict(frac=0.2)
                )
            
        before = add_layout(before, width, height)
        after = add_layout(after, width, height)
        return [before, after]