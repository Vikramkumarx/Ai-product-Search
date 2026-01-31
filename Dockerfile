# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.9

# Install system dependencies if any (none for this simplified version)

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python dependencies
# Note: sentence-transformers and torch are heavy.
# In production, use --no-cache-dir to save space.
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}

# Copy model cache (Optional but recommended to bake in model)
# For this demo, the model downloads on first run (Warm Start).
# To bake it in, run a script here to download 'paraphrase-multilingual-MiniLM-L12-v2' to a local folder
# and set SENTENCE_TRANSFORMERS_HOME.

# Set the CMD to your handler
CMD [ "lambda_handler.lambda_handler" ]
