# Notes

## Overview
- Dataset of 1460 observations and 81 features

## EDAs
- [Comprehensive Data Exploration - Marcelino](https://www.kaggle.com/pmarcelino/comprehensive-data-exploration-with-python):
    - Tactics
        - Segmenting features: define three possible segments that a feature can refer to
            - building ('OverallQual')
            - space (TotalBsmtSF)
            - location (Neighborhood)
        -  Expection of influence on Sale Price: Is it hgih medium low? 
    - Analysis
        - Sale Price
            - deviates from normal distribution: skewed to the left -> skew = 1.88
            - shows peakedness -> kurtosis = 6.54
    - Takeaways:
        - A decent number of the numerical features are skewed
        - Log transform after removing or resolving NAs
        
- [EDA 2]()
    - Tactics
    - Analysis
    - Takeaways
- [EDA 3]()
    - Tactics
    - Analysis
    - Takeaways
    
## De Cock's Paper
- Abstract
    - individual residential property from 2006 to 2010 in Ames Iowa
    - 23 nominal, 23 ordinal, 14 discrete, and 20 continuous features
- Housing Data
    - 20 continuous variables
        - relate to various area dimensions
            - lot size
            - dwelling square footage
        - Broken out into categories based on quality and type:
            - basement
            - main living
            - porches
    - 14 discrete variables
        - quantification of house items:
            - num bathrooms
            - bedrooms (full and half)
            - kitchens
            - garage capacity
            - consturction / remodeling dates
    - categorical features
        - 23 nominal
        - 23 ordinal
        - range from 2 to 28 classes 
            - STREET has gravel or paved
            - NEIGHBORHOOD has 28 classes
        - nominals typically indicate types of
            - dwellings
            - garages
            - materials
            - environmental conditions
        - Ordinal
            - rate various items in the property
        - PID and NEIGHBORHOOD are of interest:
            - PID - Parcel Identification Number
                - can be used as a key with the [Assessors Office](https://www.cityofames.org/government/departments-divisions-a-h/city-assessor) or [Beacon](https://beacon.schneidercorp.com/) websites to directly view records of a particular observation
            - NEIGHBORHOOD
                - use with the [map](https://www.amstat.org//v19n3/decock/AmesResidential.pdf)
    - De Cook identifies 5 major outliers in sales price
        - three of them are true outliers possibly partial sales that don't represent actual market values 
        - two are just unusual sales - very large houses priced relatively appropriately
        - recommends removing houses with more than 4000 sq ft. 
-  
