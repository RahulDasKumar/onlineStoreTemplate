chmod +x *.sh
cd database && chmod +x *.sh && ./resetDB.sh && cd ..
pip install -r requirements.txt
python3 scrape_movies.py