#MEMM task 1 - Model Training
##Running instructions:
1. first run `ExtractFeatures.py` as follow:
       
            python3 ExtractFeatures.py corpus_file features_file
            
2. second run ` TrainSolver.py ` as follow:

            python3 TrainSolver.py features_file model_file features_map_file