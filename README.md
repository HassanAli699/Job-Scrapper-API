**Job Scrapper API Document**

There are 2 API’s one to get the data from a specific site and one to get the collective data from all the three sites:

•	LinkedIn

•	Rozee.pk

•	Indeed


-----------------------------------------------------------------------------------------------------------------
**Specific Site API:**

This Api takes the following parameters:

•	keywords (Comma Separated String like “Android Developer, Android, Development”)

•	location (Specify the location of the job like “Islamabad”, “Karachi”, “Islamabad, Pakistan”)

•	num_pages (Number of pages to scrape from a single site like scrape 2 pages or 4 pages)

•	site (Site from which the jobs are to be scrapped)

•	page (The Page number from which you want to get data for pagination)

•	page_size (The number of jobs you want on a page)

Required Parameters and Defined Values:

Required: Keyword, Location, Site

Pre-defined: num_pages (1), page (1), per_page (10)	

End-point:
http://YOUR_LOCALHOST_URL_HERE/get_jobs_from_site

![image](https://github.com/HassanAli699/Job-Scrapper-API/assets/119949006/c24d755c-440e-485f-8319-46d8f334baa1)
------------------------------------------------------------------------------------------------------------------
 
**All Jobs API:**
This Api takes the following parameters:

•	keyword

•	location

•	num_pages

•	page

•	page_size

Required Parameters and Defined Values:

Required: Keyword, Location

Pre-defined: num_pages (1), page (1), per_page (10)	

End-point:
http://YOUR_LOCALHOST_URL_HERE/get_all_jobs

![image](https://github.com/HassanAli699/Job-Scrapper-API/assets/119949006/4d033021-7760-44a1-b9f6-a18cc4926d31)
------------------------------------------------------------------------------------------------------------------

**Data the API returns**

![image](https://github.com/HassanAli699/Job-Scrapper-API/assets/119949006/1619013e-afe2-4bae-ab73-74efbcacaccb)
------------------------------------------------------------------------------------------------------------------

**Features and DataTypes**

![image](https://github.com/HassanAli699/Job-Scrapper-API/assets/119949006/6347f328-974e-47a0-b6f3-caa9036fe860)
------------------------------------------------------------------------------------------------------------------

Packages to install for scrapper:

•	Flask

•	bs4 

There maybe one or two more packages to install.


Folder Structure:

Main.py: contains all the routes to get the data.

Job_Controller: contains all the method to get the data form the sites.

Utils: contains the helper methods

