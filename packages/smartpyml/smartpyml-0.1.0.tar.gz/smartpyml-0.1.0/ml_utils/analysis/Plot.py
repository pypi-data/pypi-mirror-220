from .Overview import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import ppscore
import scipy.stats
import statsmodels.formula.api as smf


class Plot:
    def __init__(self, dtf, max_cat=20, figsize=(10, 5)):
        self.dtf = dtf
        self.max_cat = max_cat
        self.figsize = figsize
        self.overview = Overview(dtf, max_cat, figsize)

    '''
    Plots the frequency distribution of a dtf column.
    :parameter
        :param x: str - column name
        :param max_cat: num - max number of uniques to consider a numerical variable as categorical
        :param top: num - plot setting
        :param show_perc: logic - plot setting
        :param bins: num - plot setting
        :param quantile_breaks: tuple - plot distribution between these quantiles (to exclude outilers)
        :param box_logscale: logic
    '''

    def freqdist_plot(self, x, max_cat=20, top=None, show_perc=True, bins=100, quantile_breaks=(0, 10), box_logscale=False):
        x = self.overview.utils_recognize_type(x)
        try:
            # cat --> freq
            if x == "cat":
                ax = self.dtf[x].value_counts().head(top).sort_values().plot(
                    kind="barh", figsize=self.figsize)
                totals = []
                for i in ax.patches:
                    totals.append(i.get_width())
                if show_perc == False:
                    for i in ax.patches:
                        ax.text(i.get_width() + .3, i.get_y() + .20,
                                str(i.get_width()), fontsize=10, color='black')
                else:
                    total = sum(totals)
                    for i in ax.patches:
                        ax.text(i.get_width() + .3, i.get_y() + .20, str(round((i.get_width() / total) * 100, 2)) + '%',
                                fontsize=10, color='black')
                ax.grid(axis="x")
                plt.suptitle(x, fontsize=20)
                plt.show()

            # num --> density
            else:
                fig, ax = plt.subplots(
                    nrows=1, ncols=2, sharex=False, sharey=False, figsize=self.figsize)
                fig.suptitle(x, fontsize=20)
                # distribution
                ax[0].title.set_text('distribution')
                variable = self.dtf[x].fillna(self.dtf[x].mean())
                breaks = np.quantile(variable, q=np.linspace(0, 1, 11))
                variable = variable[(variable > breaks[quantile_breaks[0]]) & (
                    variable < breaks[quantile_breaks[1]])]
                sns.distplot(variable, hist=True, kde=True,
                             kde_kws={"shade": True}, ax=ax[0])
                des = self.dtf[x].describe()
                ax[0].axvline(des["25%"], ls='--')
                ax[0].axvline(des["mean"], ls='--')
                ax[0].axvline(des["75%"], ls='--')
                ax[0].grid(True)
                des = round(des, 2).apply(lambda x: str(x))
                box = '\n'.join(
                    ("min: " + des["min"], "25%: " + des["25%"], "mean: " + des["mean"], "75%: " + des["75%"],
                     "max: " + des["max"]))
                ax[0].text(0.95, 0.95, box, transform=ax[0].transAxes, fontsize=10, va='top', ha="right",
                           bbox=dict(boxstyle='round', facecolor='white', alpha=1))
                # boxplot
                if box_logscale == True:
                    ax[1].title.set_text('outliers (log scale)')
                    tmp_dtf = pd.DataFrame(self.dtf[x])
                    tmp_dtf[x] = np.log(tmp_dtf[x])
                    tmp_dtf.boxplot(column=x, ax=ax[1])
                else:
                    ax[1].title.set_text('outliers')
                    self.dtf.boxplot(column=x, ax=ax[1])
                plt.show()

            pass
        except Exception as e:
            print("--- got error ---")
            print(e)

    '''
    Plots a bivariate analysis.
    :parameter
        :param x: str - column
        :param y: str - column
        :param max_cat: num - max number of uniques to consider a numerical variable as categorical
    '''

    def bivariate_plot(self, x, y, max_cat=20):
        x_type = self.overview.utils_recognize_type(x)  # Get type of x column
        y_type = self.overview.utils_recognize_type(y)  # Get type of y column
        try:
            # num vs num --> stacked + scatter with density
            if (x_type == "num") & (y_type == "num"):
                # stacked
                # Remove rows with NaN in x or y
                dtf_noNan = self.dtf[[x, y]].dropna()
                breaks = np.quantile(dtf_noNan[x], q=np.linspace(0, 1, 11))
                groups = dtf_noNan.groupby([pd.cut(dtf_noNan[x], bins=breaks, duplicates='drop')])[
                    y].agg(['mean', 'median', 'size'])
                fig, ax = plt.subplots(figsize=self.figsize)
                fig.suptitle(x + "   vs   " + y, fontsize=20)
                groups[["mean", "median"]].plot(kind="line", ax=ax)
                groups["size"].plot(
                    kind="bar", ax=ax, rot=45, secondary_y=True, color="grey", alpha=0.3, grid=True)
                ax.set(ylabel=y)
                ax.right_ax.set_ylabel("Observations in each bin")
                plt.show()
                # joint plot
                sns.jointplot(x=x, y=y, data=self.dtf, dropna=True, kind='reg', height=int(
                    (self.figsize[0] + self.figsize[1]) / 2))
                plt.show()

            # cat vs cat --> hist count + hist %
            elif (x_type == "cat") & (y_type == "cat"):
                fig, ax = plt.subplots(
                    nrows=1, ncols=2,  sharex=False, sharey=False, figsize=self.figsize)
                fig.suptitle(x + "   vs   " + y, fontsize=20)
                # count
                ax[0].title.set_text('count')
                order = self.dtf.groupby(x)[y].count().index.tolist()
                sns.catplot(x=x, hue=y, data=self.dtf,
                            kind='count', order=order, ax=ax[0])
                ax[0].grid(True)
                # percentage
                ax[1].title.set_text('percentage')
                a = self.dtf.groupby(x)[y].count().reset_index()
                a = a.rename(columns={y: "tot"})
                b = self.dtf.groupby([x, y])[y].count()
                b = b.rename(columns={y: 0}).reset_index()
                b = b.merge(a, how="left")
                b["%"] = b[0] / b["tot"] * 100
                sns.barplot(x=x, y="%", hue=y, data=b,
                            ax=ax[1]).get_legend().remove()
                ax[1].grid(True)
                # fix figure
                plt.close(2)
                plt.close(3)
                plt.show()

            # num vs cat --> density + stacked + boxplot
            else:
                if (x_type == "cat"):
                    cat, num = x, y
                else:
                    cat, num = y, x
                fig, ax = plt.subplots(
                    nrows=1, ncols=3,  sharex=False, sharey=False, figsize=self.figsize)
                fig.suptitle(x + "   vs   " + y, fontsize=20)
                # distribution
                ax[0].title.set_text('density')
                for i in sorted(self.dtf[cat].unique()):
                    sns.distplot(self.dtf[self.dtf[cat] == i]
                                 [num], hist=False, label=i, ax=ax[0])
                ax[0].grid(True)
                # stacked
                # Remove rows with NaN in num
                dtf_noNan = self.dtf[[cat, num]].dropna()
                ax[1].title.set_text('bins')
                breaks = np.quantile(dtf_noNan[num], q=np.linspace(0, 1, 11))
                tmp = dtf_noNan.groupby(
                    [cat, pd.cut(dtf_noNan[num], breaks, duplicates='drop')]).size().unstack().T
                tmp = tmp[dtf_noNan[cat].unique()]
                tmp["tot"] = tmp.sum(axis=1)
                for col in tmp.drop("tot", axis=1).columns:
                    tmp[col] = tmp[col] / tmp["tot"]
                tmp.drop("tot", axis=1)[sorted(self.dtf[cat].unique())].plot(
                    kind='bar', stacked=True, ax=ax[1], legend=False, grid=True)
                # boxplot
                ax[2].title.set_text('outliers')
                sns.catplot(x=cat, y=num, data=self.dtf, kind="box",
                            ax=ax[2], order=sorted(self.dtf[cat].unique()))
                ax[2].grid(True)
                # fix figure
                plt.close(2)
                plt.close(3)
                plt.show()

            pass
        except Exception as e:
            print("--- got error ---")
            print(e)

    '''
    Plots a bivariate analysis using Nan and not-Nan as categories.
    '''

    def nan_analysis(self, na_x, y, max_cat=20):
        dtf_NA = self.dtf[[na_x, y]]
        dtf_NA[na_x] = self.dtf[na_x].apply(
            lambda x: "Value" if not pd.isna(x) else "NA")
        self.bivariate_plot(x=na_x, y=y, max_cat=max_cat)

    '''
    Plots a bivariate analysis with time variable.
    '''

    def ts_analysis(self, x, y, max_cat=20):
        x_type = self.overview.utils_recognize_type(x)  # Get type of x column
        y_type = self.overview.utils_recognize_type(y)  # Get type of y column

        if y_type == "cat":
            dtf_tmp = self.dtf.groupby(x)[y].sum()
        else:
            dtf_tmp = self.dtf.groupby(x)[y].median()
        dtf_tmp.plot(title=y + " by " + x, figsize=self.figsize, grid=True)

    '''
    plots multivariate analysis.
    '''

    def cross_distributions(self, x1, x2, y, max_cat=20):
        y_type = self.overview.utils_recognize_type(y)  # Get type of y column
        x1 = self.overview.utils_recognize_type(x1)  # Get type of x1 column
        x2 = self.overview.utils_recognize_type(x2)  # Get type of x2 column
        # Y cat
        if y_type == "cat":
            # cat vs cat --> contingency table
            if (x1 == "cat") & (x2 == "cat"):
                cont_table = pd.crosstab(
                    index=self.dtf[x1], columns=self.dtf[x2], values=self.dtf[y], aggfunc="sum")
                fig, ax = plt.subplots(figsize=self.figsize)
                sns.heatmap(cont_table, annot=True, fmt='.0f', cmap="YlGnBu", ax=ax, linewidths=.5).set_title(
                    x1 + '  vs  ' + x2 + '  (filter: ' + y + ')')

             # num vs num --> scatter with hue
            elif (x1 == "num") & (x2 == "num"):
                sns.lmplot(x=x1, y=x2, data=self.dtf,
                           hue=y, height=self.figsize[1])

            # num vs cat --> boxplot with hue
            else:
                if x1 == "cat":
                    cat, num = x1, x2
                else:
                    cat, num = x2, x1
                fig, ax = plt.subplots(figsize=self.figsize)
                sns.boxplot(x=cat, y=num, hue=y, data=self.dtf, ax=ax).set_title(
                    x1 + '  vs  ' + x2 + '  (filter: ' + y + ')')
                ax.grid(True)
        # Y num
        else:
            # all num --> 3D scatter plot
            fig = plt.figure(figsize=self.figsize)
            ax = fig.gca(projection='3d')
            plot3d = ax.scatter(
                xs=self.dtf[x1], ys=self.dtf[x2], zs=self.dtf[y], c=self.dtf[y], cmap='inferno', linewidth=0.5)
            fig.colorbar(plot3d, shrink=0.5, aspect=5, label=y)
            ax.set(xlabel=x1, ylabel=x2, zlabel=y)
            plt.show()

    '''
    Computes the correlation matrix.
    :parameter
        :param method: str - "pearson" (numeric), "spearman" (categorical), "kendall"
        :param negative: bool - if False it takes the absolute values of correlation
        :param lst_filters: list - filter rows to show
        :param annotation: logic - plot setting
    '''
    def corr_matrix(self, method="pearson", negative=True, lst_filters=[], annotation=True):
        dtf_corr = self.dtf.copy()

        # Factorize categorical columns
        for col in dtf_corr.columns:
            if dtf_corr[col].dtype == "O":
                print("--- WARNING: Factorizing",
                      dtf_corr[col].nunique(), "labels of", col, "---")
                dtf_corr[col] = dtf_corr[col].factorize(sort=True)[0]

        # Filter rows if lst_filters is provided
        dtf_corr = dtf_corr.corr(method=method) if len(
            lst_filters) == 0 else dtf_corr.corr(method=method).loc[lst_filters]

        # Apply negative option
        dtf_corr = dtf_corr if negative else dtf_corr.abs()

        # Plot heatmap
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(dtf_corr, annot=annotation, fmt='.2f',
                    cmap="YlGnBu", ax=ax, cbar=True, linewidths=0.5)
        plt.title(method + " correlation")
        plt.show()

        return dtf_corr

    '''
    Computes the pps matrix.
    '''
    def pps_matrix(self, annotation=True, lst_filters=[]):
        dtf_pps = ppscore.matrix(self.dtf) if len(
            lst_filters) == 0 else ppscore.matrix(self.dtf.loc[lst_filters])
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(dtf_pps, vmin=0., vmax=1., annot=annotation,
                    fmt='.2f', cmap="YlGnBu", ax=ax, cbar=True, linewidths=0.5)
        plt.title("Predictive Power Score")
        return dtf_pps

    '''
    Computes correlation/dependancy and p-value (prob of happening something different than what observed in the sample)
    '''
    def test_corr(self, x, y, max_cat=20):
        x_type = self.overview.utils_recognize_type(x)  # Get type of x column
        y_type = self.overview.utils_recognize_type(y)  # Get type of y column

        # num vs num --> pearson
        if (x_type == "num") & (y_type == "num"):
            dtf_noNan = self.dtf.dropna(subset=[x, y])
            coeff, p = scipy.stats.pearsonr(dtf_noNan[x], dtf_noNan[y])
            coeff, p = round(coeff, 3), round(p, 3)
            conclusion = "Significant" if p < 0.05 else "Non-Significant"
            print("Pearson Correlation:", coeff,
                  conclusion, "(p-value: " + str(p) + ")")

        # cat vs cat --> cramer (chiquadro)
        elif (x_type == "cat") & (y_type == "cat"):
            cont_table = pd.crosstab(index=self.dtf[x], columns=self.dtf[y])
            chi2_test = scipy.stats.chi2_contingency(cont_table)
            chi2, p = chi2_test[0], chi2_test[1]
            n = cont_table.sum().sum()
            phi2 = chi2 / n
            r, k = cont_table.shape
            phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
            rcorr = r - ((r - 1) ** 2) / (n - 1)
            kcorr = k - ((k - 1) ** 2) / (n - 1)
            coeff = np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))
            coeff, p = round(coeff, 3), round(p, 3)
            conclusion = "Significant" if p < 0.05 else "Non-Significant"
            print("Cramer Correlation:", coeff,
                  conclusion, "(p-value: " + str(p) + ")")

        # num vs cat --> 1way anova (f: the means of the groups are different)
        else:
            if x_type == "cat":
                cat, num = x, y
            else:
                cat, num = y, x
            model = smf.ols(num + ' ~ ' + cat, data=self.dtf).fit()
            table = sm.stats.anova_lm(model)
            p = table["PR(>F)"][0]
            coeff, p = None, round(p, 3)
            conclusion = "Correlated" if p < 0.05 else "Non-Correlated"
            print("Anova F: the variables are",
                  conclusion, "(p-value: " + str(p) + ")")

        return coeff, p
