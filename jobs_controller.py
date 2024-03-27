import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import jsonify
from utils import get_indeed_search_url
from concurrent.futures import ThreadPoolExecutor
import re
import concurrent.futures


def scrape_linkedin_jobs(keywords, location, pages, page_size, page):
    base_url = f'https://www.linkedin.com/jobs/search?keywords={keywords}&location={location}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum='

    job_list = []
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    for current_page in range(1, pages + 1):
        linkedInUrl = f'{base_url}{current_page}'
        retry_attempts = 3
        while retry_attempts > 0:
            try:
                response = requests.get(linkedInUrl)
                soup = BeautifulSoup(response.text, 'html.parser')
                jobs = soup.find('ul', class_='jobs-search__results-list')
                all_jobs = jobs.find_all('li')

                for job in all_jobs:
                    try:
                        job_detail = job.find('div', class_='base-search-card__info')
                        title_element = job_detail.find('h3', class_='base-search-card__title')
                        title = title_element.get_text(strip=True) if title_element else 'None'
                        company_element = job_detail.find('h4', class_='base-search-card__subtitle')
                        company = company_element.get_text(strip=True) if company_element else 'None'
                        location_element = job_detail.find('span', class_='job-search-card__location')
                        location = location_element.get_text(strip=True) if location_element else 'None'
                        posted_time_element = job_detail.find('time', class_='job-search-card__listdate')
                        posted_time = posted_time_element.get_text(strip=True) if posted_time_element else 'None'

                        url_element = job.find('a', class_='base-card__full-link')
                        url = url_element.get('href') if url_element else 'None'

                        job_map = {
                            'job_title': title,
                            'company_name': company,
                            'job_location': location,
                            'job_posted_time': posted_time,
                            'job_link': url,
                            'job_site': 'linkedIn',
                            'job_salary': 'None',
                            'job_experience': 'None'
                        }

                        job_list.append(job_map)
                    except Exception as e:
                        print(f"An error occurred while scraping job details: {e}")
                        continue

                break  # Exit the while loop if successful
            except Exception as e:
                retry_attempts -= 1
                if retry_attempts == 0:
                    print(f"Failed to retrieve job list after multiple attempts: {e}")
                    break
                else:
                    print(f"Retrying to scrape the page. Attempts left: {retry_attempts}")
                    continue

    return {
        'jobs_data': job_list[start_index:end_index],
        'total_jobs': len(job_list),
        'current_page': page,
        'per_page': page_size
    }


def scrape_rozee_jobs(query, num_pages, page_size, page):
    jobs_data = []

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    for current_page in range(1, num_pages + 1):
        if current_page != page:
            continue

        rozeeUrl = f'https://www.rozee.pk/job/jsearch/q/{query}/fpn/{current_page}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) '
                          'Chrome/80.0.3987.162 Safari/537.36'}
        response = requests.get(rozeeUrl, headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all script tags
        scripts = soup.find_all('script')

        # Iterate over scripts to find the one containing "var apResp"
        for script in scripts:
            if 'var apResp' in script.text:
                # Use regex to extract the data inside var apResp
                match = re.search(r'var apResp = ({.*?});', script.text, re.DOTALL)
                if match:
                    data_inside_apResp = match.group(1)
                    # Parse the JSON data
                    apResp_json = json.loads(data_inside_apResp)
                    # Access the 'jobs' list
                    jobs_list = apResp_json['response']['jobs']['basic']

                    # Iterate over each job and extract the desired information
                    for job in jobs_list:
                        try:
                            job_data = {}
                            job_data['job_title'] = job.get('title') or "None"
                            job_data['company_name'] = job.get('company') or "None"
                            job_data['job_location'] = job.get('city') or "None"
                            job_data['job_posted_time'] = job.get('created') or "None"
                            job_data['job_link'] = f"https://www.rozee.pk/job/{job.get('permaLink')}" or "None"
                            job_data[
                                'job_salary'] = f"{job.get('salaryNHide_exact') or 'N/A'} - {job.get('salaryTHide_exact') or 'None'}"
                            job_data['job_skills'] = job.get('skills') or "None"
                            job_data['job_experience'] = job.get('experience_text') or "None"
                            job_data['job_site'] = 'Rozee.pk'
                            jobs_data.append(job_data)
                        except Exception as e:
                            print(f"An error occurred for job {job.get('title')}: {e}")
                            continue
                break

    return {
        'current_page': page,
        'total_jobs': len(jobs_data),
        'per_page': page_size,
        'jobs_data': jobs_data[start_index:end_index],
    }


def scrape_indeed_jobs(keyword, location, num_pages, page_size, page):
    jobs_data_list = []
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    for current_page in range(1, num_pages + 1):
        if current_page != page:
            continue

        indeed_url = get_indeed_search_url(keyword, location, current_page)

        response = requests.get(
            url='https://proxy.scrapeops.io/v1/',
            params={
                'api_key': '68bc17cc-de66-4676-ba3d-1defab82aee3',
                'url': indeed_url,
            },
        )
        decoded_content = response.content.decode('utf-8')
        soup = BeautifulSoup(decoded_content, 'html.parser')
        scripts = soup.find_all('script')
        # Iterate over scripts to find the one with id "mosaic-data"
        for script in scripts:
            if script.get('id') == 'mosaic-data':
                mosaic_data_script = script
                script_tag = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});',
                                        mosaic_data_script.text)
                json_blob = json.loads(script_tag[0])
                jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
                for index, job in enumerate(jobs_list):
                    try:
                        if job.get('jobkey') is not None:
                            job_posted_time = job.get('pubDate')
                            # Convert milliseconds to seconds
                            posted_time_seconds = int(job_posted_time) // 1000

                            # Convert to datetime object
                            posted_time = datetime.utcfromtimestamp(posted_time_seconds).strftime('%Y-%m-%d')

                            maxSalary = job.get('estimatedSalary').get('max') if job.get(
                                'estimatedSalary') is not None else 0
                            minSalary = job.get('estimatedSalary').get('min') if job.get(
                                'estimatedSalary') is not None else 0

                            job_salary = f"{minSalary}  -  {maxSalary}" if minSalary != 0 or maxSalary != 0 else None

                            jobs_data_list.append({
                                'job_location': location + ", " + job.get('jobLocationCity'),
                                'company_name': job.get('company'),
                                'job_title': job.get('title'),
                                'job_salary': job_salary,
                                'job_posted_time': posted_time,
                                'job_link': f"https://pk.indeed.com/{job.get('viewJobLink')}",
                                'job_experience': 'None',
                                'job_site': "Indeed"
                            })
                    except Exception as e:
                        print(f"An error occurred for job {job.get('title')}: {e}")
                        continue

                break

    return {
        'total_jobs': len(jobs_data_list),
        'current_page': page,
        'per_page': page_size,
        'jobs_data': jobs_data_list[start_index:end_index],
    }


def scrape_jobs_for_keyword(keyword, location, num_pages, page_size, page):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the scraping tasks
        rozee_future = executor.submit(scrape_rozee_jobs, keyword, num_pages, 100, 1)
        linkedin_future = executor.submit(scrape_linkedin_jobs, keyword, location, num_pages, 100, 1)
        indeed_future = executor.submit(scrape_indeed_jobs, keyword, location, num_pages, 100, 1)

        # Get the results
        jobs_data_rozee = rozee_future.result()
        jobs_data_linkedin = linkedin_future.result()
        jobs_data_indeed = indeed_future.result()

    combined_data = jobs_data_rozee.get('jobs_data', []) + jobs_data_linkedin.get('jobs_data',
                                                                                  []) + jobs_data_indeed.get(
        'jobs_data', [])

    # Calculate total number of jobs
    total_jobs = len(combined_data)

    # Paginate the job listings
    start_index = page_size * (page - 1)
    end_index = start_index + page_size
    paginated_data = combined_data[start_index:end_index]

    paginated_jobs_rozee = jobs_data_rozee.get('jobs_data', [])
    paginated_jobs_linkedin = jobs_data_linkedin.get('jobs_data', [])
    paginated_jobs_indeed = jobs_data_indeed.get('jobs_data', [])

    # Return the paginated results
    return jsonify({
        'linkedIn_jobs': len(paginated_jobs_linkedin),
        'rozee_jobs': len(paginated_jobs_rozee),
        'indeed_jobs': len(paginated_jobs_indeed),
        'total_jobs': total_jobs,
        'current_page': page,
        'per_page': page_size,
        'jobs_data': paginated_data,
    })
