# bsa-ad-reports
Automatically update BSA 3rd party Reports with 1st party and 3rd party data



# 1st Party data
For each advertiser:

1) assemble a query that returns impressions and clicks for _all_ line items that have run that month (paused & completed included)
2) make HTTP request
3) receive response and parse into separate line items with relevant info.
4) match line items with lines on google sheet 
