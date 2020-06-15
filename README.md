# cvpr20_scheduler
Search and filter the events in CVPR2020 based on:
  * program
  * keywords
  * authors
  * dates
  * day time (in your desired time zone)
  * paper ID

and export the results for the calendar in your time zone

# Dependencies
Install dependencies by: 
```Shell
pip install -r requirements.txt
```

# Installation
No need to install (probably this package is one time use :)). Just clone the repo and run the  `cvpr20_scheduler.py` with your search criteria.

# Example
Easily enter your criteria similar to below:
```Shell
python cvpr_2020_scheduler.py --program papers --authors black john --times 10,13 8,10 20,22 --keywords "3d" "human body" "clothing" --dates 17 18 --timezone GMT
```
