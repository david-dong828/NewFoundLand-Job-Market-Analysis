# NewFoundLand-Job-Market-Analysis

Well, the purpose of doing such an analysis is just to satisfy my curiosity: _**How tough is the Job market to CS students?**_ 😮

😎 Eventually, after spending my weekend, I scraped the data and got this analysis.

😎 Let's take a look at the result firstly, and then I will tell you how to get it. 

------

> **Interpretation**

**1. The Job word cloud: the bigger the word, the more job demands.**
   
   * Well, disappointingly, it showed a stark absence of CS-related roles.
   * Look, the only thing we saw at a glance was postions like assistant or whaever.. 
   
      <img src="https://github.com/david-dong828/NewFoundLand-Job-Market-Analysis/assets/106771290/8677c5a8-3b93-4c7c-82f1-2c4ec8930c3b" width="380" height="380">
   
**2. The Job density map: The more desity, the more jobs.**

  * I was supprised to find Two Job centers: St.John's and Labrador. I thought there would be only St.John's.
  * Also, nearby areas of St.John's like Mount Pearl and Paradise also showed significant opportunities.
  
      <img src="https://github.com/david-dong828/NewFoundLand-Job-Market-Analysis/assets/106771290/0aa7ba4c-43e0-4ab2-a124-45b07cd56014" width="380" height="380">
      <img src="https://github.com/david-dong828/NewFoundLand-Job-Market-Analysis/assets/106771290/f4813fa7-5405-4703-869b-d4fe112df1bf" width="380" height="380">

**3. HDBScan: These clusters illustrated the geographic spread of job opportunities**

  * It highlighted the concentration of jobs in St. John’s, marked by vibrant red and orange dots on the map. 
  * black dots, might representing outliers, indicated unique jobs in more remote locations.
      <img src="https://github.com/david-dong828/NewFoundLand-Job-Market-Analysis/assets/106771290/13ec29da-f584-4f49-b35f-313d6f9a6e47" width="380" height="380">


**4. LDA for job requirement analysis: to understand the nature of these jobs**

  * For topic 1, it seems to revolve around positions that require a degree of responsibility and coordination, likely in an administrative or managerial capacity 😎 . 
  * The presence of words like "assistant," "program," "manager," and "officer" suggests roles that may involve oversight, planning, and execution of various programs or projects.
  * The terms "health" and "safety" indicate a possible focus on roles related to health and safety management, while "training" and "services" might imply roles in the service industry or corporate training domains. 
  * "Valid license" suggests jobs that require certification or specific qualifications.

  
      <img src="https://github.com/david-dong828/NewFoundLand-Job-Market-Analysis/assets/106771290/0e29b3be-95e1-403d-93d6-25d8f9756044" width="420" height="380">

      <img src="https://github.com/david-dong828/NewFoundLand-Job-Market-Analysis/assets/106771290/7554dbef-c54e-432d-abb1-4e8fa5f302a4" width="420" height="380">


------

> **Method**

1. Scrape the job post data
   * I already built a way, using selenium, to scrape the data from a popular job post website. >*data_scraping.py*
   * Surely, you can take it as a reference to scrap data from other job websites.
   * I have to say, selenium is way better than the way using BeautifulSoup, especially for this kind of dynamic update website which also have anti-scrapping mechanism.
   
2. Clean the scraped data
   * This is an essential step, as the scrapped data contains noises or impurities, which will definitely affect the results.
   * In this case, I spotted the errors and areas that need to be adjusted, like moving *job type* data from *salary* column to the correct place.
   * Try >*data_clean.py*
   
3. Take a fast visulization
   * In this step, >*data_rough_viz.py* could give you a general visulization by generating the Job Word Cloud and Job density Map.
   * A little tip: When processing data, you can consider some algorithms or techniques to improve efficiency.
      * For example, when I convert city to longitude and latitude, due to server limitations, I can only process one data in 10 seconds.
      * If I simply convert one by one, then 1,000 data will take nearly 3 hours, which is too long.
      * But if I can save the existing city areas and longitudes and latitudes, then every time I process the data, I can refer to the recorded ones without having to go to the server for processing.
      * The result only takes less than 1 minute to complete.
     
4. Data mining and more visulization
   * I have already created k-means, DBscan, HDBscan and Topic modeling in >*data_mining_viz.py*
   * In this case, I used HDBscan and Topic modeling since I found these two are more suitable.
  

-------




