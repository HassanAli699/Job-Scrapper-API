from flask import Flask, jsonify, request
from jobs_controller import scrape_jobs_for_keyword, scrape_linkedin_jobs, scrape_rozee_jobs, scrape_indeed_jobs

app = Flask(__name__)


@app.route('/get_all_jobs', methods=['GET'])
def get_all_jobs():
    keyword = request.args.get('keyword')
    location = request.args.get('location')
    num_pages = int(request.args.get('num_pages', 1))
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    jobs_data = scrape_jobs_for_keyword(keyword, location, num_pages, page_size, page)

    return jobs_data


@app.route('/get_jobs_from_site', methods=['GET'])
def get_site_jobs():
    keyword = request.args.get('keyword')
    location = request.args.get('location')
    num_pages = int(request.args.get('num_pages', 1))
    site = request.args.get('site_name').lower()
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    if site.lower() == 'linkedin':
        jobs_data = scrape_linkedin_jobs(keyword, location, num_pages, page_size, page)
        return jsonify(jobs_data)
    elif site.lower() == 'rozee':
        jobs_data = scrape_rozee_jobs(keyword, num_pages, page_size, page)
        return jsonify(jobs_data)
    elif site.lower() == 'indeed':
        jobs_data = scrape_indeed_jobs(keyword, location, num_pages, page_size, page)
        return jsonify(jobs_data)
    else:
        return jsonify({'error': 'Invalid site name'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
