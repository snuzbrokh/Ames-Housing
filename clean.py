# Imports
import math
import numpy as np
import pandas as pd

def get_feature_groups():
    """ Returns a list of numerical and categorical features,
    excluding SalePrice and Id. """
    # Numerical Features
    num_features = df.select_dtypes(include=['int64','float64']).columns
    num_features = num_features.drop(['Id','SalePrice']) # drop ID and SalePrice
	# Categorical Features
    cat_features = df.select_dtypes(include=['object']).columns
    return (list(num_features),list(cat_features))


def convert_ordinal(df):
	# Street
	df.Street.replace({'Grvl': 1, 'Pave': 2},inplace=True)
	# Alley
	df.Alley.replace({'Grvl': 1, 'Pave': 2},inplace=True)
	# LotShape
	df.LotShape.replace({'Reg': 1, 'IR1': 2, 'IR2': 3,'IR3':4}, inplace=True)
	# LandContour
	df.LandContour.replace({'Lvl': 4, 'Bnk': 3, 'HLS': 2, 'Low':1}, inplace=True)
	# Utilities
	df.Utilities.replace({'AllPub': 4, 'NoSewr': 3, 'NoSeWa': 2, 'ELO':1}, inplace=True)
	# Land Slope
	df.LandSlope.replace({'Sev':1, 'Mod':2, 'Gtl':3}, inplace=True)
	# Exterior Quality
	df.ExterQual.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Exterior Condition
	df.ExterCond.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Basement Quality
	df.BsmtQual.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Basement Condition
	df.BsmtCond.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Basement Exposure
	df.BsmtExposure.replace({'No':1, 'Mn':2, 'Av':3, 'Gd':4}, inplace=True)
	# Finished Basement 1 Rating
	df.BsmtFinType1.replace({'Unf':1, 'LwQ':2, 'Rec':3, 'BLQ':4, 'ALQ':5, 'GLQ':6}, inplace=True)
	# Finished Basement 2 Rating
	df.BsmtFinType2.replace({'Unf':1, 'LwQ':2, 'Rec':3, 'BLQ':4, 'ALQ':5, 'GLQ':6}, inplace=True)
	# Heating Quality and Condition
	df.HeatingQC.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Kitchen Quality
	df.KitchenQual.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Home functionality
	df.Functional.replace({'Sal':1, 'Sev':2, 'Maj2':3, 'Maj1':4, 'Mod':5, 'Min2':6, 'Min1':7, 'Typ':8}, inplace=True)
	# Fireplace Quality
	df.FireplaceQu.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Garage Finish
	df.GarageFinish.replace({'Unf':1, 'RFn':2, 'Fin':3}, inplace=True)
	# Garage Quality
	df.GarageQual.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Garage Condition
	df.GarageCond.replace({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Paved Driveway
	df.PavedDrive.replace({'N':1, 'P':2, 'Y':3}, inplace=True)
	# Pool Quality
	df.PoolQC.replace({'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}, inplace=True)
	# Fence
	df.Fence.replace({'MnWw':2, 'GdWo':3, 'MnPrv':4, 'GdPrv':5}, inplace=True)
	# We'll set all missing values in our newly converted features to 0
	converted_features = ['Street','Alley','LotShape','LandContour','Utilities','LandSlope','ExterQual','ExterCond',
	        'BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2','HeatingQC',
	        'KitchenQual','Functional','FireplaceQu','GarageFinish','GarageQual',
	        'GarageCond','PavedDrive','PoolQC','Fence']
	df[converted_features] = df[converted_features].fillna(0)

	return



def clean(df):

	# Change these categorical variables to string 
	df['MSSubClass'] = df.MSSubClass.apply(lambda x: str(x))
	df['MoSold'] = df.MoSold.apply(lambda x: str(x))
	df['YrSold'] = df.YrSold.apply(lambda x: str(x))

	# Convert categorical variables to numerical ordinals
	convert_ordinal(df)

	num_features, cat_features = get_feature_groups()
	df[cat_features] = df[cat_features].fillna('Missing')

	df.loc[df.Electrical == 'Missing', 'Electrical'] = df.Electrical.mode()[0]
	
	df.MasVnrType.replace({'Missing':'None'}, inplace=True)

	df.loc[(df.MasVnrType == 'None') & (df.MasVnrArea > 1), 'MasVnrType'] = 'BrkFace' # most common 
	df.loc[(df.MasVnrType == 'None') & (df.MasVnrArea == 1), 'MasVnrArea'] = 0 # 1 sq ft is basically 0
	
	for vnr_type in df.MasVnrType.unique():
	    # so here we set the area equal to the mean of the given veneer type
	    df.loc[(df.MasVnrType == vnr_type) & (df.MasVnrArea == 0), 'MasVnrArea'] = \
	    df[df.MasVnrType == vnr_type].MasVnrArea.mean()

	# LotFrontage is "Linear feet of street connected to property"
	# Since it seems unlikely that there's no street connected
	# to a lot, we'll set it equal to the median LotFrontage of that street.
	df.MasVnrArea.fillna(0, inplace=True)

	# Since GarageYrBlt missing means there's no garage
	# we'll set it equal to 0
	df.GarageYrBlt.fillna(0, inplace=True)

	# Reasonable to substitude all missing with the median for that particular neighborhood
	df.LotFrontage = df.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))

	df.fillna(0, inplace=True)
	return

def add_features(df):
	# Let's add some additional features

	# Total Square Footage
	#df['TotalSF'] = df.TotalBsmtSF + df.GrLivArea
	#df['TotalFloorSF'] = df['1stFlrSF'] + df['2ndFlrSF']
	df['TotalPorchSF'] = df.OpenPorchSF + df.EnclosedPorch + df['3SsnPorch'] + df.ScreenPorch
	    
	# Total Bathrooms
	#df['TotalBathrooms'] = df.FullBath + .5 * df.HalfBath + df.BsmtFullBath + .5 * df.BsmtHalfBath

	# Booleans
	df['HasBasement'] = df.TotalBsmtSF.apply(lambda x: 1 if x > 0 else 0)
	df['HasGarage'] = df.GarageArea.apply(lambda x: 1 if x > 0 else 0)
	df['HasPorch'] = df.TotalPorchSF.apply(lambda x: 1 if x > 0 else 0)
	df['HasPool'] = df.PoolArea.apply(lambda x: 1 if x > 0 else 0)
	df['WasRemodeled'] = (df.YearRemodAdd != df.YearBuilt).astype(np.int64)
	df['IsNew'] = (df.YearBuilt > 2000).astype(np.int64)
	df['WasCompleted'] = (df.SaleCondition != 'Partial').astype(np.int64)
	df['AfterWW2'] = (df.YearBuilt >= 1946).astype(np.int64)

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
