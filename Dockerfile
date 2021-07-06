FROM opencvcourses/opencv-docker:4.4.0
RUN pip install --upgrade pip==21.1.2
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD python3 ./App.py
