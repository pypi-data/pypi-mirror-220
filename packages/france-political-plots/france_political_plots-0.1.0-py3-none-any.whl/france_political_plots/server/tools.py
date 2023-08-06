from typing import Any
import pandas as pd
import dash_ag_grid as dag
from dash import Dash, Input, Output, dcc, html

__all__ = ["AGGrid"]

FILTERS = {
    "number": {
        "filter": "agNumberColumnFilter",
        "filterParams": {
            "filterOptions": ["equals", "lessThan", "greaterThan"],
            "maxNumConditions": 1,
        },
    },
    "default": {
        "filter": True
    }
}


class AGGrid:
    def __init__(self, df: pd.DataFrame, app: Dash) -> None:
        """Takes a DataFrame as Input and implements a lazy-loading datagrid with search as
        shown in

        Args:
            df (pd.DataFrame): DataFrame to be displayed.
        """
        df = df.reset_index(drop=True)
        df["index"] = df.index

        columnDefs = columnDefs = [
            {
                "field": col,
                "sortable": True,
                "headerName": col,
                **(FILTERS["number"] if isinstance(df[col].iloc[0], (float, int)) else FILTERS['default'])
            }
            for col in df.columns
        ]

        defaultColDef = {
            "flex": 1,
            "minWidth": 150,
            "sortable": True,
            "resizable": True,
            "floatingFilter": True,
        }

        self.grid = html.Div(
            [
                dcc.Markdown("Infinite scroll with sort filter and selection"),
                dag.AgGrid(
                    id="infinite-sort-filter-grid",
                    columnDefs=columnDefs,
                    defaultColDef=defaultColDef,
                    rowModelType="infinite",
                    dashGridOptions={
                        # The number of rows rendered outside the viewable area the grid renders.
                        "rowBuffer": 25,
                        # How many blocks to keep in the store. Default is no limit, so every requested block is kept.
                        "maxBlocksInCache": 2,
                        "cacheBlockSize": 100,
                        "cacheOverflowSize": 2,
                        "maxConcurrentDatasourceRequests": 2,
                        "infiniteInitialRowCount": 100,
                        "rowSelection": "multiple",
                    },
                    getRowId="params.data.index",
                ),
            ],
            style={"margin": 20},
        )


        self.operators = {
            "greaterThanOrEqual": "ge",
            "lessThanOrEqual": "le",
            "lessThan": "lt",
            "greaterThan": "gt",
            "notEqual": "ne",
            "equals": "eq",
        }


        def filter_df(dff, filter_model, col):
            if "filter" in filter_model:
                if filter_model["filterType"] == "date":
                    crit1 = filter_model["dateFrom"]
                    crit1 = pd.Series(crit1).astype(dff[col].dtype)[0]
                    if "dateTo" in filter_model:
                        crit2 = filter_model["dateTo"]
                        crit2 = pd.Series(crit2).astype(dff[col].dtype)[0]
                else:
                    crit1 = filter_model["filter"]
                    crit1 = pd.Series(crit1).astype(dff[col].dtype)[0]
                    if "filterTo" in filter_model:
                        crit2 = filter_model["filterTo"]
                        crit2 = pd.Series(crit2).astype(dff[col].dtype)[0]
            if "type" in filter_model:
                if filter_model["type"] == "contains":
                    dff = dff.loc[dff[col].str.contains(crit1)]
                elif filter_model["type"] == "notContains":
                    dff = dff.loc[~dff[col].str.contains(crit1)]
                elif filter_model["type"] == "startsWith":
                    dff = dff.loc[dff[col].str.startswith(crit1)]
                elif filter_model["type"] == "notStartsWith":
                    dff = dff.loc[~dff[col].str.startswith(crit1)]
                elif filter_model["type"] == "endsWith":
                    dff = dff.loc[dff[col].str.endswith(crit1)]
                elif filter_model["type"] == "notEndsWith":
                    dff = dff.loc[~dff[col].str.endswith(crit1)]
                elif filter_model["type"] == "inRange":
                    if filter_model["filterType"] == "date":
                        dff = dff.loc[
                            dff[col].astype("datetime64[ns]").between_time(crit1, crit2)
                        ]
                    else:
                        dff = dff.loc[dff[col].between(crit1, crit2)]
                elif filter_model["type"] == "blank":
                    dff = dff.loc[dff[col].isnull()]
                elif filter_model["type"] == "notBlank":
                    dff = dff.loc[~dff[col].isnull()]
                else:
                    dff = dff.loc[getattr(dff[col], operators[filter_model["type"]])(crit1)]
            elif filter_model["filterType"] == "set":
                dff = dff.loc[dff[col].astype("string").isin(filter_model["values"])]
            return dff
        
        self.filter_callback = filter_df
        self.df = df
        self.columnDefs = columnDefs
        self.app = app
        
    def set_callbacks(self):
        @self.app.callback(
            Output("infinite-sort-filter-grid", "getRowsResponse"),
            Input("infinite-sort-filter-grid", "getRowsRequest"),
        )
        def infinite_scroll(request):
            dff = self.df.copy()

            if request:
                if request["filterModel"]:
                    filters = request["filterModel"]
                    for f in filters:
                        try:
                            if "operator" in filters[f]:
                                if filters[f]["operator"] == "AND":
                                    dff = self.filter_callback(dff, filters[f]["condition1"], f)
                                    dff = self.filter_callback(dff, filters[f]["condition2"], f)
                                else:
                                    dff1 = self.filter_callback(dff, filters[f]["condition1"], f)
                                    dff2 = self.filter_callback(dff, filters[f]["condition2"], f)
                                    dff = pd.concat([dff1, dff2])
                            else:
                                dff = self.filter_callback(dff, filters[f], f)
                        except:
                            pass

                if request["sortModel"]:
                    sorting = []
                    asc = []
                    for sort in request["sortModel"]:
                        sorting.append(sort["colId"])
                        if sort["sort"] == "asc":
                            asc.append(True)
                        else:
                            asc.append(False)
                    dff = dff.sort_values(by=sorting, ascending=asc)

                lines = len(dff.index)
                if lines == 0:
                    lines = 1

                partial = dff.iloc[request["startRow"] : request["endRow"]]
                return {"rowData": partial.to_dict("records"), "rowCount": lines}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.set_callbacks()
        return self.grid
    
    def make(self, *args: Any, **kwds: Any) -> Any:
        return self.__call__(*args, **kwds)
    