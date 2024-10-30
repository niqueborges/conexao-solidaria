deploy:
	@cd serverless && sls deploy

run:
	@cd serverless && sls offline

pre-commit:
	@pre-commit install

endpoints:
	@cd serverless && sls info
