from htsct.core.flow import workflow

workflow("./helo", ["5", "6"], "test", stepsCollectionName="steps", stepLogCollectionName="stepLog", host="42.244.24.75", port=27000)
