from teradataml.analytics.sqle.Antiselect import Antiselect
from teradataml.analytics.sqle.Attribution import Attribution
from teradataml.analytics.sqle.DecisionForestPredict import DecisionForestPredict
from teradataml.analytics.sqle.DecisionTreePredict import DecisionTreePredict
from teradataml.analytics.sqle.GLMPredict import GLMPredict
from teradataml.analytics.sqle.MovingAverage import MovingAverage
from teradataml.analytics.sqle.NGramSplitter import NGramSplitter
from teradataml.analytics.sqle.NPath import NPath
from teradataml.analytics.sqle.NaiveBayesPredict import NaiveBayesPredict
from teradataml.analytics.sqle.NaiveBayesTextClassifierPredict import NaiveBayesTextClassifierPredict
from teradataml.analytics.sqle.Pack import Pack
from teradataml.analytics.sqle.Sessionize import Sessionize
from teradataml.analytics.sqle.StringSimilarity import StringSimilarity
from teradataml.analytics.sqle.SVMSparsePredict import SVMSparsePredict
from teradataml.analytics.sqle.Unpack import Unpack

from teradataml.analytics.meta_class import _AnalyticFunction
from teradataml.analytics.meta_class import _common_init

_sqle_functions = ['ANOVA',
                  'Antiselect',
                  'Attribution',
                  'BincodeFit',
                  'BincodeTransform',
                  'CategoricalSummary',
                  'ChiSq',
                  'ClassificationEvaluator',
                  'ColumnSummary',
                  'ColumnTransformer',
                  'ConvertTo',
                  'DecisionForest',
                  'DecisionForestPredict',
                  'FillRowId',
                  'Fit',
                  'FTest',
                  'GetFutileColumns',
                  'GetRowsWithMissingValues',
                  'GetRowsWithoutMissingValues',
                  'GLM',
                  'GLMPredict',
                  'GLMPerSegment',
                  'GLMPredictPerSegment',
                  'Histogram',
                  'KMeans',
                  'KMeansPredict',
                  'KNN',
                  'MovingAverage',
                  'NaiveBayesTextClassifierPredict',
                  'NaiveBayesTextClassifierTrainer',
                  'NGramSplitter',
                  'NonLinearCombineFit',
                  'NonLinearCombineTransform',
                  'NPath',
                  'NumApply',
                  'OneClassSVM',
                  'OneClassSVMPredict',
                  'OneHotEncodingFit',
                  'OneHotEncodingTransform',
                  'OrdinalEncodingFit',
                  'OrdinalEncodingTransform',
                  'OutlierFilterFit',
                  'OutlierFilterTransform',
                  'Pack',
                  'PolynomialFeaturesFit',
                  'PolynomialFeaturesTransform',
                  'QQNorm',
                  'RandomProjectionFit',
                  'RandomProjectionMinComponents',
                  'RandomProjectionTransform',
                  'RegressionEvaluator',
                  'ROC',
                  'RoundColumns',
                  'RowNormalizeFit',
                  'RowNormalizeTransform',
                  'ScaleFit',
                  'ScaleTransform',
                  'SentimentExtractor',
                  'Sessionize',
                  'Silhouette',
                  'SimpleImputeFit',
                  'SimpleImputeTransform',
                  'StrApply',
                  'StringSimilarity',
                  'SVM',
                  'SVMPredict',
                  'SVMSparsePredict',
                  'TDGLMPredict',
                  'TDDecisionForestPredict',
                  'TargetEncodingFit',
                  'TargetEncodingTransform',
                  'TextParser',
                  'Transform',
                  'TrainTestSplit',
                  'UnivariateStatistics',
                  'Unpack',
                  'VectorDistance',
                  'WhichMax',
                  'WhichMin',
                  'WordEmbeddings',
                  'XGBoost',
                  'XGBoostPredict',
                  'ZTest'
                  ]

for func in _sqle_functions:
    globals()[func] = type("{}".format(func), (_AnalyticFunction, ), {"__init__": lambda self, **kwargs: _common_init(self, 'sqle',
                                                              **kwargs), "__doc__": _AnalyticFunction.__doc__})