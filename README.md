# BucketDigger

Currently this version of the tool is used to dig into S3 public buckets searching for interesting patterns.

![BucketDigger](https://user-images.githubusercontent.com/24937516/130268642-b857b4d8-6e09-472b-bf3e-c2e045a56cc5.png)


Features
---
🕵️‍♀️ Scans a bucket to find files containing keywords or patterns provided by the user.

💾 Dumps bucket contents to a local folder.


Installation
---

from source:
```
git clone git@github.com:alexeleftheriadis/BucketDigger.git
cd BucketDigger
pip3 install -r requirements.txt
```

Usage
---
```
usage: BucketDigger  [-t] [-ms] [-url] [-kw]

optional arguments:
  -h, --help        Show this help message and exit
  -t                File type to search for [Default = all]  {Supported types: .txt, .pdf, .json, .js .css .md}
  -ms               The max size of a file (in Bytes) [Default = 500000000]
  -url              The URL of the bucket
  -kw               The file containing the word(s) to search to
```

Examples
---
Look for keyword/pattern matches within all the files of a bucket 
```
python3 BucketDigger.py -kw keywords.txt -url https://[bucket_name].s3.amazonaws.com
```

Look for keyword/pattern matches in text files hosted on a bucket limiting the size of files analyzed to 500MB. 
```
python3 BucketDigger.py -t txt -ms 500000000 -kw keywords.txt -url https://[bucket_name].s3.amazonaws.com
```

Compatibility
---
Tested on Python 3.8.2 using Windows 10 + on Python 3.9.1 using Kali linux.

License
---
MIT
