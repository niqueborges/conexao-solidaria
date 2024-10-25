deploy:
	@cd conexao_solidaria && sls deploy

run:
	@cd conexao_solidaria && sls offline

pre-commit:
	@pre-commit install

endpoints:
	@cd conexao_solidaria && sls info
