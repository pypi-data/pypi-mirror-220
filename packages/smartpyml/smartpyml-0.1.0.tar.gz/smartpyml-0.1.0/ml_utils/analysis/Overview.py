import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Overview:
    def __init__(self, dtf, max_cat=20, figsize=(10, 5)):
        self.dtf = dtf
        self.max_cat = max_cat
        self.figsize = figsize
        self.dic_cols = {col: self.utils_recognize_type(
            col) for col in dtf.columns}

    '''
    Recognize whether a column is numerical or categorical.
    :parameter
        :param col: str - name of the column to analyze
    :return
    "cat" if the column is categorical, "dt" if datetime, "num" otherwise
    '''
    def utils_recognize_type(self, col):
        if (self.dtf[col].dtype == "O") or (self.dtf[col].nunique() < self.max_cat):
            return "cat"
        elif self.dtf[col].dtype in ['datetime64[ns]', '<M8[ns]']:
            return "dt"
        else:
            return "num"
        
    '''
    Get a general overview of a dataframe.
    '''
    def dtf_overview(self):
        ## print info
        len_dtf = len(self.dtf)
        print("Shape:", self.dtf.shape)
        print("-----------------")
        for col in self.dtf.columns:
            info = col + " --> Type:" + self.dic_cols[col]
            info = info + " | Nas: " + str(self.dtf[col].isna().sum()) + "(" + str(
                int(self.dtf[col].isna().mean() * 100)) + "%)"
            if self.dic_cols[col] == "cat":
                info = info + " | Categories: " + str(self.dtf[col].nunique())
            elif self.dic_cols[col] == "dt":
                info = info + " | Range: " + \
                    "({x})-({y})".format(
                        x=str(self.dtf[col].min()), y=str(self.dtf[col].max()))
            else:
                info = info + " | Min-Max: " + "({x})-({y})".format(x=str(int(self.dtf[col].min())),
                                                                    y=str(int(self.dtf[col].max())))
            if self.dtf[col].nunique() == len_dtf:
                info = info + " | Possible PK"
            print(info)

        ## plot heatmap
        fig, ax = plt.subplots(figsize=self.figsize)
        heatmap = self.dtf.isnull()
        for k, v in self.dic_cols.items():
            if v == "num":
                heatmap[k] = heatmap[k].apply(
                    lambda x: 0.5 if x is False else 1)
            else:
                heatmap[k] = heatmap[k].apply(lambda x: 0 if x is False else 1)
        sns.heatmap(heatmap, vmin=0, vmax=1, cbar=False,
                    ax=ax).set_title('Dataset Overview')
        plt.show()
        
        ## add legend
        print("\033[1;37;40m Categorical \033[m",
              "\033[1;30;41m Numerical/DateTime \033[m", "\033[1;30;47m NaN \033[m")
    
    '''
    Check the primary key of a dtf
    :parameter
        :param pk: str - column name
    '''
    def check_pk(self, pk):
        unique_pk, len_dtf = self.dtf[pk].nunique(), len(self.dtf)
        check = "unique " + pk + ": " + \
            str(unique_pk) + "  |  len dtf: " + str(len_dtf)
        if unique_pk == len_dtf:
            msg = "OK!!!  " + check
            print(msg)
        else:
            msg = "WARNING!!!  " + check
            ERROR = self.dtf.groupby(pk).size().reset_index(
                name="count").sort_values(by="count", ascending=False)
            print(msg)
            print("Example: ", pk, "==", ERROR.iloc[0, 0])

    '''
    Moves columns into a dtf.
    :parameter
        :param dtf: dataframe - input data
        :param lst_cols: list - names of the columns that must be moved
        :param where: str - "front" or "end"
    :return
    dtf with moved columns
    '''
    def pop_columns(self, lst_cols, where="front"):
        current_cols = self.dtf.columns.tolist()
        for col in lst_cols:
            current_cols.pop(current_cols.index(col))
        if where == "front":
            self.dtf = self.dtf[lst_cols + current_cols]
        elif where == "end":
            self.dtf = self.dtf[current_cols + lst_cols]

