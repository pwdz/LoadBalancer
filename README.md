# LoadBalancer
A simple loadbalancer for Cloud Computing course at AUT.  


![Architecture](https://github.com/pwdz/LoadBalancer/blob/main/screenshot.jpg)  
  
It's consisted of 3 docker containers running `fileProcessor.py`.  
## Image Supported Operations
|operation name|Description|
|--|--|
|min|find the minimum number in a given file|
|max|find the maximum number in a given file|
|average|find the average of numbers in a given file|
|sort|sort the numbers in a given file|
|wordcount|find the count of occurrence of each word in a given file|  
  
**Request format:**
```
{<operationName, inputFilePath>, <operationName, inputFilePath>, …, <outputDirectory>}
```
**Example request:**
```
{<min,/tmp/grade.txt>, <max, /tmp/grade.txt>, </tmp/gradeStat>}  
```
Also `.cpp` and `.py` programs can be executed inside container using the below request format:
```
Request format: {<programName, inputFilePath>, <programName, inputFilePath>, …, <outputDirectory>}
```
