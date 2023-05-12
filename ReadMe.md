#### WineQuality End to End ML Project - with MLOps



ml flow server command
'''
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./artifacts \
    --host 0.0.0.0 -p 1234

'''