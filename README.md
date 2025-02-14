# File Compare Using the MD5

## Scenario
You have a set of files that should be identical. In my case, I have some network configuration from Cisco routers that 
should be identical. I retrieve the configuration from each router and save it into a file. This is a mechanism where
I can check if the files are identical using the MD5 for each of the files.

```
python /home/stevebj/PycharmProjects/FileCompareCheck/main.py 
4221d002ceb5d3c9e9137e495ceaa647 : file1.txt
4221d002ceb5d3c9e9137e495ceaa647 : file2.txt
4221d002ceb5d3c9e9137e495ceaa647 : file3.txt
8556852b063d5ec80a717166b8e3e81f : file4.txt

Process finished with exit code 0
```
