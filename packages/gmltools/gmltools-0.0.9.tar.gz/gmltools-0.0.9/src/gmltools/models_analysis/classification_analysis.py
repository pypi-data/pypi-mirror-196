from sklearn import metrics as mtrs
from scipy.stats import norm, binom_test
from statsmodels.stats import contingency_tables as cont_tab
import matplotlib.pyplot as plt
import numpy as np
from sklearn.inspection import permutation_importance
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import seaborn as sns
import math
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from sklearn.pipeline import Pipeline
from scipy import stats



class Canalysis:
    """
    Class to calculate classification metrics analysis.
    """
    def __init__(self,model, X_train, y_train, X_test, y_test):

        assert isinstance(X_train, pd.core.frame.DataFrame), 'X_train must be a pandas DataFrame'
        assert isinstance(y_train, pd.core.series.Series), 'y_train must be a pandas Series'
        assert isinstance(X_test, pd.core.frame.DataFrame), 'X_test must be a pandas DataFrame'
        assert isinstance(y_test, pd.core.series.Series), 'y_test must be a pandas Series'

        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test


    def confusion_matrix(self, train_or_test, labels, sample_weight=None, normalize:bool=True):
        """
        Calculate confusion matrix and classification metrics.
        For Multiclass uses Macro average, for binary uses binary average.

        Parameters
        ----------
        train_or_test : str, optional
            Whether to calculate metrics on training or test set, by default 'train'
        labels : list
            List of labels. Vector of output categories
        sample_weight : list, optional
            Weights assigned to output samples in training process, by default None.
            ([int, int, ...])
        normalize : bool, optional
            normalize classification metrics when possible, by default True.

        Returns
        -------
        None
            Print confusion matrix and classification metrics
        """
        assert isinstance(train_or_test, str), 'train_or_test must be a string'
        assert train_or_test.lower() in ['train', 'test'], 'train_or_test must be either "train" or "test"'
        # Check if train or test
        if train_or_test.lower() == 'train':
            y_true = self.y_train
            y_pred = self.model.predict(self.X_train)
        elif train_or_test.lower() == 'test':
            y_true = self.y_test
            y_pred = self.model.predict(self.X_test)

        # Calculate confusion matrix
        print('Confusion Matrix and Statistics\n\t   Prediction')
        # if labels is None:
        #     labels = list(y_true.unique())
        cm = mtrs.confusion_matrix(y_true, y_pred, labels=labels, sample_weight=sample_weight, normalize=None)
        cm_df = pd.DataFrame(cm, columns=labels)
        cm_df = pd.DataFrame(labels, columns=['Reference']).join(cm_df)
        print(cm_df.to_string(index=False))
        # Calculate metrics depending on type of classification, multiclass or binary
        try:   
            if len(y_true.unique()) == 2: # binary
                average = 'binary'
            else: # multiclass
                average = 'macro'     
        except:
            if len(np.unique(y_true)) == 2: # binary
                average = 'binary'
            else: # multiclass
                average = 'macro'
                
        # Calculate accuracy
        acc = mtrs.accuracy_score(y_true, y_pred, normalize=normalize, sample_weight=sample_weight)
        # Calculate No Information Rate
        combos = np.array(np.meshgrid(y_pred, y_true)).reshape(2, -1)
        noi = mtrs.accuracy_score(combos[0], combos[1], normalize=normalize, sample_weight=sample_weight)
        # Calculate p-value Acc > NIR
        res = binom_test(cm.diagonal().sum(), cm.sum(), max(pd.DataFrame(cm).apply(sum,axis=1)/cm.sum()),'greater')
        # Calculate P-value mcnemar test
        MCN_pvalue = cont_tab.mcnemar(cm).pvalue
        # Calculate Kappa
        Kappa = mtrs.cohen_kappa_score(y_true, y_pred, labels=labels, sample_weight=sample_weight)
        # Obtain positive label
        pos_label = labels[0]
        # Calculate precision
        precision = mtrs.precision_score(y_true, y_pred, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)
        # Calculate recall 
        recall = mtrs.recall_score(y_true, y_pred, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)
        # Calculate F1 score
        F_score = mtrs.f1_score(y_true, y_pred, labels=labels, pos_label=pos_label, average=average, sample_weight=sample_weight)
        # Calculate balanced accuracy
        Balanced_acc = mtrs.balanced_accuracy_score(y_true, y_pred, sample_weight=sample_weight)
        if average == 'binary': # binary
            # Calculate sensitivity, specificity et al
            TP = cm[1,1]
            TN = cm[0,0]
            FP = cm[0,1]
            FN = cm[1,0]
            sens = TP / (TP + FN)
            spec = TN / (TN + FP)
            Prevalence = (TP + FN) / (TP + TN + FP + FN)
            Detection_rate = TP / (TP + TN + FP + FN)
            Detection_prevalence = (TP + FP) /  (TP + TN + FP + FN)
            
            
            # print all the measures
            out_str = '\nAccuracy: ' + str(round(acc,3)) + '\n' + \
            'No Information Rate: ' + str(round(noi,3)) + '\n' + \
            'P-Value [Acc > NIR]: ' + str(round(res,3)) + '\n' + \
            'Kappa: ' + str(round(Kappa,3)) + '\n' + \
            'Mcnemar\'s Test P-Value: ' + str(round(MCN_pvalue,3)) + '\n' + \
            'Sensitivity: ' + str(round(sens,3)) + '\n' + \
            'Specificity: ' + str(round(spec,3)) + '\n' + \
            'Precision: ' + str(round(precision,3)) + '\n' + \
            'Recall: ' + str(round(recall,3)) + '\n' + \
            'Prevalence: ' + str(round(Prevalence,3)) + '\n' + \
            'Detection Rate: ' + str(round(Detection_rate,3)) + '\n' + \
            'Detection prevalence: ' + str(round(Detection_prevalence,3)) + '\n' + \
            'Balanced accuracy: ' + str(round(Balanced_acc,3)) + '\n' + \
            'F1 Score: ' + str(round(F_score,3)) + '\n' + \
            'Positive label: ' + str(pos_label) 
        else: # multiclass
                    # print all the measures
            out_str = '\n Overall Multiclass Score Using Macro' + '\n'  + \
            '\nAccuracy: ' + str(round(acc,3)) + '\n' + \
            'No Information Rate: ' + str(round(noi,3)) + '\n' + \
            'P-Value [Acc > NIR]: ' + str(round(res,3)) + '\n' + \
            'Kappa: ' + str(round(Kappa,3)) + '\n' + \
            'Mcnemar\'s Test P-Value: ' + str(round(MCN_pvalue,3)) + '\n' + \
            'Precision: ' + str(round(precision,3)) + '\n' + \
            'Recall: ' + str(round(recall,3)) + '\n' + \
            'Balanced accuracy: ' + str(round(Balanced_acc,3)) + '\n' + \
            'F1 Score: ' + str(round(F_score,3))  + '\n' + '\n' + \
            'Individual Class Scores' 
            
            # Calculate metrics for each class
            for i in range(len(labels)):
                labels_index = [i for i in range(len(labels))]
                labels_index.remove(i)
                # Calculate sensitivity, specificity et al
                TP = cm[i,i]
                cm2=np.delete(cm,i,0)
                TN = np.delete(cm2,i,1).sum()
                FP = np.delete(cm[:,i],i).sum()
                FN = np.delete(cm[i],i).sum()
                rec = TP / (TP + FN)
                spec_2 = TN / (TN + FP)
                prec= TP / (TP + FP)
                # print all the measures
                out_str += '\n' + 'Class: ' + str(labels[i]) + '\n' + \
                'Recall: ' + str(round(rec,3)) + '\n' + \
                'Specificity: ' + str(round(spec_2,3)) + '\n' + \
                'Precision: ' + str(round(prec,3)) + '\n' + \
                'F1 Score: ' + str(round((2*prec*rec)/(prec+rec),3)) + '\n' 
        print(out_str)

    #generate a permutation importance plot
    def permutation_importance(self,n_repeats=10,random_state=None,figsize=(12, 4)):
        """
        Generate a permutation importance plot. Is used
        to determine the importance of each feature in the model.

        Parameters
        ----------
        n_repeats : int, optional
            Number of times to permute a feature. The default is 10.

        random_state : int, optional
            Random state for the permutation. The default is None.

        figsize : tuple, optional
            Size of the figure. The default is (12, 4).

        Returns
        -------
        None.
            Plot is generated.
        """
        assert n_repeats > 0, "n_repeats must be greater than 0 for permutation importance"
        assert random_state is None or isinstance(random_state, int), "random_state must be an integer or None"
        assert isinstance(figsize, tuple) and len(figsize) == 2, "figsize must be a tuple and figsize must be a tuple of length 2"
        importances = permutation_importance(self.model, 
                                    self.X_train, self.y_train,
                                    n_repeats=n_repeats,
                                    random_state=random_state)
        
        fig = plt.figure(2, figsize=figsize) 
        plt.bar(self.X_train.columns, importances.importances_mean, yerr=importances.importances_std,color='black', alpha=0.5)
        plt.xlabel('Feature')
        plt.ylabel('Permutation Importance')
        plt.xticks(rotation=90)
        plt.grid()
        plt.show()

class Ranalysis:
    """
    
    """
    def __init__(self,model, X_train, y_train, X_test, y_test):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def residual_analysis(self, train_or_test, figsize=(1400, 1000), bins=30, smooth_order=5):
        """
        Generate a residual analysis plot. Is used to determine if the model is overfitting or underfitting.
        Studying the variance and the bias of the residuals.

        Parameters
        ----------
        train_or_test : str
            Whether to use the training or test data.

        figsize : tuple, optional
            Size of the figure. The default is (1400, 1000).
        
        bins : int, optional
            Number of bins for the histogram. The default is 30.
        
        smooth_order : int, optional
            Order of the smoothing polynomial. The default is 5.
        
        Returns
        -------
        None.
            Plot is generated.
        """
        assert train_or_test.lower() in ['train', 'test'], "train_or_test must be either 'train' or 'test'"
        assert isinstance(figsize, tuple) and len(figsize) == 2, "figsize must be a tuple and figsize must be a tuple of length 2"
        assert isinstance(bins, int) and bins > 0, "bins must be an integer greater than 0"
        assert isinstance(smooth_order, int) and smooth_order > 0, "smooth_order must be an integer greater than 0"

        df=pd.DataFrame(columns=['y_true', 'y_pred'])
        if train_or_test.lower() == 'train':
            y_pred = self.model.predict(self.X_train)
            y_true = self.y_train
            df[self.X_train.columns] = self.X_train
        else:
            y_pred = self.model.predict(self.X_test)
            y_true = self.y_test
            df[self.X_test.columns] = self.X_test
        df['y_true'] = y_true
        df['y_pred'] = y_pred
        df['residuals'] = df['y_true'] - df['y_pred']
        out_num = np.where(df.columns.values == 'residuals')[0]
        nplots = df.shape[1] - 1  # Exclude the residuals column from the number of plots
        # Create subplots
        fig = make_subplots(rows=int(np.floor(np.sqrt(nplots)))+1, cols=int(np.ceil(np.sqrt(nplots))),
                            specs=[[{'type': 'histogram'} if i == out_num else {'type': 'xy'} for i in range(nplots)]],
                            subplot_titles=[f"{df.columns[i]} vs residuals" for i in range(df.shape[1]) if i != out_num])
        
        input_num = 0
        for i in range(1, fig.layout.grid_size['rows']+1):
            for j in range(1, fig.layout.grid_size['columns']+1):
                if input_num < nplots:
                    # Create plots
                    if input_num == out_num:
                        fig.add_trace(go.Histogram(x=df['residuals'], nbinsx=bins), row=i, col=j)
                    else:
                        if df.iloc[:,input_num].dtype.name == 'category':
                            fig.add_trace(go.Box(x=df.columns[input_num], y=df['residuals']), row=i, col=j)
                        else:
                            fig.add_trace(go.Scatter(x=df.iloc[:,input_num], y=df['residuals'], mode='markers'),
                                        row=i, col=j)
                            fig.add_trace(go.Scatter(x=df.iloc[:,input_num], y=df['residuals'].rolling(smooth_order, center=True).mean(),
                                                    mode='lines', line=dict(color='navy')), row=i, col=j)
                    input_num += 1
                else:
                    fig.update_layout(showlegend=False)
                    break
        
        fig.update_layout(title='Model Diagnosis Plot', height=figsize[0], width=figsize[1],font=dict(size=20))
        fig.show()






    def summaryLinReg(self, use_old:bool= True):
        """
        Summary of scikit 'LinearRegression' models.
        
        Provide feature information of linear regression models,
        such as coefficient, standard error and p-value. It is adapted
        to stand-alone and Pipeline scikit models.
        
        Important restriction of the function is that LinearRegression 
        must be the last step of the Pipeline.

        Parameters
        ----------
        use_old (bool)
            Use previous version of summary of linear regression, useful when multicollinearity breaks new method. Default to True.
        """
        #assert that the model is linear regression or is a Linear Regression inside a pipeline
        assert type(self.model) is LinearRegression , "model must be a LinearRegression or a Pipeline with a LinearRegression as last step. Try model.best_estimator_ if you are using GridSearchCV or RandomizedSearchCV"
    
        if use_old:
            # Obtain coefficients of the model
            if type(self.model) is LinearRegression:
                coefs = self.model.coef_
                intercept = self.model.intercept_
            else:
                coefs = self.model[len(self.model) - 1].coef_ #We suppose last position of pipeline is the linear regression model
                intercept = self.model[len(self.model) - 1].intercept_
            
            if type(self.model) is Pipeline:
                X_design = self.model[0].transform(X)
                coefnames = list()
                if hasattr(self.model[0],"transformers_"):
                    for tt in range(len(self.model[0].transformers_)):
                        try:
                            if hasattr(self.model[0].transformers_[tt][1].steps[-1][1],"get_feature_names"):
                                aux = self.model[0].transformers_[tt][1].steps[-1][1].get_feature_names_out(self.model[0].transformers_[tt][2])
                                if type(aux)==list:
                                    coefnames = coefnames + aux
                                else:
                                    coefnames = coefnames + aux.tolist()
                            else:
                                coefnames = coefnames + self.model[0].transformers_[tt][2]
                        except:
                            continue
                else:
                    coefnames = self.X_train.columns.values.tolist()
            
                
            ## include constant ------------- 
            if self.model[len(self.model) - 1].intercept_ != 0:
                coefnames.insert(0,'Intercept')
                if type(X_design).__module__ == np.__name__:
                    X_design = np.hstack([np.ones((X_design.shape[0], 1)), X_design])
                    X_design = pd.DataFrame(X_design, columns=coefnames)
                elif type(X_design).__module__ == 'pandas.core.frame':
                    pass
                else:
                    X_design = np.hstack([np.ones((X_design.shape[0], 1)), X_design.toarray()])
                    X_design = pd.DataFrame(X_design, columns=coefnames)    
            else:
                try:
                    X_design = X_design.toarray()
                    X_design = pd.DataFrame(X_design, columns=coefnames)
                except:
                    pass
            

            ols = sm.OLS(y.values, X_design)
            ols_result = ols.fit()
            return ols_result.summary()
        else:
            # Obtain coefficients of the model
            if type(self.model) is LinearRegression:
                coefs = self.model.coef_
                intercept = self.model.intercept_
                input_names = self.X_train.columns
                X_t = self.X_train
            else:
                coefs = self.model[len(self.model) - 1].coef_ #We suppose last position of pipeline is the linear regression model
                intercept = self.model[len(self.model) - 1].intercept_
                X_t = self.model[len(self.model) - 2].transform(self.X_train)
                input_names = self.model[len(self.model) - 2].get_feature_names_out().tolist()

            intercept_included = True
            params = coefs
            if not intercept == 0 and not 'Intercept' in input_names:
                params = np.append(intercept,coefs)
                input_names = ['Intercept'] + input_names
                intercept_included = False
            elif 'Intercept' in input_names:
                coefs[input_names.index('Intercept')] = intercept
                params = coefs
            predictions = self.model.predict(self.X_train)
            residuals = self.y_train - predictions

            print('Residuals:')
            quantiles = np.quantile(residuals, [0,0.25,0.5,0.75,1], axis=0)
            quantiles = pd.DataFrame(quantiles, index=['Min','1Q','Median','3Q','Max'])
            print(quantiles.transpose())
            # Note if you don't want to use a DataFrame replace the two lines above with
            if not intercept_included:
                if not type(X_t) == pd.core.frame.DataFrame and not type(X_t) == np.ndarray:
                    newX = np.append(np.ones((len(X_t.toarray()),1)), X_t.toarray(), axis=1)
                else:
                    newX = np.append(np.ones((len(X_t),1)), X_t, axis=1)
            else:
                if not type(X_t) == pd.core.frame.DataFrame:
                    newX = X_t.toarray()
                else:
                    newX = X_t.values
                
            MSE = (sum((residuals)**2))/(len(newX)-len(newX[0]))

            var_b = MSE * (np.linalg.inv(np.dot(newX.T,newX)).diagonal())
            sd_b = np.sqrt(var_b)
            ts_b = params / sd_b

            p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-len(newX[0])))) for i in ts_b]

            sd_b = np.round(sd_b,3)
            ts_b = np.round(ts_b,3)
            p_values = np.round(p_values,3)
            params = np.round(params,4)

            myDF3 = pd.DataFrame()
            myDF3["Input"], myDF3["Coefficients"], myDF3["Standard Errors"], myDF3["t values"], myDF3["Pr(>|t|)"], myDF3["Signif"] = [input_names, params, sd_b, ts_b, p_values, np.vectorize(lambda x: '***' if x < 0.001 else ('**' if x < 0.01 else ('*' if x < 0.05 else ('.' if x < 0.1 else ' '))))(p_values)]
            myDF3.set_index("Input", inplace=True)
            myDF3.index.name = None
            print(myDF3)
            print('---\nSignif. codes:  0 `***` 0.001 `**` 0.01 `*` 0.05 `.` 0.1 ` ` 1\n')
            print(f'Residual Standard Error: {round(np.std(residuals), 3)} on {residuals.shape[0]} degrees of freedom')
            # error metrics
            r2 = mtrs.r2_score(y, predictions)
            n = len(self.y_train)
            k = self.X_train.shape[1]
            adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - k - 1)
            RMSE = np.sqrt(mtrs.mean_squared_error(self.y_train, predictions))
            MAE = mtrs.mean_absolute_error(self.y_train, predictions)
            print(f'R-squared: {round(r2, 3)}, Adjusted R-squared: {round(adjusted_r2, 3)}, RMSE: {round(RMSE, 3)}, MAE: {round(MAE, 3)}')
            # F test
            TSS = np.sum(y - predictions) ** 2
            RSS = (1 - r2) * TSS
            num_f = (TSS - RSS) / k
            den_f = RSS / (n - k - 1)
            f = num_f / den_f
            p_f = 1 - stats.f.cdf(f, k, (n - k - 1)) 
            print(f'F-statistic: {round(f, 3)} on {k} and {n - k - 1} DOF, P(F-statistic): {round(p_f, 3)}')
            return            

    
