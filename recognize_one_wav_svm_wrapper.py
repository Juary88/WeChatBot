import rpy2.robjects as robjects

# sample usage
#from recognize_one_wav_svm_wrapper import recognize_one_wav_svm
#wavFile = "xxx.wav"
#print(recognize_one_wav_svm(wavFile))

# Use the script above to get the gender of voice of the wav file
# Note that this shouold be in the same folder as recognize_one_wav_svm.R and genderSvm.rds
def recognize_one_wav_svm(wavFile):
    r = robjects.r
    r.source("recognize_one_wav_svm.R")
    return r['get_gender'](wavFile)
    