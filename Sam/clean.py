# Imports
import math
import numpy as np
import pandas as pd

def get_feature_groups():
    """ Returns a list of numerical and categorical features,
    excluding SalePrice and Id. """
    # Numerical Features
    num_features = train.select_dtypes(include=['int64','float64']).columns
    num_features = num_features.drop(['Id','SalePrice']) # drop ID and SalePrice
	# Categorical Features
    cat_features = train.select_dtypes(include=['object']).columns
    return (list(num_features),list(cat_features))


def convert_ordinal(train):
	# Street
	train.Street.replace({'Grvl': 1, 'Pave': 2},inplace=True)
	# Alley
	train.Alley.replace({'Grvl': 1, 'Pave': 2},inplace=True)
	# LotShape
	train.LotShape.replace({'Reg': 1, 'IR1': 2, 'IR2': 3,'IR3':4}, inplace=True)
	# LandContour
	train.LandContour.replace({'Lvl': 4, 'Bnk': 3, 'HLS': 2, 'Low':1}, inplace=True)
	# Utilities
	train.Utilities.replace({'AllPub': 4, 'NoSewr': 3, 'NoSeWa': 2, 'ELO':1}, inplace=True)
	# Land Slope
	train.LandSlope.replace({'Sev':1, 'Mod':2, 'Gtl':3}, inplace=True)
	# Exterior Quality
	train.ExterQual.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Exterior Condition
	train.ExterCond.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Basement Quality
	train.BsmtQual.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Basement Condition
	train.BsmtCond.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Basement Exposure
	train.BsmtExposure.replace({'No':1, 'Mn':2, 'Av':3, 'Gd':4}, inplace=True)
	# Finished Basement 1 Rating
	train.BsmtFinType1.replace({'Unf':1, 'LwQ':2, 'Rec':3, 'BLQ':4, 'ALQ':5, 'GLQ':6}, inplace=True)
	# Finished Basement 2 Rating
	train.BsmtFinType2.replace({'Unf':1, 'LwQ':2, 'Rec':3, 'BLQ':4, 'ALQ':5, 'GLQ':6}, inplace=True)
	# Heating Quality and Condition
	train.HeatingQC.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Kitchen Quality
	train.KitchenQual.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Home functionality
	train.Functional.replace({'Sal':1, 'Sev':2, 'Maj2':3, 'Maj1':4, 'Mod':5, 'Min2':6, 'Min1':7, 'Typ':8}, inplace=True)
	# Fireplace Quality
	train.FireplaceQu.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Garage Finish
	train.GarageFinish.replace({'Unf':1, 'RFn':2, 'Fin':3}, inplace=True)
	# Garage Quality
	train.GarageQual.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Garage Condition
	train.GarageCond.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Paved Driveway
	train.PavedDrive.replace({'N':1, 'P':2, 'Y':3}, inplace=True)
	# Pool Quality
	train.PoolQC.replace({'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Fence
	train.Fence.replace({'MnWw':2, 'GdWo':3, 'MnPrv':4, 'GdPrv':5}, inplace=True)
	# We'll set all missing values in our newly converted features to 0
	converted_features = ['Street','Alley','LotShape','LandContour','Utilities','LandSlope','ExterQual','ExterCond',
	        'BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2','HeatingQC',
	        'KitchenQual','Functional','FireplaceQu','GarageFinish','GarageQual',
	        'GarageCond','PavedDrive','PoolQC','Fence']
	train[converted_features] = train[converted_features].fillna(0)

	return



def clean(train):

	# Change these categorical variables to string 
	train['MSSubClass'] = train.MSSubClass.apply(lambda x: str(x))
	train['MoSold'] = train.MoSold.apply(lambda x: str(x))
	train['YrSold'] = train.YrSold.apply(lambda x: str(x))

	# Convert categorical variables to numerical ordinals
	convert_ordinal(train)

	num_features, cat_features = get_feature_groups()
	train[cat_features] = train[cat_features].fillna('Missing')

	train.loc[train.Electrical == 'Missing', 'Electrical'] = train.Electrical.mode()[0]
	
	train.MasVnrType.replace({'Missing':'None'}, inplace=True)

	train.loc[(train.MasVnrType == 'None') & (train.MasVnrArea > 1), 'MasVnrType'] = 'BrkFace' # most common 
	train.loc[(train.MasVnrType == 'None') & (train.MasVnrArea == 1), 'MasVnrArea'] = 0 # 1 sq ft is basically 0
	
	for vnr_type in train.MasVnrType.unique():
	    # so here we set the area equal to the mean of the given veneer type
	    train.loc[(train.MasVnrType == vnr_type) & (train.MasVnrArea == 0), 'MasVnrArea'] = \
	    train[train.MasVnrType == vnr_type].MasVnrArea.mean()

	# LotFrontage is "Linear feet of street connected to property"
	# Since it seems unlikely that there's no street connected
	# to a lot, we'll set it equal to the median LotFrontage of that street.
	train.MasVnrArea.fillna(0, inplace=True)

	# Since GarageYrBlt missing means there's no garage
	# we'll set it equal to 0
	train.GarageYrBlt.fillna(0, inplace=True)

	# Questionable
	train.LotFrontage = train.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))
	return

def add_features(train):
	# Let's add some additional features

	# Total Square Footage
	train['TotalSF'] = train.TotalBsmtSF + train.GrLivArea
	train['TotalFloorSF'] = train['1stFlrSF'] + train['2ndFlrSF']
	train['TotalPorchSF'] = train.OpenPorchSF + train.EnclosedPorch + train['3SsnPorch'] + train.ScreenPorch
	    
	# Total Bathrooms
	train['TotalBathrooms'] = train.FullBath + .5 * train.HalfBath + train.BsmtFullBath + .5 * train.BsmtHalfBath

	# Booleans
	train['HasBasement'] = train.TotalBsmtSF.apply(lambda x: 1 if x > 0 else 0)
	train['HasGarage'] = train.GarageArea.apply(lambda x: 1 if x > 0 else 0)
	train['HasPorch'] = train.TotalPorchSF.apply(lambda x: 1 if x > 0 else 0)
	train['HasPool'] = train.PoolArea.apply(lambda x: 1 if x > 0 else 0)
	train['WasRemodeled'] = (train.YearRemodAdd != train.YearBuilt).astype(np.int64)
	train['IsNew'] = (train.YearBuilt > 2000).astype(np.int64)
	train['WasCompleted'] = (train.SaleCondition != 'Partial').astype(np.int64)

	return

# Let's get some data
train = pd.read_csv('./data/train.csv')
test = pd.read_csv('./data/test.csv')

clean(train)
clean(test)

add_features(train)
add_features(test)

# We heed the author's advice and cut out anything over 4,000 sq ft
train.drop(train[train.GrLivArea >= 4000].index, inplace=True)

train.to_csv('./data/train_clean.csv')
test.to_csv('./data/test_clean.csv')
