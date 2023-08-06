import random
import pandas as pd
import utils

path = "/Users/bob/Documents/Studium/8. Semester/Bachelorarbeit/henhoe2vec_output/henhoe2vec_results.emb"

test_data = {
            "source":       ['n1', 'n2', 'n3', 'n1', 'n4', 'n5', 'n1'],
            "source_layer": ['l1', 'l1', 'l2', 'l2', 'l2', 'l1', 'l1'],
            "target":       ['n2', 'n3', 'n1', 'n2', 'n5', 'n1', 'n5'],
            "target_layer": ['l1', 'l2', 'l1', 'l2', 'l2', 'l1', 'l1'],
            "weight":       [1, 0.5, 0.2, 1.1, 0.1, 0.3, 0.4]
        }

df = utils.emb_to_dataframe(path)
print(df)