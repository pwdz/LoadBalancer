# LoadBalancer
A simple loadbalancer for Cloud Computing course at AUT.  


![Architecture](https://github.com/pwdz/LoadBalancer/blob/main/screenshot.jpg)  
  
It's consisted of 3 docker containers running `fileProcessor.py`.  
## commands
|commandName|Description|
|--|--|
| min | |
| max | |
| average | |
| sort | |
| wordcount | |  

**Request format: **
```
{<operation name, input file path>, <operation
name, input file path>, …, <output directory>}
```
**Example request:**
```
{<min,/tmp/grade.txt>, <max, /tmp/grade.txt>,
</tmp/gradeStat>}  
```
