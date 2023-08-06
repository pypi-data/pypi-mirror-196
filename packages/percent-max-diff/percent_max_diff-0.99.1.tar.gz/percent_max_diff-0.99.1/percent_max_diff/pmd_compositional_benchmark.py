import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from pyminer_norm.downsample import new_rewrite_get_transcript_vect as ds
#from percent_max_diff.percent_max_diff import pmd



main_lambda_vect = [10000,7500,5000, 2500, 1000, 100, 10, 1]
lambda_sd = 0.05
#num_per_group_vect = [3, 12, 48]

main_iters = 1

sampling_depths = [[10000, 10000, 10000, 10000, 10000, 10000],
                   [10000, 10000, 10000, 1000, 1000, 1000],
                   [10000, 10000, 10000, 100, 100, 100]]



for it in range(main_iters):
	for sampling_depth in sampling_depths:
		temp_mat = np.zeros((len(main_lambda_vect),len(sampling_depth)),dtype=np.int32)
		## sampling_depth has the main vect for each "subject" ie: column
		for col in range(len(sampling_depth)):
			for row in range(len(main_lambda_vect)):
				temp_lambda = main_lambda_vect[row]
				temp_lambda = temp_lambda +(temp_lambda + np.random.normal(0,lambda_sd))
				temp_mat[row,col] = np.random.poisson(lam=temp_lambda)
			temp_mat[:,col] = ds(temp_mat[:,col], num_final_transcripts=sampling_depth[col])
		print(temp_mat)
		temp_pmd_res = pmd(temp_mat)
		sns.heatmap(temp_pmd_res.adjusted_z_scores)
		plt.show()



effect_1_vect = [[1,1,1,2,2,2],
                 [1,1,1,1.5,1.5,1.5]]#,
                 # [1,1,1,1.25,1.25,1.25],
                 # [1,1,1,1.05,1.05,1.05],
                 # [1,1,1,.95,.95,.95],
                 # [1,1,1,.75,.75,.75],
                 # [1,1,1,.5,.5,.5]]


effect_2_vect=[[1,1,1,1,1,1], 
               np.random.uniform(.5,1.5,size=6).tolist()]


signal_injection_rows = [[0],
                         # [1],
                         # [2],
                         # [3],
                         # [4],
                         # [5],
                          [0,4]]



for it in range(main_iters):
	for effect_1 in effect_1_vect:
		for effect_2 in effect_2_vect:
			for signal_injection_row in signal_injection_rows:#range(len(main_lambda_vect)):
				for sampling_depth in sampling_depths:
					temp_mat = np.zeros((len(main_lambda_vect),len(sampling_depth)),dtype=np.int32)
					## sampling_depth has the main vect for each "subject" ie: column
					for col in range(len(sampling_depth)):
						for row in range(len(main_lambda_vect)):
							temp_lambda = main_lambda_vect[row]
							if row in signal_injection_row:
								temp_lambda = temp_lambda + (temp_lambda * effect_1[col])+ (temp_lambda * effect_2[col]) #+ (temp_lambda + np.random.normal(0,lambda_sd))
							else:
								pass
							temp_mat[row,col] = np.random.poisson(lam=temp_lambda)
						temp_mat[:,col] = ds(temp_mat[:,col], num_final_transcripts=sampling_depth[col])
					temp_pmd_res = pmd(temp_mat)
					print("effect_1:",effect_1)
					print("effect_2:",effect_2)
					print("signal_injection_row:",signal_injection_row)
					print("sampling_depth:",sampling_depth)
					print(temp_mat)
					sns.heatmap(temp_pmd_res.z_scores)
					plt.show()
					sns.heatmap(temp_pmd_res.adjusted_z_scores)
					plt.show()





for i in range(temp_pmd_res.residuals.shape[1]):
    plt.scatter(temp_pmd_res.residuals.iloc[0,i],np.sum(temp_pmd_res.residuals.iloc[1:,i]))

plt.show()


for i in range(temp_pmd_res.adjusted_residuals.shape[1]):
    plt.scatter(temp_pmd_res.adjusted_residuals.iloc[0,i],np.sum(temp_pmd_res.adjusted_residuals.iloc[1:,i]))

plt.show()


