
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirement.txt
EXPOSE 8000
CMD ["uvicorn", "combined_script:app", "--host", "0.0.0.0", "--port", "8001"]

