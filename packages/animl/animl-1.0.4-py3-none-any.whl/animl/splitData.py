def getEmpty(dataframe):
    # Removes all images that MegaDetector gave no detection for
    otherdf = dataframe[dataframe['category'].astype(int) != 1]
    otherdf = otherdf.reset_index(drop=True)
    otherdf = otherdf.rename(columns={'category': 'class'})
    # Numbers the class of the non-animals correctly
    if not otherdf.empty:
        otherdf = otherdf.replace('2',"human")
        otherdf = otherdf.replace('3',"vehicle")
        otherdf = otherdf.replace('0',"empty")
    return otherdf
    
    
def getAnimals(dataframe):
    animaldf = dataframe[dataframe['category'].astype(int) == 1]
    animaldf = animaldf.reset_index(drop=True)
    return animaldf
	
